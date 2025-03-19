import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quick Data Audit", page_icon="📊", layout="wide")

st.title("Quick Data Audit Tool")
st.markdown("Assess the quality of your business data in minutes. Upload your dataset to get an instant audit report.")

uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

def audit_data(df):
    report = {
        "Total Rows": df.shape[0],
        "Total Columns": df.shape[1],
        "Missing Values (%)": df.isnull().sum().sum() / df.size * 100,
        "Duplicate Rows": df.duplicated().sum(),
        "Columns with Missing Values": df.columns[df.isnull().any()].tolist(),
        "Column Types": df.dtypes.to_dict()
    }
    return report

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
        else:
            df = pd.read_excel(uploaded_file)

        
        st.subheader("📌 Audit Report")
        report = audit_data(df)
        st.json(report)
        st.subheader("Column-Wise Summary Statistics")
        st.write(df.describe())

        if report["Missing Values (%)"] > 10 or report["Duplicate Rows"] > 0:
            st.warning("⚠️ Your data has quality issues. Consider improving it before use.")
            st.markdown("[Book a Free Consultation](https://yourconsultationwebsite.com)")
        else:
            st.success("✅ Your data quality is good!")
    except Exception as e:
        st.error(f"Error processing file: {e}")


st.markdown("### Why Audit Your Data?")
st.markdown("- To identify missing or inconsistent data\n- Ensure your data is ready for analysis\n- To improve decision-making with clean data")
