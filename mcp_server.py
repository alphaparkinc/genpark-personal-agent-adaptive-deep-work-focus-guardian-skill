#!/usr/bin/env python3
import json
import sys
from client import PersonalAgentAdaptiveDeepWorkFocusGuardian

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        guardian = PersonalAgentAdaptiveDeepWorkFocusGuardian()
        ping = {"sender": "Alex", "relationship_tier": "STANDARD", "message_urgency": "MEDIUM", "text": "Quick question regarding sync"}
        state = {"is_in_deep_work": True, "session_elapsed_mins": 45, "active_task_name": "Core Refactor"}
        res = guardian.evaluate_interruption_and_schedule(ping, state)
        assert res["interruption_permitted"] is False
        assert res["decision"] == "SHIELDED_HELD_FOR_FOCUS_BREAK"
        print(f"[TEST PASS] Focus Guardian Shielded: {res['decision']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-focus-guardian", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "evaluate_interruption_and_schedule", "description": "Adaptive deep work focus triage and state resumption"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                guardian = PersonalAgentAdaptiveDeepWorkFocusGuardian()
                out = guardian.evaluate_interruption_and_schedule(args.get("incoming_ping", {}), args.get("focus_state", {}))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
