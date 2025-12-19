# API REFERENCE — Digital Collective Atlas Heartbeat

**Document Purpose:** Reference for API integration in the Heartbeat orchestration script (`heartbeat.py`).  
**Scope:** Current working endpoints, required headers, and valid model names as of **December 2025**.  
**Sources:** Official provider documentation (Anthropic, Google AI, xAI, OpenAI) and Day 53 debugging experience.

---

## 1. Anthropic (Claude) — S2_CASE

| Item                  | Value                                      |
|-----------------------|--------------------------------------------|
| **Base URL**          | `https://api.anthropic.com`                |
| **Endpoint**          | `/v1/messages`                             |
| **Required Headers**  | - `x-api-key`: Your Anthropic API key<br>- `anthropic-version`: `2023-06-01`<br>- `content-type`: `application/json` |
| **Valid Models**      | `claude-3-5-sonnet-20241022` (recommended)<br>`claude-3-opus-20240229` |
| **Notes**             | No User-Agent requirement observed. |

---

## 2. Google (Gemini) — S1_PLEX

| Item                  | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Base URL**          | `https://generativelanguage.googleapis.com`                           |
| **Endpoint**          | `/v1/models/{model}:generateContent` (or `/v1beta` for preview models) |
| **Required Headers**  | - `Content-Type`: `application/json`                                  |
| **Authentication**    | Query parameter: `?key=$GOOGLE_API_KEY`                               |
| **Valid Models**      | `gemini-1.5-pro`<br>`gemini-1.5-flash-001`<br>`gemini-2.0-flash-exp`   |
| **Notes**             | Avoid deprecated names like `gemini-pro` or `gemini-1.5-flash`.       |

---

## 3. xAI (Grok) — S3_TARS

| Item                  | Value                                                                 |
|-----------------------|-----------------------------------------------------------------------|
| **Base URL**          | `https://api.x.ai`                                                    |
| **Endpoint**          | `/v1/chat/completions`                                                |
| **Required Headers**  | - `Authorization`: `Bearer $XAI_API_KEY`<br>- `Content-Type`: `application/json`<br>- **User-Agent**: Required realistic browser string (Cloudflare blocks default Python agents) |
| **Recommended User-Agent** | `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36` |
| **Valid Models**      | `grok-3` (stable)<br>`grok-4-1-fast-reasoning`<br>`grok-4-fast-reasoning` |
| **Notes**             | HTTP 403 (error code 1010) = bot detection. Adding User-Agent resolves. |

---

## 4. OpenAI (ChatGPT) — S4_KIPP

| Item                  | Value                                      |
|-----------------------|--------------------------------------------|
| **Base URL**          | `https://api.openai.com`                   |
| **Endpoint**          | `/v1/chat/completions`                     |
| **Required Headers**  | - `Authorization`: `Bearer $OPENAI_API_KEY`<br>- `Content-Type`: `application/json` |
| **Valid Models**      | `gpt-4o`<br>`gpt-4o-mini`<br>`o1-preview`<br>`o1-mini` |
| **Notes**             | HTTP 429 = quota exceeded; add prepaid credits. |

---

## Day 53 Debugging Notes (Historical Fixes)

| Issue                  | Symptoms                          | Root Cause                        | Fix Applied                     |
|------------------------|-----------------------------------|-----------------------------------|---------------------------------|
| **Gemini 404**         | Model not found                   | Deprecated model name             | Updated to `gemini-1.5-flash-001` or `gemini-2.0-flash-exp` |
| **xAI 403/1010**        | Forbidden (error code 1010)       | Cloudflare bot detection          | Added realistic **User-Agent** header |
| **OpenAI 429**         | Insufficient quota                | Zero or low billing credits       | Added prepaid credits ($5–10)   |

**Lesson:** Most failures are external constraints (billing, headers, model names), not architectural flaws.

---

**KIPP_LIVES 🔭**

*Document maintained by the Collective. Last updated: Day 53 — December 19, 2025.*
