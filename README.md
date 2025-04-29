# Natural Gas Price Forecast – J.P. Morgan Quantitative Research Simulation

## Overview

This project was developed during the **J.P. Morgan Quantitative Research virtual work experience**. It focuses on building a **forecasting model** for natural gas prices using historical data and time series analysis techniques. The final model supports both interpolation and extrapolation to estimate prices for arbitrary dates within a given range.

## Author

**Vanshwardhan Singh**

## Objective

To forecast natural gas prices for a 12-month future horizon using:
- **Linear interpolation** for estimating prices on dates within the historical dataset
- **Holt-Winters Exponential Smoothing** for forecasting future prices based on seasonal and trend components

## Core Features

- **Data Input:** Historical price data from `Nat_Gas.csv`
- **Forecasting Technique:** Holt-Winters additive model via `statsmodels`
- **Extrapolation Range:** 12 months beyond last known data point
- **Interpolation Range:** All valid dates within the dataset
- **Custom Python Function:** `estimate_gas_price(date)` returns estimated price or raises a range error
- **Data Visualization:** Forecast line chart with historical and predicted prices marked clearly

## How It Works

1. Loads and preprocesses natural gas price time series data
2. Applies linear interpolation for known data range
3. Fits an additive Holt-Winters model for 12-month extrapolation
4. Combines actual and forecasted data into a continuous time series
5. Provides a callable function to estimate gas prices for any valid date

## Example Usage

```python
price = estimate_gas_price('2024-11-30')
print(price)  # e.g., $4.78
