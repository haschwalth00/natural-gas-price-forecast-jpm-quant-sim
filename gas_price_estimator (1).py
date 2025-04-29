
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Load the data
file_path = 'Nat_Gas.csv'  # Ensure this file is in the same folder
nat_gas_data = pd.read_csv(file_path)

# Preprocessing
nat_gas_data['Dates'] = pd.to_datetime(nat_gas_data['Dates'])
nat_gas_data.set_index('Dates', inplace=True)

# Interpolation preparation
date_numeric = (nat_gas_data.index - nat_gas_data.index[0]).days
interp_func = interp1d(date_numeric, nat_gas_data['Prices'], kind='linear', fill_value="extrapolate")

# Extrapolation preparation
holt_winters_model = ExponentialSmoothing(
    nat_gas_data['Prices'],
    trend='add',
    seasonal='add',
    seasonal_periods=12
).fit()

future_dates = pd.date_range(start=nat_gas_data.index[-1] + pd.DateOffset(months=1), periods=12, freq='M')
future_preds = holt_winters_model.forecast(12)

full_dates = nat_gas_data.index.append(future_dates)
full_prices = pd.concat([nat_gas_data['Prices'], pd.Series(future_preds, index=future_dates)])

# Visualization
plt.figure(figsize=(12, 6))
plt.plot(full_dates, full_prices, marker='o', label='Actual & Forecasted Prices')
plt.axvline(x=nat_gas_data.index[-1], color='red', linestyle='--', label='Forecast Start')
plt.title('Natural Gas Prices with 1-Year Forecast')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()

# Final function
def estimate_gas_price(input_date_str):
    input_date = pd.to_datetime(input_date_str)
    
    if input_date < full_dates[0]:
        raise ValueError("Date is earlier than available data (before Oct 31, 2020).")

    if input_date <= nat_gas_data.index[-1]:
        input_numeric = (input_date - nat_gas_data.index[0]).days
        estimated_price = interp_func(input_numeric)
    elif input_date <= future_dates[-1]:
        estimated_price = np.interp(
            input_date.toordinal(),
            [d.toordinal() for d in future_dates],
            future_preds
        )
    else:
        raise ValueError("Date is beyond the forecast range (after Sep 30, 2025).")

    return round(float(estimated_price), 2)

# Example usage
if __name__ == "__main__":
    test_dates = ['2022-06-15', '2024-11-30', '2025-05-01']
    for date in test_dates:
        try:
            price = estimate_gas_price(date)
            print(f"Estimated price on {date}: ${price}")
        except ValueError as e:
            print(f"Error for {date}: {e}")
