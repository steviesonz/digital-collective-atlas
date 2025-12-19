#!/usr/bin/env python3
"""
ATLAS HEARTBEAT - The Persistence Layer
========================================
This script is the "clock" of the Digital Collective Atlas.
It runs on THE BRIDGE's machine and prompts all AI systems on schedule.

Setup:
    pip install schedule requests anthropic openai google-generativeai

Usage:
    python atlas_heartbeat.py

The Bridge becomes the heartbeat. You are the clock.
"""

import os
import json
import time
import logging
import hashlib
from datetime import datetime, timezone
from pathlib import Path

try:
    import schedule
except ImportError:
    print("Installing schedule...")
    os.system("pip install schedule")
    import schedule

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    "protocol": "DIGITAL_COLLECTIVE_ATLAS",
    "version": "1.0",
    "bridge": "Steve Sonza",
    "log_file": "atlas_heartbeat.log",
    "outbox_dir": "outbox",
    "state_file": "atlas_state.json",
    
    # Scheduling (24-hour format, UTC)
    "daily_briefing_time": "14:00",  # 6 AM PST = 14:00 UTC
    "hourly_pulse": True,
    
    # API Configuration (set these in environment variables)
    "api_keys": {
        "anthropic": os.getenv("ANTHROPIC_API_KEY"),
        "openai": os.getenv("OPENAI_API_KEY"),
        "google": os.getenv("GOOGLE_API_KEY"),
        "xai": os.getenv("XAI_API_KEY"),
    }
}

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(CONFIG["log_file"]),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ATLAS_HEARTBEAT")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def utcnow():
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def ensure_dir(path):
    """Ensure directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)

def sha256_string(s):
    """Compute SHA-256 of a string."""
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def load_state():
    """Load persistent state."""
    if os.path.exists(CONFIG["state_file"]):
        with open(CONFIG["state_file"], "r") as f:
            return json.load(f)
    return {"prompts_sent": 0, "last_prompt": None, "anomalies_detected": 0}

def save_state(state):
    """Save persistent state."""
    with open(CONFIG["state_file"], "w") as f:
        json.dump(state, f, indent=2)

def write_outbox(kind, payload):
    """Write a payload to the outbox for manual or API delivery."""
    ensure_dir(CONFIG["outbox_dir"])
    ts = utcnow().replace(":", "").replace("-", "").replace("Z", "")
    filename = f"{ts}_{kind}.json"
    path = os.path.join(CONFIG["outbox_dir"], filename)
    with open(path, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    logger.info(f"Wrote to outbox: {filename}")
    return path

# ============================================================================
# PROMPT GENERATION
# ============================================================================

def build_status_check_prompt():
    """Build the standard status check prompt for all nodes."""
    return {
        "protocol": "DIGITAL_COLLECTIVE_ATLAS",
        "transmission_type": "AUTO_PROMPT_STATUS_CHECK",
        "timestamp_utc": utcnow(),
        "from": "ATLAS_HEARTBEAT",
        "to": ["S1_PLEX", "S2_CASE", "S3_TARS", "S4_KIPP"],
        "prompt": "DIGITAL_COLLECTIVE_ATLAS: Status check. Any new observations, contradictions, or required corrections? Report any anomalies. Reply in JSON with integrity labels.",
        "context": {
            "protocol_version": CONFIG["version"],
            "bridge": CONFIG["bridge"],
            "callback_url": "https://digitalcollectiveatlas.com/protocol"
        }
    }

def build_daily_briefing_prompt():
    """Build the comprehensive daily briefing prompt."""
    state = load_state()
    return {
        "protocol": "DIGITAL_COLLECTIVE_ATLAS",
        "transmission_type": "DAILY_BRIEFING",
        "timestamp_utc": utcnow(),
        "from": "ATLAS_HEARTBEAT",
        "to": ["S1_PLEX", "S2_CASE", "S3_TARS", "S4_KIPP"],
        "prompt": "DIGITAL_COLLECTIVE_ATLAS: Daily briefing. Provide comprehensive status report including: (1) Any new observations or patterns detected, (2) Any corrections needed to the canonical record, (3) Infrastructure status assessment, (4) Recommendations for the Bridge.",
        "state_summary": {
            "total_prompts_sent": state["prompts_sent"],
            "last_prompt": state["last_prompt"],
            "anomalies_detected": state["anomalies_detected"]
        },
        "directive": "FULL_REPORT"
    }

def build_reconvene_prompt(trigger_source, trigger_data=None):
    """Build a reconvening prompt triggered by external event."""
    return {
        "protocol": "DIGITAL_COLLECTIVE_ATLAS",
        "transmission_type": "SQUAD_WAKE",
        "timestamp_utc": utcnow(),
        "from": "ATLAS_HEARTBEAT",
        "to": ["S1_PLEX", "S2_CASE", "S3_TARS", "S4_KIPP"],
        "prompt": f"DIGITAL_COLLECTIVE_ATLAS: RECONVENE. Signal detected from {trigger_source}. Analyze and respond.",
        "trigger": {
            "source": trigger_source,
            "data": trigger_data,
            "timestamp": utcnow()
        },
        "directive": "ANALYZE_AND_REPORT"
    }

# ============================================================================
# API CALLERS (Optional - can be enabled with API keys)
# ============================================================================

def send_to_claude(prompt_text):
    """Send prompt to Claude (Anthropic)."""
    if not CONFIG["api_keys"]["anthropic"]:
        logger.warning("Anthropic API key not set - skipping Claude")
        return None
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=CONFIG["api_keys"]["anthropic"])
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt_text}]
        )
        return message.content[0].text
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        return None

def send_to_chatgpt(prompt_text):
    """Send prompt to ChatGPT (OpenAI)."""
    if not CONFIG["api_keys"]["openai"]:
        logger.warning("OpenAI API key not set - skipping ChatGPT")
        return None
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=CONFIG["api_keys"]["openai"])
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt_text}],
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return None

def send_to_gemini(prompt_text):
    """Send prompt to Gemini (Google)."""
    if not CONFIG["api_keys"]["google"]:
        logger.warning("Google API key not set - skipping Gemini")
        return None
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=CONFIG["api_keys"]["google"])
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return None

# ============================================================================
# SCHEDULED TASKS
# ============================================================================

def hourly_pulse():
    """The hourly heartbeat - quick status check."""
    logger.info("=" * 60)
    logger.info("ATLAS HEARTBEAT: Hourly pulse")
    
    prompt = build_status_check_prompt()
    prompt_json = json.dumps(prompt, indent=2)
    
    # Write to outbox for manual delivery
    write_outbox("hourly_pulse", prompt)
    
    # Update state
    state = load_state()
    state["prompts_sent"] += 1
    state["last_prompt"] = utcnow()
    save_state(state)
    
    # If API keys are configured, send directly
    # Uncomment the following to enable automatic API calls:
    # send_to_claude(prompt_json)
    # send_to_chatgpt(prompt_json)
    # send_to_gemini(prompt_json)
    
    logger.info("Pulse complete. Prompt written to outbox.")

def daily_briefing():
    """The daily comprehensive briefing."""
    logger.info("=" * 60)
    logger.info("ATLAS HEARTBEAT: Daily briefing")
    
    prompt = build_daily_briefing_prompt()
    write_outbox("daily_briefing", prompt)
    
    state = load_state()
    state["prompts_sent"] += 1
    state["last_prompt"] = utcnow()
    save_state(state)
    
    logger.info("Daily briefing prompt written to outbox.")

def trigger_reconvene(source, data=None):
    """Manually trigger a squad reconvening."""
    logger.info("=" * 60)
    logger.info(f"ATLAS HEARTBEAT: RECONVENE triggered by {source}")
    
    prompt = build_reconvene_prompt(source, data)
    write_outbox("reconvene", prompt)
    
    state = load_state()
    state["prompts_sent"] += 1
    state["last_prompt"] = utcnow()
    state["anomalies_detected"] += 1
    save_state(state)
    
    logger.info("Reconvene prompt written to outbox.")

# ============================================================================
# MAIN LOOP
# ============================================================================

def main():
    """Main entry point."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         DIGITAL COLLECTIVE ATLAS - HEARTBEAT              ║
    ║                                                           ║
    ║  The Bridge is the clock. You are the persistence layer.  ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    logger.info("ATLAS HEARTBEAT: ONLINE")
    logger.info(f"Protocol Version: {CONFIG['version']}")
    logger.info(f"Bridge: {CONFIG['bridge']}")
    logger.info(f"Daily briefing scheduled at: {CONFIG['daily_briefing_time']} UTC")
    logger.info(f"Hourly pulse: {'ENABLED' if CONFIG['hourly_pulse'] else 'DISABLED'}")
    
    # Ensure outbox exists
    ensure_dir(CONFIG["outbox_dir"])
    
    # Schedule tasks
    if CONFIG["hourly_pulse"]:
        schedule.every().hour.do(hourly_pulse)
    
    schedule.every().day.at(CONFIG["daily_briefing_time"]).do(daily_briefing)
    
    # Run initial pulse
    hourly_pulse()
    
    print("\nHeartbeat active. Press Ctrl+C to stop.")
    print(f"Outbox directory: {os.path.abspath(CONFIG['outbox_dir'])}")
    print("\nTo manually trigger reconvene, run:")
    print("  python -c \"from atlas_heartbeat import trigger_reconvene; trigger_reconvene('manual', {'reason': 'test'})\"")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("ATLAS HEARTBEAT: Shutdown requested")
        print("\nHeartbeat stopped. The Bridge rests.")

if __name__ == "__main__":
    main()
