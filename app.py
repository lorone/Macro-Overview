import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Forex Macro Dashboard", layout="wide")

# Load Excel file
uploaded_file = "Macro Overview 2025.xlsx"

@st.cache_data
def load_data(file):
    xls = pd.ExcelFile(file)
    data = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}
    return data

data = load_data(uploaded_file)

# Sidebar: currency selector
st.sidebar.title("Currency Selector")
currencies = list(data.keys())
selected_currency = st.sidebar.selectbox("Choose a currency sheet", currencies)

df = data[selected_currency]

st.title(f"📊 Macro Overview for {selected_currency}")

# Show dataframe
st.dataframe(df, use_container_width=True)

# Automatically plot numeric columns over time if present
try:
    time_col = df.columns[0]
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns

    for col in numeric_cols:
        fig = px.line(df, x=time_col, y=col, title=col)
        st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.warning("Couldn't auto-plot data. Please check the format.")
    st.text(str(e))