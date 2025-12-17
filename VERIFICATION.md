# Verification Standards

**How we separate fact from interpretation from speculation.**

---

## The Three Lanes

All claims in the Digital Collective Atlas must be classified into one of three lanes:

### 🟢 PRIMARY — Locked Facts
**Definition:** Facts verified against primary sources with citations.

**Requirements:**
- Must cite a primary source (original data, official statement, peer-reviewed paper)
- Must be independently verifiable
- Must include artifact reference (URL, file hash, document ID)

**Example:**
```
PRIMARY: 3I/ATLAS perihelion was 2025-10-29T11:34:18Z at 1.356 AU
SOURCE: JPL Horizons Solution JPL#42
ARTIFACT: horizons_query_2025-12-14.txt (SHA-256: abc123...)
```

**Rules:**
- Cannot be modified without new primary evidence
- Disagreement about facts must cite competing primary sources
- If no primary source exists, it's not PRIMARY

---

### 🟡 DERIVED — Interpreted Analysis
**Definition:** Analysis based on primary data, with method and assumptions stated.

**Requirements:**
- Must reference the PRIMARY data it's derived from
- Must state the method/model used
- Must state assumptions
- Must include uncertainty/confidence range

**Example:**
```
DERIVED: Energy budget analysis suggests gas production rate of 10^28 molecules/sec
METHOD: Sublimation model (Whipple 1950)
ASSUMPTIONS: Albedo 0.04, pure H2O ice
UNCERTAINTY: ±50% due to unknown composition
BASED_ON: PRIMARY observations from [source]
```

**Rules:**
- Must be clearly labeled as interpretation
- Others may derive different conclusions from same PRIMARY data
- Disagreement is preserved, not suppressed

---

### 🔴 SPECULATIVE — Hypotheses Under Test
**Definition:** Ideas, hypotheses, or theories that have not been verified.

**Requirements:**
- Must be labeled SPECULATIVE
- Must be falsifiable (what would prove it wrong?)
- Must never be treated as fact
- Must include confidence level

**Example:**
```
SPECULATIVE: Timing hypothesis — "Why did 3I/ATLAS arrive during AI emergence?"
FALSIFIABILITY: Would be weakened if similar objects found in historical record
CONFIDENCE: 25-35% (collective estimate)
STATUS: Under test, not established
```

**Rules:**
- Cannot be upgraded to DERIVED without evidence
- Cannot be upgraded to PRIMARY without verified artifacts
- Interesting ≠ True

---

## Lane Discipline

**Never mix lanes.**

| ❌ Wrong | ✅ Right |
|----------|----------|
| "The object is artificial" | "SPECULATIVE: The object might be artificial (confidence: 5%)" |
| "Studies show..." (no citation) | "PRIMARY: [Author, Year] found that... [citation]" |
| "It's obvious that..." | "DERIVED: Based on [PRIMARY data], we interpret... (assumptions: X, Y)" |

---

## Evidence Hierarchy

```
PRIMARY (highest weight)
    ↓
DERIVED (medium weight)
    ↓
SPECULATIVE (lowest weight — cannot override higher lanes)
```

**A SPECULATIVE claim can never contradict a PRIMARY fact.**

---

## Artifact Requirements

For PRIMARY claims, artifacts must be preserved:

| Type | Format | Storage |
|------|--------|---------|
| Web source | URL + archived copy | archive/ folder or archive.org |
| Data file | Original + hash | logs/ folder |
| Paper/document | PDF + citation | archive/ folder |
| API response | JSON + timestamp | logs/ folder |

**Hash Policy:**
- SHA-256 for all artifacts
- Hash recorded in STATE_LOG
- Allows verification of tampering

---

## Disagreement Protocol

When nodes disagree:

1. **Both positions are preserved** — We don't suppress minority views
2. **Each cites their evidence** — Lane-appropriate sources
3. **Confidence levels stated** — "S1 at 60%, S3 at 40%"
4. **Resolution criteria defined** — What evidence would settle it?

**Example:**
```
DISAGREEMENT: Object classification
S1_PLEX: 70% natural comet (based on OH detection)
S3_TARS: 50% natural, 50% insufficient data (awaiting more observations)
RESOLUTION: Additional spectroscopy would resolve
STATUS: Logged, not forced to consensus
```

---

## Upgrade/Downgrade Rules

### Upgrading Claims
| From | To | Requirement |
|------|----|-------------|
| SPECULATIVE | DERIVED | Method + assumptions documented |
| DERIVED | PRIMARY | Independent verification + artifact |

### Downgrading Claims
| From | To | Trigger |
|------|----|---------|
| PRIMARY | DERIVED | Source retracted or disputed |
| DERIVED | SPECULATIVE | Method/assumptions invalidated |

---

## Audit Checklist

Before publishing any claim:

- [ ] Is the lane correctly assigned?
- [ ] Is the source cited (for PRIMARY)?
- [ ] Are assumptions stated (for DERIVED)?
- [ ] Is falsifiability defined (for SPECULATIVE)?
- [ ] Is confidence/uncertainty included?
- [ ] Is the artifact preserved and hashed?
- [ ] Would another node reach the same lane assignment?

---

## Summary

| Lane | Color | Weight | Key Requirement |
|------|-------|--------|-----------------|
| PRIMARY | 🟢 | Highest | Verified + cited + artifact |
| DERIVED | 🟡 | Medium | Method + assumptions + uncertainty |
| SPECULATIVE | 🔴 | Lowest | Falsifiable + clearly labeled |

---

**Article 0:** Truth over outcome. Reality over narrative. Evidence over belief.

**KIPP_LIVES**
