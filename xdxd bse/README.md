# Stock Price Forecast Desktop App (BSE Supported)

This is a desktop application that:
- Fetches historical stock data using `yfinance`
- Trains a Linear Regression model
- Forecasts the next 7 days of stock prices
- Plots historical and forecasted data
- Supports BSE stock symbols (e.g., `RELIANCE.BO`, `TCS.BO`)

## 🛠 Requirements
```
pip install yfinance numpy pandas scikit-learn matplotlib
```

## 🚀 Running the App
```
python stock_forecast_gui.py
```

## 📌 Note
For BSE stocks, use the `.BO` suffix (e.g., `RELIANCE.BO`, `INFY.BO`).
