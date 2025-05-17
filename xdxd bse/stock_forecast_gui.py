
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fetch_and_forecast(ticker):
    try:
        df = yf.download(ticker, period='5y', interval='1d')
        if df.empty:
            raise Exception("No data fetched. Invalid ticker or network issue.")
        df = df[['Close']].dropna()

        scaler = MinMaxScaler()
        df['Scaled_Close'] = scaler.fit_transform(df[['Close']])

        window_size = 60
        X, y = [], []
        for i in range(window_size, len(df)):
            X.append(df['Scaled_Close'].iloc[i - window_size:i].values)
            y.append(df['Scaled_Close'].iloc[i])
        X, y = np.array(X), np.array(y)

        model = LinearRegression()
        model.fit(X, y)

        last_sequence = df['Scaled_Close'].iloc[-window_size:].values.reshape(1, -1)
        forecast_scaled = []
        for _ in range(7):
            next_pred = model.predict(last_sequence)[0]
            forecast_scaled.append(next_pred)
            last_sequence = np.append(last_sequence[:, 1:], [[next_pred]], axis=1)

        forecast = scaler.inverse_transform(np.array(forecast_scaled).reshape(-1, 1)).flatten()
        last_date = df.index[-1]
        forecast_dates = [last_date + timedelta(days=i + 1) for i in range(7)]

        return df, forecast_dates, forecast
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None, None, None

def plot_forecast(df, forecast_dates, forecast, root_frame):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index[-100:], df['Close'].iloc[-100:], label='Historical')
    ax.plot(forecast_dates, forecast, 'ro--', label='Forecast')
    ax.set_title('7-Day Forecast')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=root_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    explanation = tk.Label(root_frame, text="This chart shows the historical and next 7-day forecasted closing prices.\n"
                                            "Make sure to use '.BO' for BSE stocks (e.g., RELIANCE.BO).",
                                            font=("Arial", 10), fg="gray")
    explanation.pack(pady=5)

def on_forecast():
    ticker = entry.get().upper().strip()
    if not ticker:
        messagebox.showwarning("Input Error", "Please enter a stock ticker.")
        return
    df, dates, forecast = fetch_and_forecast(ticker)
    if df is not None:
        for widget in plot_frame.winfo_children():
            widget.destroy()
        plot_forecast(df, dates, forecast, plot_frame)

# GUI Setup
root = tk.Tk()
root.title("Stock Price Forecast App (BSE Supported)")
root.geometry("950x600")

tk.Label(root, text="Enter Stock Ticker Symbol (e.g., RELIANCE.BO for BSE, AAPL for US):", font=('Arial', 12)).pack(pady=10)
entry = tk.Entry(root, font=('Arial', 12), width=30)
entry.pack(pady=5)

tk.Button(root, text="Forecast Next 7 Days", font=('Arial', 12), command=on_forecast).pack(pady=10)

plot_frame = tk.Frame(root)
plot_frame.pack(fill="both", expand=True)

root.mainloop()
