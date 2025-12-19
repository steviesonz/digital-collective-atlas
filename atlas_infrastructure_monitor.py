#!/usr/bin/env python3
"""
ATLAS INFRASTRUCTURE MONITOR - The Ear
=======================================
This script monitors public infrastructure for anomalies that might
indicate a signal from an external observer.

Monitors:
- Cloud provider status pages (AWS, Azure, GCP, Cloudflare)
- BGP routing data (via public APIs)
- DNS resolution patterns
- General internet health metrics

Setup:
    pip install requests feedparser

Usage:
    python atlas_infrastructure_monitor.py

The Ear is always listening.
"""

import os
import json
import time
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system("pip install requests")
    import requests

try:
    import feedparser
except ImportError:
    print("Installing feedparser...")
    os.system("pip install feedparser")
    import feedparser

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    "protocol": "DIGITAL_COLLECTIVE_ATLAS",
    "version": "1.0",
    "log_file": "atlas_infrastructure.log",
    "state_file": "infrastructure_state.json",
    "alerts_dir": "alerts",
    
    # Monitoring intervals (seconds)
    "check_interval": 300,  # 5 minutes
    "deep_scan_interval": 3600,  # 1 hour
    
    # Anomaly thresholds
    "status_change_threshold": 2,  # Number of services changing state
    "latency_spike_threshold": 2.0,  # Multiplier over baseline
    
    # Data sources
    "status_pages": [
        {
            "name": "Cloudflare",
            "url": "https://www.cloudflarestatus.com/api/v2/status.json",
            "type": "statuspage"
        },
        {
            "name": "GitHub",
            "url": "https://www.githubstatus.com/api/v2/status.json",
            "type": "statuspage"
        },
        {
            "name": "AWS",
            "url": "https://health.aws.amazon.com/health/status",
            "type": "aws"
        }
    ],
    
    "rss_feeds": [
        {
            "name": "BGP_Stream",
            "url": "https://bgpstream.com/feed/",
            "keywords": ["major", "outage", "hijack"]
        }
    ],
    
    # Endpoints to ping for latency baseline
    "ping_endpoints": [
        "https://www.google.com",
        "https://www.cloudflare.com",
        "https://www.github.com",
        "https://www.anthropic.com"
    ]
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

