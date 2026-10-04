"""
AromaKart Perfume Sales — Exploratory Data Analysis
Day 4 of 7 — Python / Pandas Analysis

This script loads perfume_sales.csv, cleans it, explores it, and produces
6 charts answering the core business questions from Day 1.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#CCCCCC"
plt.rcParams["figure.facecolor"] = "white"

PURPLE = "#5B2C6F"
GOLD = "#D4AF37"
PALETTE = ["#5B2C6F", "#8E44AD", "#D4AF37", "#C0392B", "#2980B9", "#27AE60",
           "#E67E22", "#16A085", "#7D3C98", "#B03A2E", "#2C3E50", "#F39C12"]

# --------------------------------------------------------------------------
# 1. LOAD & CLEAN
# --------------------------------------------------------------------------
import os

CSV_CANDIDATES = ["../data/perfume_sales.csv", "perfume_sales.csv", "data/perfume_sales.csv"]
CSV_PATH = next((p for p in CSV_CANDIDATES if os.path.exists(p)), CSV_CANDIDATES[0])
df = pd.read_csv(CSV_PATH, parse_dates=["Order_Date"])

print("Shape:", df.shape)
print("\nData types:\n", df.dtypes)
print("\nMissing values:\n", df.isnull().sum())
print("\nDuplicate Order_IDs:", df["Order_ID"].duplicated().sum())
print("\nDescribe (numeric):\n", df.describe())

# Brand tier mapping used throughout the analysis
premium_brands = ["Dior", "Chanel", "Gucci", "Versace", "Tom Ford", "Burberry", "Armani"]
mid_brands = ["Calvin Klein", "Zara"]

def brand_tier(b):
    if b in premium_brands:
        return "Premium"
    if b in mid_brands:
        return "Mid"
    return "Budget"

df["Brand_Tier"] = df["Brand"].apply(brand_tier)
df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)

# --------------------------------------------------------------------------
# 2. CHART 1 — Monthly Revenue Trend (seasonality)
# --------------------------------------------------------------------------
monthly = df.groupby("Month")["Total_Amount"].sum().reset_index()
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(monthly["Month"], monthly["Total_Amount"], marker="o", color=PURPLE, linewidth=2)
ax.fill_between(range(len(monthly)), monthly["Total_Amount"], color=PURPLE, alpha=0.08)
ax.set_title("Monthly Revenue Trend — AromaKart (Jan 2025 – Jun 2026)", fontsize=13, fontweight="bold", color=PURPLE)
ax.set_ylabel("Revenue (Rs.)")
ax.set_xlabel("Month")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e5:.1f}L"))
plt.xticks(rotation=60, ha="right", fontsize=8)
plt.tight_layout()
plt.savefig("../visuals/01_monthly_revenue_trend.png", dpi=150)
plt.close()

# --------------------------------------------------------------------------
# 3. CHART 2 — Revenue by City (top 12)
# --------------------------------------------------------------------------
city_rev = df.groupby("City")["Total_Amount"].sum().sort_values(ascending=False).head(12)
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(city_rev.index[::-1], city_rev.values[::-1], color=PURPLE)
ax.set_title("Top 12 Cities by Revenue", fontsize=13, fontweight="bold", color=PURPLE)
ax.set_xlabel("Revenue (Rs.)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e5:.1f}L"))
for bar in bars:
    ax.text(bar.get_width() * 1.01, bar.get_y() + bar.get_height() / 2,
            f"{bar.get_width()/1e5:.1f}L", va="center", fontsize=8)
plt.tight_layout()
plt.savefig("../visuals/02_revenue_by_city.png", dpi=150)
plt.close()

# --------------------------------------------------------------------------
# 4. CHART 3 — Revenue vs. Order Volume by Brand (premium vs budget trade-off)
# --------------------------------------------------------------------------
brand_stats = df.groupby(["Brand", "Brand_Tier"]).agg(
    revenue=("Total_Amount", "sum"), orders=("Order_ID", "count")
).reset_index()
fig, ax = plt.subplots(figsize=(9, 7))
tier_colors = {"Premium": "#5B2C6F", "Mid": "#D4AF37", "Budget": "#27AE60"}
for tier, grp in brand_stats.groupby("Brand_Tier"):
    ax.scatter(grp["orders"], grp["revenue"], s=140, color=tier_colors[tier], label=tier, edgecolor="white", linewidth=1)
    for _, row in grp.iterrows():
        ax.annotate(row["Brand"], (row["orders"], row["revenue"]), fontsize=8,
                    xytext=(6, 4), textcoords="offset points")
ax.set_title("Brand Revenue vs. Order Volume (Premium vs Mid vs Budget)", fontsize=13, fontweight="bold", color=PURPLE)
ax.set_xlabel("Total Orders")
ax.set_ylabel("Total Revenue (Rs.)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e5:.1f}L"))
ax.legend(title="Brand Tier")
plt.tight_layout()
plt.savefig("../visuals/03_brand_revenue_vs_volume.png", dpi=150)
plt.close()

# --------------------------------------------------------------------------
# 5. CHART 4 — Delivery Status by Brand Tier (return-rate insight)
# --------------------------------------------------------------------------
status_tier = pd.crosstab(df["Brand_Tier"], df["Delivery_Status"], normalize="index") * 100
status_tier = status_tier[["Delivered", "Returned", "Cancelled"]].loc[["Premium", "Mid", "Budget"]]
fig, ax = plt.subplots(figsize=(8, 5))
status_tier.plot(kind="bar", stacked=True, ax=ax, color=["#27AE60", "#E67E22", "#C0392B"])
ax.set_title("Delivery Outcome % by Brand Tier", fontsize=13, fontweight="bold", color=PURPLE)
ax.set_ylabel("% of Orders")
ax.set_xlabel("Brand Tier")
plt.xticks(rotation=0)
ax.legend(title="Status", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig("../visuals/04_delivery_status_by_tier.png", dpi=150)
plt.close()

# --------------------------------------------------------------------------
# 6. CHART 5 — Payment Method Mix
# --------------------------------------------------------------------------
pay_counts = df["Payment_Method"].value_counts()
fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    pay_counts.values, labels=pay_counts.index, autopct="%1.1f%%",
    colors=PALETTE, startangle=90, textprops={"fontsize": 9}
)
ax.set_title("Orders by Payment Method", fontsize=13, fontweight="bold", color=PURPLE)
plt.tight_layout()
plt.savefig("../visuals/05_payment_method_mix.png", dpi=150)
plt.close()

# --------------------------------------------------------------------------
# 7. CHART 6 — Repeat vs. One-Time Customer Revenue Share
# --------------------------------------------------------------------------
cust_orders = df.groupby("Customer_ID").agg(orders=("Order_ID", "count"), revenue=("Total_Amount", "sum"))
cust_orders["type"] = np.where(cust_orders["orders"] > 1, "Repeat Customer", "One-Time Customer")
rev_share = cust_orders.groupby("type")["revenue"].sum()
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(rev_share.values, labels=rev_share.index, autopct="%1.1f%%",
       colors=[PURPLE, GOLD], startangle=90, textprops={"fontsize": 10})
ax.set_title("Revenue Share: Repeat vs. One-Time Customers", fontsize=13, fontweight="bold", color=PURPLE)
plt.tight_layout()
plt.savefig("../visuals/06_repeat_vs_onetime_revenue.png", dpi=150)
plt.close()

print("\nAll 6 charts saved to ../visuals/")

# --------------------------------------------------------------------------
# 8. KEY METRICS SUMMARY (printed for the write-up)
# --------------------------------------------------------------------------
print("\n--- KEY METRICS ---")
print("Total Revenue: Rs.", round(df["Total_Amount"].sum(), 2))
print("Total Orders:", len(df))
print("Average Order Value: Rs.", round(df["Total_Amount"].mean(), 2))
print("Unique Customers:", df["Customer_ID"].nunique())
print("Return Rate: {:.1f}%".format(100 * (df["Delivery_Status"] == "Returned").mean()))
print("Cancellation Rate: {:.1f}%".format(100 * (df["Delivery_Status"] == "Cancelled").mean()))
print("Top City:", df.groupby("City")["Total_Amount"].sum().idxmax())
print("Top Brand:", df.groupby("Brand")["Total_Amount"].sum().idxmax())
