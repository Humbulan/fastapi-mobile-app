import express from 'express';
import { v4 as uuidv4 } from 'uuid';
import { exec } from 'child_process';
import { promisify } from 'util';
import mysql from 'mysql2/promise';

const execAsync = promisify(exec);
const app = express();
app.use(express.json());

// ---------- MariaDB pool (your existing vulnerability logging) ----------
let pool = mysql.createPool({
    socketPath: '/data/data/com.termux/files/home/mysql_run/mysql.sock',
    user: 'root',
    password: 'RootStrongPass123!',
    database: 'imperial_nexus'
});

// ---------- Health check (added) ----------
app.get('/healthz', (req, res) => {
    res.status(200).json({
        status: 'ok',
        service: 'MCP Nexus',
        timestamp: new Date().toISOString()
    });
});

// ---------- Vulnerability logging routes (your existing code) ----------
app.post('/log', async (req, res) => {
    const { vulnerability, severity, target_port } = req.body;
    if (!vulnerability || !severity || target_port === undefined) {
        return res.status(400).json({ error: 'Missing fields' });
    }
    try {
        await pool.query(
            "INSERT INTO vulnerability_logs (vulnerability_type, severity, target_port) VALUES (?, ?, ?)",
            [vulnerability, severity, target_port]
        );
        res.status(200).json({ success: true });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get("/vuln-dashboard", async (req, res) => {
    try {
        const [rows] = await pool.query(
            "SELECT id, vulnerability_type, severity, target_port, logged_at, notified FROM vulnerability_logs ORDER BY logged_at DESC LIMIT 50"
        );
        let html = `<html><head><title>Vulnerability Dashboard</title>
            <style>body { font-family: sans-serif; } table { border-collapse: collapse; } td, th { border: 1px solid #ccc; padding: 8px; }</style>
            </head><body><h1>Recent Vulnerabilities</h1><table>
            <tr><th>ID</th><th>Type</th><th>Severity</th><th>Port</th><th>Logged</th><th>Notified</th></tr>`;
        rows.forEach(r => {
            html += `<tr><td>${r.id}</td><td>${r.vulnerability_type}</td><td>${r.severity}</td><td>${r.target_port}</td><td>${r.logged_at}</td><td>${r.notified ? "Yes" : "No"}</td></tr>`;
        });
        html += `</table></body></html>`;
        res.send(html);
    } catch (err) {
        res.status(500).send("Error: " + err.message);
    }
});

// ---------- Full MCP Nexus (SSE, tools, messages) ----------
const sessions = new Map();

// SSE endpoint
app.get('/sse', (req, res) => {
    const sessionId = uuidv4();
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.flushHeaders();

    sessions.set(sessionId, { res, messageQueue: [] });
    res.write(`event: endpoint\ndata: /messages?sessionId=${sessionId}\n\n`);

    // Timeout after 60 seconds
    setTimeout(() => {
        sessions.delete(sessionId);
    }, 60000);

    req.on('close', () => {
        // Session kept for pending requests
    });
});

// Message endpoint
app.post('/messages', async (req, res) => {
    const sessionId = req.query.sessionId;
    const session = sessions.get(sessionId);
    if (!session) {
        return res.status(400).json({ error: 'No active transport session' });
    }

    const { jsonrpc, method, params, id } = req.body;
    let result = null;

    try {
        if (method === 'initialize') {
            result = { protocolVersion: "2024-11-05", capabilities: {} };
        } else if (method === 'tools/list') {
            result = {
                tools: [
                    { name: 'get-system-status', inputSchema: { type: 'object', properties: {} }, execution: { taskSupport: 'forbidden' } },
                    { name: 'run-diagnostics', inputSchema: { type: 'object', properties: {} }, execution: { taskSupport: 'forbidden' } }
                ]
            };
        } else if (method === 'tools/call') {
            const { name, arguments: args } = params;
            if (name === 'get-system-status') {
                try {
                    const { stdout } = await execAsync('python3 ~/imperial_network/get_imperial_metrics.py');
                    const data = JSON.parse(stdout);
                    result = { status: 'operational', ...data, timestamp: new Date().toISOString() };
                } catch (err) {
                    result = { status: 'error', error: err.message, timestamp: new Date().toISOString() };
                }
            } else if (name === 'run-diagnostics') {
                result = { diagnostics: 'All systems nominal', timestamp: new Date().toISOString() };
            } else {
                throw new Error(`Unknown tool: ${name}`);
            }
        } else {
            throw new Error(`Unknown method: ${method}`);
        }

        const response = { jsonrpc: '2.0', id, result };
        session.res.write(`event: message\ndata: ${JSON.stringify(response)}\n\n`);
        res.status(202).end();
    } catch (err) {
        const errorResponse = { jsonrpc: '2.0', id, error: { code: -32603, message: err.message } };
        session.res.write(`event: error\ndata: ${JSON.stringify(errorResponse)}\n\n`);
        res.status(500).json({ error: err.message });
    }
});

// ---------- Start the server ----------
const PORT = 8002;
app.listen(PORT, () => {
    console.log(`✅ MCP Nexus Server running on port ${PORT}`);
});
