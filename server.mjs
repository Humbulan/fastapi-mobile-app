import express from 'express';
import { v4 as uuidv4 } from 'uuid';
import { exec } from 'child_process';
import { promisify } from 'util';
const execAsync = promisify(exec);

const app = express();
app.use(express.json());

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

  req.on('close', () => {
    sessions.delete(sessionId);
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
      // Send a successful response; no need to write to SSE
    } else if (method === 'tools/list') {
      result = {
        tools: [
          {
            name: 'get-system-status',
            inputSchema: { type: 'object', properties: {} },
            execution: { taskSupport: 'forbidden' }
          },
          {
            name: 'run-diagnostics',
            inputSchema: { type: 'object', properties: {} },
            execution: { taskSupport: 'forbidden' }
          }
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

const PORT = 8002;
app.listen(PORT, () => {
  console.log(`MCP Nexus Server running on port ${PORT}`);
});
