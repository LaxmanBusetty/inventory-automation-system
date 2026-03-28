# eCommerce Inventory Automation System

A Python-based inventory automation project tailored for Data & Automation / Python roles. This project simulates a real-world eCommerce workflow: ingesting inventory data, analyzing stock health with Pandas, generating restock recommendations, exposing results through a FastAPI service, and exporting CSV reports for business teams.

## Why this project is useful

This project demonstrates:
- Python for business automation
- Pandas and NumPy for inventory analysis
- REST API development with FastAPI
- Data pipeline design and report generation
- Clean project structure suitable for GitHub and interviews

## Features

- Load product inventory from CSV
- Analyze stock levels, sales velocity, days of cover, and reorder urgency
- Generate restocking recommendations automatically
- Expose results through FastAPI endpoints
- Export restock reports to CSV
- Mock external API sync for inventory updates
- Unit tests for core business logic

## Project structure

```text
inventory_automation/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── services/
│   │   ├── inventory_service.py
│   │   ├── mock_supplier_api.py
│   │   └── report_service.py
│   ├── __init__.py
│   └── main.py
├── data/
│   └── inventory_sample.csv
├── reports/
├── tests/
│   └── test_inventory_service.py
├── .env.example
├── requirements.txt
└── README.md
```

## Business logic

For each SKU, the pipeline calculates:
- `daily_sales_avg`: estimated average daily sales
- `days_of_cover`: current_stock / daily_sales_avg
- `reorder_point`: lead_time_days * daily_sales_avg + safety_stock
- `recommended_reorder_qty`: max(target_stock_days * daily_sales_avg - current_stock, 0)
- `priority`: Critical / High / Medium / Low

### Priority rules
- **Critical**: stock is zero or negative
- **High**: days of cover <= lead time
- **Medium**: days of cover <= lead time + 3 days
- **Low**: otherwise

## Quickstart

### 1) Clone and create a virtual environment

```bash
git clone <your-repo-url>
cd reli_inventory_automation
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the API

```bash
uvicorn app.main:app --reload
```

API docs:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints

### Health check
```http
GET /health
```

### View raw inventory
```http
GET /inventory
```

### Analyze inventory and get restock recommendations
```http
GET /inventory/analyze
```

### Export report to CSV
```http
POST /inventory/export-report
```

### Simulate supplier sync / stock update
```http
POST /inventory/sync-supplier
```

## Example output fields

```json
{
  "sku": "SKU-1001",
  "product_name": "Wireless Mouse",
  "current_stock": 14,
  "daily_sales_avg": 6.5,
  "days_of_cover": 2.15,
  "reorder_point": 34.5,
  "recommended_reorder_qty": 116,
  "priority": "High"
}
```

## Run the pipeline manually

You can also use the service classes directly in Python.

```python
from app.services.inventory_service import InventoryAnalyzer

analyzer = InventoryAnalyzer("data/inventory_sample.csv")
raw_df = analyzer.load_inventory()
analysis_df = analyzer.analyze_inventory(raw_df)
print(analysis_df.head())
```

## Run tests

```bash
pytest -q
```

## Interview talking points

You can present this project as:
- A Python automation system for inventory decision support
- A data pipeline that converts raw inventory and sales data into operational recommendations
- An API-ready service that could plug into Amazon, Shopify, Walmart, or ERP workflows

## Ideas for extension

- Add a scheduler with cron or Airflow
- Connect to a real marketplace API
- Store inventory snapshots in PostgreSQL
- Add email or Slack alerts for critical stockouts
- Build a Streamlit dashboard for operations teams

## Resume bullet you can use

Built a Python-based inventory automation system using Pandas, NumPy, and FastAPI to analyze stock health, generate reorder recommendations, and export business-ready reports through API-driven workflows.
