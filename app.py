from flask import Flask, render_template, request, redirect,url_for, flash
from bokeh.plotting import figure, output_file, show
import requests
import pandas as pd
    
app = Flask(__name__)
app.debug = True


@app.route('/index', methods=('GET', 'POST'))
@app.route('/', methods=('GET', 'POST'))
def index():   
    if request.method == 'POST':
        ticker = request.form['ticker']
        if not ticker:
            flash('Ticker is required!')
        else:           
            plot_api(ticker)
            return redirect('/line')
                    
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/line')
def line():
    return render_template('line.html')


def plot_api(ticker):
    key = '0PWT5UI5CZ6GN1XQ'
    ticker = ticker
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key)
    response = requests.get(url)
    j = response.json()["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(j).T    
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    output_file("templates/line.html")
    p = figure(plot_width=800, plot_height=600, x_axis_type="datetime", x_axis_label="Date", y_axis_label="Price", title='Daily Closing Stock Price')
    # add a line renderer
    p.line(df.index, df['4. close'].astype(float), line_width=2)
    show(p)
    return 0


if __name__ == '__main__':
    app.run()
