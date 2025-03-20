import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Function to render Power BI report
def render_powerbi_report():
    st.subheader(" Power BI Visualization")
    st.markdown("""
        <iframe width="100%" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiNzhlNDc1NzEtMzVlYi00M2ZhLTg4NTktNTc5MDAwZTI0NTRkIiwidCI6ImRmNTRjNDdhLTk2OWMtNGVhNi1iMmI0LWUxZmM3NmE0MjE3MyJ9" 
        frameborder="0" allowFullScreen="true"></iframe>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Excel Statistical Analysis", layout="wide")

    # Navigation menu
    selected_page = st.sidebar.radio("Select Page", ["Statistical Analysis", "Visualization"])

    if selected_page == "Statistical Analysis":
        st.title(" Excel Statistical Analysis Tool")
        
        uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xls", "xlsx"], help="Supports .xls and .xlsx formats")
        
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            st.subheader(" Preview of Uploaded Data")
            st.dataframe(df.head())
            
            numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
            categorical_columns = df.select_dtypes(include='object').columns.tolist()
            
            col1, col2 = st.columns([1, 1])
            with col1:
                selected_column = st.selectbox(" Select a column for analysis", numeric_columns + categorical_columns)
            with col2:
                stat_tool = st.selectbox(" Select a statistical tool", [
                    "Mean", "Median", "Mode", "Variance", "Standard Deviation", "Chi-Square Test", 
                ])
            
            if stat_tool != "Chi-Square Test" and st.button(" Calculate"):
                if stat_tool == "Mean":
                    st.success(f" Mean: {df[selected_column].mean()}")
                elif stat_tool == "Median":
                    st.success(f"Median: {df[selected_column].median()}")
                elif stat_tool == "Mode":
                    st.success(f"Mode: {df[selected_column].mode()[0]}")
                elif stat_tool == "Variance":
                    st.success(f" Variance: {df[selected_column].var()}")
                elif stat_tool == "Standard Deviation":
                    st.success(f" Standard Deviation: {df[selected_column].std()}")
               
            
            if stat_tool == "Chi-Square Test" and len(categorical_columns) >= 2:
                cat_col1 = st.selectbox("📂 Select first categorical column", categorical_columns, key="chi1")
                cat_col2 = st.selectbox("📂 Select second categorical column", categorical_columns, key="chi2")
                if st.button("🔍 Run Chi-Square Test"):
                    contingency_table = pd.crosstab(df[cat_col1], df[cat_col2])
                    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
                    st.success(f"Chi-Square Statistic: {chi2:.4f}, Degrees of Freedom: {dof}, P-Value: {p:.4f}")
            
           

    elif selected_page == "Visualization":
        render_powerbi_report()

if __name__ == "__main__":
    main()
