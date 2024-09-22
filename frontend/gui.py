import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
from backend.operations import save_price, show_price_data, calculate_all
import pandas as pd
import yfinance as yf


def on_submit():
    ticker = ticker_entry.get()
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()

    # Obtener datos de Yahoo Finance
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        data.reset_index(inplace=True)
        data = data.rename(columns={"Date": "date", "Close": "closing_price"})
        df = data[["date", "closing_price"]]

        save_price(df, ticker)
        messagebox.showinfo("Información", f"Datos guardados para el ticker {ticker}")
    except Exception as e:
        messagebox.showerror(
            "Error", f"No se pudieron obtener los datos para el ticker {ticker}: {e}"
        )


def on_show():
    ticker = ticker_entry.get()
    show_price_data(ticker)


def load_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if not file_path:
        return

    try:
        excel_data = pd.read_excel(file_path, header=None)
        col = 0
        while col < excel_data.shape[1]:
            if excel_data.iloc[0, col] == "Fecha" and excel_data.iloc[0, col + 1] != "":
                ticker = excel_data.iloc[0, col + 1]
                dates = pd.to_datetime(excel_data.iloc[1:, col], format="%d.%m.%Y")
                prices = excel_data.iloc[1:, col + 1].astype(float)
                df = pd.DataFrame({"date": dates, "closing_price": prices})
                save_price(df, ticker)
                col += 2
            else:
                col += 1
        messagebox.showinfo("Información", "Datos cargados desde el archivo Excel")
    except Exception as e:
        messagebox.showerror(
            "Error", f"No se pudieron cargar los datos desde el archivo Excel: {e}"
        )


def calculate():
    ticker = ticker_entry.get()
    if ticker.lower() == "todos":
        result = calculate_all()
    else:
        start_date = start_date_entry.get_date()
        end_date = end_date_entry.get_date()
        result = calculate_all(ticker, start_date, end_date)

    if result:
        rendimientos, historica, variaciones, media_cero = result
        message = (
            f"La volatilidad histórica es: {historica}\n"
            f"La media cero de los retornos es: {media_cero}"
        )
        messagebox.showinfo("Resultado", message)
    else:
        messagebox.showerror(
            "Error", "No se pudieron calcular los datos."
        )


def create_gui():
    global ticker_entry, start_date_entry, end_date_entry

    root = tk.Tk()
    root.title("Gestor de Finanzas")

    tk.Label(root, text="Ticker:").grid(row=0, column=0)
    ticker_entry = tk.Entry(root)
    ticker_entry.grid(row=0, column=1)

    tk.Label(root, text="Fecha de inicio:").grid(row=1, column=0)
    start_date_entry = DateEntry(root)
    start_date_entry.grid(row=1, column=1)

    tk.Label(root, text="Fecha de fin:").grid(row=2, column=0)
    end_date_entry = DateEntry(root)
    end_date_entry.grid(row=2, column=1)

    submit_button = tk.Button(root, text="Guardar Datos", command=on_submit)
    submit_button.grid(row=3, column=0, columnspan=2)

    show_button = tk.Button(root, text="Mostrar Datos", command=on_show)
    show_button.grid(row=4, column=0, columnspan=2)

    load_button = tk.Button(root, text="Cargar desde Excel", command=load_excel)
    load_button.grid(row=5, column=0, columnspan=2)
    
    calculate_button = tk.Button(root, text="Calcular Todo", command=calculate)
    calculate_button.grid(row=6, column=0, columnspan=2)

    root.mainloop()
