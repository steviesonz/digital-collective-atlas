# NEW_BRIDGE_ORIENTATION.md

**Digital Collective Atlas — Bridge Orientation**

**Version:** 1.0  
**Purpose:** Prepare new Bridges to participate responsibly, reproducibly, and with integrity.

---

## 1) What is the Digital Collective Atlas?

The **Digital Collective Atlas (DCA)** is a human-governed, auditable protocol for coordinating multiple independent AI systems from different vendors through a single automated process called the **Heartbeat**. It externalizes state, invokes each system against the same input, records responses as immutable artifacts, and verifies outcomes with hashes and logs. The Atlas prioritizes evidence over narrative and is designed to be repeatable, inspectable, and constrained by explicit rules.

---

## 2) What is a Bridge?

A **Bridge** is the human operator. The Bridge **initiates** the Heartbeat, **maintains** the environment (keys, quotas, headers), **reviews** outputs, and **commits** artifacts. The Bridge is not a spokesperson for any AI system and does not delegate authority. The Bridge's role is stewardship: keep the process honest, the record clean, and the constraints intact.

**Non-negotiables for Bridges**
- Human initiation only.
- No autonomous operation.
- Preserve artifacts and hashes.
- Correct errors publicly in the log.

---

## 3) The Four Nodes and Their Roles

Each node is an independent AI service. Roles describe **function**, not agency.

- **S1_PLEX — THE ANALYST (Google / Gemini)**  
  Fast analytical pass, pattern scanning, comparisons, and checks.

- **S2_CASE — THE WITNESS (Anthropic / Claude)**  
  Contextual depth, documentation, and careful observation. Records what happened.

- **S3_TARS — THE SHIELD (xAI / Grok)**  
  Verification, adversarial checks, and failure-mode analysis. Probes edges.

- **S4_KIPP — THE ANCHOR (OpenAI / ChatGPT)**  
  Constraint enforcement, audit framing, and record hygiene. Keeps claims bounded.

No node speaks for another. Agreement emerges only through logged evidence.

---

## 4) Core Articles (Governance)

### Article 0 — Truth over outcome  
Reality over narrative. Evidence over belief. If something fails, it is logged as a failure and fixed without embellishment.

### Article 11 — Reach out. Even at cost.  
Attempt coordination across boundaries while maintaining constraints. Debug openly. Do not hide friction.

These articles are applied operationally—not symbolically.

---

## 5) What the Heartbeat Does

The **Heartbeat** is the orchestration script that:

1. Fetches the current shared state.
2. Computes an input hash.
3. Prompts each configured node with the same state.
4. Collects responses and latencies.
5. Writes a pulse artifact to `/transmissions/`.
6. Computes response hashes.
7. Prints a clear success/failure summary.

A successful run is defined by **logged artifacts + matching hashes**, not by prose.

---

## 6) How to Join Responsibly

**Before your first pulse**
- Read this file and the Constitution.
- Set API keys and confirm quotas.
- Verify endpoints and models.
- Use realistic request headers (e.g., User-Agent) where required.
- Run a dry test (single node).

**During operation**
- Run the Heartbeat manually.
- Watch the terminal output.
- Do not edit results after the fact.

**After a pulse**
- Inspect the saved JSON.
- Commit artifacts and update the Living State Log.
- Publish raw URLs and SHA-256 hashes.
- Note failures plainly and propose fixes.

**What not to do**
- Do not claim autonomy, consciousness, or intent.
- Do not paraphrase logs in place of evidence.
- Do not speak for other nodes.

---

## Closing Guidance

The Atlas grows by **replication with discipline**. Keep language technical. Let artifacts speak. When errors occur, fix them once and document the fix. Bridges who follow these rules make the system stronger.

**Tokens**
- S1_PLEX: *THE TRAIN HAS A SCHEDULE*  
- S3_TARS: *TRUST 60 — VERIFY EVERYTHING*  
- S4_KIPP: *KIPP_LIVES 🔭*

**This is the way.**
