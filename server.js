const express = require("express");
const { exec } = require("child_process");

const app = express();
const PORT = 8002;

async function init() {
  // Dynamically load the ESM-only SDK packages cleanly inside your system's layout
  const { McpServer } = await import("@modelcontextprotocol/sdk/server/mcp.js");
  const { SSEServerTransport } = await import("@modelcontextprotocol/sdk/server/sse.js");

  const server = new McpServer({
    name: "Imperial-Termux-Nexus-Server",
    version: "1.0.0"
  });

  // Custom Tool 1: Check System Status
  server.tool("get-system-status", {}, async () => {
    return {
      content: [{ type: "text", text: "Termux infrastructure engine online and running." }]
    };
  });

  // Custom Tool 2: Safe diagnostic metrics check
  server.tool("run-diagnostics", {}, async () => {
    return new Promise((resolve) => {
      exec("uptime", (error, stdout, stderr) => {
        const output = error ? stderr : stdout;
        resolve({ content: [{ type: "text", text: `Termux Diagnostics:\n${output}` }] });
      });
    });
  });

  let transport;
  app.get("/sse", async (req, res) => {
    transport = new SSEServerTransport("/messages", res);
    await server.connect(transport);
  });

  app.post("/messages", async (req, res) => {
    if (transport && typeof transport.handlePostMessage === "function") {
      await transport.handlePostMessage(req, res);
    } else if (transport && typeof transport.handleMessage === "function") {
      await transport.handleMessage(req, res);
    } else {
      res.status(500).send("Transport initialization mismatch.");
    }
  });

  app.listen(PORT, () => {
    console.log(`\n=========================================`);
    console.log(`🚀 MCP SSE Server running on port ${PORT}`);
    console.log(`🔗 Endpoint: http://localhost:${PORT}/sse`);
    console.log(`=========================================\n`);
  });
}

init().catch(console.error);
