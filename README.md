# Dodd-Frank Stress Test Macroeconomic Model

This repository contains Python utilities for implementing the Federal Reserve's
macroeconomic projection framework that underpins the Dodd-Frank Act stress
tests. The implementation follows the public "Macroeconomic Model for the
Dodd-Frank Stress Tests" guide released by the Board of Governors and included
in the `documents/model` directory of this project.

## Repository structure

- `documents/model/macroeconomic-model-guide.pdf` – Source documentation from
the Federal Reserve that details the equations used in supervisory stress
tests.
- `documents/model/macroeconomic-model-guide-extracted.txt` – Text extraction of
the guide that enables quick searches and line-based citations.
- `src/macro_model/` – Python package that houses the simulation engine and
data input helpers for reproducing the model dynamics.
- `templates/` – Markdown template that mirrors the guide and can be customized
for institution-specific documentation.

## Getting started

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies from `requirements.txt` if provided, or install
   `numpy` and `pandas` manually since they are required by the simulator.
3. Run simulations using the convenience wrapper in `macro_model`:

```bash
PYTHONPATH=src python - <<'PY'
from macro_model import MacroModelInputs, simulate_macro_model
import numpy as np

horizon = 12
inputs = MacroModelInputs(
    horizon=horizon,
    unemployment=[3.7, 3.8],
    natural_unemployment=[4.0] * horizon,
    potential_gdp=np.linspace(20000, 20600, horizon),
    real_gdp_initial=19800.0,
    nominal_gdp_initial=23500.0,
    nominal_dpi_initial=17000.0,
    core_inflation_initial=[3.0, 2.8],
    inflation_expectations=[2.0] * horizon,
    inflation_target=[2.0] * horizon,
    natural_rate=[0.5] * horizon,
    policy_rate_initial=2.5,
    term_premium10_intercept=1.0,
    term_premium5_intercept=0.8,
    term_premium10_initial=1.0,
    term_premium5_initial=0.8,
    bbb_spread_initial=2.0,
)

simulation = simulate_macro_model(inputs)
print(simulation.head())
PY
```

The resulting `pandas.DataFrame` contains the key variables tracked in the
stress test projections: unemployment, inflation measures, policy rates,
Treasury yields, credit spreads, and nominal aggregates.

## Next steps

The current code focuses on faithfully transcribing the Board's published
equations. Future work will expand the API for scenario management, integrate
calibration data sets, and expose automated validation aligned with the stress
test governance process.
