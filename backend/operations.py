from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from src.config import connect_bd
from src.yahoo_finance import get_yahoo_data, get_action_name
from src.db_operations import insert_business, get_business_id, save_price, verify_business_insertion, list_businesses

def run_operations(ticker, start_date, end_date):
    engine = connect_bd()
    df_yahoo = get_yahoo_data(ticker, start_date, end_date)
    business_name = get_action_name(ticker)
    
    with engine.begin() as conn:
        insert_business(ticker, business_name, conn)
        if verify_business_insertion(ticker, conn):
            business_id = get_business_id(ticker, conn)
            if business_id:
                df_yahoo.reset_index(inplace=True)
                df_yahoo = df_yahoo[['Date', 'Close']]
                print(df_yahoo)
                df_yahoo.columns = ['date', 'closing_price']
                save_price(df_yahoo, business_id, conn)
                return "Datos guardados correctamente."
            else:
                return "No se pudo obtener el ID de la empresa."
        else:
            return "No se pudo insertar la empresa."

def update_operations(ticker):
    engine = connect_bd()
    
    with engine.begin() as conn:
        business_id = get_business_id(ticker, conn)
        if business_id:
            query = text("SELECT MAX(date) FROM price WHERE business_id = :business_id;")
            result = conn.execute(query, {'business_id': business_id})
            last_date = result.fetchone()[0]
            if last_date:
                start_date = last_date + timedelta(days=1)
                end_date = datetime.now().strftime('%Y-%m-%d')
                df_yahoo = get_yahoo_data(ticker, start_date, end_date)
                df_yahoo.reset_index(inplace=True)
                df_yahoo = df_yahoo[['Date', 'Close']]
                df_yahoo.columns = ['date', 'closing_price']
                save_price(df_yahoo, business_id, conn)
                return "Datos actualizados correctamente."
            else:
                return "No se encontraron datos para actualizar."
        else:
            return "No se pudo obtener el ID de la empresa."

def show_all_businesses():
    engine = connect_bd()
    with engine.begin() as conn:
        businesses = list_businesses(conn)
        return businesses
