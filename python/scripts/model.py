# python/scripts/model.py
import joblib
import pandas as pd
import os

# Load model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = joblib.load(os.path.join(BASE_DIR, 'python', 'scripts', 'rf_model.pkl'))

def predict_risk(features_df):
    return model.predict(features_df)

def simulate_scenario(df, symbol, improvement):
    row = df[df['symbol'] == symbol].copy()
    row['Total ESG Risk score'] -= improvement
    feats = row[[
        'Total ESG Risk score', 'Environment Risk Score',
        'Social Risk Score', 'Governance Risk Score',
        'debt_to_equity', 'roe'
    ]]
    pred = predict_risk(feats)
    row['Total ESG Risk score'] += improvement  # restore
    return pred, row