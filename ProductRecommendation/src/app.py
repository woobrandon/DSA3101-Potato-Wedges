from flask import Flask, render_template, url_for
import pandas as pd
import numpy as np
import seaborn as sns
import warnings
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
warnings.filterwarnings("ignore")


### Product Recommendation
product_df = pd.read_csv("../data/product_df.csv")
product_df['vector'] = product_df['vector'].apply(lambda x: np.fromstring(x, sep=',') if isinstance(x, str) else x)
associated_items = pd.read_csv("../data/crosssell.csv")
user_history = pd.read_csv("../data/user_history.csv", dtype = {'user_id':'str', 'product_id':'str'})
id_name_df = pd.read_csv("../data/id_name_df.csv")

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

@app.route('/users')
def users():
    users_html = user_history[['user_id']].drop_duplicates().sort_values('user_id').to_html(classes='dataframe', index=False)
    return render_template('users.html', df_html=users_html)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)