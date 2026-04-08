# 🏥 Health Economics & Outcomes Research (HEOR): Antimalarial Predictive Supply Chain & Financial Audit

## 📌 Project Overview
This project digitizes and analyzes an 8-month longitudinal sample (August 2025 – April 2026) of primary healthcare data from a Nigerian State Hospital. The objective is to evaluate the utilization, financial burden, and clinical safety of Artemisinin-based Combination Therapies (ACTs). 

Built as an interactive **Streamlit Dashboard**, this tool transitions pharmacy operations from reactive paper-based tracking to predictive, data-driven supply chain management using time-series trend analysis.

## 🎯 Core Objectives
1. **Longitudinal Trend Analysis:** Track the month-over-month dispensing volume of ACTs to identify seasonal malaria spikes and forecast future stock requirements.
2. **Financial Impact Analysis:** Quantify the monthly financial burn rate of antimalarial drugs distributed under the state's "Free Health" subsidy program, mapping it against demand surges.
3. **Clinical Audit (HEOR):** Automate the flagging of female patients receiving ACTs to ensure strict compliance with national malaria treatment guidelines regarding pregnancy.
4. **Supply Chain Optimization:** Analyze age-weight demographics to forecast the correct ratio of pack sizes (e.g., adult AL4 vs. pediatric AL2) required for upcoming procurement cycles.

## 🛠️ Technology Stack
* **Python** (Data manipulation, time-series formatting, and cleaning)
* **Pandas & NumPy** (Handling missing values, standardizing clinical text, grouping temporal data)
* **Plotly** (Interactive data visualization and line charts)
* **Streamlit** (Web application deployment)

## 💡 Key Business & Clinical Insights
* **The Volatility of Adult Malaria:** Time-series analysis reveals that pediatric ACT demand remains relatively flat year-round, whereas adult (AL4) demand is highly volatile. Future procurement must front-load AL4 inventory just before historical peak months (e.g., August/November) to prevent critical stockouts.
* **Predicting the "Free Health" Financial Hemorrhage:** The financial burden absorbed by the hospital is not a flat monthly cost; it aggressively mirrors the AL4 demand spikes. This dynamic model provides the Ministry of Health with hard evidence to request targeted, mid-year budget top-ups before the malaria season peaks.
* **Automated Safety Auditing:** The tool successfully cross-references patient gender, age, and pregnancy status to isolate high-risk dispensing events, acting as an automated antimicrobial stewardship system.

## 🚀 How to Run Locally
1. Clone this repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/antimalarial-heor-dashboard.git](https://github.com/TheDataPharm/antimalarial-heor-dashboard.git)
