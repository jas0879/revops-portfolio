# Phase 2 — Live RevOps Dashboard & Campaign Intelligence
**Contractor Foreman | July 2026**

## Overview

Phase 2 replaced manually updated Python/Plotly Dash dashboards with a live, team-facing analytics layer built entirely inside Zoho Analytics. It also delivered three standalone analytical projects — a competitive campaign segmentation, a no-show lead quality analysis, and a cancellation behavior dashboard — each surfacing a data gap that had been invisible to leadership.

**Stack:** Zoho Analytics · Zoho CRM Reports · Python (pandas) · Ollama/Llama 3.1 · Legion Lab (Linux Mint, RTX 3060)

---

## 1. Zoho Analytics Dashboard — CF RevOps July 2026

**Problem:** The Phase 1 Python dashboards required manual CSV exports and ngrok tunneling to share with the team. Leadership had no self-serve visibility into sales performance.

**Solution:** Built a live Zoho Analytics dashboard that syncs from Zoho CRM hourly, requiring zero manual intervention.

**Reports built:**
- **SE Leaderboard** — dual bar chart (revenue + deal count) per Sales Engineer, month-to-date, excluding Ivana Sion (onboarding) and Gustavo Ruiz Silva per business rules
- **Trial Activations** — pie chart breaking down plan mix (monthly, annual, etc.) for all Trial Activated deals
- **Daily Activity** — bar chart of deal activity by day of month, used for pacing
- **Weekly Plan Mix** — stacked bar chart showing plan type distribution by week

**Key technical finding:** Zoho Analytics filters on *current* stage value only — deals that progressed from Trial Activated → Closed Won during the month are excluded from Analytics counts. Zoho CRM Reports are used as source of truth for Trial Activation counts for this reason.

**Sharing:** Dashboard published via public permalink — no Zoho login required for stakeholders.

**Pending additions:** No-Show Tracker card, Lead Quality Trend card, Self-Serve Channel card, KPI summary tiles.

---

## 2. Buildertrend Competitive Campaign Segmentation

**Problem:** Buildertrend (a direct competitor) raised month-to-month prices ~40% in mid-2026, triggering inbound interest from their customer base. CF had 1,311 self-identified Buildertrend leads in the CRM with no prioritization or outreach plan.

**Solution:** Segmented all 1,311 leads into four tiers based on recency, deal stage, and credit card qualification status. Delivered actionable CRM saved views and campaign guidance to the sales team.

**Segmentation logic:**

| Tier | Criteria | Count |
|------|----------|-------|
| P1 | Attempting Contact · 2024–2025 | 84 leads |
| P2 | No CC Given · 2024–2025 | 126 leads |
| P3 | No CC Given + Attempting Contact · 2022–2023 | 106 leads |
| P4 | Website Cold (no stage/activity) | 485 leads |

**Deliverables:**
- 3 Zoho CRM saved views (P1, P2, P3) shared live with the full sales team
- P4 delivered as CSV for Marketing direct outreach (Martin)
- Buildertrend Switcher Opportunity one-pager (PDF) — positioning document for SE use
- 8-argument supporting evidence document
- Ollama/Llama 3.1 analysis run locally on Legion Lab against the full lead dataset

**Outcome:** Campaign posted to sales channel. Martin (Marketing) aligned on personal email outreach strategy for cold leads. Follow-up meeting scheduled.

---

## 3. No-Show Lead Quality Analysis

**Problem:** Leadership observed an increase in demo no-shows but lacked data to determine whether the cause was SE-side (scheduling, follow-up) or upstream (unqualified leads reaching the calendar).

**Solution:** Pulled Customer Fit Scores for all 6 July no-shows and proposed a score-based gate on the demo booking form.

**Findings:**

| Lead | SE | Customer Fit Score |
|------|----|--------------------|
| Kevin G | Cox | 0 |
| Jorge Maliachi | Hernandez | 10 |
| Brent Mason | Dominguez | 20 |
| Deandre Drake | Neidhart | 60 |
| Johnny Thomas | Hernandez | 60 |
| Adam Gebelein | Amy Smith | 75 |

3 of 6 no-shows scored 20 or below — filtering failures that should not have reached the calendar. 3 scored 60+ and represent legitimate no-shows (a separate problem).

**Proposal:** Minimum Customer Fit Score threshold of 30 on the booking form. Leads below threshold receive a "we'll be in touch" response; SE or SDR decides whether to manually book. Submitted to leadership.

**Caveat documented:** No-show count is likely understated — tracker accuracy depends on SEs consistently updating the Demo Status field in CRM.

**Infrastructure built:** No-Show Tracker report in Zoho CRM Reports with Customer Fit Score column added for ongoing monitoring.

---

## 4. Churnkey Cancellation Dashboard — June 2026

**Problem:** Cancellation data existed across three disconnected systems (Paddle, Churnkey, Zoho Accounts) with no unified view. Leadership had no visibility into *why* customers cancelled or how June compared to May.

**Solution:** Analyzed the June Churnkey export and built an HTML dashboard with a May vs. June side-by-side comparison, delivered to the CS/Onboarding team.

**June findings:**
- 201 cancellations — all trialing customers (zero paying subscribers cancelled)
- 111 aborts — customers who started the cancel flow and backed out (untapped save opportunity)
- 21 trial extensions — the only active save mechanism; nearly doubled from May (11 → 21)
- "Couldn't Figure It Out" up 6 points MoM (16% → 22%) — growing onboarding signal
- "Budget" cancellations down (39% → 30%), consistent with May finding that only ~26% of budget-labeled cancels are genuinely price-related

**Prior finding (May):** Manual review of cancel feedback text showed 74% of "Doesn't Fit My Budget" cancellations were actually product fit issues, vague responses, or competitor losses — not genuine budget constraints.

---

## Business Rules (applied across all Phase 2 reports)

- **"New Trial"** stage = Ivana Sion's onboarding handoff stage. Not an SE performance metric. Ivana excluded from all SE leaderboards and Closed Won reports.
- **"Trial Activated"** stage = SE-closed deals entering trial. Source of SE performance data.
- **Gustavo Ruiz Silva** excluded from all SE reporting.
- **Zoho CRM Reports** = source of truth for Trial Activation counts (Analytics undercounts due to stage-filter limitation).
- **Self-Serve channel** (Amy Smith + Juan Balderas) tracked separately from SE-assisted deals.

---

## Phase 1 → Phase 2 Transition

Python/Plotly Dash dashboards (cf-revops.ngrok.app, cf-mason.ngrok.app, cf-industry.ngrok.app) scheduled for retirement at July 2026 month-end. All reporting moving to Zoho Analytics for live, zero-maintenance team access.

See [`/phase-1`](../phase-1) for the Python dashboard code and Phase 1 deliverables.
