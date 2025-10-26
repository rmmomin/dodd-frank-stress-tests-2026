"""Simulation engine for the Board's macroeconomic stress testing model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd


def _as_array(
    values: Sequence[float] | float | None,
    length: int,
    *,
    fill_value: float = 0.0,
) -> np.ndarray:
    """Return ``values`` as a NumPy array of ``length``.

    Scalars are broadcast, sequences are truncated or padded with their last value,
    and ``None`` results in an array filled with ``fill_value``.
    """

    if values is None:
        return np.full(length, fill_value, dtype=float)

    if isinstance(values, (int, float)):
        return np.full(length, float(values), dtype=float)

    arr = np.asarray(list(values), dtype=float)
    if arr.size == 0:
        return np.full(length, fill_value, dtype=float)
    if arr.size >= length:
        return arr[:length].copy()
    pad_value = arr[-1]
    pad = np.full(length - arr.size, pad_value, dtype=float)
    return np.concatenate([arr, pad])


def _forward_average(series: np.ndarray, start: int, horizon: int) -> float:
    """Average ``series`` from ``start`` forward ``horizon`` steps."""

    end = min(series.size, start + horizon)
    window = series[start:end]
    if window.size == horizon:
        return float(window.mean())
    if window.size == 0:
        return float(series[-1])
    pad_value = series[-1]
    padded = np.concatenate([window, np.full(horizon - window.size, pad_value)])
    return float(padded.mean())


def _moving_average(series: np.ndarray, end: int, window: int) -> float:
    """Average ``series`` over the last ``window`` observations up to ``end``."""

    start = max(0, end - window + 1)
    segment = series[start : end + 1]
    if segment.size == 0:
        return 0.0
    return float(segment.mean())


@dataclass
class MacroModelInputs:
    """Container for the macroeconomic model inputs and calibration constants."""

    horizon: int
    unemployment: Sequence[float]
    natural_unemployment: Sequence[float]
    potential_gdp: Sequence[float]
    real_gdp_initial: float
    nominal_gdp_initial: float
    nominal_dpi_initial: float
    core_inflation_initial: Sequence[float]
    inflation_expectations: Sequence[float]
    inflation_target: Sequence[float]
    natural_rate: Sequence[float]
    policy_rate_initial: float
    term_premium10_intercept: Sequence[float] | float
    term_premium5_intercept: Sequence[float] | float
    term_premium10_initial: float
    term_premium5_initial: float
    bbb_spread_initial: float
    headline_wedge_initial: float = 0.0
    cpi_wedge_initial: float = 0.0
    gdp_wedge_initial: float = 0.0
    cpi_intercept: float = 0.48
    core_inflation_shocks: Sequence[float] | None = None
    headline_wedge_shocks: Sequence[float] | None = None
    cpi_wedge_shocks: Sequence[float] | None = None
    gdp_wedge_shocks: Sequence[float] | None = None
    term_premium10_shocks: Sequence[float] | None = None
    term_premium5_shocks: Sequence[float] | None = None
    bbb_spread_shocks: Sequence[float] | None = None
    okun_coefficient: float = 1.4
    phi_core_lag1: float = 0.36
    phi_core_lag2: float = 0.23
    phi_core_expectations: float = 0.41
    phi_core_unemployment_gap: float = 0.08
    phi_headline_wedge: float = 0.36
    phi_cpi_wedge: float = 0.11
    phi_gdp_wedge: float = 0.45
    phi_term_premium10: float = 0.81
    phi_term_premium5: float = 0.74
    phi_bbb_spread: float = 0.87

    def __post_init__(self) -> None:
        if self.horizon <= 0:
            raise ValueError("horizon must be positive")
        if len(self.core_inflation_initial) < 2:
            raise ValueError(
                "core_inflation_initial must provide at least two starting values"
            )
        if len(self.unemployment) < 2:
            raise ValueError(
                "unemployment must include at least two values to seed Equation B1"
            )


class MacroModelSimulator:
    """Run simulations of the macroeconomic model described in the Board's guide."""

    def __init__(self, inputs: MacroModelInputs):
        self.inputs = inputs

    def simulate(self) -> pd.DataFrame:
        inp = self.inputs
        T = inp.horizon

        # Extend unemployment using the AR(2) process from Equation B1.
        u_star = _as_array(inp.natural_unemployment, T)
        unemployment = list(np.asarray(inp.unemployment, dtype=float))
        if len(unemployment) < T:
            for t in range(len(unemployment), T):
                gap_lag1 = unemployment[t - 1] - u_star[t - 1]
                gap_lag2 = unemployment[t - 2] - u_star[t - 2]
                gap = 1.65 * gap_lag1 - 0.68 * gap_lag2
                unemployment.append(u_star[t] + gap)
        unemployment = np.asarray(unemployment[:T], dtype=float)

        # Core PCE inflation dynamics (Equation D1).
        core_pi = np.zeros(T)
        initial_core = np.asarray(inp.core_inflation_initial, dtype=float)
        seed = min(initial_core.size, T)
        core_pi[:seed] = initial_core[:seed]
        pi_expect = _as_array(inp.inflation_expectations, T)
        core_shock = _as_array(inp.core_inflation_shocks, T)

        u_gap = unemployment - u_star
        for t in range(seed, T):
            term_lag1 = inp.phi_core_lag1 * core_pi[t - 1]
            term_lag2 = inp.phi_core_lag2 * core_pi[t - 2]
            expect_term = inp.phi_core_expectations * pi_expect[t]
            gap_term = inp.phi_core_unemployment_gap * u_gap[t]
            core_pi[t] = term_lag1 + term_lag2 + expect_term + gap_term + core_shock[t]

        # Headline PCE inflation wedge (Equations D2-D5).
        headline_wedge = np.zeros(T)
        headline_wedge[0] = inp.headline_wedge_initial
        headline_shock = _as_array(inp.headline_wedge_shocks, T)
        for t in range(1, T):
            headline_wedge[t] = (
                inp.phi_headline_wedge * headline_wedge[t - 1] + headline_shock[t]
            )
        headline_pi = core_pi + headline_wedge

        # CPI inflation (Equations D6-D7).
        cpi_wedge = np.zeros(T)
        cpi_wedge[0] = inp.cpi_wedge_initial
        cpi_shock = _as_array(inp.cpi_wedge_shocks, T)
        for t in range(1, T):
            cpi_wedge[t] = inp.phi_cpi_wedge * cpi_wedge[t - 1] + cpi_shock[t]
        cpi_pi = inp.cpi_intercept + headline_pi + cpi_wedge

        # GDP deflator inflation (Equations D8-D9).
        gdp_wedge = np.zeros(T)
        gdp_wedge[0] = inp.gdp_wedge_initial
        gdp_shock = _as_array(inp.gdp_wedge_shocks, T)
        for t in range(1, T):
            gdp_wedge[t] = inp.phi_gdp_wedge * gdp_wedge[t - 1] + gdp_shock[t]
        gdp_pi = headline_pi + gdp_wedge

        # Real GDP via Okun's Law (Equation C1).
        potential = _as_array(inp.potential_gdp, T)
        real_gdp = np.zeros(T)
        real_gdp[0] = inp.real_gdp_initial
        real_growth = np.full(T, np.nan)
        for t in range(1, T):
            potential_growth = 400.0 * np.log(potential[t] / potential[t - 1])
            delta_u = unemployment[t] - unemployment[t - 1]
            real_growth[t] = potential_growth - 4.0 * inp.okun_coefficient * delta_u
            real_gdp[t] = real_gdp[t - 1] * np.exp(real_growth[t] / 400.0)

        # Output gap as log difference between realized and potential GDP.
        output_gap = 100.0 * np.log(real_gdp / potential)

        # Monetary policy rule (Equations F1-F3).
        r_star = _as_array(inp.natural_rate, T)
        pi_target = _as_array(inp.inflation_target, T)
        policy_rate = np.zeros(T)
        prev_rate = inp.policy_rate_initial
        t_bill_rate = np.zeros(T)
        for t in range(T):
            avg_core = _moving_average(core_pi, t, 4)
            gap_component = output_gap[t] if output_gap[t] < 0 else 0.0
            unemployment_drag = 0.0
            if t >= 2:
                delta_two = unemployment[t] - unemployment[t - 2]
                if (unemployment[t] > u_star[t]) and (delta_two > 0):
                    unemployment_drag = 0.85 * delta_two
            rule_base = (
                r_star[t]
                + avg_core
                + 0.5 * (avg_core - pi_target[t])
            )
            raw_rate = (
                0.85 * prev_rate
                + 0.15 * rule_base
                + 0.15 * gap_component
                - unemployment_drag
            )
            policy_rate[t] = max(raw_rate, 0.125)
            prev_rate = policy_rate[t]
            t_bill_rate[t] = policy_rate[t]

        # Expected short-rate components for long-term yields (Equations G1-G4).
        expected_5y = np.array([
            _forward_average(policy_rate, t, 20) for t in range(T)
        ])
        expected_10y = np.array([
            _forward_average(policy_rate, t, 40) for t in range(T)
        ])

        # Term premiums (Equations H1-H4).
        tp10_intercept = _as_array(inp.term_premium10_intercept, T)
        tp5_intercept = _as_array(inp.term_premium5_intercept, T)
        tp10_shock = _as_array(inp.term_premium10_shocks, T)
        tp5_shock = _as_array(inp.term_premium5_shocks, T)

        term_premium10 = np.zeros(T)
        term_premium5 = np.zeros(T)
        prev_tp10 = inp.term_premium10_initial
        prev_tp5 = inp.term_premium5_initial
        for t in range(T):
            prev_tp10 = (
                tp10_intercept[t]
                + inp.phi_term_premium10 * (prev_tp10 - tp10_intercept[t])
                + tp10_shock[t]
            )
            prev_tp5 = (
                tp5_intercept[t]
                + inp.phi_term_premium5 * (prev_tp5 - tp5_intercept[t])
                + tp5_shock[t]
            )
            term_premium10[t] = prev_tp10
            term_premium5[t] = prev_tp5

        yield_10y = expected_10y + term_premium10
        yield_5y = expected_5y + term_premium5

        # BBB spread dynamics (Equations I1-I2).
        bbb_shock = _as_array(inp.bbb_spread_shocks, T)
        bbb_spread = np.zeros(T)
        prev_spread = inp.bbb_spread_initial
        for t in range(T):
            prev_spread = 1.66 + inp.phi_bbb_spread * (prev_spread - 1.66) + bbb_shock[t]
            bbb_spread[t] = prev_spread
        bbb_yield = bbb_spread + yield_10y

        # Nominal aggregates and disposable income (Equations E1 and J identities).
        nominal_gdp = np.zeros(T)
        nominal_gdp[0] = inp.nominal_gdp_initial
        nominal_dpi = np.zeros(T)
        nominal_dpi[0] = inp.nominal_dpi_initial
        for t in range(1, T):
            # Nominal GDP growth combines real growth and the GDP deflator inflation.
            if np.isnan(real_growth[t]):
                real_growth_t = 0.0
            else:
                real_growth_t = real_growth[t]
            growth_factor = np.exp((real_growth_t + gdp_pi[t]) / 400.0)
            nominal_gdp[t] = nominal_gdp[t - 1] * growth_factor

            unemployment_change = unemployment[t] - unemployment[t - 1]
            dpi_growth = growth_factor * np.exp(0.0058 * unemployment_change)
            nominal_dpi[t] = nominal_dpi[t - 1] * dpi_growth

        data = {
            "unemployment_rate": unemployment,
            "natural_unemployment": u_star,
            "unemployment_gap": u_gap,
            "real_gdp": real_gdp,
            "potential_gdp": potential,
            "real_gdp_growth": real_growth,
            "output_gap": output_gap,
            "core_pce_inflation": core_pi,
            "headline_pce_inflation": headline_pi,
            "cpi_inflation": cpi_pi,
            "gdp_deflator_inflation": gdp_pi,
            "policy_rate": policy_rate,
            "three_month_tbill": t_bill_rate,
            "expected_short_rate_5y": expected_5y,
            "expected_short_rate_10y": expected_10y,
            "term_premium_5y": term_premium5,
            "term_premium_10y": term_premium10,
            "yield_5y": yield_5y,
            "yield_10y": yield_10y,
            "bbb_spread": bbb_spread,
            "bbb_yield": bbb_yield,
            "nominal_gdp": nominal_gdp,
            "nominal_dpi": nominal_dpi,
        }
        return pd.DataFrame(data)


def simulate_macro_model(inputs: MacroModelInputs) -> pd.DataFrame:
    """Convenience wrapper that instantiates :class:`MacroModelSimulator`."""

    return MacroModelSimulator(inputs).simulate()
