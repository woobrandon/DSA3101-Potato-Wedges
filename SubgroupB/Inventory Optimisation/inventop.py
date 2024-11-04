import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

cleaned_synthetic_v3 = pd.read_csv("cleaned_synthetic_v3.csv")

# Step 1: ARIMA Forecasting for Time Series Data

# Filter for one product (you can loop over all products)
product_id = 'GGOEAAYC068756'  # Replace with a valid product_id
product_data = cleaned_synthetic_v3[cleaned_synthetic_v3['product_id'] == product_id]

# Convert 'year_month' to datetime and set as index
product_data['year_month'] = pd.to_datetime(product_data['year_month'], format='%Y-%m-%d')
product_data.set_index('year_month', inplace=True)

# Aggregate monthly sales (if needed)
monthly_sales = product_data['present_total_qty'].resample('M').sum()

# Train ARIMA model
arima_model = ARIMA(monthly_sales, order=(1, 1, 1))  # You can auto-tune ARIMA parameters with auto_arima
arima_model_fit = arima_model.fit()

# Forecast the next 1 month using ARIMA (baseline forecast)
arima_forecast = arima_model_fit.forecast(steps=1)[0]  # Get next month's forecast

# Step 2: Feature Engineering for XGBoost

# Add lag feature for previous month's sales
product_data['prev_month_sales'] = product_data['present_total_qty'].shift(1)

# Create additional features like 'month' and 'year' from the datetime index
product_data['month'] = product_data.index.month
product_data['year'] = product_data.index.year

# Drop the first row with NaN (because of the shift)
product_data.dropna(inplace=True)

# Features and target
X = product_data[['month', 'year', 'product_price', 'prev_month_sales']]
y = product_data['present_total_qty']

# Step 3: Train XGBoost on top of ARIMA
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Initialize and train the XGBoost model
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
xgb_model.fit(X_train, y_train)

# Make predictions using XGBoost (deviations from ARIMA forecast)
xgb_pred = xgb_model.predict(X_test)

# Evaluate the XGBoost model
rmse_xgb = mean_squared_error(y_test, xgb_pred, squared=False)
print(f"XGBoost Test RMSE: {rmse_xgb}")

# Step 4: Combine ARIMA and XGBoost Predictions
# Forecast for the next month using XGBoost
X_new = pd.DataFrame({
    'month': [7],  # July
    'year': [2017],  # Forecasting for July 2017
    'product_price': [product_data['product_price'].iloc[-1]],  # Use the most recent price
    'prev_month_sales': [arima_forecast]  # Use ARIMA forecast as previous month's sales
})

# Predict deviations from ARIMA using XGBoost
xgb_forecast = xgb_model.predict(X_new)[0]

# Combine ARIMA and XGBoost forecasts
final_forecast = arima_forecast + xgb_forecast

print(f"Final Combined Forecast for July 2017: {final_forecast}")

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(monthly_sales, label='Historical Sales')
plt.axvline(monthly_sales.index[-1], color='gray', linestyle='--', label='Forecast Period')
plt.plot([monthly_sales.index[-1] + pd.DateOffset(months=1)], [final_forecast], 'ro', label='Combined Forecast')
plt.title(f"Hybrid ARIMA + XGBoost Forecast for Product {product_id}")
plt.legend()
plt.show()

# Now you can use the final forecast to adjust your inventory for the next month
initial_stock = 100
reorder_amount = max(0, final_forecast - initial_stock)
print(f"Reorder amount for July 2017: {reorder_amount}")
