import math

def qual_lt_500mn_module(input_json):
    """
    Calculate the Qual < 500mn Score, PD, and CG mapping.

    Parameters:
        input_json (dict): Dictionary with the following keys:
            {
                "auditing_firms": float,
                "industry_prospects": float,
                "industry_group": float,
                "region": float,
                "years_customer_relationship": float
            }

    Returns:
        dict: { "score": float, "pd": float, "cg": str }
    """

    # Coefficients from the sheet
    intercept = -4.911121
    coef = {
        "auditing_firms": -0.945392,
        "industry_prospects": -0.993696,
        "industry_group": -0.786204,
        "region": -1.05275,
        "years_customer_relationship": -0.5
    }

    # Extract input values
    af = input_json.get("auditing_firms", 0)
    ip = input_json.get("industry_prospects", 0)
    ig = input_json.get("industry_group", 0)
    rg = input_json.get("region", 0)
    ycr = input_json.get("years_customer_relationship", 0)

    # Compute score
    score = (
        intercept
        + coef["auditing_firms"] * af
        + coef["industry_prospects"] * ip
        + coef["industry_group"] * ig
        + coef["region"] * rg
        + coef["years_customer_relationship"] * ycr
    )

    # Logistic regression for PD
    pd = 1 / (1 + math.exp(-score))

    # Dummy CG mapping (can be customized based on PD thresholds)
    if pd < 0.02:
        cg = "AAA"
    elif pd < 0.05:
        cg = "AA"
    elif pd < 0.1:
        cg = "A"
    elif pd < 0.2:
        cg = "BBB"
    else:
        cg = "BB or lower"

    return {
        "score": score,
        "pd": pd,
        "cg": cg
    }

# Example usage
sample_input = {
    "auditing_firms": 1,
    "industry_prospects": 2,
    "industry_group": 3,
    "region": 1,
    "years_customer_relationship": 10
}

result = qual_lt_500mn_module(sample_input)
print(result)
