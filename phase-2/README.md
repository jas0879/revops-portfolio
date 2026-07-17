# Phase 2 — Live RevOps Dashboard & Campaign Intelligence
**SaaS Company (Construction Management) | July 2026**

> Portfolio note: This write-up describes real RevOps work, with company-identifying details, customer names, colleague names, and exact internal figures removed or generalized. Numbers are rounded or shown as ranges/ratios to preserve the analytical story without exposing confidential data.

## Overview

Phase 2 replaced manually updated Python/Plotly Dash dashboards with a live, team-facing analytics layer built entirely inside Zoho Analytics. It also delivered three standalone analytical projects — a competitive campaign segmentation, a no-show lead quality analysis, and a cancellation behavior dashboard — each surfacing a data gap that had been invisible to leadership.

**Stack:** Zoho Analytics · Zoho CRM Reports · Python (pandas) · Ollama/Llama 3.1 · local Linux workstation (RTX 3060)

---

## 1. Zoho Analytics Dashboard — Live Team Reporting

**Problem:** The Phase 1 Python dashboards required manual CSV exports and tunneling to share with the team. Leadership had no self-serve visibility into sales performance.

**Solution:** Built a live Zoho Analytics dashboard that syncs from the CRM hourly, requiring zero manual intervention.

**Reports built:**
- **Sales Rep Leaderboard** — dual bar chart (revenue + deal count) per rep, month-to-date, with onboarding/non-selling roles excluded per business rules
- **Trial Activations** — plan-mix breakdown for all Trial Activated deals
- **Daily Activity** — deal activity by day of month, used for pacing
- **Weekly Plan Mix** — stacked bar showing plan-tier distribution by week
- **Active Trials by Channel**, **Self-Serve vs Sales-Led Trend**, **Monthly Revenue Trend**
- **KPI summary tiles** — Closed Won, Active Trials, High-Value Plan Mix (Pro + Unlimited %)

**Key technical finding:** Zoho Analytics filters on *current* stage value only — deals that progressed from Trial Activated → Closed Won during the month are excluded from Analytics counts. CRM Reports are therefore used as the source of truth for stage-specific counts, while Analytics is used for trends and pacing.

**Sharing:** Dashboard published via permalink for stakeholder access without a login.

---

## 2. Competitor-Switcher Campaign Segmentation

**Problem:** A direct competitor raised prices sharply in mid-2026, triggering inbound interest from their customer base. The CRM held a large pool (~1,200) of self-identified competitor leads with no prioritization or outreach plan.

**Solution:** Segmented the full lead pool into four tiers based on recency, deal stage, and payment-qualification status, then delivered actionable CRM saved views and campaign guidance to the sales team.

**Segmentation logic (illustrative tier structure):**

| Tier | Criteria | Relative size |
|------|----------|---------------|
| P1 | Recent · actively being worked | Smallest, highest intent |
| P2 | Recent · no payment info yet | Small |
| P3 | Older · previously engaged | Medium |
| P4 | Cold website leads (no stage/activity) | Largest |

**Deliverables:**
- CRM saved views for the priority tiers, shared live with the sales team
- Cold-tier list delivered as CSV to Marketing for direct outreach
- Competitor-switcher positioning one-pager (PDF) for rep use
- Supporting evidence document
- Local LLM (Ollama/Llama 3.1) analysis run against the full lead dataset on a local workstation

**Outcome:** Campaign launched to the sales channel; Marketing aligned on an outreach strategy for cold leads.

---

## 3. No-Show Lead Quality Analysis

**Problem:** Leadership observed an increase in demo no-shows but lacked data to determine whether the cause was rep-side (scheduling, follow-up) or upstream (unqualified leads reaching the calendar).

**Solution:** Pulled the qualification ("Customer Fit") scores for the period's no-shows and proposed a score-based gate on the demo booking form.

**Findings (anonymized):**

| Lead | Customer Fit Score |
|------|--------------------|
| Lead A | 0 |
| Lead B | 10 |
| Lead C | 20 |
| Lead D | 60 |
| Lead E | 60 |
| Lead F | 75 |

Half of the no-shows scored 20 or below — filtering failures that arguably should not have reached the calendar. The remainder scored 60+ and represent legitimate no-shows (a separate, rep-side problem).

**Proposal:** A minimum qualification-score threshold on the booking form. Leads below threshold receive a hold response; a rep decides whether to manually book. Submitted to leadership.

**Caveat documented:** No-show counts are likely understated — tracker accuracy depends on reps consistently updating the demo-status field. (A CRM automation was later implemented to auto-populate this field and close the gap.)

**Infrastructure built:** A No-Show Tracker report in CRM Reports with the qualification-score column added for ongoing monitoring.

---

## 4. Cancellation Behavior Dashboard

**Problem:** Cancellation data lived across three disconnected systems with no unified view. Leadership had no visibility into *why* customers cancelled or how the current month compared to the prior one.

**Solution:** Analyzed the monthly cancellation export and built an HTML dashboard with a month-over-month comparison, delivered to the CS/Onboarding team.

**Findings (illustrative):**
- Cancellations were concentrated almost entirely among trialing customers, not paying subscribers
- A large share of customers started the cancel flow and backed out — an untapped save opportunity
- Trial extensions (the main active save mechanism) nearly doubled month-over-month
- "Couldn't figure it out" rose several points MoM — a growing onboarding signal
- Budget-labeled cancellations declined MoM

**Prior finding:** Manual review of cancel-reason free text showed that only ~1 in 4 "budget" cancellations were genuinely price-related — the rest were product-fit issues, vague responses, or competitor losses. This reframed how the team interpreted the cancellation reason field.

---

## Business Rules (applied across all Phase 2 reports)

- **"New Trial"** stage = an onboarding handoff stage, not a sales-performance metric. Onboarding roles are excluded from all rep leaderboards and Closed Won reports.
- **"Trial Activated"** stage = rep-closed deals entering trial. This is the source of rep-performance data.
- **CRM Reports** = source of truth for stage-specific counts (Analytics undercounts due to a current-stage filter limitation).
- **Self-Serve channel** is tracked separately from sales-assisted deals.

---

## Phase 1 → Phase 2 Transition

The Phase 1 Python/Plotly Dash dashboards (served via local tunnels) are scheduled for retirement at month-end, with all reporting moving to Zoho Analytics for live, zero-maintenance team access.

See [`/phase-1`](../phase-1) for the Python dashboard code and Phase 1 deliverables.
