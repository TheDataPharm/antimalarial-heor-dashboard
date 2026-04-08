import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Pharmacy HEOR Dashboard", page_icon="💊", layout="wide")
st.title("🏥 Antimalarial Supply Chain & HEOR Dashboard")
st.markdown("**State Hospital Ogbomosho | Predictive Analytics Pilot**")
st.markdown("---")

# --- 2. DATA LOADING & CLEANING ---
@st.cache_data
def load_data():
    # To use your real data, uncomment the line below and ensure the file is in the 'data' folder
    
    
    df = pd.read_excel(r"C:\Users\findo\OneDrive\Desktop\Antimalarial Demand Optimization\data\ogbomosho_dispensing.xlsx")
    
    
    # Sort chronologically
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
    
    # Financial Mapping (State Procurement Estimates)
    cost_map = {'AL4': 2500, 'AL3': 1800, 'AL2': 1800, 'AL1': 1000}
    df['Unit_Cost_NGN'] = df['Drug_Name'].map(cost_map)
    df['Total_Cost_NGN'] = df['Unit_Cost_NGN'] * df['Quantity_Dispensed']
    
    # Create Year-Month column for Time-Series grouping
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

# We calculate monthly average instead of annual since we have 8 months of data
monthly_burn_rate = total_free_subsidy / 8 if len(filtered_df) > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total AL Packs Dispensed", f"{int(total_packs)} Boxes")
col2.metric("Total Dispensed Value", f"₦{filtered_df['Total_Cost_NGN'].sum():,.2f}")
col3.metric("Absorbed by Free Health", f"₦{total_free_subsidy:,.2f}")
col4.metric("Avg. Monthly Subsidy Burn", f"₦{monthly_burn_rate:,.2f}")

st.markdown("---")

# --- 5. INTERACTIVE CHARTS ---
tab1, tab2, tab3 = st.tabs(["📈 Time-Series Trends", "📊 Clinical & Demographic Audit", "💳 Financial Distribution"])

with tab1:
    st.markdown("### Longitudinal Demand & Financial Forecasting")
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        # Time-Series: Volume by Drug over time
        monthly_vol = filtered_df.groupby(['Month_Year', 'Drug_Name'])['Quantity_Dispensed'].sum().reset_index()
        fig_trend = px.line(monthly_vol, x="Month_Year", y="Quantity_Dispensed", color="Drug_Name", markers=True,
                            title="Monthly Dispensing Volume (AL4 vs AL2)",
                            labels={"Quantity_Dispensed": "Packs Dispensed", "Month_Year": "Timeline"})
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_t2:
        # Time-Series: Financial Burn Rate over time for Free Health
        free_health_trend = free_health_df.groupby('Month_Year')['Total_Cost_NGN'].sum().reset_index()
        fig_fin_trend = px.area(free_health_trend, x="Month_Year", y="Total_Cost_NGN",
                                title="Free Health Financial Burden Over Time",
                                labels={"Total_Cost_NGN": "Cost Absorbed (₦)", "Month_Year": "Timeline"},
                                color_discrete_sequence=['#ef553b'])
        st.plotly_chart(fig_fin_trend, use_container_width=True)

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