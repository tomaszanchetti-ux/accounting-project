# Executive Demo Script (2m30)

## Objective

Short executive walkthrough for the **Accounting Reconciliation MVP**.

Audience:

- finance leaders
- controllers
- operations or transformation sponsors

Target length:

- around `2 minutes 30 seconds`

Core message:

> Instead of manually reviewing thousands of payroll lines to understand why accounting does not reconcile, the team can move from variance to probable cause to evidence in minutes.

---

## Demo Flow

### 1. Opening Context — 20 seconds

**What to show**

- home / setup screen

**What to say**

> What you are seeing is a focused MVP for payroll-to-accounting reconciliation.  
> The goal is not just to show that totals do not match, but to explain why they do not match and let a finance team reach supporting evidence quickly.

---

### 2. Setup — 20 seconds

**What to show**

- period already selected
- demo workspace ready
- start run / run already prepared

**What to say**

> The setup is intentionally narrow. We define the payroll period, attach the payroll file, confirm the expected totals reference, and start a reconciliation run.  
> In a real operating model this would be fed by recurring extracts, but for the MVP we keep the workflow controlled and repeatable.

---

### 3. Summary — 35 seconds

**What to show**

- run summary header
- KPI cards
- concept table
- highlight `MEAL_VOUCHER`

**What to say**

> Once the run is processed, the summary gives an executive view of the period in one pass.  
> We immediately see how many concepts reconciled, which ones remain open, and where the material differences sit.  
> Here, `MEAL_VOUCHER` stands out as the main unreconciled concept, so that becomes the natural entry point for investigation.

---

### 4. Concept Analysis — 45 seconds

**What to show**

- open `MEAL_VOUCHER`
- expected vs observed
- summary statement
- top causes
- recommended action

**What to say**

> This is the core differentiator of the product.  
> We are not just flagging a variance. We are providing a structured explanation of the variance.  
> In this example, the difference is not driven by a single issue. The system surfaces a combination of likely causes such as out-of-period records, duplicate records, and mapping issues.  
> That means the reviewer does not start from a blank page. They start from a ranked hypothesis supported by the data.

---

### 5. Drill-down — 20 seconds

**What to show**

- open detailed records
- anomaly tags
- filtered rows or highest-signal rows

**What to say**

> From here, we can move directly into the detailed records behind that explanation.  
> This is where the reviewer validates the story at row level, sees which employees or transactions are impacted, and confirms the anomaly pattern without leaving the workflow.

---

### 6. Close — 10 seconds

**What to show**

- drill-down or back to summary

**What to say**

> So the value is simple: instead of spending hours moving manually from totals to spreadsheets to root-cause analysis, the team can go from variance to explanation to evidence in a guided flow in just a few minutes.

---

## Presenter Notes

### Keep the focus on:

- speed to insight
- explainability
- traceability
- operational usefulness for finance teams

### Avoid spending time on:

- technical architecture
- deployment details
- raw file mechanics
- every KPI on screen

### Best narrative path

1. setup briefly
2. summary quickly
3. spend most time on `MEAL_VOUCHER`
4. use drill-down only to confirm credibility
5. close on business value

---

## Short Version

> This MVP helps finance teams reconcile payroll against accounting in a much more intelligent way.  
> First, it processes the payroll period against expected totals.  
> Then it gives an executive summary of what reconciled and what did not.  
> From there, the reviewer can open a concept like `MEAL_VOUCHER`, see the likely drivers of the variance, and move directly into the supporting records.  
> The result is faster review, better explainability, and much stronger traceability than a manual spreadsheet-based process.
