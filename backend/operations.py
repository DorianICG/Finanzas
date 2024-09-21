import pandas as pd

# Variable global para almacenar los datos
price_data = {}


def save_price(df, ticker):
    global price_data
    df = df.copy()
    df = df[["date", "closing_price"]]
    try:
        if ticker in price_data:
            price_data[ticker] = pd.concat([price_data[ticker], df])
        else:
            price_data[ticker] = df
        print(f"Datos guardados correctamente para el ticker {ticker}.")
    except Exception as e:
        print(f"Error saving price data for {ticker}: {e}")


def show_price_data(ticker):
    global price_data
    if ticker in price_data:
        print(price_data[ticker])
    else:
        print(f"No hay datos disponibles para el ticker {ticker}.")
