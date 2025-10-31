import pandas as pd
from sqlalchemy import create_engine

# SQLite engine
engine = create_engine('sqlite:///../../hsbc_risk_esg.db')

# Pull from merged view
df = pd.read_sql('SELECT * FROM merged_data_view', engine)

# Additional processing: Normalize ESG score
df['esg_score_normalized'] = (df['esg_score'] - df['esg_score'].min()) / (df['esg_score'].max() - df['esg_score'].min())

# Save for quick dashboard load
df.to_pickle('../../data/processed/pipeline_output.pkl')