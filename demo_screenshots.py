"""
demo_screenshots.py — generate preview images for the README.

Runs a small synthetic 3-month budget through matplotlib and saves PNGs
to screenshots/. Data is illustrative only — not real spending. Re-run
with `python demo_screenshots.py` to refresh.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="talk")

OUT = "screenshots"
os.makedirs(OUT, exist_ok=True)

# ---------- Synthetic data ----------
months = ["Jan", "Feb", "Mar"]
income = np.array([4500, 4500, 4800])
needs_total = np.array([2050, 2120, 2200])
wants_total = np.array([1100, 1250, 1280])
savings = income - needs_total - wants_total

latest_income = income[-1]
latest_expenses = {
    "Housing": 1300, "Groceries": 350, "Transportation": 280,
    "Health": 150, "Insurance": 120, "Dining": 280,
    "Entertainment": 220, "Subscriptions": 90, "Personal": 360,
}
needs_set = {"Housing", "Groceries", "Transportation", "Health", "Insurance"}
recommended_rule = {"Needs": 0.50, "Wants": 0.30, "Savings": 0.20}
caps = {
    "Housing": 0.25, "Groceries": 0.08, "Transportation": 0.07,
    "Insurance": 0.03, "Health": 0.07, "Debt Payments": 0.05,
    "Dining": 0.04, "Entertainment": 0.03, "Subscriptions": 0.02,
}

# ---------- 1. Category bars with cap lines ----------
df = pd.DataFrame([
    {"category": k, "amount": v, "group": "Needs" if k in needs_set else "Wants"}
    for k, v in latest_expenses.items()
])
order = df.sort_values("amount", ascending=False)["category"]
plt.figure(figsize=(12, 6.5))
ax = sns.barplot(
    data=df, x="category", y="amount", hue="group",
    order=order, palette={"Needs": "#3b82f6", "Wants": "#22c55e"},
)
for idx, cat in enumerate(order):
    if cat in caps:
        cap_value = latest_income * caps[cat]
        ax.hlines(y=cap_value, xmin=idx - 0.4, xmax=idx + 0.4,
                  colors="#dc2626", linestyles="--", linewidth=1.6)
        ax.text(idx, cap_value, " cap", color="#dc2626",
                ha="center", va="bottom", fontsize=10)
ax.set_title("Planned Spending by Category — Mar (with 50/30/20 caps)")
ax.set_ylabel("Amount ($)")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig(f"{OUT}/01-category-bars.png", dpi=130)
plt.close()

# ---------- 2. Allocation vs 50/30/20 ----------
needs_pct = needs_total[-1] / latest_income
wants_pct = wants_total[-1] / latest_income
savings_pct = savings[-1] / latest_income

labels = ["Baseline 50/30/20", "Your Mar Plan"]
needs_vals = [recommended_rule["Needs"] * 100, needs_pct * 100]
wants_vals = [recommended_rule["Wants"] * 100, wants_pct * 100]
saves_vals = [recommended_rule["Savings"] * 100, savings_pct * 100]

plt.figure(figsize=(9, 6))
plt.bar(labels, needs_vals, label="Needs", color="#3b82f6")
plt.bar(labels, wants_vals, bottom=needs_vals, label="Wants", color="#22c55e")
plt.bar(labels, saves_vals,
        bottom=np.array(needs_vals) + np.array(wants_vals),
        label="Savings", color="#f59e0b")
plt.title("Allocation vs. 50/30/20 Guideline")
plt.ylabel("Percent of Income (%)")
plt.legend(frameon=False, loc="upper right")
plt.tight_layout()
plt.savefig(f"{OUT}/02-allocation-vs-rule.png", dpi=130)
plt.close()

# ---------- 3. Month-over-month trends ----------
plt.figure(figsize=(11, 5.5))
plt.plot(months, income, marker="o", linewidth=2.5, label="Income")
plt.plot(months, needs_total, marker="o", linewidth=2.5, label="Needs")
plt.plot(months, wants_total, marker="o", linewidth=2.5, label="Wants")
plt.plot(months, savings, marker="o", linewidth=2.5, label="Savings")
plt.title("Month-over-Month Trends")
plt.ylabel("Amount ($)")
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig(f"{OUT}/03-mom-trends.png", dpi=130)
plt.close()

# ---------- 4. Savings projection (12 months) ----------
avg_savings = float(np.mean(savings))
t = np.arange(0, 13)
proj = avg_savings * t

plt.figure(figsize=(11, 5.5))
plt.plot(t, proj, linewidth=3, color="#0f3460", label="Projected savings")
for marker_m in [3, 6, 12]:
    plt.scatter([marker_m], [proj[marker_m]], s=80, color="#0f3460", zorder=5)
    plt.text(marker_m, proj[marker_m], f"  M{marker_m}: ${proj[marker_m]:,.0f}",
             va="center", fontsize=11)
plt.title("Savings Projection — Next 12 Months")
plt.xlabel("Months From Now")
plt.ylabel("Total Saved ($)")
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig(f"{OUT}/04-savings-projection.png", dpi=130)
plt.close()

# ---------- 5. Investment growth scenarios ----------
def future_values(months_n, contrib, apr):
    r = apr / 12.0
    out, total = [], 0.0
    for _ in range(months_n + 1):
        out.append(total)
        total = total * (1 + r) + contrib
    return np.array(out)

horizon = 60
xh = np.arange(horizon + 1)
fv0 = future_values(horizon, avg_savings, 0.00)
fv5 = future_values(horizon, avg_savings, 0.05)
fv8 = future_values(horizon, avg_savings, 0.08)

plt.figure(figsize=(11, 5.5))
plt.plot(xh, fv0, linewidth=2.5, label="0% APR")
plt.plot(xh, fv5, linewidth=2.5, label="5% APR")
plt.plot(xh, fv8, linewidth=2.5, label="8% APR")
for label, vals in [("0%", fv0), ("5%", fv5), ("8%", fv8)]:
    plt.text(horizon, vals[-1], f"  {label}: ${vals[-1]:,.0f}",
             va="center", fontsize=11)
plt.title("Investment Growth Scenarios (Monthly Contributions)")
plt.xlabel("Months From Now")
plt.ylabel("Portfolio Value ($)")
plt.legend(frameon=False, loc="upper left")
plt.tight_layout()
plt.savefig(f"{OUT}/05-investment-growth.png", dpi=130)
plt.close()

print("Saved 5 screenshots to", OUT + "/")
