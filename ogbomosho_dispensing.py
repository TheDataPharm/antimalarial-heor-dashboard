import pandas as pd
import numpy as np

# 1. Load your newly minted dataset 
# Replace 'ogbomoso_dispensing.csv' with your actual file name
# df = pd.read_csv('ogbomoso_dispensing.csv')

# (I am recreating a small chunk of your data here so the code runs perfectly for you to test)
data = {
    'Date_Dispensed': ['2025-10-06', '2025-10-06', '2025-10-06', '2025-10-06'],
    'Drug_Name': ['AL4', 'AL4', 'AL4', 'AL4'],
    'Quantity_Dispensed': [1.0, 1.0, 1.0, 1.0],
    'Patient_Category': ['Free Health', 'Free Health', 'Free Health', 'Free Health'],
    'Gender': ['F', 'F', 'F', 'F'],
    'Age': ['14', '40', 'N/A', 'N/A'],
    'Pregnancy': ['NP', 'NP', 'NP', 'NP']
}
df = pd.read_excel(r"C:\Users\findo\OneDrive\Documents\SPSS\Data Excel SHEETS COLLECTED\Register.xlsx")

# 2. Standardize the Date Format for Time-Series Analysis
df['Date_Dispensed'] = pd.to_datetime(df['Date_Dispensed'])

# 3. Handle the "N/A = Adult" Discovery
def categorize_age(age_val):
    if str(age_val).strip().upper() == 'N/A':
        return 'Adult'
    try:
        age_num = float(age_val)
        if age_num < 3: return 'Infant/Toddler'
        elif age_num <= 14: return 'Child/Adolescent'
        else: return 'Adult'
    except:
        return 'Unknown'

# Apply the categorization rule
df['Age_Group'] = df['Age'].apply(categorize_age)

# Create a strict numbers-only column for statistical math (forces N/A to become NaN)
df['Age_Numeric'] = pd.to_numeric(df['Age'], errors='coerce')

# 4. The Inventory Bonus: Map AL packs to total tablets
al_tablet_map = {'AL4': 24, 'AL3': 18, 'AL2': 12, 'AL1': 6}
df['Total_Tablets'] = df['Drug_Name'].map(al_tablet_map) * df['Quantity_Dispensed']

# 1. Clean up the text (remove accidental spaces and make everything uppercase)
df['Pregnancy'] = df['Pregnancy'].astype(str).str.strip().str.upper()
df['Gender'] = df['Gender'].astype(str).str.strip().str.upper()

# 2. The Clinical Logic Check: Force all Males to 'N/A' for Pregnancy
df.loc[df['Gender'] == 'M', 'Pregnancy'] = 'N/A'

# 3. Create a clean mapping dictionary for female patients
def standardize_pregnancy(status):
    if status in ['NP', 'NO', 'NONE', 'NON-PREGNANT']:
        return 'Non-Pregnant'
    elif status in ['P', 'YES', 'PREG', 'PREGNANT']:
        return 'Pregnant'
    elif status in ['N/A', 'NAN', 'UNKNOWN']:
        return 'Not Applicable / Unknown'
    else:
        return 'Not Applicable / Unknown' # Catch-all for weird entries

# Apply the function to create a clean analytical column
df['Pregnancy_Status'] = df['Pregnancy'].apply(standardize_pregnancy)

# Let's verify the cleanup by looking at the breakdown
print("Pregnancy Status Breakdown:")
print(df['Pregnancy_Status'].value_counts())

# Let's see the magic
print("Data shape:", df.shape)
print(df.head())
df.to_excel(r"C:\Users\findo\OneDrive\Desktop\ogbomosho_dispensing.xlsx")