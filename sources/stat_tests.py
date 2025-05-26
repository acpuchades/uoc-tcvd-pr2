from scipy.stats import levene
import statsmodels.stats.nonparametric as nonp
from statsmodels.stats.weightstats import ttest_ind
from statsmodels.stats.diagnostic import kstest_normal

from idealista_data import datos

## KOLMOGOROV-SMIRNOFF TEST FOR NORMALITY

res = kstest_normal(datos.price_m2)
print(f"Normality test for property prices: {res[1]:.3f}")

## NON-PARAMETRIC MANN-WHITNEY'S U TEST

lift_properties = datos[datos.ascensor == 2]
nolift_properties = datos[datos.ascensor == 1]
res = nonp.rank_compare_2indep(lift_properties['price_m2'], nolift_properties['price_m2'])
print(f"Mann-Whitney's U rank-sum test: W={res.statistic:.3f}, p-value={res.pvalue:.3f}")

## LEVENE'S TEST FOR HOMOSKEDASTICITY

res = levene(
	lift_properties['price_m2'] ** (1/4),
    nolift_properties['price_m2'] ** (1/4),
    center='mean'
)

print(f"Levene's test for homogeneity of variances: F={res.statistic:.3f}, p-value={res.pvalue:.3f}")

## PARAMETRIC WELCH'S T TEST

res = ttest_ind(
	lift_properties['price_m2'] ** (1/4),
    nolift_properties['price_m2'] ** (1/4),
    usevar='unequal'
)

print(f"Welch's t-test: t={res[0]:.3f}, p-value={res[1]:.3f}")
