# -*- coding: utf-8 -*-
"""Adaptive Deep Work Focus Guardian Skill for GenPark Personal Agents."""
import json
from typing import Dict, Any

def allocate_dynamic_focus_sprint(user_hrv_rmssd_ms: float, hours_awake: float, task_complexity: str, consecutive_sprints_completed: int = 0) -> Dict[str, Any]:
    # Base focus duration: standard 90-minute ultradian rhythm
    base_minutes = 90.0

    # HRV recovery modifier
    if user_hrv_rmssd_ms >= 65.0:
        hrv_factor = 1.05
    elif user_hrv_rmssd_ms >= 45.0:
        hrv_factor = 1.0
    else:
        hrv_factor = 0.75 # Fatigue detected, shorten sprint

    # Circadian awake decay
    if hours_awake > 14.0:
        awake_factor = 0.60
    elif hours_awake > 10.0:
        awake_factor = 0.85
    else:
        awake_factor = 1.0

    # Consecutive sprint fatigue decay (25m Pomodoro fallback if heavily fatigued)
    sprint_decay = max(0.60, 1.0 - (consecutive_sprints_completed * 0.12))

    adjusted_duration = round(base_minutes * hrv_factor * awake_factor * sprint_decay, 0)
    adjusted_duration = max(25.0, min(90.0, adjusted_duration))

    # Recommended subsequent restorative break duration
    if adjusted_duration >= 75.0:
        break_duration = 20
        break_protocol = "Non-Sleep Deep Rest (NSDR), outdoor walk, or optical horizon viewing."
    elif adjusted_duration >= 45.0:
        break_duration = 10
        break_protocol = "Physical mobility, hydration, zero-screen rest."
    else:
        break_duration = 5
        break_protocol = "Micro-pause stretching."

    return {
        "recommended_focus_sprint_minutes": int(adjusted_duration),
        "post_sprint_break_minutes": break_duration,
        "restorative_protocol": break_protocol,
        "fatigue_modifiers": {
            "hrv_scaling": round(hrv_factor, 2),
            "circadian_scaling": round(awake_factor, 2),
            "sprint_saturation_scaling": round(sprint_decay, 2)
        },
        "target_cognitive_state": "FLOW_STATE_ACTIVE",
        "guardian": "GenPark Neuro-Ergonomic Flow Allocator"
    }

def evaluate_interruption_triage(sender_priority: str, remaining_focus_minutes: int, message_urgency_score: float) -> Dict[str, Any]:
    # VIP Breakthrough conditions
    is_vip = sender_priority in ["vip_family", "executive_leadership"]
    
    if is_vip and message_urgency_score >= 0.85:
        action = "BREAKTHROUGH_AUDIBLE_ALERT"
        rationale = "High-urgency escalation from designated priority sender overrides deep work boundary."
    elif is_vip:
        action = "SILENT_HAPTIC_NUDGE"
        rationale = "Priority contact logged silently on lock screen without audio/visual interruption."
    elif message_urgency_score >= 0.95:
        action = "SYSTEMIC_CRITICAL_ESCALATION"
        rationale = "Severe urgency threshold reached; routing through safety bypass."
    else:
        action = "SQUELCH_AND_BATCH_DIGEST"
        rationale = f"Notification held in ambient escrow; scheduled for release in {remaining_focus_minutes} minutes upon sprint completion."

    return {
        "interruption_action": action,
        "sender_category": sender_priority,
        "active_focus_time_remaining_min": remaining_focus_minutes,
        "action_rationale": rationale,
        "flow_shield_status": "PROTECTED" if action.startswith("SQUELCH") else "CONTROLLED_BYPASS"
    }
