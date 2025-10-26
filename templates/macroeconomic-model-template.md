# Macroeconomic Model Documentation Template

## Document Metadata
- **Model name:** 
- **Supervisory cycle / scenario year:** 
- **Prepared by:** 
- **Last updated:** 
- **Related supervisory materials / links:** 

## 1. Purpose and Role of the Macro Model
- Summarize the objectives the model serves in scenario design (e.g., generating trajectories for GDP, inflation, income, short- and long-term rates, extending projections beyond guide horizons). Reference how the model complements variable-specific guides and baseline forecasts.【F:documents/model/macroeconomic-model-guide-extracted.txt†L163-L218】
- Describe how external forecasts (e.g., Blue Chip, CBO) anchor baseline projections before the model takes over, and identify variables lacking external sources that rely on the model equations.【F:documents/model/macroeconomic-model-guide-extracted.txt†L228-L248】
- Note key design principles (simplicity, transparency, conservatism) and how they shape modeling choices versus larger structural models.【F:documents/model/macroeconomic-model-guide-extracted.txt†L250-L276】【F:documents/model/macroeconomic-model-guide-extracted.txt†L340-L357】
- Record any scenario-specific policy considerations or documentation references (e.g., policy statements, speeches).

## 2. Baseline & Scenario Integration
- Describe the interaction between supervisory guides (typically first 13 quarters) and dynamic equations beyond the guide horizon.【F:documents/model/macroeconomic-model-guide-extracted.txt†L200-L218】【F:documents/model/macroeconomic-model-guide-extracted.txt†L285-L299】
- Capture assumptions on how baseline forecasts are spliced with model dynamics after external projections expire.【F:documents/model/macroeconomic-model-guide-extracted.txt†L233-L240】
- Document any constraints or manual adjustments applied during scenario calibration (e.g., peak unemployment, inflation floors, term structure alignment).

## 3. Core Modeling Principles & Data Sources
- List data sources for exogenous inputs (population, natural rate of unemployment, potential GDP, long-run inflation expectations, policy objective, natural rate of interest). Include mnemonics and published sources (CBO, Blue Chip, FOMC).【F:documents/model/macroeconomic-model-guide-extracted.txt†L3360-L3427】
- Summarize estimation windows and source data for key equations (e.g., CBO natural rate 1967-2019 for unemployment).【F:documents/model/macroeconomic-model-guide-extracted.txt†L423-L454】【F:documents/model/macroeconomic-model-guide-extracted.txt†L1890-L1929】
- Note any calibration principles (e.g., using public estimates, avoiding reliance on proprietary data, maintaining conservatism).【F:documents/model/macroeconomic-model-guide-extracted.txt†L270-L327】

## 4. Model Component Templates
For each component below, document the items listed. Use tables or bullet lists as appropriate.

### 4.1 Unemployment Rate
- **Equation form:** Provide the AR(2) representation of deviations from the natural rate (Equation B1). Record coefficient placeholders, shock term, and natural rate input.【F:documents/model/macroeconomic-model-guide-extracted.txt†L423-L493】
- **Calibration details:** Sample period, data source, and estimation diagnostics (e.g., fit over 2007-2009 crisis).【F:documents/model/macroeconomic-model-guide-extracted.txt†L448-L624】
- **Guide interface:** Describe how supervisory guides fix the trajectory through quarter 13 and when the dynamic equation takes over.【F:documents/model/macroeconomic-model-guide-extracted.txt†L484-L520】【F:documents/model/macroeconomic-model-guide-extracted.txt†L600-L636】
- **Stress-test notes:** Include constraints (peak, recovery pace), checks against historical episodes, and rationale for linear specification.

### 4.2 Real Gross Domestic Product (GDP)
- **Equation form:** Document the growth-rate Okun's Law specification (Equation C1), including sensitivity parameter and role of potential GDP.【F:documents/model/macroeconomic-model-guide-extracted.txt†L682-L757】
- **Calibration:** Sample details, data transformations (log differences), potential GDP inputs, and reasons for growth specification vs. level (refer to Appendix A if needed).【F:documents/model/macroeconomic-model-guide-extracted.txt†L727-L757】【F:documents/model/macroeconomic-model-guide-extracted.txt†L3556-L3560】
- **Diagnostics:** Summarize validation against historical downturns and expansion phases (figures C3-C4 references if applicable).
- **Scenario interface:** Note dependence on unemployment paths and how GDP feeds downstream variables.

### 4.3 Prices and Inflation Measures
- **Core PCE inflation:** Capture the distributed-lag equation (Equation D1) with coefficients and shock term.【F:documents/model/macroeconomic-model-guide-extracted.txt†L1191-L1257】
- **Headline measures:** Explain how headline PCE, CPI, and GDP deflator inflation inherit dynamics from core PCE and connect to policy rates or income deflators.【F:documents/model/macroeconomic-model-guide-extracted.txt†L1194-L1226】
- **Calibration & validation:** Provide sample periods, references, and figure callouts demonstrating fit.
- **Guide interaction:** Note constraints (e.g., CPI guide) and how model transitions beyond guide horizon.

