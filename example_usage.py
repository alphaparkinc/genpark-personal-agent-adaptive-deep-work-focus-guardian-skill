from client import PersonalAgentAdaptiveDeepWorkFocusGuardian

def main():
    guardian = PersonalAgentAdaptiveDeepWorkFocusGuardian()
    ping = {"sender": "CEO", "relationship_tier": "VIP", "message_urgency": "CRITICAL", "text": "Server outage needs review"}
    state = {"is_in_deep_work": True, "session_elapsed_mins": 60, "active_task_name": "Quarterly Planning"}
    res = guardian.evaluate_interruption_and_schedule(ping, state)
    print("--- Focus Guardian Triage Decision ---")
    print(f"Decision: {res['decision']}")
    print(f"Permitted: {res['interruption_permitted']}")
    print(f"Action Token: {res['active_task_resumption_snapshot']}")
    print(f"Advice: {res['delivery_advice']}")

if __name__ == "__main__":
    main()
