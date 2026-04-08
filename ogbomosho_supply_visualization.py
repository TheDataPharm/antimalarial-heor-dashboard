import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Set the visual style for professional charts
df = pd.read_excel(r"C:\Users\findo\OneDrive\Desktop\ogbomosho_dispensing.xlsx")
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# ==========================================
# CHART 1: Drug Dispensing by Age Group
# ==========================================
# This answers: "Are we dispensing the right AL packs to the right age groups?"

plt.figure(figsize=(10, 6))
# We use countplot to easily count how many times each drug appears per age group
ax1 = sns.countplot(data=df, x='Age_Group', hue='Drug_Name', palette='viridis')

plt.title('Antimalarial (AL) Dispensing Volume by Age Group', fontsize=14, fontweight='bold')
plt.xlabel('Patient Age Category', fontsize=12)
plt.ylabel('Number of Prescriptions (Packs)', fontsize=12)
plt.legend(title='Drug Type (Pack Size)')

# Add actual numbers on top of the bars for the HOD to see clearly
for p in ax1.patches:
    ax1.annotate(f'{int(p.get_height())}', 
                 (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha = 'center', va = 'center', 
                 xytext = (0, 9), 
                 textcoords = 'offset points')

plt.tight_layout()
plt.show()

# ==========================================
# CHART 2: Patient Payment Categories
# ==========================================
# This answers: "What is the financial burden on the pharmacy?" 
# Useful for the Ministry of Health to see how many people rely on "Free Health".

plt.figure(figsize=(8, 5))
patient_counts = df['Patient_Category'].value_counts()

# A clean pie chart for financial/category distribution
plt.pie(patient_counts.values, labels=patient_counts.index, autopct='%1.1f%%', 
        startangle=140, colors=sns.color_palette('pastel'))
plt.title('Distribution of Patients by Payment Category', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()

# ==========================================
# CHART 3: The Clinical Audit (Pregnancy Flag)
# ==========================================
# This is your HEOR masterpiece. It flags any pregnant women who received AL.

plt.figure(figsize=(7, 5))
# Filter for only female patients to keep the chart relevant
female_df = df[df['Gender'] == 'F']

sns.countplot(data=female_df, x='Pregnancy_Status', hue='Drug_Name', palette='flare')
plt.title('ACT Dispensing among Female Patients (Pregnancy Audit)', fontsize=14, fontweight='bold')
plt.xlabel('Pregnancy Status', fontsize=12)
plt.ylabel('Number of Prescriptions', fontsize=12)

plt.tight_layout()
plt.show()