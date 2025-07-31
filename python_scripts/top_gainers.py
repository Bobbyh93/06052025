"""Fetch daily top gainers from CoinGecko and compute intraday stats.

This script fetches the top three cryptocurrencies by 24h price change
at a specified Pacific Time hour. It then downloads hourly price data
for the past 24h and calculates gains over 6h, 18h and 24h windows as
well as simple predictability metrics.
"""
from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

# --- configuration -------------------------------------------------------
CG_KEY = os.getenv("CG_KEY", "CG-UNmqcc4pQzwgzr9jk2Zrk4TD")
MIN_VOL_USD = 10_000_000
HEADERS = {"x-cg-demo-api-key": CG_KEY}

# Pacific time at which we want to inspect the market
PT_TARGET_HOUR = int(os.getenv("PT_TARGET_HOUR", "8"))  # default 08:00 PT

pt_zone = ZoneInfo("America/Los_Angeles")
utc_now = dt.datetime.now(dt.timezone.utc)
pt_now = utc_now.astimezone(pt_zone).replace(minute=0, second=0, microsecond=0)
# align to the requested hour, going back if needed
if pt_now.hour < PT_TARGET_HOUR:
    pt_now -= dt.timedelta(days=1)
pt_target = pt_now.replace(hour=PT_TARGET_HOUR)
utc_target = pt_target.astimezone(dt.timezone.utc)

# --- 1. top gainers ------------------------------------------------------
top_url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "price_change_percentage_24h_desc",
    "per_page": 50,
    "page": 1,
    "price_change_percentage": "24h",
}
leaders = (
    pd.DataFrame(requests.get(top_url, params=params, headers=HEADERS, timeout=10).json())
    .query("total_volume > @MIN_VOL_USD")
    .head(3)
)

# --- 2. hourly prices and stats -----------------------------------------
g_rows: list[list[float]] = []
m_rows: list[list[float]] = []

for _, coin in leaders.iterrows():
    cid, sym = coin["id"], coin["symbol"].upper()
    chart_url = f"https://api.coingecko.com/api/v3/coins/{cid}/market_chart"
    hist = requests.get(
        chart_url,
        params={"vs_currency": "usd", "days": 1, "interval": "hourly"},
        headers=HEADERS,
        timeout=10,
    ).json()["prices"]
    hourly = pd.DataFrame(hist, columns=["ts", "price"])
    hourly["ts"] = pd.to_datetime(hourly["ts"], unit="ms", utc=True)
    hourly.set_index("ts", inplace=True)
    hourly = hourly.loc[:utc_target]

    if len(hourly) < 25:
        # not enough data; skip this coin
        continue

    p_now = hourly.iloc[-1]["price"]
    p_6h = hourly.iloc[-7]["price"]
    p_18h = hourly.iloc[-19]["price"]
    p_24h = hourly.iloc[0]["price"]
    g_rows.append([
        sym,
        (p_now - p_6h) / p_6h * 100,
        (p_now - p_18h) / p_18h * 100,
        (p_now - p_24h) / p_24h * 100,
    ])

    ret = hourly["price"].pct_change().dropna()
    sigma = ret.std() * np.sqrt(len(ret))
    rho1 = ret.autocorr(1)
    hurst = np.polyfit(
        np.log(np.arange(2, len(ret) + 2)),
        np.log(ret.cumsum().abs() + 1e-12),
        1,
    )[0]
    m_rows.append([sym, sigma, rho1, hurst])

if not g_rows:
    raise SystemExit("Not enough historical data to compute gains")

gains = pd.DataFrame(g_rows, columns=["Coin", "Gain_6h_%", "Gain_18h_%", "Gain_24h_%"]).set_index(
    "Coin"
)
metrics = pd.DataFrame(m_rows, columns=["Coin", "sigma_24h", "rho1", "Hurst"]).set_index("Coin")

local_label = pt_target.strftime("%H:%M %Z")
ax = gains.plot.bar(figsize=(8, 4), ylabel="% Gain", title=f"{local_label} Intraday % Gains")
plt.tight_layout()
plt.show()

print(gains.round(2))
print(metrics.round(4))
