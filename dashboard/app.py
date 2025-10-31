# dashboard/app.py — FINAL: NO ERRORS, GEMINI AI, PDF FIXED
import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import google.generativeai as genai

# === PATHS ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'merged_data.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'python', 'scripts', 'rf_model.pkl')

# === LOAD DATA & MODEL ===
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df)} companies")
    return df

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

df = load_data()
model = load_model()

# === GEMINI SETUP ===
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.5-flash')
else:
    gemini_model = None
    st.warning("GEMINI_API_KEY not found. Add to .streamlit/secrets.toml")

# === FEATURE COLUMNS (MUST MATCH TRAINING) ===
feature_cols = [
    'Total ESG Risk score', 'Environment Risk Score',
    'Social Risk Score', 'Governance Risk Score',
    'debt_to_equity', 'roe'
]

# === HSBC LOGO ===
logo_path = os.path.join(BASE_DIR, 'assets', 'logo.png')
if os.path.exists(logo_path):
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(logo_path, width=120, use_container_width=False)  # Reduced from 180 to 120
else:
    st.warning("Logo not found. Place logo.png in the assets folder.")

st.title("HSBC ESG Risk Analyzer")
st.markdown("**379 S&P 500 Companies | AI-Powered Risk Simulation**")

# === PORTFOLIO SUMMARY ===
st.subheader("Portfolio Risk Summary")
col1, col2, col3 = st.columns(3)
high_risk = df['risk_flag'].sum()
total = len(df)
avg_esg = df['Total ESG Risk score'].mean()

with col1:
    st.metric("Total Companies", total)
with col2:
    st.metric("High Risk", high_risk, f"{high_risk/total:.1%}")
with col3:
    st.metric("Avg ESG Score", f"{avg_esg:.1f}")

# === ESG DISTRIBUTION (FIXED) ===
st.subheader("ESG Score Distribution")
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(df['Total ESG Risk score'], bins=30, color='#ff4b4b', alpha=0.8, edgecolor='white')
ax.axvline(avg_esg, color='yellow', linestyle='--', linewidth=2, label=f'Mean: {avg_esg:.1f}')
ax.set_title("ESG Risk Score Distribution (Lower = Better)")
ax.set_xlabel("ESG Risk Score")
ax.set_ylabel("Companies")
ax.legend()
st.pyplot(fig)

# === FILTERS ===
st.subheader("Company Analysis")
col1, col2 = st.columns([1, 2])
with col1:
    sectors = ['All'] + sorted(df['Sector'].dropna().unique().tolist())
    sector = st.selectbox("Sector", sectors)
with col2:
    df_filtered = df if sector == 'All' else df[df['Sector'] == sector]
    company_symbol = st.selectbox("Select Company", df_filtered['Symbol'])

row = df_filtered[df_filtered['Symbol'] == company_symbol].iloc[0]

# === COMPANY DETAIL ===
col1, col2 = st.columns(2)
with col1:
    st.metric("Company", row['name'])
    st.metric("Sector", row['Sector'])
with col2:
    st.metric("Current ESG Score", f"{row['Total ESG Risk score']:.1f}")
    st.metric("Current Risk", "High" if row['risk_flag'] else "Low")

# === TOP 5 RISKIEST ===
st.subheader("Top 5 Riskiest Companies")
top5 = df.nlargest(5, 'Total ESG Risk score')[['Symbol', 'name', 'Sector', 'Total ESG Risk score', 'risk_flag']]
st.dataframe(top5.style.format({'Total ESG Risk score': '{:.1f}'}))

# === SIMULATION (FIXED) ===
st.subheader("What If We Improve ESG?")
improvement = st.slider("Reduce ESG Score by (points)", 0, 30, 10, 1)
new_esg = row['Total ESG Risk score'] - improvement

# === PREDICTION (FIXED WITH DataFrame) ===
pred_df = pd.DataFrame([[
    new_esg,
    row['Environment Risk Score'],
    row['Social Risk Score'],
    row['Governance Risk Score'],
    row['debt_to_equity'],
    row['roe']
]], columns=feature_cols)

new_pred = model.predict(pred_df)[0]
new_risk = "High" if new_pred else "Low"
delta = "Risk Reduced" if new_pred < row['risk_flag'] else "Risk Increased" if new_pred > row['risk_flag'] else "No Change"

col1, col2 = st.columns(2)
with col1:
    st.metric("New ESG Score", f"{new_esg:.1f}", f"-{improvement}")
with col2:
    st.metric("New Risk Level", new_risk, delta)

# === RECOMMENDED TARGET (FIXED) ===
st.info("**Finding minimum ESG score for Low Risk...**")
test_esg = row['Total ESG Risk score']
while test_esg > 0:
    test_df = pd.DataFrame([[
        test_esg, row['Environment Risk Score'], row['Social Risk Score'],
        row['Governance Risk Score'], row['debt_to_equity'], row['roe']
    ]], columns=feature_cols)
    if model.predict(test_df)[0] == 0:
        break
    test_esg -= 0.1
st.success(f"**Recommended ESG Target: <= {test_esg:.1f}** to achieve **Low Risk**")

# === GEMINI AI INSIGHT ===
if st.checkbox("Get AI-Powered Insight (Gemini)"):
    if gemini_model:
        with st.spinner("Asking Gemini..."):
            prompt = f"""
            Company: {row['name']} ({company_symbol})
            Sector: {row['Sector']}
            Current ESG: {row['Total ESG Risk score']:.1f}
            Risk: {'High' if row['risk_flag'] else 'Low'}
            Target ESG for Low Risk: {test_esg:.1f}
            
            Give a 2-sentence business recommendation for HSBC on how to engage this client on ESG improvement.
            """
            try:
                response = gemini_model.generate_content(prompt)
                st.markdown("### Gemini AI Recommendation")
                st.write(response.text)
            except Exception as e:
                st.error(f"Gemini error: {e}")
    else:
        st.error("Gemini API not configured.")

# === PDF REPORT (UTF-8 FIXED) ===
@st.cache_data
def generate_pdf(symbol):
    row = df[df['Symbol'] == symbol].iloc[0]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "HSBC ESG Risk Report", ln=1, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Company: {row['name']} ({symbol})", ln=1)
    pdf.cell(0, 10, f"Sector: {row['Sector']}", ln=1)
    pdf.cell(0, 10, f"Current ESG: {row['Total ESG Risk score']:.1f} | Risk: {'High' if row['risk_flag'] else 'Low'}", ln=1)
    pdf.cell(0, 10, f"Recommended ESG: <= {test_esg:.1f} for Low Risk", ln=1)
    
    # Save with UTF-8
    pdf_path = "report.pdf"
    pdf.output(pdf_path)
    with open(pdf_path, "rb") as f:
        return f.read()

if st.button("Export PDF Report"):
    pdf_data = generate_pdf(company_symbol)
    st.download_button("Download PDF", pdf_data, "HSBC_ESG_Report.pdf", "application/pdf")

# === DOWNLOAD CSV ===
csv = df.to_csv(index=False).encode()
st.download_button("Download Full Dataset", csv, "esg_risk_portfolio.csv", "text/csv")

st.markdown("---")
st.caption("Built with Python, Streamlit, Random Forest, Gemini AI | Data: S&P 500 ESG + Financials")