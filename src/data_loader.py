import pandas as pd
from datetime import datetime
from backend.operations import run_operations, insert_business, verify_business_insertion, get_business_id, save_price
from src.yahoo_finance import get_action_name
from src.config import connect_bd

def load_excel(file_path):
    # Leer el archivo Excel
    df = pd.read_excel(file_path, engine='openpyxl')
    
    # Verificar que la primera columna tenga el nombre correcto
    if df.columns[0] != 'Fecha':
        raise ValueError("El archivo Excel debe tener 'Fecha' en A1")
    
    # Obtener el ticker de la segunda columna
    ticker = df.columns[1]
    
    # Obtener el nombre de la empresa usando get_action_name
    business_name = get_action_name(ticker)
    
    # Conectar a la base de datos
    engine = connect_bd()
    
    with engine.begin() as conn:
        # Insertar la empresa en la base de datos si no existe
        insert_business(ticker, business_name, conn)
        if verify_business_insertion(ticker, conn):
            business_id = get_business_id(ticker, conn)
            if business_id:
                # Convertir las fechas al formato YYYY-MM-DD
                df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')
                
                # Procesar los datos y guardar los precios en la base de datos
                for index, row in df.iterrows():
                    if index == 0:
                        continue
                    date = row['Fecha']
                    price = row[ticker]
                    save_price(pd.DataFrame({'date': [date], 'closing_price': [price]}), business_id, conn)
                print("Datos guardados correctamente.")
            else:
                print("No se pudo obtener el ID de la empresa.")
        else:
            print("No se pudo insertar la empresa.")

if __name__ == "__main__":
    file_path = 'data/precios.xlsx'  # Reemplaza esto con la ruta a tu archivo Excel
    load_excel(file_path)