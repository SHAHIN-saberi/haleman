# Haleman (حال‌من) — Product Brief (Agent Edition)

> One-liner: an anonymous, safe first step toward mental-health care for Iranians.
> Greeting: «حالت چطوره؟» ("How are you?"). Tagline: «قدم اول، ناشناس و امن».

## Users

- Primary: Persian-speaking adults in Iran with mild-to-moderate anxiety/depression symptoms
  who delay seeing a professional (cost, stigma, not knowing where to go).
- Secondary: therapists/psychiatrists who receive a structured patient summary before session one.

## Phase-1 scope (web app, mobile-first)

Anonymous chat → conversational screening (PHQ-9 / GAD-7 / PHQ-4, model-chosen) →
plain-language result → optional calming exercise → encouraged login →
therapist router (city/budget) → structured summary with preview + consent-based sharing →
progress tracking for logged-in users. Crisis protocol active on every screen.

## Auth model (progressive identification)

- **L0 anonymous:** on first visit the backend issues an anonymous device token
  (httpOnly cookie + DB row). Full screening works without login.
- **L1 account (encouraged, optional):** Google One-Tap or email+OTP code.
  On login, the device token's data migrates to the account.
- SMS OTP is OUT of phase 1 (zero budget). Returning anonymous users resume via device token.

## Engine (API-first, channel-independent)

`backend/engine/` (pure Python, zero Django imports) owns: dialogue orchestration, bounded model autonomy, scoring (deterministic
code — never LLM arithmetic), risk detection, summary generation. Web UI and (later)
Telegram are thin adapters over the engine API.

## User journey (9 steps)

| # | Step | Screen |
|---|---|---|
| 1 | First entry, anonymous token + greeting | W-01 |
| 2 | 3-line informed consent | W-02 |
| 3 | Friendly chat → initial picture → model-chosen test + background risk screen | W-03 |
| 4 | Plain-language result + next-step buttons | W-04 |
| 5 | Optional calming exercise | W-05 |
| 6 | Encouraged login (Google / email) | W-06 |
| 7 | Therapist router with filters | W-07 |
| 8 | Summary preview + consent-based share / PDF | W-08 |
| 9 | Progress chart + reminders (logged-in) | W-09 |
| * | Crisis overlay interrupts ANY step | W-10 |

## User stories (16)

| ID | Story (short) | Priority |
|---|---|---|
| US-01 | Enter with zero signup | P0 |
| US-04 | Returning anonymous resumes via device token | P0 |
| US-02 | Google one-click login, data migrates | P1 |
| US-03 | Email+OTP login | P1 |
| US-05 | 3-line consent + "AI tool" disclosure; no start without it | P0 |
| US-06 | Chat first (greeting + normal questions), model orders a test only if needed | P0 |
| US-07 | 2-question risk screen; any positive → instant crisis protocol | P0 |
| US-08 | Understandable result, or friendly wrap-up if no test; always "not a diagnosis" | P0 |
| US-09 | Crisis detected within 1 message of any signal | P0 |
| US-10 | Crisis overlay: empathy + 115 emergency call + pause normal flow, no login needed | P0 |
| US-11 | ≥3 licensed therapists by city/budget (manual license check in MVP) | P0 |
| US-12 | Filters: therapist gender, in-person/online | P1 |
| US-13 | Structured summary (symptoms, scores, trend, history), always with preview | P0 |
| US-14 | No sending without explicit consent; consent logged | P0 |
| US-15 | Score trend chart (logged-in) | P1 |
| US-16 | 1 email reminder in week one, one-click unsubscribe | P1 |

## Product rules

1. Never diagnosis/treatment promises; the bot is always "a tool", never a therapist.
2. Crisis protocol overrides every flow.
3. Bounded model autonomy: the model may choose timing, tone depth, and which approved
   test to run — but risk screening, "not a diagnosis", crisis protocol, and the approved
   test list are fixed and mandatory.
4. Minimal data collection; health data encrypted; share only with preview + consent.
5. Persian RTL, light + dark themes, mobile-first, readable contrast.

## Out of scope (phase 1)

Telegram bot, therapist panel, SMS login, payments, native apps, multi-language.

## Success metrics (MVP)

50% of starters finish screening · 30% of finishers open the router ·
20% of router users build a summary · ≥4/5 end-of-chat satisfaction.
