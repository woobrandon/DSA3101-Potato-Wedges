from flask import Flask, render_template, url_for
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import warnings
import threading
warnings.filterwarnings("ignore")

historical_data = pd.read_csv("../data/train_true.csv")
forecast_data = pd.read_csv("../data/test_predictions.csv")
historical_data['year_month'] = pd.to_datetime(historical_data['year_month'])
forecast_data['year_month'] = pd.to_datetime(forecast_data['year_month'])

all_months = ['Jul 2016', 'Aug 2016', 'Sep 2016', 'Oct 2016', 'Nov 2016', 'Dec 2016', 'Jan 2017', 'Feb 2017', 'Mar 2017', 'Apr 2017', 'May 2017', 'Jun 2017', 'Jul 2017']

def plot_graph(id, price):

    plt.switch_backend('Agg')

    past = historical_data.loc[(historical_data['product_id'] == id) & (historical_data['product_price'] == price)]
    forecast = forecast_data.loc[(forecast_data['product_id'] == id) & (forecast_data['product_price'] == price)]
    name = forecast['product_name'].unique()
    forecast.rename({"forecast_qty":'qty'}, axis = 1, inplace = True)
    past.rename({"present_total_qty":'qty'}, axis = 1, inplace = True)
    trend_df = pd.concat([past, forecast])
    trend_df['ym'] = trend_df['year_month'].dt.strftime('%b %Y')

    plt.figure(figsize=(10, 6))
    ax = sns.lineplot(data=trend_df, x='ym', y='qty', errorbar=None)
    x_last = trend_df['ym'].values[-2:]
    y_last = trend_df['qty'].values[-2:]
    ax.plot(x_last, y_last, linestyle=':', color='white', label = 'Predicted')  # Use a different color if desired
    legend_elements = [
        Line2D([0], [0], color='blue', label='Historical Data'),  # Color matches the main line
        Line2D([0], [0], color='blue', linestyle=':', label='Prediction')  # Dotted line
    ]
    ax.legend(handles=legend_elements)
    plt.xticks(rotation=45)
    plt.xlabel('Month')
    plt.ylabel('Sales quantity')
    plt.title(f'Sales trend and forecast for {name[0]}')
    
    image_path = f"static/images/test.png"
    plt.savefig(image_path, dpi = 300)
    plt.close()

    return f'images/test.png'

from flask import Flask, render_template, request
import pandas as pd
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_path = None

    if request.method == "POST":
        input_text = request.form["input_text"] 
        id = input_text.split(",")[0].strip()
        price = float(input_text.split(",")[1].strip())

        try:
            forecast_qty = forecast_data.loc[(forecast_data['product_id'] == id) & (forecast_data['product_price'] == price), 'forecast_qty'].values[0].astype(int)
            image_path = plot_graph(id, price)
            result = f"Forecasted demand for product {id} at price {price} is {forecast_qty} units."
        except IndexError:
            result = f"No data found for product ID {id} at price {price}."

    return render_template("index.html", result=result, image_path=image_path)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5001)