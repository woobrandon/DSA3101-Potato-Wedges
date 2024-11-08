import pandas as pd
import numpy as np
from scipy.stats import norm

# Load data
data = pd.read_csv('train_predictions.csv')

# Convert 'year_month' to datetime format
data['year_month'] = pd.to_datetime(data['year_month'], format='%Y-%m-%d')

# Step 1: Calculate mean and standard deviation of demand (forecast_qty) for each category
category_demand_stats = data.groupby('product_category')['forecast_qty'].agg(['mean', 'std']).reset_index()
category_demand_stats['CV'] = category_demand_stats['std'] / category_demand_stats['mean']  # Coefficient of Variation

# Step 2: Define a function to assign service levels based on CV with adjusted ranges
def assign_service_level(cv):
    if cv < 1:
        return 0.90  # Low variability
    elif 1 <= cv < 2:
        return 0.93  # Moderate variability
    elif 2 <= cv < 3:
        return 0.95  # High variability
    elif 3 <= cv < 4:
        return 0.97  # Very high variability
    else:
        return 0.98  # Extremely high variability

# Apply the function to determine service levels based on CV
category_demand_stats['service_level'] = category_demand_stats['CV'].apply(assign_service_level)

# Step 3: Map the calculated service levels back to the main data
service_level_mapping = category_demand_stats.set_index('product_category')['service_level'].to_dict()
data['service_level'] = data['product_category'].map(service_level_mapping)

# Calculate Z-score based on the dynamically assigned service level
data['Z_score'] = data['service_level'].apply(lambda x: norm.ppf(x))

# Display results
print(category_demand_stats[['product_category', 'CV', 'service_level']])




# Step 1: Map Product Categories to Profit Margins
# Define profit margin mapping for each product category based on industry data
profit_margin_mapping = {
    'Accessories': 0.46,
    'Apparel': 0.416,
    'Bags': 0.416,
    'Drinkware': 0.478,
    'Electronics': 0.337,
    'Fun': 0.462,
    'Gift Cards': 0.401,
    'Headgear': 0.416,
    'Housewares': 0.375,
    'Lifestyle': 0.401,
    'Notebooks & Journals': 0.401,
    'Office': 0.337
}

# Map the product categories to their respective gross profit margins
data['gross_profit_margin'] = data['product_category'].map(profit_margin_mapping)

# Step 2: Calculate Demand Variability (Standard Deviation of Demand)
# Group by product_id and calculate standard deviation of demand to measure variability
data['demand_variability'] = data.groupby('product_id')['forecast_qty'].transform('std').fillna(0)

# Step 3: Set Lead Time and Base Service Level
lead_time = 2  # Lead time in weeks (adjust based on actual lead time)
base_service_level = 0.95  # Base service level (e.g., 95%)

# Step 4: Dynamic Service Level Based on Product Category
# Set higher service levels for certain product categories 
service_level_mapping = {
    'Accessories': 0.95,
    'Apparel': 0.97,
    'Bags': 0.95,
    'Drinkware': 0.95,
    'Electronics': 0.95,
    'Fun': 0.95,
    'Gift Cards': 0.93,
    'Headgear': 0.98,
    'Housewares': 0.93,
    'Lifestyle': 0.95,
    'Notebooks & Journals': 0.95,
    'Office': 0.97
}
data['service_level'] = data['product_category'].map(service_level_mapping).fillna(base_service_level)

# Calculate Z-score based on service level for each product
data['Z_score'] = data['service_level'].apply(lambda x: norm.ppf(x))

# Step 5: Base Safety Stock Calculation
# Calculate base safety stock using demand variability, lead time, and service level Z-score
data['base_safety_stock'] = data['Z_score'] * data['demand_variability'] * np.sqrt(lead_time)

# Step 6: Adjust Safety Stock with Profit Margin
# Scaling factor for profit margin to prioritize high-margin items
profit_margin_scale = 0.3
data['adjusted_safety_stock'] = data['base_safety_stock'] * (1 + data['gross_profit_margin'] * profit_margin_scale)

# Step 7: Seasonal Adjustment (Optional)
# Assume seasonal factors for certain months (e.g., holiday season in December)
data['month'] = data['year_month'].dt.month
seasonal_multiplier = 1.2  # 20% additional buffer during peak months (e.g., December)
data['seasonal_adjustment'] = np.where(data['month'] == 12, seasonal_multiplier, 1.0)
data['final_safety_stock'] = data['adjusted_safety_stock'] * data['seasonal_adjustment']

# Step 8: Calculate Reorder Amount
# Add safety stock to forecasted demand to determine reorder amount
data['reorder_amount'] = np.maximum(0, data['forecast_qty'] + data['final_safety_stock'] - data['forecast_qty'])

# Step 9: Final Adjustments for High-Variability Items
# For items with high demand variability, add an additional buffer
high_variability_threshold = 10  # Threshold for high variability
variability_multiplier = 1.1  # Extra 10% buffer for high-variability items
data['final_reorder_amount'] = np.where(
    data['demand_variability'] > high_variability_threshold,
    data['reorder_amount'] * variability_multiplier,
    data['reorder_amount']
)
data['final_reorder_amount'] = np.ceil(data['final_reorder_amount'])


# Group by month and product to calculate monthly reorder amounts if needed
monthly_reorder = data.groupby([data['year_month'].dt.to_period('M'), 'product_id'])['final_reorder_amount'].sum().reset_index()
monthly_reorder['year_month'] = monthly_reorder['year_month'].dt.to_timestamp()


# Display results
print(monthly_reorder.head())


test_data = pd.read_csv('test_predictions.csv')
test_data['year_month'] = pd.to_datetime(test_data['year_month'], format='%Y-%m-%d')

test_data['service_level'] = test_data['product_category'].map(service_level_mapping)
test_data['gross_profit_margin'] = test_data['product_category'].map(profit_margin_mapping)
test_data['demand_variability'] = test_data.groupby('product_id')['forecast_qty'].transform('std').fillna(0)
test_data['Z_score'] = test_data['service_level'].apply(lambda x: norm.ppf(x))
test_data['base_safety_stock'] = test_data['Z_score'] * test_data['demand_variability'] * np.sqrt(lead_time)
test_data['adjusted_safety_stock'] = test_data['base_safety_stock'] * (1 + test_data['gross_profit_margin'] * profit_margin_scale)
test_data['seasonal_adjustment'] = np.where(test_data['year_month'].dt.month == 12, seasonal_multiplier, 1.0)
test_data['final_safety_stock'] = test_data['adjusted_safety_stock'] * test_data['seasonal_adjustment']
test_data['reorder_amount'] = np.maximum(0, test_data['forecast_qty'] + test_data['final_safety_stock'] - test_data['forecast_qty'])
test_data['final_reorder_amount'] = np.where(
    test_data['demand_variability'] > high_variability_threshold,
    test_data['reorder_amount'] * variability_multiplier,
    test_data['reorder_amount']
)
test_data['final_reorder_amount'] = np.ceil(test_data['final_reorder_amount'])

monthly_reorder_test = test_data.groupby([test_data['year_month'].dt.to_period('M'), 'product_id'])['final_reorder_amount'].sum().reset_index()
monthly_reorder_test['year_month'] = monthly_reorder_test['year_month'].dt.to_timestamp()

print("\nNext Month's Reorder Plan:")
print(monthly_reorder_test)