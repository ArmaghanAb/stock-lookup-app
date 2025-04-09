from flask import Flask, request, render_template
import yfinance as yf
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_info = None
    error = None

    if request.method == 'POST':
        symbol = request.form['symbol'].upper()

        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            if 'longName' not in info:
                raise ValueError("Invalid stock symbol")

            stock_info = {
                'datetime': datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Z %Y'),
                'name': f"{info['longName']} ({symbol})",
                'price': info['regularMarketPrice'],
                'change': info['regularMarketChange'],
                'percent': info['regularMarketChangePercent']
            }
        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template('index.html', stock_info=stock_info, error=error)

if __name__ == '__main__':
    app.run(debug=True)
