from extract import fetch_shifts
from transform import calculate_shift_cost, extract_models
from load import insert_shifts, insert_breaks, insert_allowances, insert_awards
from kpis import calculate_and_insert_kpis

def run_etl():
    """
    Runs the ETL pipeline.
    """
    # Step 1: Extract
    print("Fetching shifts from API...")
    shifts = fetch_shifts()

    # Step 2: Transform
    print("Transforming data...")
    shifts = calculate_shift_cost(shifts)
    breaks, allowances, awards = extract_models(shifts)

    # Step 3: Load
    print("Loading data into the database...")
    insert_shifts(shifts)
    insert_breaks(breaks)
    insert_allowances(allowances)
    insert_awards(awards)

    # Step 4: Calculate KPIs
    print("Calculating KPIs...")
    calculate_and_insert_kpis()

    print("ETL pipeline completed successfully!")

if __name__ == "__main__":
    run_etl()