import numpy as np

# --- WOE mapping for turnover ---
def turnover_usd_up_bin(value):
    if value is None or value < 0:
        return 1.959225
    elif value <= 2e9:
        return -0.1462
    elif value <= 5e9:
        return 0.012617
    elif value <= 22e9:
        return 0.613084
    else:
        return 1.959225


# --- Risk Driver Estimates ---
ESTIMATES = {
    "Intercept": -5.515189,
    "turnover_usd_up_bin": -1.025649,
    "liquidity": -0.181371,
    "debt_to_equity": 0.362569,
    "int_exp_to_tot_sal": 17.915711,
    "npbt_to_sal_log": -0.039781,
    "ebitda_to_interest_logv2": -0.132455
}


# --- Financial Score & PD Calculation ---
def calculate_financial_pd(inputs: dict) -> dict:
    """
    inputs = {
        "turnover_usd_up": <float in USD>,
        "liquidity": <float>,
        "debt_to_equity": <float>,
        "int_exp_to_tot_sal": <float>,
        "npbt_to_sal_log": <float>,
        "ebitda_to_interest_logv2": <float>
    }
    """
    # map turnover to WOE
    turnover_bin = turnover_usd_up_bin(inputs.get("turnover_usd_up", None))

    # collect values
    values = {
        "turnover_usd_up_bin": turnover_bin,
        "liquidity": inputs.get("liquidity", 0.0),
        "debt_to_equity": inputs.get("debt_to_equity", 0.0),
        "int_exp_to_tot_sal": inputs.get("int_exp_to_tot_sal", 0.0),
        "npbt_to_sal_log": inputs.get("npbt_to_sal_log", 0.0),
        "ebitda_to_interest_logv2": inputs.get("ebitda_to_interest_logv2", 0.0)
    }

    # financial score
    score = ESTIMATES["Intercept"]
    for k, v in values.items():
        score += v * ESTIMATES[k]

    # PD using logistic regression
    pd_value = 1 / (1 + np.exp(-score))

    return {
        "Financial_Score": score,
        "Financial_PD": pd_value
        # "Financial_CG": mapping_function(pd_value)  # if ECMS mapping table available
    }


# --- Example Usage ---
if __name__ == "__main__":
    example_input = {
        "turnover_usd_up": 8e9,      # Example turnover
        "liquidity": 1.2,
        "debt_to_equity": 0.8,
        "int_exp_to_tot_sal": 0.05,
        "npbt_to_sal_log": 2.3,
        "ebitda_to_interest_logv2": 1.5
    }

    result = calculate_financial_pd(example_input)
    print(result)