### 4.4 Nominal and Real Disposable Income
- **Equation form:** Outline Equation E1 linking nominal DPI to nominal GDP and unemployment (countercyclical adjustment).【F:documents/model/macroeconomic-model-guide-extracted.txt†L1883-L1943】
- **Calibration:** Document estimation period and sources, rationale for focusing on GDP link instead of detailed income components.【F:documents/model/macroeconomic-model-guide-extracted.txt†L1884-L1933】
- **Real DPI:** Specify deflation approach (headline PCE level) and stress-test considerations.【F:documents/model/macroeconomic-model-guide-extracted.txt†L1961-L1969】

### 4.5 Monetary Policy (Federal Funds & 3-Month Treasury Bill)
- **Policy rule:** Record coefficients, expectations averaging, and output/inflation gap terms in Equation F1.【F:documents/model/macroeconomic-model-guide-extracted.txt†L1991-L2067】
- **Effective lower bound (ELB):** Document threshold (0.125%) and application logic (Equation F2).【F:documents/model/macroeconomic-model-guide-extracted.txt†L2077-L2094】
- **Transmission:** Explain how policy expectations influence short-term rates and feed into long-term yields.
- **Scenario overrides:** Capture any manual adjustments or alternative policy paths used in stress design.

### 4.6 Long-Term Interest Rates
- **Structure:** Describe decomposition into expected policy path and term premium for 5-year and 10-year Treasury yields (Equations G1-G4).【F:documents/model/macroeconomic-model-guide-extracted.txt†L2205-L2338】
- **Expectations:** Note averaging horizons (20 quarters for 5-year, 40 for 10-year) and dependency on policy rule outputs.【F:documents/model/macroeconomic-model-guide-extracted.txt†L2272-L2338】
- **Scenario handling:** Detail how guides cover early quarters and when model expectations drive rates beyond guide horizon.

### 4.7 Term Premiums
- **Equation form:** Summarize AR(1) processes guiding convergence to long-run means (Equation H1/H2 as applicable).【F:documents/model/macroeconomic-model-guide-extracted.txt†L2345-L2396】
- **Role:** Explain interaction with long-term yields when guides expire and rationale for simple specification.【F:documents/model/macroeconomic-model-guide-extracted.txt†L2353-L2383】
- **Calibration:** Document historical estimation approach and long-run target values.

### 4.8 Variables with Complete Guides
For each variable below, provide baseline equations, guide integration, estimation details, and recovery assumptions.
- **BBB spread and yield (Equations I1–I2).**【F:documents/model/macroeconomic-model-guide-extracted.txt†L2853-L2916】
- **House price ratio (Equations I3–I4).**【F:documents/model/macroeconomic-model-guide-extracted.txt†L2923-L3015】
- **Equity price dynamics (Equation I5 and recovery adjustments).**【F:documents/model/macroeconomic-model-guide-extracted.txt†L3023-L3049】
- **VIX, mortgage rate, commercial real estate price, prime rate:** Summarize each guide-driven equation and how the model supports projections beyond quarter 13.【F:documents/model/macroeconomic-model-guide-extracted.txt†L2853-L3049】【F:documents/model/macroeconomic-model-guide-extracted.txt†L3049-L3282】

### 4.9 Model Identities
- List accounting identities linking real and nominal aggregates, price levels, and inflation transformations (log-difference definitions).【F:documents/model/macroeconomic-model-guide-extracted.txt†L3285-L3349】
- Note any additional definitional relationships (e.g., gap measures, conversions between annualized and quarterly rates).

### 4.10 Exogenous Variables
- Provide a table mirroring Table K1 with mnemonics, sources, and update cadence. Include assumptions about long-run inflation anchoring at 2 percent.【F:documents/model/macroeconomic-model-guide-extracted.txt†L3360-L3427】
- Document any additional exogenous assumptions (e.g., population growth adjustments, natural rate shifts).

### 4.11 Variable Inventory
- Maintain a comprehensive table of variables and mnemonics used in the model, referencing Section L.【F:documents/model/macroeconomic-model-guide-extracted.txt†L3441-L3554】
- Track which components produce each variable (equation vs. identity vs. exogenous) and note data availability constraints.

## 5. Simulation & Implementation Notes
- Outline the chronological steps for running baseline and stress simulations (guide application, model hand-off, ELB enforcement, long-term expectations updates).
- Specify forecast horizon length, iteration order, and convergence checks.
- Document tooling, code repositories, or statistical packages required.

## 6. Validation & Diagnostics
- Record historical scenario backtests (e.g., Great Recession replication) and key performance metrics for each major variable.【F:documents/model/macroeconomic-model-guide-extracted.txt†L600-L668】【F:documents/model/macroeconomic-model-guide-extracted.txt†L1961-L1968】
- Track sensitivity analyses (e.g., alternative Okun coefficients, policy rule shocks) and document outcomes.
- Capture governance reviews, approvals, or validation sign-offs.

## 7. Change Log & Governance
- Summarize model updates, recalibrations, or guide changes by cycle.
- Note dependencies on policy statements or regulatory guidance revisions.

## Appendices
- **Appendix A placeholder:** Summarize takeaways from the level vs. growth Okun specification analysis and how to revisit if unemployment dynamics change.【F:documents/model/macroeconomic-model-guide-extracted.txt†L3556-L3560】
- **Appendix B placeholder:** Document assumptions on long-run Treasury yields and calibration of steady-state term premiums.
- Include additional appendices for scenario-specific overrides, data transformations, or alternative specifications as needed.
