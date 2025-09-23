import numpy as np

def qual_500mm_score(liquidity, ceo, region, competitive_advantage, industry_group):
    intercept = 5.036414
    coef_liquidity = -0.794952
    coef_ceo = -0.648591
    coef_region = -0.734823
    coef_comp_adv = -0.757865
    coef_ind_group = -0.531175
    score = (
        intercept
        + coef_liquidity * liquidity
        + coef_ceo * ceo
        + coef_region * region
        + coef_comp_adv * competitive_advantage
        + coef_ind_group * industry_group
    )
    return score

def qual_500mm_pd(score):
    pd = 1 / (1 + np.exp(score))
    return pd

# Example usage
liquidity_val = 2.10887         # Liquidity bin value
ceo_val = 1.90971               # CEO bin value
region_val = 1.277317           # Region bin value
comp_adv_val = 0.77377          # Competitive Advantage bin value
industry_group_val = 0.77377    # Industry Group bin value

score = qual_500mm_score(liquidity_val, ceo_val, region_val, comp_adv_val, industry_group_val)
pd = qual_500mm_pd(score)

print("Qual >= 500mm Score:", score)
print("Qual >= 500mm PD:", pd)
