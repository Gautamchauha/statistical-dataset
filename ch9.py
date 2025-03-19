import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("Nissan_GTR (1).xlsx")

df = load_data()

# Dashboard UI
st.set_page_config(page_title="Nissan GT-R Dashboard", layout="wide")
st.title("🚗 NISSAN GT-R DASHBOARD")

# Theme switcher
def set_theme():
    theme = st.radio("Select Theme:", ["Light", "Dark"], horizontal=True)
    if theme == "Light":
        st.markdown("""<style>body {background-color: #f5f5f5; color: black;}""", unsafe_allow_html=True)
    else:
        st.markdown("""<style>body {background-color: #333; color: white;}""", unsafe_allow_html=True)

set_theme()

# Sidebar navigation
st.sidebar.header("Navigation")
nav_option = st.sidebar.radio("Go to", ["Dashboard", "Statistical Analysis"])

if nav_option == "Dashboard":
    # Sidebar for column selection
    selected_column = st.sidebar.selectbox("Select a column for visualization", df.columns)

    # Layout for charts
    col1, col2, col3 = st.columns(3)

    # Exhaust System Analysis
    with col1:
        st.subheader("Exhaust System by Model")
        fig, ax = plt.subplots()
        sns.countplot(x="Exhaust System", hue="Model", data=df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Sound System Analysis
    with col2:
        st.subheader("Sound System by Model")
        fig, ax = plt.subplots()
        sns.countplot(x="Model", hue="Sound System", data=df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Airbag Count Analysis
    with col3:
        st.subheader("Sum of Airbag Count by Model")
        airbag_summary = df.groupby("Model")["Airbag Count"].sum().reset_index()
        fig, ax = plt.subplots()
        sns.barplot(x="Model", y="Airbag Count", data=airbag_summary, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Interior Material Analysis
    with col1:
        st.subheader("Model Count by Interior Material")
        fig, ax = plt.subplots()
        df["Interior Material"].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)
        st.pyplot(fig)

    # Aftermarket Mods Analysis
    with col2:
        st.subheader("Popular Aftermarket Mods by Model")
        fig, ax = plt.subplots()
        sns.countplot(y="Model", hue="Popular Aftermarket Mods", data=df, ax=ax)
        st.pyplot(fig)

    # Connectivity Features Analysis
    with col3:
        st.subheader("Connectivity Features by Model")
        fig, ax = plt.subplots()
        sns.countplot(x="Model", hue="Connectivity Features", data=df, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Dropdown for visualization mode
    st.sidebar.subheader("Visualization Mode")
    mode = st.sidebar.selectbox("Choose visualization mode", ["Histogram", "Boxplot", "Scatterplot"])

    # Dynamic Column Visualization
    st.subheader(f"{mode} of {selected_column}")
    fig, ax = plt.subplots()
    if mode == "Histogram":
        if df[selected_column].dtype == 'object':
            sns.countplot(y=selected_column, data=df, ax=ax)
        else:
            sns.histplot(df[selected_column], kde=True, ax=ax)
    elif mode == "Boxplot":
        sns.boxplot(y=selected_column, data=df, ax=ax)
    elif mode == "Scatterplot":
        numerical_columns = df.select_dtypes(include=['number']).columns
        x_col = st.sidebar.selectbox("Select X-axis column", numerical_columns)
        sns.scatterplot(x=df[x_col], y=df[selected_column], ax=ax)
    st.pyplot(fig)

    st.success("Dashboard generated successfully! 🚀")

elif nav_option == "Statistical Analysis":
    st.set_page_config(page_title="Excel Statistical Analysis", layout="wide")
    st.title("📊 Excel Statistical Analysis Tool")
    
    uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xls", "xlsx"], help="Supports .xls and .xlsx formats")
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.subheader("🔍 Preview of Uploaded Data")
        st.dataframe(df.head())
        
        numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
        categorical_columns = df.select_dtypes(include='object').columns.tolist()
        
        col1, col2 = st.columns([1, 1])
        with col1:
            selected_column = st.selectbox("📌 Select a column for analysis", numeric_columns + categorical_columns)
        with col2:
            stat_tool = st.selectbox("📊 Select a statistical tool", [
                "Mean", "Median", "Mode", "Variance", "Standard Deviation", "Chi-Square Test", "Correlation", "ANOVA"
            ])
        
        if stat_tool != "Chi-Square Test" and st.button("📈 Calculate"):
            if stat_tool == "Mean":
                st.success(f"📊 Mean: {df[selected_column].mean()}")
            elif stat_tool == "Median":
                st.success(f"📊 Median: {df[selected_column].median()}")
            elif stat_tool == "Mode":
                st.success(f"📊 Mode: {df[selected_column].mode()[0]}")
            elif stat_tool == "Variance":
                st.success(f"📊 Variance: {df[selected_column].var()}")
            elif stat_tool == "Standard Deviation":
                st.success(f"📊 Standard Deviation: {df[selected_column].std()}")
            elif stat_tool == "Correlation" and len(numeric_columns) > 1:
                colA, colB = st.columns(2)
                with colA:
                    col1 = st.selectbox("🔗 Select first numeric column", numeric_columns, key="corr1")
                with colB:
                    col2 = st.selectbox("🔗 Select second numeric column", numeric_columns, key="corr2")
                if st.button("🔍 Compute Correlation"):
                    st.success(f"🔗 Correlation: {df[col1].corr(df[col2])}")
            elif stat_tool == "ANOVA" and categorical_columns:
                factor_col = st.selectbox("📊 Select categorical factor column", categorical_columns)
                if factor_col:
                    anova_groups = [group[selected_column].dropna() for _, group in df.groupby(factor_col)]
                    f_stat, p_value = stats.f_oneway(*anova_groups)
                    st.success(f"📊 ANOVA F-Statistic: {f_stat:.4f}, P-Value: {p_value:.4f}")
        
        if stat_tool == "Chi-Square Test" and len(categorical_columns) >= 2:
            cat_col1 = st.selectbox("📂 Select first categorical column", categorical_columns, key="chi1")
            cat_col2 = st.selectbox("📂 Select second categorical column", categorical_columns, key="chi2")
            if st.button("🔍 Run Chi-Square Test"):
                contingency_table = pd.crosstab(df[cat_col1], df[cat_col2])
                chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
                st.success(f"📊 Chi-Square Statistic: {chi2:.4f}, Degrees of Freedom: {dof}, P-Value: {p:.4f}")
    
    st.success("Statistical analysis performed successfully! 🚀")
