import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

# Load data
df = pd.read_csv('data/ab_test_data.csv')

st.title("📊 Feature Impact Analyzer - A/B Test Dashboard")

# Metrics summary
st.header("🧪 Test Groups Summary")
group_summary = df.groupby("group").agg({
    "converted": "mean",
    "retained_day7": "mean",
    "time_spent_sec": "mean"
}).rename(columns={
    "converted": "Conversion Rate",
    "retained_day7": "Retention Rate (Day 7)",
    "time_spent_sec": "Avg Time on Page (sec)"
})

st.dataframe(group_summary.style.format("{:.2%}"))

# Plot Conversion Rate
st.header("📈 Conversion Rate by Group")
fig1, ax1 = plt.subplots()
sns.barplot(data=df, x="group", y="converted", ci=None, ax=ax1)
ax1.set_ylabel("Conversion Rate")
st.pyplot(fig1)

# Run statistical test - Conversion
st.subheader("🔬 Conversion Significance Test")
contingency = pd.crosstab(df['group'], df['converted'])
chi2, p_conv, _, _ = stats.chi2_contingency(contingency)
st.write(f"**P-Value for Conversion Rate:** `{p_conv:.4f}`")
if p_conv < 0.05:
    st.success("✅ Conversion Rate is Statistically Significant")
else:
    st.warning("⚠️ Conversion Rate is Not Statistically Significant")

# Time Spent Plot
st.header("🕒 Average Time Spent on Page")
fig2, ax2 = plt.subplots()
sns.boxplot(data=df, x="group", y="time_spent_sec", ax=ax2)
st.pyplot(fig2)

# Time Spent Test
group_a_time = df[df['group'] == 'A']['time_spent_sec']
group_b_time = df[df['group'] == 'B']['time_spent_sec']
t_stat_time, p_time = stats.ttest_ind(group_a_time, group_b_time)
st.subheader("🧪 Time Spent Significance Test")
st.write(f"**P-Value for Time Spent:** `{p_time:.4f}`")
if p_time < 0.05:
    st.success("✅ Time Spent is Statistically Significant")
else:
    st.warning("⚠️ Time Spent is Not Statistically Significant")

# Retention Test
st.header("📈 Retention Rate Test")
contingency_ret = pd.crosstab(df['group'], df['retained_day7'])
chi2_ret, p_ret, _, _ = stats.chi2_contingency(contingency_ret)
st.write(f"**P-Value for Retention Rate:** `{p_ret:.4f}`")
if p_ret < 0.05:
    st.success("✅ Retention Rate is Statistically Significant")
else:
    st.warning("⚠️ Retention Rate is Not Statistically Significant")

# Final Recommendation
st.header("📌 Final Product Decision")

# Metric Averages
conv_a = group_summary.loc["A", "Conversion Rate"]
conv_b = group_summary.loc["B", "Conversion Rate"]
ret_a = group_summary.loc["A", "Retention Rate (Day 7)"]
ret_b = group_summary.loc["B", "Retention Rate (Day 7)"]
time_a = group_summary.loc["A", "Avg Time on Page (sec)"]
time_b = group_summary.loc["B", "Avg Time on Page (sec)"]

# Conditions
conv_better = (conv_b > conv_a) and (p_conv < 0.05)
ret_better = (ret_b > ret_a) and (p_ret < 0.05)
time_better = (time_b > time_a) and (p_time < 0.05)

# Final Verdict
if conv_better and ret_better and time_better:
    st.success("🎯 Group B wins on **all KPIs** — Strongly recommend rollout!")
elif conv_better and (ret_better or time_better):
    st.info("✅ Group B shows improvement in key areas — Recommend rollout with close monitoring.")
elif conv_better:
    st.warning("🟡 Conversion is better, but retention/time are not — Suggest extended testing before rollout.")
else:
    st.error("❌ No significant improvement — Do NOT rollout yet.")

