package main

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
	"strings"
)

func executeCommand(command string) string {
	cmd := exec.Command("bash", "-c", command)
	var out bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &out
	err := cmd.Run()
	if err != nil {
		return fmt.Sprintf("Error: %v\nOutput: %s", err, out.String())
	}
	if out.String() == "" {
		return "Success (no output)"
	}
	return out.String()
}

func main() {
	userInput := "help"
	if len(os.Args) > 1 {
		userInput = strings.Join(os.Args[1:], " ")
	}
	lowerInput := strings.ToLower(userInput)

	// 1. Sanitize port 5173
	if strings.Contains(lowerInput, "sanitize") && (strings.Contains(lowerInput, "5173") || strings.Contains(lowerInput, "port")) {
		cmd := "lsof -t -i :5173 | xargs kill -9 2>/dev/null || echo 'No process on port 5173'"
		fmt.Printf("\n[Imperial Agent] Action: sanitize port 5173\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 2. Delete large logs
	if strings.Contains(lowerInput, "delete") && strings.Contains(lowerInput, "log") && strings.Contains(lowerInput, "100mb") {
		cmd := "find ~ -type f -name '*.log' -size +100M -exec rm -v {} \\;"
		fmt.Printf("\n[Imperial Agent] Action: delete large log files\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 3. Verify stack ports
	if strings.Contains(lowerInput, "verify") || strings.Contains(lowerInput, "stack") {
		cmd := "netstat -tuln 2>/dev/null | grep -E ':(5173|8080|8000|11434)' || ss -tuln 2>/dev/null | grep -E ':(5173|8080|8000|11434)'"
		fmt.Printf("\n[Imperial Agent] Action: stack port verification\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 4. Restart AI Proxy
	if strings.Contains(lowerInput, "restart") && strings.Contains(lowerInput, "proxy") {
		cmd := "pkill -f 'uvicorn ai_integration:app' 2>/dev/null; cd ~/imperial_network && nohup uvicorn ai_integration:app --host 0.0.0.0 --port 8118 > ~/ai_proxy.log 2>&1 & echo 'AI Proxy restarted'"
		fmt.Printf("\n[Imperial Agent] Action: restart AI Proxy\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 5. Restart Business API
	if strings.Contains(lowerInput, "restart") && strings.Contains(lowerInput, "business") {
		cmd := "pkill -f 'uvicorn main:app' 2>/dev/null; cd ~/imperial_network/fastapi-mobile-app && nohup uvicorn main:app --host 0.0.0.0 --port 8000 > ~/business_api.log 2>&1 & echo 'Business API restarted'"
		fmt.Printf("\n[Imperial Agent] Action: restart Business API\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 6. Restart Ollama
	if strings.Contains(lowerInput, "restart") && strings.Contains(lowerInput, "ollama") {
		cmd := "pkill -f 'ollama serve' 2>/dev/null; sleep 1; nohup ollama serve > ~/ollama.log 2>&1 & echo 'Ollama restarted'"
		fmt.Printf("\n[Imperial Agent] Action: restart Ollama\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 7. Sync state JSON
	if strings.Contains(lowerInput, "sync state") {
		cmd := "TRUE_VAL=$(sqlite3 ~/imperial_network/instance/imperial.db \"SELECT SUM(amount) FROM payment WHERE payment_method LIKE 'SADC%' OR payment_method='IMPERIAL_WEB_UPGRADE';\") && echo \"{\\\"valuation\\\": $TRUE_VAL, \\\"timestamp\\\": \\\"$(date -Iseconds)\\\", \\\"status\\\": \\\"operational\\\"}\" > ~/imperial_network/instance/state_sync.json && echo 'State synced'"
		fmt.Printf("\n[Imperial Agent] Action: sync state JSON\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 8. Show disk usage
	if strings.Contains(lowerInput, "disk") || strings.Contains(lowerInput, "space") {
		cmd := "df -h /data"
		fmt.Printf("\n[Imperial Agent] Action: disk usage\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 9. Clean Ollama cache
	if strings.Contains(lowerInput, "clean ollama") {
		cmd := "ollama list | grep -v 'cloud' | awk 'NR>1 {print $1}' | xargs -I {} ollama rm {} 2>/dev/null; echo 'Ollama cache cleaned (cloud models preserved)'"
		fmt.Printf("\n[Imperial Agent] Action: clean Ollama cache\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 10. Run dawn report
	if strings.Contains(lowerInput, "dawn report") {
		cmd := "bash ~/imperial_network/dawn_report_enhanced.sh"
		fmt.Printf("\n[Imperial Agent] Action: run dawn report\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 11. Backup config
	if strings.Contains(lowerInput, "backup config") {
		cmd := "mkdir -p ~/imperial_backups && cp ~/imperial_network/.env ~/imperial_backups/.env.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null; cp ~/imperial_network/instance/imperial.db ~/imperial_backups/imperial.db.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null; cp ~/imperial_network/config.json ~/imperial_backups/config.json.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null; echo 'Config backup completed in ~/imperial_backups'"
		fmt.Printf("\n[Imperial Agent] Action: backup config\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 12. Check MCP server (by process)
	if strings.Contains(lowerInput, "check mcp") {
		cmd := "pgrep -f 'node server.mjs' > /dev/null && echo 'MCP server is running (port 8002)' || echo 'MCP server is NOT running'"
		fmt.Printf("\n[Imperial Agent] Action: check MCP server\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 13. Full system health
	if strings.Contains(lowerInput, "health") {
		fmt.Printf("\n[Imperial Agent] Action: full system health check\n")
		cmds := []string{
			"echo '=== Disk usage ===' && df -h /data",
			"echo '=== Ollama status ===' && curl -s http://localhost:11434/api/tags | head -c 200 || echo 'Ollama not responding'",
			"echo '=== AI Proxy status ===' && curl -s -o /dev/null -w '%{http_code}' http://localhost:8118/health || echo 'AI Proxy down'",
			"echo '=== MCP Nexus status ===' && pgrep -f 'node server.mjs' > /dev/null && echo 'MCP running' || echo 'MCP not running'",
			"echo '=== Business API status ===' && curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/ || echo 'Business API down'",
		}
		for _, c := range cmds {
			fmt.Printf("\n---\n")
			res := executeCommand(c)
			fmt.Printf("%s\n", res)
		}
		return
	}

	// 14. Restart all Imperial services (no sleeps, exits immediately)
	if strings.Contains(lowerInput, "restart all") {
		cmds := []string{
			"(pgrep -f 'uvicorn ai_integration:app' | grep -v $$ | xargs kill -9 2>/dev/null) || true",
			"(pgrep -f 'uvicorn main:app' | grep -v $$ | xargs kill -9 2>/dev/null) || true",
			"(pgrep -f 'ollama serve' | grep -v $$ | xargs kill -9 2>/dev/null) || true",
			"(pgrep -f 'node server.mjs' | grep -v $$ | xargs kill -9 2>/dev/null) || true",
			"cd ~/imperial_network && nohup uvicorn ai_integration:app --host 0.0.0.0 --port 8118 > ~/ai_proxy.log 2>&1 &",
			"cd ~/imperial_network/fastapi-mobile-app && nohup uvicorn main:app --host 0.0.0.0 --port 8000 > ~/business_api.log 2>&1 &",
			"nohup ollama serve > ~/ollama.log 2>&1 &",
			"cd ~/imperial_network && nohup node server.mjs > mcp_output.log 2>&1 &",
			"echo 'All services restarted (backgrounded)'",
		}
		cmd := strings.Join(cmds, "\n")
		fmt.Printf("\n[Imperial Agent] Action: restart all services\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 15. Backup logs (tar all .log files)
	if strings.Contains(lowerInput, "backup logs") {
		cmd := "mkdir -p ~/imperial_backups && tar -czf ~/imperial_backups/logs_$(date +%Y%m%d_%H%M%S).tar.gz ~/*.log ~/imperial_network/*.log 2>/dev/null && echo 'Logs backed up to ~/imperial_backups/'"
		fmt.Printf("\n[Imperial Agent] Action: backup logs\n")
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 16. Clean temporary files
	if strings.Contains(lowerInput, "clean tmp") {
		cmd := "rm -rf /tmp/* ~/.cache/* 2>/dev/null && echo 'Temporary files cleaned'"
		fmt.Printf("\n[Imperial Agent] Action: clean temporary files\n")
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 17. Full status report
	if strings.Contains(lowerInput, "status all") {
		cmds := []string{
			"echo '=== Ollama ===' && pgrep -f 'ollama serve' > /dev/null && echo 'Running' || echo 'Stopped'",
			"echo '=== AI Proxy ===' && curl -s -o /dev/null -w '%{http_code}' http://localhost:8118/health",
			"echo '=== Business API ===' && curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/",
			"echo '=== MCP Nexus ===' && pgrep -f 'node server.mjs' > /dev/null && echo 'Running' || echo 'Stopped'",
			"echo '=== Disk usage ===' && df -h /data | tail -1",
		}
		fmt.Printf("\n[Imperial Agent] Action: full status\n")
		for _, c := range cmds {
			fmt.Printf("\n---\n%s\n", executeCommand(c))
		}
		return
	}

	// 18. EMERGENCY LOCKDOWN & SHIELD MODE
	if strings.Contains(lowerInput, "lockdown") || strings.Contains(lowerInput, "protect") {
		fmt.Printf("\n🚨 [IMPERIAL SENTRY] DEPLOYING DEFENSIVE SHIELD PROTOCOLS...\n")
		shieldCmds := []string{
			"echo '[1/4] Severing external entry points (Cloudflare tunnel)...'",
			"pgrep -f 'cloudflared' | grep -v 'imperial-agent' | xargs kill -9 2>/dev/null || true",
			"echo '[2/4] Hard‑sanitizing rogue listeners (ports 5173, 8080, 18790)...'",
			"lsof -t -i:5173 -i:8080 -i:18790 | xargs kill -9 2>/dev/null || true",
			"echo '[3/4] Purging memory cache to relieve RAM/Swap pressure...'",
			"sync && echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || echo 'Cache clearing skipped (requires root)'",
			"echo '[4/4] Restricting Imperial stack to local loopback (127.0.0.1)...'",
			"lsof -t -i:8118 -i:8000 | xargs kill -9 2>/dev/null || true",
			"cd ~/imperial_network && nohup uvicorn ai_integration:app --host 127.0.0.1 --port 8118 > ~/ai_proxy.log 2>&1 &",
			"cd ~/imperial_network/fastapi-mobile-app && nohup uvicorn main:app --host 127.0.0.1 --port 8000 > ~/business_api.log 2>&1 &",
			"echo '🔒 PERIMETER LOCKED. External ingress dropped. Stack in local safe mode.'",
		}
		cmd := strings.Join(shieldCmds, "\n")
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 19. Restart MCP Nexus server
	if strings.Contains(lowerInput, "restart mcp") {
		cmd := "(pgrep -f 'node server.mjs' | xargs kill -9 2>/dev/null || true) && cd ~/imperial_network && nohup node server.mjs > mcp_output.log 2>&1 & echo 'MCP Nexus restarted'"
		fmt.Printf("\n[Imperial Agent] Action: restart MCP\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 20. Rotate logs (keep last 5, gzip old)
	if strings.Contains(lowerInput, "rotate logs") {
		cmd := "cd ~ && for f in *.log imperial_network/*.log; do [ -f \"$f\" ] && gzip -c \"$f\" > \"$f.$(date +%Y%m%d_%H%M%S).gz\" && > \"$f\"; done && echo 'Logs rotated'"
		fmt.Printf("\n[Imperial Agent] Action: rotate logs\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// 21. Deploy / restart Cloudflare tunnel (safe version, no self‑kill)
	if strings.Contains(lowerInput, "deploy tunnel") {
		cmd := "pgrep -f 'cloudflared' | grep -v 'imperial-agent' | xargs kill -9 2>/dev/null || true; nohup cloudflared tunnel --config ~/.cloudflared/config.yml run d512566a-7849-4442-8e07-97b74eaccc37 > ~/cloudflared.log 2>&1 & sleep 2 && echo 'Cloudflare tunnel restarted'"
		fmt.Printf("\n[Imperial Agent] Action: deploy tunnel\n")
		fmt.Printf("[Command]: %s\n", cmd)
		result := executeCommand(cmd)
		fmt.Printf("[Output]:\n%s\n", result)
		return
	}

	// ========== FALLBACK to Python Claude‑like agent ==========
	fmt.Printf("\n[Imperial Agent] No direct override. Asking Claude agent...\n")
	cmd := fmt.Sprintf("cd ~/Build-your-own-Claude-Code && ./your_program.sh -p \"%s\"", strings.ReplaceAll(userInput, `"`, `\"`))
	result := executeCommand(cmd)
	fmt.Printf("[Output]:\n%s\n", result)
}