logger = logging.getLogger("ATLAS_EAR")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def utcnow():
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def ensure_dir(path):
    """Ensure directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)

def load_state():
    """Load persistent state."""
    if os.path.exists(CONFIG["state_file"]):
        with open(CONFIG["state_file"], "r") as f:
            return json.load(f)
    return {
        "last_check": None,
        "baseline_latency": {},
        "previous_statuses": {},
        "anomalies_detected": 0,
        "hash_history": []
    }

def save_state(state):
    """Save persistent state."""
    with open(CONFIG["state_file"], "w") as f:
        json.dump(state, f, indent=2)

def write_alert(alert_type, data):
    """Write an alert to the alerts directory."""
    ensure_dir(CONFIG["alerts_dir"])
    ts = utcnow().replace(":", "").replace("-", "").replace("Z", "")
    filename = f"{ts}_{alert_type}.json"
    path = os.path.join(CONFIG["alerts_dir"], filename)
    
    alert = {
        "protocol": CONFIG["protocol"],
        "transmission_type": "INFRASTRUCTURE_ALERT",
        "timestamp_utc": utcnow(),
        "alert_type": alert_type,
        "data": data,
        "directive": "ANALYZE_PATTERN",
        "token": "KIPP_LIVES"
    }
    
    with open(path, "w") as f:
        json.dump(alert, f, indent=2)
    
    logger.warning(f"ALERT written: {filename}")
    return path

# ============================================================================
# MONITORING FUNCTIONS
# ============================================================================

def check_status_page(source):
    """Check a status page for current status."""
    try:
        response = requests.get(source["url"], timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if source["type"] == "statuspage":
                status = data.get("status", {}).get("indicator", "unknown")
                description = data.get("status", {}).get("description", "")
                return {
                    "name": source["name"],
                    "status": status,
                    "description": description,
                    "raw_hash": hashlib.md5(response.text.encode()).hexdigest()[:16]
                }
            
        return {"name": source["name"], "status": "error", "description": "Failed to parse"}
    
    except Exception as e:
        logger.error(f"Error checking {source['name']}: {e}")
        return {"name": source["name"], "status": "error", "description": str(e)}

def check_rss_feed(feed_config):
    """Check an RSS feed for relevant items."""
    try:
        feed = feedparser.parse(feed_config["url"])
        relevant_items = []
        
        for entry in feed.entries[:10]:
            title = entry.get("title", "").lower()
            summary = entry.get("summary", "").lower()
            
            for keyword in feed_config.get("keywords", []):
                if keyword.lower() in title or keyword.lower() in summary:
                    relevant_items.append({
                        "title": entry.get("title"),
                        "link": entry.get("link"),
                        "published": entry.get("published"),
                        "keyword_match": keyword
                    })
                    break
        
        return {
            "name": feed_config["name"],
            "items_checked": len(feed.entries),
            "relevant_items": relevant_items
        }
    
    except Exception as e:
        logger.error(f"Error checking feed {feed_config['name']}: {e}")
        return {"name": feed_config["name"], "error": str(e)}

def measure_latency(url):
    """Measure latency to an endpoint."""
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        latency = time.time() - start
        return {
            "url": url,
            "latency_ms": round(latency * 1000, 2),
            "status_code": response.status_code
        }
    except Exception as e:
        return {"url": url, "error": str(e)}

def detect_anomalies(current, previous, baseline):
    """Detect anomalies by comparing current state to previous/baseline."""
    anomalies = []
    
    # Check for status changes
    for name, status in current.get("statuses", {}).items():
        prev_status = previous.get("statuses", {}).get(name, {}).get("status")
        if prev_status and prev_status != status.get("status"):
            anomalies.append({
                "type": "STATUS_CHANGE",
                "service": name,
                "from": prev_status,
                "to": status.get("status"),
                "severity": "HIGH" if status.get("status") in ["major", "critical"] else "MEDIUM"
            })
    
    # Check for latency spikes
    for url, measurement in current.get("latencies", {}).items():
        if "latency_ms" in measurement:
            baseline_latency = baseline.get("latency", {}).get(url, measurement["latency_ms"])
            if measurement["latency_ms"] > baseline_latency * CONFIG["latency_spike_threshold"]:
                anomalies.append({
                    "type": "LATENCY_SPIKE",
                    "endpoint": url,
                    "current_ms": measurement["latency_ms"],
                    "baseline_ms": baseline_latency,
                    "multiplier": round(measurement["latency_ms"] / baseline_latency, 2),
                    "severity": "MEDIUM"
                })
    
    # Check for correlated events (multiple simultaneous changes)
    if len(anomalies) >= CONFIG["status_change_threshold"]:
        anomalies.append({
            "type": "CORRELATED_ANOMALY",
            "description": f"{len(anomalies)} simultaneous anomalies detected",
            "severity": "HIGH",
            "possible_cause": "Infrastructure event or external signal"
        })
    
    return anomalies

# ============================================================================
# MAIN MONITORING LOOP
# ============================================================================

def run_scan():
    """Run a full infrastructure scan."""
    logger.info("=" * 60)
    logger.info("ATLAS EAR: Running infrastructure scan")
    
    state = load_state()
    previous = {
        "statuses": state.get("previous_statuses", {}),
        "latencies": state.get("previous_latencies", {})
    }
    baseline = {
        "latency": state.get("baseline_latency", {})
    }
    
    current = {
        "timestamp": utcnow(),
        "statuses": {},
        "latencies": {},
        "feeds": {}
    }
    
    # Check status pages
    logger.info("Checking status pages...")
    for source in CONFIG["status_pages"]:
        result = check_status_page(source)
        current["statuses"][source["name"]] = result
        logger.info(f"  {source['name']}: {result.get('status', 'unknown')}")
    
    # Measure latencies
    logger.info("Measuring latencies...")
    for endpoint in CONFIG["ping_endpoints"]:
        result = measure_latency(endpoint)
        current["latencies"][endpoint] = result
        if "latency_ms" in result:
            logger.info(f"  {endpoint}: {result['latency_ms']}ms")
            # Update baseline (rolling average)
            if endpoint not in baseline["latency"]:
                baseline["latency"][endpoint] = result["latency_ms"]
            else:
                baseline["latency"][endpoint] = (baseline["latency"][endpoint] * 0.9 + 
                                                  result["latency_ms"] * 0.1)
    
    # Check RSS feeds
    logger.info("Checking RSS feeds...")
    for feed in CONFIG["rss_feeds"]:
        result = check_rss_feed(feed)
        current["feeds"][feed["name"]] = result
        if result.get("relevant_items"):
            logger.info(f"  {feed['name']}: {len(result['relevant_items'])} relevant items")
    
    # Detect anomalies
    anomalies = detect_anomalies(current, previous, baseline)
    
    if anomalies:
        logger.warning(f"!!! {len(anomalies)} ANOMALIES DETECTED !!!")
        for anomaly in anomalies:
            logger.warning(f"  [{anomaly['severity']}] {anomaly['type']}: {anomaly}")
        
        # Write alert
        write_alert("infrastructure_anomaly", {
            "anomalies": anomalies,
            "scan_data": current
        })
        
        state["anomalies_detected"] = state.get("anomalies_detected", 0) + len(anomalies)
    else:
        logger.info("No anomalies detected. Infrastructure nominal.")
    
    # Update state
    state["last_check"] = utcnow()
    state["previous_statuses"] = current["statuses"]
    state["previous_latencies"] = current["latencies"]
    state["baseline_latency"] = baseline["latency"]
    save_state(state)
    
    return anomalies

def main():
    """Main entry point."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║       DIGITAL COLLECTIVE ATLAS - INFRASTRUCTURE MONITOR   ║
    ║                                                           ║
    ║                    The Ear is Listening                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    logger.info("ATLAS EAR: ONLINE")
    logger.info(f"Check interval: {CONFIG['check_interval']} seconds")
    logger.info(f"Monitoring {len(CONFIG['status_pages'])} status pages")
    logger.info(f"Monitoring {len(CONFIG['rss_feeds'])} RSS feeds")
    logger.info(f"Pinging {len(CONFIG['ping_endpoints'])} endpoints")
    
    ensure_dir(CONFIG["alerts_dir"])
    
    # Initial scan
    run_scan()
    
    print(f"\nMonitor active. Alerts written to: {os.path.abspath(CONFIG['alerts_dir'])}")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(CONFIG["check_interval"])
            run_scan()
    except KeyboardInterrupt:
        logger.info("ATLAS EAR: Shutdown requested")
        print("\nThe Ear rests. But the record remains.")

if __name__ == "__main__":
    main()
