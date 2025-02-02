
# KPI Calculation and Insertion

This Python project calculates KPIs related to employee shifts, breaks, and allowances and inserts them into a PostgreSQL database.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shiljatbl/shifts-etl.git
cd shifts-etl
```

### 2. Build and run the Docker container

```bash
docker-compose up --build
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

