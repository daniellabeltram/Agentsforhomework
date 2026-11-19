"""
First-pass valuation ranges for PRH top-10 acquisition targets.

Source list: docs/prh-top-10-acquisition-targets.md (Nov 19, 2026).
Currency: USD millions (target local GAAP / unaudited estimates; NOT IFRS-converted).
Fiscal year: latest available annual figure per target (see rev_basis).
IMPORTANT: 9 of 10 targets have NO public financials. Only IDW (OTC, 10-K) reports.
Revenue for the rest is an estimate built from aggregator data, stale trade-press
figures or deal anchors; ranges are deliberately wide. Not a fairness opinion.

Structure: 1) INPUTS  2) CALCULATIONS  3) OUTPUTS (CSV + console table).
Run: python3 models/top10_valuation.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

# =============================================================================
# 1. INPUTS
# =============================================================================
FX_GBP_USD = 1.27          # assumption; refresh at time of use
TAX_RATE = 0.25            # blended assumption; confirm with tax-accounting-specialist
WACC = 0.09                # assumption for synergy NPV (USD, mid-size trade publishing)
TERM_GROWTH = 0.01         # synergy run-rate growth after year 5
HURDLE_ROIC = 0.09         # placeholder; PRH/Bertelsmann hurdle not provided
P_COST = 0.75              # probability weight, cost synergies
P_REV = 0.40               # probability weight, revenue synergies (conservative)
REV_SYN_FLOWTHROUGH = 0.30 # EBITDA flow-through on incremental revenue (after royalty, COGS)
RAMP = [0.4, 0.8, 1.0, 1.0, 1.0]   # synergy phasing years 1-5
INTEG_COST_X = 1.25        # one-off integration cost = x times run-rate cost synergies

# Segment multiple ranges (EV/Revenue lo, hi ; EV/EBITDA lo, hi).
# Anchors: Seven Seas ~1.6x rev (Media Do, Mar 2026, doc); Cottage Door ~$71M
# (Scholastic, Oct 2026; revenue not disclosed); Entangled ~$400M minority-round
# valuation (Dec 2025, doc); Podium $400M+ (audio, Sep 2026). Well-known trade
# precedents (from memory, verify): KKR/S&S 2023 ~$1.62B (~1.4x rev, ~7-8x EBITDA);
# PRH/S&S 2020 agreed $2.175B (~2.2x rev, ~11-12x EBITDA, blocked).
SEGMENTS = {
    "Comics/IP owner (media upside)":  (1.0, 1.8, 9.0, 13.0),
    "Comics, licence-dependent":       (0.4, 0.9, 7.0, 10.0),
    "Children's brand + DTC":          (1.0, 1.8, 8.0, 12.0),
    "Niche backlist (MBS)":            (1.0, 1.7, 8.0, 12.0),
    "Premium illustrated/art":         (0.8, 1.3, 8.0, 11.0),
    "Gift/calendar/humor + IP":        (0.8, 1.3, 7.0, 10.0),
    "Licensed fiction/comics":         (0.7, 1.2, 7.0, 10.0),
    "Hit-driven genre (romantasy)":    (1.8, 3.2, 9.0, 14.0),
    "Licensed illustrated":            (0.6, 1.1, 7.0, 10.0),
}

# Per-target inputs. rev in USD M; margin = EBITDA margin range (est.).
# prhps = already distributed by PRH Publisher Services (cost synergies limited
# to back office/printing; distribution fee is already intra-group post-deal).
# cost_syn / rev_syn = run-rate % of target revenue (lo, hi), before probability.
T = [
 # rank, name, segment, rev_lo, rev_hi, basis, m_lo, m_hi, prhps, cost_syn, rev_syn
 (1, "Dark Horse", "Comics/IP owner (media upside)", 70, 110,
  "est.: Embracer 2021 guide ~SEK 900M sales / SEK 130M EBIT (~$105M) less post-Diamond decline",
  0.08, 0.14, True, (0.02, 0.04), (0.02, 0.05)),
 (2, "Highlights for Children (whole co.)", "Children's brand + DTC", 120, 250,
  "est.: aggregators (Owler $100-500M, Growjo $123M, Zippia $180M, Prospeo $246M); ~340 staff (LeadIQ)",
  0.08, 0.15, True, (0.015, 0.03), (0.01, 0.03)),
 (3, "Shambhala Publications", "Niche backlist (MBS)", 8, 15,
  "est.: PW 2010 ~$10M; aggregators $1-5M (low quality); ~40-80 staff",
  0.08, 0.15, True, (0.03, 0.05), (0.02, 0.05)),
 (4, "Phaidon Press", "Premium illustrated/art", 38, 42,
  "reported via aggregator: GBP 31.3M FY Jun-2024 (Endole from Companies House); op. profit GBP 0.5M FY2021",
  0.03, 0.08, False, (0.04, 0.07), (0.02, 0.04)),
 (5, "IDW Publishing", "Comics, licence-dependent", 21, 24,
  "reported: $23.16M FY Oct-2025 (-12.5%), net loss $1.41M (10-K/StockAnalysis)",
  -0.08, 0.02, True, (0.04, 0.07), (0.01, 0.03)),
 (6, "Andrews McMeel Universal", "Gift/calendar/humor + IP", 100, 140,
  "est.: ~$115M (2018, PW) + Quirk (Oct 2025); aggregator $11-21M figures rejected as implausible",
  0.10, 0.15, False, (0.04, 0.07), (0.01, 0.03)),
 (7, "Titan Publishing Group", "Licensed fiction/comics", 45, 75,
  "est.: UK 'large company' filer (turnover likely >GBP 36M); no turnover found",
  0.07, 0.12, True, (0.02, 0.04), (0.01, 0.03)),
 (8, "Oni Press (Oni-Lion Forge)", "Comics, licence-dependent", 8, 15,
  "est.: no data; small comics house",
  0.00, 0.08, True, (0.04, 0.07), (0.01, 0.03)),
 (9, "Entangled Publishing", "Hit-driven genre (romantasy)", 100, 200,
  "est.: Empyrean unit sales (Fourth Wing 2.7M+ US copies by Dec-2024, PW) x ~$10-14 net/unit + list; anchor $400M minority valuation",
  0.18, 0.30, False, (0.03, 0.05), (0.02, 0.05)),
 (10, "Insight Editions (+Weldon Owen)", "Licensed illustrated", 35, 60,
  "est.: aggregators Insight $14-38M + Weldon Owen $14-25M",
  0.06, 0.12, False, (0.04, 0.07), (0.02, 0.04)),
]
COLS = ["rank", "target", "segment", "rev_lo", "rev_hi", "rev_basis",
        "margin_lo", "margin_hi", "prhps_client", "cost_syn_pct", "rev_syn_pct"]

# =============================================================================
# 2. CALCULATIONS
# =============================================================================
def annuity_factor(ramp, r, g):
    """PV of $1 run-rate with ramp in yrs 1-5, then growing perpetuity."""
    pv = sum(w / (1 + r) ** (t + 1) for t, w in enumerate(ramp))
    tv = ramp[-1] * (1 + g) / (r - g) / (1 + r) ** len(ramp)
    return pv + tv

AF = annuity_factor(RAMP, WACC, TERM_GROWTH)

df = pd.DataFrame(T, columns=COLS)
seg = pd.DataFrame(SEGMENTS, index=["evr_lo", "evr_hi", "eve_lo", "eve_hi"]).T
df = df.join(seg, on="segment")
df["rev_mid"] = (df.rev_lo + df.rev_hi) / 2
df["ebitda_lo"] = df.rev_lo * df.margin_lo
df["ebitda_hi"] = df.rev_hi * df.margin_hi
df["ebitda_mid"] = df.rev_mid * (df.margin_lo + df.margin_hi) / 2

# Method A: EV/Revenue
df["evA_lo"] = df.rev_lo * df.evr_lo
df["evA_hi"] = df.rev_hi * df.evr_hi
df["evA_mid"] = df.rev_mid * (df.evr_lo + df.evr_hi) / 2
# Method B: EV/EBITDA (only where EBITDA positive)
df["evB_lo"] = np.where(df.ebitda_lo > 0, df.ebitda_lo * df.eve_lo, np.nan)
df["evB_hi"] = np.where(df.ebitda_hi > 0, df.ebitda_hi * df.eve_hi, np.nan)
df["evB_mid"] = np.where(df.ebitda_mid > 0, df.ebitda_mid * (df.eve_lo + df.eve_hi) / 2, np.nan)

# Standalone EV = simple average of methods where B available, else A only
for k in ["lo", "mid", "hi"]:
    df[f"sa_{k}"] = df[[f"evA_{k}", f"evB_{k}"]].mean(axis=1, skipna=True)
# Sort lo/hi so lo <= mid <= hi after blending
df[["sa_lo", "sa_mid", "sa_hi"]] = np.sort(df[["sa_lo", "sa_mid", "sa_hi"]].values, axis=1)

# Synergies (run-rate EBITDA, mid revenue)
df["cost_syn_rr"] = df.rev_mid * df.cost_syn_pct.apply(np.mean)
df["rev_syn_rr"] = df.rev_mid * df.rev_syn_pct.apply(np.mean) * REV_SYN_FLOWTHROUGH
df["syn_rr_rw"] = df.cost_syn_rr * P_COST + df.rev_syn_rr * P_REV
df["integ_cost"] = df.cost_syn_rr * INTEG_COST_X
df["syn_npv"] = df.syn_rr_rw * (1 - TAX_RATE) * AF - df.integ_cost * (1 - TAX_RATE)
df["value_to_prh"] = df.sa_mid + df.syn_npv

# Price guidance
df["opening_bid"] = 0.90 * df.sa_mid                 # below standalone mid, no synergies shared
df["target_price"] = df.sa_mid + 0.25 * df.syn_npv   # share up to 25% of net synergies
df["walk_away"] = df.sa_mid + 0.50 * df.syn_npv      # never pay away >50% of net synergies
df["walk_gt_sa_hi"] = df.walk_away > df.sa_hi

# Year-3 ROIC at target price (EBITA ~ 90% of EBITDA; full run-rate synergies)
df["roic_y3"] = ((df.ebitda_mid * 0.9 + df.syn_rr_rw) * (1 - TAX_RATE)
                 / (df.target_price + df.integ_cost))
df["roic_vs_hurdle"] = np.where(df.roic_y3 >= HURDLE_ROIC, "above", "below")

# =============================================================================
# 3. OUTPUTS
# =============================================================================
out_cols = ["rank", "target", "segment", "prhps_client", "rev_lo", "rev_hi", "rev_basis",
            "margin_lo", "margin_hi", "evr_lo", "evr_hi", "eve_lo", "eve_hi",
            "ebitda_mid", "sa_lo", "sa_mid", "sa_hi", "cost_syn_rr", "rev_syn_rr",
            "syn_rr_rw", "integ_cost", "syn_npv", "value_to_prh",
            "opening_bid", "target_price", "walk_away", "walk_gt_sa_hi",
            "roic_y3", "roic_vs_hurdle"]
out = df[out_cols].copy()
out["cost_syn_pct"] = df.cost_syn_pct.astype(str)
out["rev_syn_pct"] = df.rev_syn_pct.astype(str)
num = out.select_dtypes("number").columns
out[num] = out[num].round(2)

here = Path(__file__).resolve().parent
out.to_csv(here / "top10_valuation.csv", index=False)

if __name__ == "__main__":
    pd.set_option("display.width", 250)
    print(f"Synergy annuity factor: {AF:.2f}x run-rate (pre-tax)")
    show = out[["rank", "target", "prhps_client", "rev_lo", "rev_hi", "sa_lo", "sa_mid", "sa_hi",
                "syn_rr_rw", "syn_npv", "opening_bid", "target_price", "walk_away", "roic_y3"]]
    print(show.round(1).to_string(index=False))
    print("Totals (sa_mid, syn_npv):", out.sa_mid.sum().round(0), out.syn_npv.sum().round(0))
