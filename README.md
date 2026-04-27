# MarTech-dashboard

MarTech dashboard demo built with Streamlit. It reads CSV files from `data/` and provides bilingual (zh-TW / EN) KPI views for revenue, customer, product, store, and discount analysis.

## Features

- Global filters: date range, country, city, store type, brand, category, and loyalty status.
- KPI cards: revenue, profit, margin rate, orders, active customers, AOV, and average discount.
- Thematic tabs:
	- Overview (revenue/profit trends, member contribution)
	- Customer (new vs existing cohort, age distribution)
	- Product & Brand (brand and category performance, cocoa vs margin)
	- Store Channel (country/store type/city performance)
	- Discount Impact (discount buckets and margin relation)
- Data quality panel: row count, date coverage, and null-column checks.

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── data/
│   ├── calendar.csv
│   ├── customers.csv
│   ├── products.csv
│   ├── sales.csv
│   └── stores.csv
└── README.md
```

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

4. Open the local URL shown in terminal (usually `http://localhost:8501`).

## Notes

- `sales.csv` is large, so loading may take longer on first run.
- The app uses Streamlit cache to speed up repeated interactions.
- Default language is zh-TW; switch in the sidebar.

