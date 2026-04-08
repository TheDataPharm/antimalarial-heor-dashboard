# 🏥 Health Economics & Outcomes Research (HEOR): Antimalarial Financial Audit

## 📌 Project Overview
This project digitizes and analyzes primary healthcare data from a Nigerian State Hospital to evaluate the utilization, financial burden, and clinical safety of Artemisinin-based Combination Therapies (ACTs). 

Built as an interactive **Streamlit Dashboard**, this tool transitions pharmacy operations from reactive paper-based tracking to predictive, data-driven supply chain management.

## 🎯 Core Objectives
1. **Financial Impact Analysis:** Quantify the monthly financial burn rate of antimalarial drugs distributed under the state's "Free Health" subsidy program.
2. **Clinical Audit (HEOR):** Automate the flagging of pregnant patients receiving ACTs to ensure compliance with national malaria treatment guidelines.
3. **Supply Chain Optimization:** Analyze age-weight demographics to forecast the correct ratio of pack sizes (AL4 vs. AL2) required for upcoming procurement cycles.

## 🛠️ Technology Stack
* **Python** (Data manipulation and cleaning)
* **Pandas & NumPy** (Handling missing values, standardizing clinical text)
* **Plotly** (Interactive data visualization)
* **Streamlit** (Web application deployment)

## 💡 Key Business Insights
* **Demographic Targeting:** Adult patients account for the highest volume of ACT consumption. Future procurement cycles should weight AL4 heavily over pediatric formulations to prevent capital tie-up.
* **The Cost of Subsidy:** A significant percentage of ACTs dispensed fall under the "Free Health" category, providing the Ministry of Health with hard data to justify budget increases before peak malaria season.

## 🚀 How to Run Locally
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py`