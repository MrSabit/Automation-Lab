import pandas as pd
import os

# File paths
BASE_DIR = os.path.dirname(__file__)

input_file = os.path.join(BASE_DIR, "data", "sales_data.xlsx")
output_file = os.path.join(BASE_DIR, "output", "sales_report.xlsx")

# Load Excel
df = pd.read_excel(input_file)

# Process Data
summary = df.groupby("Name")["Amount"].sum()

# Convert to DataFrame
summary_df = summary.reset_index()

# Save Output
os.makedirs(os.path.join(BASE_DIR, "output"), exist_ok=True)

summary_df.to_excel(output_file, index=False)

print("Report Generated Successfully!")