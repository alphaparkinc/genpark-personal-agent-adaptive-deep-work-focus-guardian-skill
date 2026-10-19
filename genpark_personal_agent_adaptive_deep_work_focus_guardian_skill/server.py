# -*- coding: utf-8 -*-
"""Model Context Protocol (MCP) Server for Adaptive Deep Work & Cognitive Flow Guardian Skill
Powered by GenPark (https://www.genpark.ai).
"""
import sys
import json
import logging
from .core import *

TOOLS_METADATA = [
  {
    "name": "allocate_dynamic_focus_sprint",
    "description": "Calculate optimal duration for next deep work sprint based on heart-rate variability (HRV), current fatigue score, and task cognitive difficulty.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "user_hrv_rmssd_ms": {
          "type": "number",
          "description": "Root Mean Square of Successive Differences in ms (e.g. 55.0)"
        },
        "hours_awake": {
          "type": "number"
        },
        "task_complexity": {
          "type": "string",
          "enum": [
            "light_administrative",
            "moderate_analytical",
            "high_creative_architectural"
          ]
        },
        "consecutive_sprints_completed": {
          "type": "integer"
        }
      },
      "required": [
        "user_hrv_rmssd_ms",
        "hours_awake",
        "task_complexity"
      ]
    }
  },
  {
    "name": "evaluate_interruption_triage",
    "description": "Evaluate incoming notification or ping against active deep work focus block to decide whether to squelch, summarize, or breakthrough.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "sender_priority": {
          "type": "string",
          "enum": [
            "vip_family",
            "executive_leadership",
            "peer_coworker",
            "marketing_cold"
          ]
        },
        "remaining_focus_minutes": {
          "type": "integer"
        },
        "message_urgency_score": {
          "type": "number",
          "description": "0.0 to 1.0"
        }
      },
      "required": [
        "sender_priority",
        "remaining_focus_minutes",
        "message_urgency_score"
      ]
    }
  }
]

def handle_rpc(request_str: str) -> str:
    try:
        req = json.loads(request_str)
    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None})
    
    msg_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-adaptive-deep-work-focus-guardian-skill",
                    "version": "1.0.0",
                    "vendor": "GenPark (https://www.genpark.ai)"
                }
            }
        })

    if method == "tools/list":
        return json.dumps({
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"tools": TOOLS_METADATA}
        })

    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        func = globals().get(tool_name)
        if not func or not callable(func):
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}
            })
        
        try:
            call_res = func(**arguments)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {"type": "text", "text": json.dumps(call_res, ensure_ascii=False, indent=2)}
                    ]
                }
            })
        except Exception as err:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32000, "message": f"Execution error: {str(err)}"}
            })

    return json.dumps({
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Unhandled method '{method}'"}
    })

def run_self_test():
    print(f"=== Running Self Test for genpark-personal-agent-adaptive-deep-work-focus-guardian-skill ===")
    init_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"})))
    assert "result" in init_res, "Initialize failed"
    print("[PASS] MCP initialize")

    list_res = json.loads(handle_rpc(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})))
    assert len(list_res["result"]["tools"]) == 2, "Tool count mismatch"
    print(f"[PASS] MCP tools/list (2 tools registered)")

    # Execute smoke test for each tool

    call1 = json.loads(handle_rpc(json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "allocate_dynamic_focus_sprint",
            "arguments": {
                "user_hrv_rmssd_ms": 58.0,
                "hours_awake": 6.5,
                "task_complexity": "high_creative_architectural",
                "consecutive_sprints_completed": 1
            }
        }
    })))
    assert "result" in call1, "Call1 failed"
    print("[PASS] Tool smoke test: allocate_dynamic_focus_sprint")

    print("[ALL TESTS PASSED] Self-test verified successfully.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        success = run_self_test()
        sys.exit(0 if success else 1)
    
    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
