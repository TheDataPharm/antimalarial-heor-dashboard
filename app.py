import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Pharmacy HEOR Dashboard", layout="wide")
st.title("🏥 Antimalarial Supply Chain & HEOR Dashboard")
st.markdown("**State Hospital Ogbomosho | Predictive Analytics Pilot**")
st.markdown("---")

# --- 2. DATA LOADING & CLEANING ---
@st.cache_data
def load_data():
    
    df = pd.read_excel(r"C:\Users\findo\OneDrive\Desktop\HEOR_Pharmacy_Dashboard\data\ogbomosho_dispensing.xlsx")
    df = df.sort_values('Date_Dispensed').reset_index(drop=True)
    # ---------------------------------------------------------------
    
    # Data Cleaning Logic
    df['Date_Dispensed'] = pd.to_datetime(df['Date_Dispensed'])
    
    def categorize_age(age_val):
        if str(age_val).strip().upper() == 'N/A': return 'Adult'
        try:
            num = float(age_val)
            if num < 3: return 'Infant/Toddler'
            elif num <= 14: return 'Child/Adolescent'
            else: return 'Adult'
        except: return 'Unknown'
        
    df['Age_Group'] = df['Age'].apply(categorize_age)
    df.loc[df['Gender'] == 'M', 'Pregnancy'] = 'N/A'
    
    def standardize_preg(status):
        if status in ['NP', 'NO', 'NONE']: return 'Non-Pregnant'
        elif status in ['P', 'YES', 'PREG']: return 'Pregnant'
        else: return 'N/A'
    df['Pregnancy_Status'] = df['Pregnancy'].apply(standardize_preg)
    
    # Financial Mapping
    cost_map = {'AL4': 2500, 'AL3': 1800, 'AL2': 1800, 'AL1': 1000}
    df['Unit_Cost_NGN'] = df['Drug_Name'].map(cost_map)
    df['Total_Cost_NGN'] = df['Unit_Cost_NGN'] * df['Quantity_Dispensed']
    
    df['Month_Year'] = df['Date_Dispensed'].dt.to_period('M').astype(str)
    return df

df = load_data()

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")
selected_category = st.sidebar.multiselect("Patient Category", options=df['Patient_Category'].unique(), default=df['Patient_Category'].unique())
selected_drugs = st.sidebar.multiselect("Drug Pack Size", options=df['Drug_Name'].unique(), default=df['Drug_Name'].unique())

filtered_df = df[(df['Patient_Category'].isin(selected_category)) & (df['Drug_Name'].isin(selected_drugs))]

# --- 4. FINANCIAL KPIs ---
st.subheader("💰 Financial Burden & Inventory Metrics (8-Month Tracking)")
total_packs = filtered_df['Quantity_Dispensed'].sum()
free_health_df = filtered_df[filtered_df['Patient_Category'] == 'Free Health']
total_free_subsidy = free_health_df['Total_Cost_NGN'].sum()
monthly_burn_rate = total_free_subsidy / 8 if len(filtered_df) > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total AL Packs Dispensed", f"{int(total_packs)} Boxes")
col2.metric("Total Dispensed Value", f"₦{filtered_df['Total_Cost_NGN'].sum():,.2f}")
col3.metric("Absorbed by Free Health", f"₦{total_free_subsidy:,.2f}")
col4.metric("Avg. Monthly Subsidy Burn", f"₦{monthly_burn_rate:,.2f}")

st.markdown("---")

# --- 5. INTERACTIVE CHARTS ---
tab1, tab2, tab3 = st.tabs(["📈 Time-Series Trends & Forecasting", "📊 Clinical & Demographic Audit", "💳 Financial Distribution"])

