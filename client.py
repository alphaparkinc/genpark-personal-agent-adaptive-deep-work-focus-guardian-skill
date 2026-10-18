"""
Personal Agent Adaptive Deep Work Focus Guardian (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import time
import hashlib
from typing import Dict, Any, Optional

class PersonalAgentAdaptiveDeepWorkFocusGuardian:
    def __init__(self, guardian_name: str = "Today-Focus-Guardian"):
        self.guardian_name = guardian_name

    def evaluate_interruption_and_schedule(self, incoming_ping: Dict[str, Any], focus_state: Dict[str, Any]) -> Dict[str, Any]:
        in_deep_work = bool(focus_state.get("is_in_deep_work", False))
        elapsed_mins = int(focus_state.get("session_elapsed_mins", 30))
        active_task = focus_state.get("active_task_name", "Architecture Design")
        
        sender = incoming_ping.get("sender", "Colleague")
        tier = incoming_ping.get("relationship_tier", "STANDARD").upper()
        urgency = incoming_ping.get("message_urgency", "LOW").upper()
        
        # Immediate break-through: Only VIP contacts with CRITICAL urgency can interrupt deep work
        can_break_through = (not in_deep_work) or (tier == "VIP" and urgency == "CRITICAL")
        
        resumption_token = None
        if not can_break_through:
            decision = "SHIELDED_HELD_FOR_FOCUS_BREAK"
            mins_until_break = max(5, 90 - elapsed_mins)
            delivery_advice = f"Auto-reply sent: User is in deep work focus on '{active_task}'. Notification queued for delivery in {mins_until_break} mins."
        else:
            decision = "PERMIT_BREAKTHROUGH_INTERRUPTION"
            delivery_advice = "Urgent high-priority alert permitted immediately."
            # Checkpoint active task state for instant restoration
            token_src = f"{active_task}:{time.time()}"
            resumption_token = f"SNAP-{hashlib.sha256(token_src.encode('utf-8')).hexdigest()[:10].upper()}"
            
        return {
            "guardian": self.guardian_name,
            "decision": decision,
            "interruption_permitted": can_break_through,
            "delivery_advice": delivery_advice,
            "active_task_resumption_snapshot": resumption_token,
            "verdict": "FOCUS_PROTECTION_ENFORCED"
        }
