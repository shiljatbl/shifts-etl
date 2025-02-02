from datetime import datetime, timedelta
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

def calculate_and_insert_kpis():
    """
    Calculates KPIs and inserts them into the `kpis` table.
    """
    conn = connect_to_db()
    if not conn:
        return
    cur = conn.cursor()

    try:
        today = datetime.utcnow().date()

        # 1. Mean break length in minutes (removed date filter)
        cur.execute("""
            INSERT INTO kpis (kpi_name, kpi_date, kpi_value)
            SELECT 'mean_break_length_in_minutes', %s, 
                COALESCE(
                    AVG(EXTRACT(EPOCH FROM (b.break_finish - b.break_start)) / 60), 
                    0
                )
            FROM breaks b
            WHERE b.break_finish IS NOT NULL
            AND b.break_start IS NOT NULL
            ON CONFLICT (kpi_name, kpi_date) DO UPDATE
            SET kpi_value = EXCLUDED.kpi_value;
        """, (today,))

        # 2. Mean shift cost (removed date filter)
        cur.execute("""
            INSERT INTO kpis (kpi_name, kpi_date, kpi_value)
            SELECT 'mean_shift_cost', %s, COALESCE(AVG(s.shift_cost), 0)
            FROM shifts s
            WHERE s.shift_cost IS NOT NULL
            ON CONFLICT (kpi_name, kpi_date) DO UPDATE
            SET kpi_value = EXCLUDED.kpi_value;
        """, (today,))

        # 3. Max allowance cost in the last 14 days (removed specific date filter)
        cur.execute("""
            INSERT INTO kpis (kpi_name, kpi_date, kpi_value)
            SELECT 'max_allowance_cost_14d', %s, COALESCE(MAX(a.allowance_cost), 0)
            FROM allowances a
            JOIN shifts s ON s.shift_id = a.shift_id
            WHERE s.shift_date BETWEEN %s AND %s
            ON CONFLICT (kpi_name, kpi_date) DO UPDATE
            SET kpi_value = EXCLUDED.kpi_value;
        """, (today, today - timedelta(days=14), today))

        # 4. Max break-free shift period in days (removed date filter)
        cur.execute("""
            WITH break_free_periods AS (
                SELECT shift_date::timestamp,  -- Cast to timestamp
                    LAG(shift_date::timestamp) OVER (ORDER BY shift_date) AS prev_shift_date
                FROM shifts
                WHERE shift_id NOT IN (SELECT DISTINCT shift_id FROM breaks)
            )
            INSERT INTO kpis (kpi_name, kpi_date, kpi_value)
            SELECT 'max_break_free_shift_period_in_days', %s, 
                COALESCE(MAX(EXTRACT(EPOCH FROM (shift_date - prev_shift_date)) / 86400), 0)
            FROM break_free_periods
            ON CONFLICT (kpi_name, kpi_date) DO UPDATE
            SET kpi_value = EXCLUDED.kpi_value;
        """, (today,))

        # 5. Min shift length in hours (removed date filter)
        cur.execute("""
            INSERT INTO kpis (kpi_name, kpi_date, kpi_value)
            SELECT 'min_shift_length_in_hours', %s, COALESCE(MIN(EXTRACT(EPOCH FROM (s.shift_finish - s.shift_start)) / 3600), 0)
            FROM shifts s
            WHERE s.shift_start IS NOT NULL AND s.shift_finish IS NOT NULL
            ON CONFLICT (kpi_name, kpi_date) DO UPDATE
            SET kpi_value = EXCLUDED.kpi_value;
        """, (today,))

        # 6. Total number of paid breaks (removed date filter)
        cur.execute("""
            INSERT INTO kpis (kpi_name, kpi_date, kpi_value)
            SELECT 'total_number_of_paid_breaks', %s, COALESCE(COUNT(*), 0)
            FROM breaks b
            JOIN shifts s ON s.shift_id = b.shift_id
            WHERE b.is_paid = TRUE
            ON CONFLICT (kpi_name, kpi_date) DO UPDATE
            SET kpi_value = EXCLUDED.kpi_value;
        """, (today,))

        conn.commit()
    except psycopg2.Error as e:
        print(f"Error calculating or inserting KPIs: {e}")
    finally:
        cur.close()
        conn.close()
