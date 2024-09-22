import pandas as pd
import numpy as np
import statistics 

# Variable global para almacenar los datos
price_data = {}


def save_price(df, ticker):
    global price_data
    df = df.copy()
    df = df[["date", "closing_price"]]
    print(df)
    try:
        if ticker in price_data:
            combined_df = pd.concat([price_data[ticker], df])
            combined_df = combined_df.drop_duplicates(subset="date", keep="last")
        else:
            combined_df = df

        # Ordenar por fecha de la más antigua a la más reciente
        combined_df = combined_df.sort_values(by="date", ascending=True)

        # Obtener el rango de fechas del DataFrame
        start_date = combined_df["date"].min()
        end_date = combined_df["date"].max()

        # Crear un rango completo de fechas
        all_dates = pd.date_range(start=start_date, end=end_date, freq="D")

        # Reindexar el DataFrame para incluir todas las fechas en el rango
        combined_df = (
            combined_df.set_index("date")
            .reindex(all_dates)
            .rename_axis("date")
            .reset_index()
        )

        # Rellenar los valores faltantes con el precio de cierre de la fecha anterior
        combined_df["closing_price"] = combined_df["closing_price"].ffill()

        price_data[ticker] = combined_df

        print(f"Datos guardados correctamente para el ticker {ticker}.")
        print(f"Total de datos: {len(price_data[ticker])}")
    except Exception as e:
        print(f"Error saving price data for {ticker}: {e}")


def show_price_data(ticker):
    global price_data
    if ticker in price_data:
        print(price_data[ticker])
    else:
        print(f"No hay datos disponibles para el ticker {ticker}.")


def calculate_log(ticker=None, start_date=None, end_date=None):
    global price_data
    try:
        if ticker:
            df = price_data.get(ticker)
            if df is None:
                return f"No hay datos disponibles para el ticker {ticker}."
            if start_date and end_date:
                # Convertir start_date y end_date a tipo datetime
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
        else:
            df = pd.concat(price_data.values())

        # Crear un arreglo para almacenar los log returns
        log_returns = []

        # Calcular los log returns
        for i in range(1, len(df)):
            log_return = np.log(
                df["closing_price"].iloc[i] / df["closing_price"].iloc[i - 1]
            )
            log_returns.append(log_return)

        print(f"Retornos logarítmicos calculados para el ticker {ticker}. con un total de {len(log_returns)} retornos.")
        return log_returns
    except Exception as e:
        return f"Error al calcular los retornos logarítmicos: {e}"


def calculate_media_variations(rendimientos):
    try:
        variations = [r ** 2 for r in rendimientos]
        return variations
    except Exception as e:
        return f"Error al calcular las variaciones de media: {e}"


def calculate_media_cero(variaciones):
    try:
        suma_variaciones = sum(variaciones)
        total_variaciones = len(variaciones)
        media_cero = np.sqrt(suma_variaciones / total_variaciones)
        return media_cero
    except Exception as e:
        return f"Error al calcular la media cero: {e}"
    


def calculate_all(ticker=None, start_date=None, end_date=None):
    rendimientos = calculate_log(ticker, start_date, end_date)
    historica = statistics.pstdev(rendimientos)
    variaciones = calculate_media_variations(rendimientos)
    media_cero = calculate_media_cero(variaciones)


    rendimientos_porcentaje = [round(r * 100, 3) for r in rendimientos]
    historica_porcentaje = round(historica * 100, 3)
    variaciones_porcentaje = [round(v * 100, 3) for v in variaciones]
    media_cero_porcentaje = round(media_cero * 100, 3)

    return rendimientos_porcentaje, historica_porcentaje, variaciones_porcentaje, media_cero_porcentaje