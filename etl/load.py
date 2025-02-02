import psycopg2
from psycopg2 import sql
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def connect_to_db():
    """
    Establishes a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def insert_shifts(shifts):
    """
    Inserts shift data into the `shifts` table, skipping existing records.
    """
    conn = connect_to_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        for shift in shifts:
            cur.execute("SELECT 1 FROM shifts WHERE shift_id = %s", (shift['id'],))
            if cur.fetchone():
                continue  # Skip existing shift
            cur.execute(
                sql.SQL("""
                    INSERT INTO shifts (shift_id, shift_date, shift_start, shift_finish, shift_cost)
                    VALUES (%s, %s, %s, %s, %s)
                """),
                (shift['id'], shift['date'], shift['start'], shift['finish'], shift['cost'])
            )
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error inserting shifts: {e}")
    finally:
        cur.close()
        conn.close()

def insert_breaks(breaks):
    """
    Inserts break data into the `breaks` table, skipping existing records.
    """
    conn = connect_to_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        for break_ in breaks:
            cur.execute("SELECT 1 FROM breaks WHERE break_id = %s", (break_['id'],))
            if cur.fetchone():
                continue  # Skip existing break
            cur.execute(
                sql.SQL("""
                    INSERT INTO breaks (break_id, shift_id, break_start, break_finish, is_paid)
                    VALUES (%s, %s, %s, %s, %s)
                """),
                (break_['id'], break_['shift_id'], break_['start'], break_['finish'], break_['is_paid'])
            )
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error inserting breaks: {e}")
    finally:
        cur.close()
        conn.close()

def insert_allowances(allowances):
    """
    Inserts allowance data into the `allowances` table, skipping existing records.
    """
    conn = connect_to_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        for allowance in allowances:
            cur.execute("SELECT 1 FROM allowances WHERE allowance_id = %s", (allowance['id'],))
            if cur.fetchone():
                continue  # Skip existing allowance
            cur.execute(
                sql.SQL("""
                    INSERT INTO allowances (allowance_id, shift_id, allowance_value, allowance_cost)
                    VALUES (%s, %s, %s, %s)
                """),
                (allowance['id'], allowance['shift_id'], allowance['allowance_value'], allowance['allowance_cost'])
            )
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error inserting allowances: {e}")
    finally:
        cur.close()
        conn.close()

def insert_awards(awards):
    """
    Inserts award interpretation data into the `award_interpretations` table, skipping existing records.
    """
    conn = connect_to_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        for award in awards:
            cur.execute("SELECT 1 FROM award_interpretations WHERE award_id = %s", (award['id'],))
            if cur.fetchone():
                continue  # Skip existing award
            cur.execute(
                sql.SQL("""
                    INSERT INTO award_interpretations (award_id, shift_id, award_date, award_units, award_cost)
                    VALUES (%s, %s, %s, %s, %s)
                """),
                (award['id'], award['shift_id'], award['award_date'], award['award_units'], award['award_cost'])
            )
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error inserting award interpretations: {e}")
    finally:
        cur.close()
        conn.close()
