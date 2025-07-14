import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('data/ab_test_data.csv')

# Summary
print("Basic Info:")
print(df.groupby("group")["converted"].mean())
print(df.groupby("group")["retained_day7"].mean())
print(df.groupby("group")["time_spent_sec"].mean())

# Chi-square test for conversion
contingency_conversion = pd.crosstab(df['group'], df['converted'])
chi2_conv, p_conv, _, _ = stats.chi2_contingency(contingency_conversion)
print("\n🔍 Conversion Rate P-value:", round(p_conv, 4))

# t-test for time_spent
group_a = df[df['group'] == 'A']['time_spent_sec']
group_b = df[df['group'] == 'B']['time_spent_sec']
t_stat, p_time = stats.ttest_ind(group_a, group_b)
print("🕒 Time Spent P-value:", round(p_time, 4))

# Chi-square test for retention
contingency_ret = pd.crosstab(df['group'], df['retained_day7'])
chi2_ret, p_ret, _, _ = stats.chi2_contingency(contingency_ret)
print("📈 Retention Rate P-value:", round(p_ret, 4))

# Optional Plot - Conversion
sns.barplot(data=df, x='group', y='converted', ci=None)
plt.title("Conversion Rate by Group")
plt.ylabel("Conversion Rate")
plt.savefig("data/conversion_plot.png")
plt.show()
