import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

data = pd.read_csv('train_predictions.csv')
data['year_month'] = pd.to_datetime(data['year_month'], format='%Y-%m-%d')

category_demand_stats = data.groupby('product_category')['forecast_qty'].agg(['mean', 'std']).reset_index()
category_demand_stats['CV'] = category_demand_stats['std'] / category_demand_stats['mean']

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

category_demand_stats['service_level'] = category_demand_stats['CV'].apply(assign_service_level)

service_level_mapping = category_demand_stats.set_index('product_category')['service_level'].to_dict()
data['service_level'] = data['product_category'].map(service_level_mapping)
data['Z_score'] = data['service_level'].apply(lambda x: norm.ppf(x))

print(category_demand_stats[['product_category', 'CV', 'service_level']])


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

data['gross_profit_margin'] = data['product_category'].map(profit_margin_mapping)

data['demand_variability'] = data.groupby('product_id')['forecast_qty'].transform('std').fillna(0)

lead_time = 2
base_service_level = 0.95

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
data['Z_score'] = data['service_level'].apply(lambda x: norm.ppf(x))

data['base_safety_stock'] = data['Z_score'] * data['demand_variability'] * np.sqrt(lead_time)

profit_margin_scale = 0.3
data['adjusted_safety_stock'] = data['base_safety_stock'] * (1 + data['gross_profit_margin'] * profit_margin_scale)

data['month'] = data['year_month'].dt.month
seasonal_multipliers = {
    1: 1.1,  # January - New Year sales
    2: 1.05,  # February - Slight bump for Valentine's Day
    3: 1.0,  # March - Lower demand
    4: 1.0,  # April - Steady demand
    5: 1.05,  # May - Increase for Mother's Day
    6: 1.0,  # June - Steady demand
    7: 1.15,  # July - Mid-year/back-to-school sales start in some regions
    8: 1.1,  # August - Back-to-school peaks
    9: 1.0,  # September - Steady demand
    10: 1.2,  # October - Halloween preparation
    11: 1.25,  # November - Black Friday/Cyber Monday
    12: 1.3   # December - Holiday/Christmas season
}

data['seasonal_adjustment'] = data['month'].map(seasonal_multipliers).fillna(1.0)
data['final_safety_stock'] = data['adjusted_safety_stock'] * data['seasonal_adjustment']

data['reorder_amount'] = data['forecast_qty'] + data['final_safety_stock']
high_variability_threshold = 10
variability_multiplier = 1.1
data['final_reorder_amount'] = np.where(
    data['demand_variability'] > high_variability_threshold,
    data['reorder_amount'] * variability_multiplier,
    data['reorder_amount']
)
data['final_reorder_amount'] = np.ceil(data['final_reorder_amount'])

monthly_reorder = data.groupby([data['year_month'].dt.to_period('M'), 'product_id'])['final_reorder_amount'].sum().reset_index()
monthly_reorder['year_month'] = monthly_reorder['year_month'].dt.to_timestamp()

print(monthly_reorder.head)

sample_product_id = 'GGOEA0CH077599' # Replace with product id for viewing

sample_reorder_train = monthly_reorder[monthly_reorder['product_id'] == sample_product_id]

plt.figure(figsize=(12, 6))
plt.plot(sample_reorder_train['year_month'], sample_reorder_train['final_reorder_amount'], marker='o', color='b', label='Reorder Amount')
plt.title(f'Reorder Amount Over Time for Product ID: {sample_product_id}')
plt.xlabel('Month')
plt.ylabel('Reorder Amount')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()


test_data = pd.read_csv('forecast_predictions.csv')

test_data['year_month'] = pd.to_datetime('2017-08-01')

test_data['service_level'] = test_data['product_category'].map(service_level_mapping)
test_data['gross_profit_margin'] = test_data['product_category'].map(profit_margin_mapping)

historical_demand_variability = data.groupby('product_id')['forecast_qty'].std()
test_data['demand_variability'] = test_data['product_id'].map(historical_demand_variability).fillna(0)

august_multiplier = seasonal_multipliers.get(8, 1.0)
test_data['seasonal_adjustment'] = august_multiplier

test_data['Z_score'] = test_data['service_level'].apply(lambda x: norm.ppf(x))
test_data['base_safety_stock'] = test_data['Z_score'] * test_data['demand_variability'] * np.sqrt(lead_time)
test_data['adjusted_safety_stock'] = test_data['base_safety_stock'] * (1 + test_data['gross_profit_margin'] * profit_margin_scale)
test_data['final_safety_stock'] = test_data['adjusted_safety_stock'] * test_data['seasonal_adjustment']
test_data['reorder_amount'] = test_data['forecast_qty'] + test_data['final_safety_stock']

test_data['final_reorder_amount'] = np.where(
    test_data['demand_variability'] > high_variability_threshold,
    test_data['reorder_amount'] * variability_multiplier,
    test_data['reorder_amount']
)
test_data['final_reorder_amount'] = np.ceil(test_data['final_reorder_amount'])

monthly_reorder_test = test_data.groupby(['year_month', 'product_id'])['final_reorder_amount'].sum().reset_index()

print("\nNext Month's Reorder Plan (Test Data - August 2017):")
print(monthly_reorder_test.head())
