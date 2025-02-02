
# ETL Pipeline

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shiljatbl/shifts-etl.git
```
Navigate to the project root folder
```bash
cd shifts-etl
```
### 2. Build and run the Docker container

```bash
docker-compose up -d
```

### 3. Set Up Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  .\venv\Scripts\activate
  ```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```


### 5. Run the ETL Pipeline

```bash
python etl/main.py
```


# ETL Pipeline Approach

## Overview
The ETL (Extract, Transform, Load) pipeline is designed to:

- Extract shift data from a paginated REST API.
- Transform the raw data by calculating derived fields and extracting nested models.
- Load the transformed data into a PostgreSQL database.
- Calculate KPIs based on the loaded data and store them in the `kpis` table.

The pipeline is implemented in Python and uses Docker to set up the Shift API and PostgreSQL database locally.
Database credentials are located in the config.py file.

---

## 1. Extract
The pipeline fetches shift data from the Shift API, which exposes paginated data for the past year.

- The `fetch_shifts` function handles pagination by iterating through all pages until no more data is available.
- The API response is parsed into a list of shifts, each containing nested models for breaks, allowances, and award interpretations.

---

## 2. Transform
The raw shift data is transformed to:

- Calculate the total shift cost by summing the costs of allowances and award interpretations.
- Extract nested models (breaks, allowances, and award interpretations) into separate lists for loading into their respective tables.
- Ensure all IDs are preserved and all records are processed.

---

## 3. Load
The transformed data is loaded into the following PostgreSQL tables:

- **`shifts`**: Contains shift details (ID, date, start, finish, cost).
- **`breaks`**: Contains break details (ID, shift ID, start, finish, is_paid).
- **`allowances`**: Contains allowance details (ID, shift ID, value, cost).
- **`award_interpretations`**: Contains award details (ID, shift ID, date, units, cost).

The functions `insert_shifts`, `insert_breaks`, `insert_allowances`, and `insert_awards` handle data insertion into the respective tables.

Primary key constraints ensure that duplicate records are not inserted.

---

## 4. Calculate KPIs
The pipeline calculates the following KPIs and stores them in the `kpis` table:

- **Mean break length in minutes**: Average length of breaks for the day.
- **Mean shift cost**: Average cost of shifts for the day.
- **Max allowance cost in the last 14 days**: Maximum allowance cost in the past 14 days.
- **Max break-free shift period in days**: Longest period (in days) without breaks.
- **Min shift length in hours**: Shortest shift duration for the day.
- **Total number of paid breaks**: Total number of paid breaks for the day.

The `calculate_and_insert_kpis` function computes these KPIs and inserts them into the `kpis` table, updating existing records if necessary.

---

## 5. Error Handling
The pipeline includes basic error handling for:

- API connection issues.
- Database connection issues.
- Data transformation and insertion errors.

Errors are logged to the console for debugging.

---

## 6. Deployment
The pipeline is designed to run locally using Docker Compose.

- The `docker-compose.yml` file sets up the Shift API and PostgreSQL database.

---

## 7. Cleanup
To stop and remove Docker containers, run:

```bash
docker-compose down
```

