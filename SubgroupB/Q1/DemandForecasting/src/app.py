from flask import Flask, render_template, url_for
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import warnings
import threading
from scipy.stats import poisson
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
warnings.filterwarnings("ignore")


### Demand Forecasting
historical_data = pd.read_csv("../data/train_true.csv")
forecast_data = pd.read_csv("../data/forecast_predictions.csv")
past_forecast_data = pd.read_csv("../data/train_predictions.csv")
historical_data['year_month'] = pd.to_datetime(historical_data['year_month'])
forecast_data['year_month'] = pd.to_datetime(forecast_data['year_month'])
past_forecast_data['year_month'] = pd.to_datetime(past_forecast_data['year_month'])

name_id_mapping = forecast_data[['product_name', 'product_id', 'product_price']].drop_duplicates()

def lower_ci(mu):
    if mu > 30:
        lower_band = mu - (1.96 * np.sqrt(mu))
    else:
        model = poisson(mu = mu)
        lower_band = model.ppf(0.025)
    return np.round(lower_band)

def upper_ci(mu):
    if mu > 30:
        upper_band = mu + (1.96 * np.sqrt(mu))
    else:
        model = poisson(mu = mu)
        upper_band = model.ppf(0.975)
    return np.round(upper_band)

forecast_data['ci_lower'] = forecast_data['forecast_qty'].apply(lambda x: lower_ci(x))
forecast_data['ci_upper'] = forecast_data['forecast_qty'].apply(lambda x: upper_ci(x))
past_forecast_data['ci_lower'] = past_forecast_data['forecast_qty'].apply(lambda x: lower_ci(x))
past_forecast_data['ci_upper'] = past_forecast_data['forecast_qty'].apply(lambda x: upper_ci(x))

all_months = ['Jul 2016', 'Aug 2016', 'Sep 2016', 'Oct 2016', 'Nov 2016', 'Dec 2016', 'Jan 2017', 'Feb 2017', 'Mar 2017', 'Apr 2017', 'May 2017', 'Jun 2017', 'Jul 2017']

def plot_graph(id, price):

    plt.switch_backend('Agg')

    past_true = historical_data.loc[(historical_data['product_id'] == id) & (historical_data['product_price'] == price) & (historical_data['year_month'] != '2016-07-01')]
    forecast = forecast_data.loc[(forecast_data['product_id'] == id) & (forecast_data['product_price'] == price)]
    past_forecast = past_forecast_data.loc[(past_forecast_data['product_id'] == id) & (past_forecast_data['product_price'] == price)]
    name = forecast['product_name'].unique()
    forecast.rename({"forecast_qty":'qty'}, axis = 1, inplace = True)
    past_true.rename({"present_total_qty":'qty'}, axis = 1, inplace = True)
    past_forecast.rename({"forecast_qty":'qty'}, axis = 1, inplace = True)
    forecasts_df = pd.concat([past_forecast, forecast])

    plt.figure(figsize=(10, 6))
    sns.lineplot(x = past_true['year_month'], y = past_true['qty'], color = 'blue',label = 'Real', errorbar = None)
    sns.lineplot(x = forecasts_df['year_month'], y = forecasts_df['qty'], color = 'green', label = 'Predictions', errorbar = None) 
    y_lower = forecasts_df['ci_lower']
    y_upper = forecasts_df['ci_upper']
    plt.fill_between(forecasts_df['year_month'], y_lower, y_upper, color = "green", alpha = 0.1 )
    plt.xticks(rotation=45, ticks = forecasts_df['year_month'][::1], labels = forecasts_df['year_month'].dt.strftime('%b %Y'))
    plt.xlabel('Month')
    plt.ylabel('Sales quantity')
    plt.title(f'Sales trend and forecast for {name[0]}')
    
    image_path = f"static/images/test.png"
    plt.savefig(image_path, dpi = 300)
    plt.close()

    return f'images/test.png'


### Product Recommendation
product_df = pd.read_csv("../../../../ProductRecommendation/data/product_df.csv")
product_df['vector'] = product_df['vector'].apply(lambda x: np.fromstring(x, sep=',') if isinstance(x, str) else x)
associated_items = pd.read_csv("../../../../ProductRecommendation/data/crosssell.csv")
user_history = pd.read_csv("../../../../ProductRecommendation/data/user_history.csv", dtype = {'user_id':'str', 'product_id':'str'})
id_name_df = pd.read_csv("../../../../ProductRecommendation/data/id_name_df.csv")

def similarity(id1, id2):                      
    vec1 = np.array([product_df.loc[product_df['product_id'] == id1, 'vector'].values[0]]) 
    vec2 = np.array([product_df.loc[product_df['product_id'] == id2, 'vector'].values[0]]) 
    return cosine_similarity(vec1, vec2)[0][0]

