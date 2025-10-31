# AI-driven Risk & ESG Compliance Analyzer

Intern project for HSBC Risk Compliance team. Combines ESG and financial data with ML for risk analysis.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Place raw CSVs in `data/raw/`.
3. Run `python/scripts/create_db.py` to create SQLite DB (if not exists).
4. Run SQL scripts in VS Code SQLite extension: schema.sql then etl.sql.
5. Run notebooks: data_cleaning.ipynb (loads/merges data), model_training.ipynb (trains model).
6. Launch dashboard: `streamlit run dashboard/app.py`

## Notes
- Uses SQLite for simplicity.
- Merged data: Inner join on Symbol (~100 companies).
- For PostgreSQL, update engines accordingly.