with tab1:
    st.markdown("### Longitudinal Demand & Financial Burden")
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        monthly_vol = filtered_df.groupby(['Month_Year', 'Drug_Name'])['Quantity_Dispensed'].sum().reset_index()
        fig_trend = px.line(monthly_vol, x="Month_Year", y="Quantity_Dispensed", color="Drug_Name", markers=True,
                            title="Historical Monthly Dispensing Volume",
                            color_discrete_sequence=px.colors.qualitative.Set1)
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_t2:
        free_health_trend = free_health_df.groupby('Month_Year')['Total_Cost_NGN'].sum().reset_index()
        fig_fin_trend = px.area(free_health_trend, x="Month_Year", y="Total_Cost_NGN",
                                title="Free Health Financial Burden Over Time",
                                color_discrete_sequence=['#ef553b'])
        st.plotly_chart(fig_fin_trend, use_container_width=True)
        
    st.markdown("---")
    st.markdown("### 🔮 Predictive Demand Forecasting (Adult AL4)")
    st.markdown("Using an ARIMA (AutoRegressive Integrated Moving Average) model to forecast the next 4 weeks of AL4 demand compared to a Naive baseline.")
    
    # Forecasting Logic
    # 1. Group data by Week for AL4
    al4_df = df[df['Drug_Name'] == 'AL4'].copy()
    weekly_al4 = al4_df.groupby(pd.Grouper(key='Date_Dispensed', freq='W'))['Quantity_Dispensed'].sum().reset_index()
    
    if len(weekly_al4) > 10: # Ensure we have enough data to run a model
        # 2. Train Advanced Model (ARIMA)
        model = ARIMA(weekly_al4['Quantity_Dispensed'], order=(1, 1, 1))
        fitted_model = model.fit()
        forecast_advanced = fitted_model.forecast(steps=4)
        
        # 3. Train Baseline Model (Naive Forecast: Next week = Last week)
        last_val = weekly_al4['Quantity_Dispensed'].iloc[-1]
        forecast_naive = [last_val] * 4
        
        # 4. Prepare dates for forecast
        last_date = weekly_al4['Date_Dispensed'].iloc[-1]
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=7), periods=4, freq='W')
        
        # 5. Plotting with Plotly Graph Objects
        fig_forecast = go.Figure()
        
        # Historical Data
        fig_forecast.add_trace(go.Scatter(x=weekly_al4['Date_Dispensed'], y=weekly_al4['Quantity_Dispensed'],
                                          mode='lines+markers', name='Historical AL4 Demand', line=dict(color='blue')))
        # Advanced Forecast (ARIMA)
        fig_forecast.add_trace(go.Scatter(x=future_dates, y=forecast_advanced,
                                          mode='lines+markers', name='Advanced Forecast (ARIMA)', line=dict(color='red', dash='dash')))
        # Baseline Forecast (Naive)
        fig_forecast.add_trace(go.Scatter(x=future_dates, y=forecast_naive,
                                          mode='lines+markers', name='Baseline Forecast (Naive)', line=dict(color='grey', dash='dot')))
        
        fig_forecast.update_layout(title="4-Week Predictive Demand Forecast (AL4)", xaxis_title="Timeline", yaxis_title="Packs Dispensed")
        st.plotly_chart(fig_forecast, use_container_width=True)
    else:
        st.warning("Not enough temporal data to generate a reliable ARIMA forecast. Need at least 10 weeks of data.")

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        fig_age = px.histogram(filtered_df, x="Age_Group", color="Drug_Name", barmode="group",
                               title="Dispensing Volume by Age Group",
                               color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_age, use_container_width=True)
    with col_b:
        female_df = filtered_df[filtered_df['Gender'] == 'F']
        fig_preg = px.histogram(female_df, x="Pregnancy_Status", color="Drug_Name",
                                title="ACT Dispensing: Pregnancy Audit (Females Only)",
                                color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_preg, use_container_width=True)

with tab3:
    cost_by_category = filtered_df.groupby('Patient_Category')['Total_Cost_NGN'].sum().reset_index()
    fig_pie = px.pie(cost_by_category, values='Total_Cost_NGN', names='Patient_Category', 
                     title="Total Financial Burden by Payment Scheme", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 6. RAW DATA EXPORT ---
with st.expander("View & Export Cleaned Data"):
    st.dataframe(filtered_df)
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Cleaned Data (CSV)", data=csv, file_name="cleaned_pharmacy_data.csv", mime="text/csv")