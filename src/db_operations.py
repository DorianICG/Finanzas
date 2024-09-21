from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text


def insert_business(ticker, business_name, conn):
    insert_query = text(
        """
      INSERT INTO business (ticker, business_name)
      VALUES (UPPER(:ticker), :business_name)
      ON CONFLICT (ticker) DO NOTHING;
    """
    )

    try:
        conn.execute(insert_query, {"ticker": ticker, "business_name": business_name})
        print(f"Intento de inserción: ticker={ticker}, business_name={business_name}")
    except SQLAlchemyError as e:
        print(f"Error inserting business: {e}")


def get_business_id(ticker, conn):
    select_query = text("SELECT id FROM business WHERE ticker = :ticker;")

    try:
        result = conn.execute(select_query, {"ticker": ticker})
        business_id = result.fetchone()
        if business_id:
            return business_id[0]
        else:
            print(f"Error: No se encontró el business_id para el ticker {ticker}")
            return None
    except SQLAlchemyError as e:
        print(f"Error retrieving business_id: {e}")
        return None


def save_price(df, business_id, conn):
    df = (
        df.copy()
    )  
    df["business_id"] = business_id
    df = df[
        ["date", "closing_price", "business_id"]
    ]  
    try:
        df.to_sql("price", conn, if_exists="replace", index=False)
    except SQLAlchemyError as e:
        print(f"Error saving price data: {e}")


def list_businesses(conn):
    query = text("SELECT ticker FROM business;")
    try:
        result = conn.execute(query)
        businesses = [row[0] for row in result]
        return businesses
    except SQLAlchemyError as e:
        print(f"Error listing businesses: {e}")
        return []


def add_ticker(conn, ticker):
    query = text(
        """
    INSERT INTO business (ticker)
    VALUES (:ticker)
    ON CONFLICT (ticker) DO NOTHING;
    """
    )
    try:
        conn.execute(query, {"ticker": ticker})
    except SQLAlchemyError as e:
        print(f"Error adding ticker: {e}")


def verify_business_insertion(ticker, conn):
    business_id = get_business_id(ticker, conn)
    if business_id:
        print(
            f"Empresa con ticker {ticker} se ha insertado correctamente con ID {business_id}."
        )
        return True
    else:
        print(f"Error: Empresa con ticker {ticker} no se ha insertado correctamente.")
        return False