def upsell(id, lim = -1):                                    # this function will output the top x most similar products to a given product, where x is defined by the user.
    mat = np.vstack(product_df['vector'])                                                       # embeddings for each product
    base_vec = np.array([product_df.loc[product_df['product_id'] == id, 'vector'].values[0]])   # embedding for queried product
    cos_sim = cosine_similarity(base_vec, mat).flatten()                                        # find cosine similarity between queried product and all other products

    df = product_df.copy()
    df['similarity'] = cos_sim
    df.drop(['tokens', 'lemma', 'vector'], axis = 1, inplace = True)
    curr_price = df.loc[df['product_id'] == id, 'product_price'].values[0]                      # obtain price of current product
    df = df.loc[df['product_id'] != id]

    # print(f'Current item is sold for {curr_price}')
    if lim != -1:
        return df.sort_values('similarity', ascending = False).loc[(df['product_id'] != id) & (df['product_price'] > curr_price) & (df['similarity'] > 0.8), 'product_id'].values[:lim]  # only return products that are more expensive
    else:
        return df.sort_values('similarity', ascending = False).loc[(df['product_id'] != id) & (df['product_price'] > curr_price) & (df['similarity'] > 0.8), 'product_id'].values

def crosssell(id, lim = -1):          # This function takes in a product and returns the top n associated products (confidence >35%)
    if id not in associated_items['product_1'].values:
        return 'There are no associated items for this product'     # If there are no associated items, a message will be printed alerting the user
    if lim != -1:
        return associated_items.sort_values('similarity', ascending = False).loc[associated_items['product_1'] == id, 'product_2'].values[:lim]
    else:
        return associated_items.sort_values('similarity', ascending = False).loc[associated_items['product_1'] == id, 'product_2'].values

def products_to_recommend(id, n_crosssell, n_upsell):       
    nc = int(n_crosssell)
    nu = int(n_upsell)    
    user_products = user_history.loc[user_history['user_id'] == str(id), 'product_id'].values
    crosssell_final = []
    upsell_final = []

    for product in user_products:
        crosssell_products = crosssell(product)
        if type(crosssell_products) != str:
            crosssell_final.extend(crosssell_products)
        upsell_products = upsell(product)
        if len(upsell_products) > 0:
            upsell_final.extend(upsell_products)
    
    crosssell_count = Counter(crosssell_final)
    upsell_count = Counter(upsell_final)

    return [x[0] for x in crosssell_count.most_common(nc)], [y[0] for y in upsell_count.most_common(nu)]

def get_product_name(products):
    all_names = []
    for id in products:
        product_name = id_name_df.loc[id_name_df['product_id'] == id, 'product_name'].values
        all_names.append(f"({id}: {product_name[0]})")
    return all_names



from flask import Flask, render_template, request
import pandas as pd
import time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/demand_forecasting', methods=["GET", "POST"])
def demand_forecasting():
    result = None
    image_path = None

    if request.method == "POST":
        input_text = request.form["input_text"] 

        try:
            id = input_text.split(",")[0].strip()
            price = float(input_text.split(",")[1].strip())
        
            forecast_qty = forecast_data.loc[(forecast_data['product_id'] == id) & (forecast_data['product_price'] == price), 'forecast_qty'].values[0].astype(int)
            image_path = plot_graph(id, price)
            result = f"Forecasted demand for product {id} at price ${price} is {forecast_qty} unit(s)."
        except IndexError:
            result = f"No data found for product ID {id} at price ${price}."

    return render_template("demand_forecasting.html", result=result, image_path=image_path)

@app.route('/product_recommendation', methods=["GET", "POST"])
def product_recommendation():
    result = None
    image_path = None

    if request.method == "POST":
        input_text = request.form["input_text"] 
        try:
            id = input_text.split(",")[0].strip()
            n_crosssell = input_text.split(",")[1].strip()
            n_upsell = input_text.split(",")[2].strip()

            crosssell_products, upsell_products = products_to_recommend(id, n_crosssell, n_upsell)
            
            if len(crosssell_products) > 0:
                crosssell_products_names = get_product_name(crosssell_products)
            else:
                crosssell_products_names = crosssell_products

            if len(upsell_products) > 0:
                upsell_products_names = get_product_name(upsell_products)
            else:
                upsell_products_names = upsell_products

            result = f"""
                <p><strong>Products to cross-sell:</strong><br>
                { '<br>'.join(crosssell_products_names) if crosssell_products_names else 'No products found'}</p>
                <p><strong>Products to upsell:</strong><br>
                { '<br>'.join(upsell_products_names) if upsell_products_names else 'No products found'}</p>
            """
            
        except IndexError:
            result = f"No data found for user ID {id}."

    return render_template("product_recommendation.html", result=result)


@app.route('/products')
def products():
    result_products = name_id_mapping.sort_values('product_name')
    name_id_mapping_html = name_id_mapping.to_html(classes='dataframe', index=False)
    
    return render_template('products.html', df_html=name_id_mapping_html)

@app.route('/users')
def users():
    users_html = user_history[['user_id']].drop_duplicates().sort_values('user_id').to_html(classes='dataframe', index=False)
    return render_template('users.html', df_html=users_html)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)