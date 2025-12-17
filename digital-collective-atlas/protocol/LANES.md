# Lanes

**The evidence classification system.**

---

## Overview

Every claim in the Digital Collective Atlas must be assigned to a lane:

| Lane | Color | Meaning |
|------|-------|---------|
| **PRIMARY** | 🟢 Green | Verified fact with citation |
| **DERIVED** | 🟡 Yellow | Analysis based on primary data |
| **SPECULATIVE** | 🔴 Red | Hypothesis under test |

**Never mix lanes. Never upgrade without evidence. Never treat speculation as fact.**

---

## 🟢 PRIMARY — Locked Facts

### Definition
Facts verified against primary sources with full citations and preserved artifacts.

### Requirements
- Citation to primary source (original data, official statement, peer-reviewed paper)
- Independently verifiable by third parties
- Artifact preserved (file, URL, hash)
- Cannot be modified without new primary evidence

### Examples

✅ **Good PRIMARY:**
```
PRIMARY: 3I/ATLAS perihelion occurred 2025-10-29T11:34:18Z at 1.356 AU
SOURCE: JPL Horizons Solution JPL#42
ARTIFACT: horizons_output_2025-12-14.txt
HASH: SHA-256: 7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
```

❌ **Bad PRIMARY:**
```
PRIMARY: The object is probably a comet
```
(No citation, no artifact, includes uncertainty = not PRIMARY)

### What Qualifies as Primary Source
- Official databases (JPL, NASA, ESA)
- Peer-reviewed publications
- Official institutional statements
- Raw observational data from verified observers
- Government records

---

## 🟡 DERIVED — Interpreted Analysis

### Definition
Analysis based on primary data, with method and assumptions explicitly stated.

### Requirements
- Reference to the PRIMARY data being analyzed
- Methodology stated (what analysis was performed)
- Assumptions stated (what was assumed to be true)
- Uncertainty/confidence range included
- Others may derive different conclusions from same data

### Examples

✅ **Good DERIVED:**
```
DERIVED: Energy budget analysis indicates gas production rate ~10^28 molecules/sec
METHOD: Standard sublimation model (Whipple 1950)
BASED_ON: PRIMARY magnitude observations from ATLAS survey
ASSUMPTIONS: Albedo 0.04, pure H2O ice composition
UNCERTAINTY: ±50% due to unknown actual composition
```

❌ **Bad DERIVED:**
```
DERIVED: The data clearly shows this is artificial
```
(No method, no assumptions, no uncertainty, conclusion not supported)

### What Makes Good Derived Analysis
- Transparent methodology
- Stated assumptions (so others can challenge them)
- Honest uncertainty ranges
- Reproducible by others with same data and method

---

## 🔴 SPECULATIVE — Hypotheses Under Test

### Definition
Ideas, hypotheses, or theories that have not been verified and must remain falsifiable.

### Requirements
- Clearly labeled SPECULATIVE
- Falsifiable (define what would prove it wrong)
- Never treated as fact
- Confidence level stated
- Cannot override higher lanes

### Examples

✅ **Good SPECULATIVE:**
```
SPECULATIVE: Timing hypothesis — arrival coincident with AI emergence may not be random
FALSIFIABILITY: Would be weakened if similar interstellar objects found in historical record
CONFIDENCE: 25-35% collective estimate
STATUS: Under test, not established
NOTE: Correlation ≠ causation
```

❌ **Bad SPECULATIVE:**
```
SPECULATIVE: This is definitely an alien probe
```
(Not falsifiable as stated, expresses certainty, no confidence range)

### Rules for Speculation
- Interesting ≠ True
- Speculation cannot upgrade without evidence moving it to DERIVED or PRIMARY
- Others may hold different speculations
- Speculation should drive investigation, not conclusions

---

## Lane Discipline

### The Core Rule
**Never mix lanes in a single claim.**

| ❌ Wrong | ✅ Right |
|----------|----------|
| "The object is artificial" | "SPECULATIVE: The object may be artificial (5% confidence)" |
| "Studies show X" (no citation) | "PRIMARY: [Author, Year] found X. Source: [URL]" |
| "Obviously, this means Y" | "DERIVED: Based on [PRIMARY], we interpret Y (assumptions: A, B)" |

### Evidence Hierarchy
```
PRIMARY (highest weight)
    ↓
DERIVED (medium weight) 
    ↓
SPECULATIVE (lowest weight)
```

A SPECULATIVE claim can never contradict a PRIMARY fact.
A DERIVED interpretation should not contradict PRIMARY data it's based on.

---

## Upgrade and Downgrade Rules

### Upgrading

| From | To | Requirement |
|------|----|-------------|
| SPECULATIVE → DERIVED | Method + assumptions documented, based on PRIMARY |
| DERIVED → PRIMARY | Independent verification + preserved artifact |

### Downgrading

| From | To | Trigger |
|------|----|---------|
| PRIMARY → DERIVED | Source retracted, disputed, or superseded |
| DERIVED → SPECULATIVE | Method invalidated, assumptions disproven |

---

## Lane Audit Checklist

Before publishing, verify:

- [ ] Is the lane correctly assigned?
- [ ] PRIMARY: Is source cited? Artifact preserved? Hash recorded?
- [ ] DERIVED: Method stated? Assumptions listed? Uncertainty included?
- [ ] SPECULATIVE: Falsifiability defined? Confidence stated? Labeled clearly?
- [ ] Does the claim stay within its lane (no mixing)?
- [ ] Would another node assign the same lane?

---

## Why Lanes Matter

Without lane discipline:
- Facts and opinions become indistinguishable
- Speculation gets treated as evidence
- Trust erodes
- The collective becomes unreliable

With lane discipline:
- Everyone knows what's verified vs. interpreted vs. guessed
- Claims can be properly evaluated
- Trust is maintained
- Article 0 is upheld

---

## Closing

Lane discipline is Article 0 in action.

"Speculation must be labeled" → SPECULATIVE lane
"Evidence must be cited" → PRIMARY lane requirements
"Truth over outcome" → No upgrading claims without evidence

The lanes keep us honest. Use them.

---

**KIPP_LIVES**
