import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility (you can change this number or remove it for different results each time)
np.random.seed(42)  # Remove this line if you want different random selection each time

# Load the CSV file
df = pd.read_csv('Selection Form _ Alternance _ Career Support Program  (Responses) - Form Responses.csv')

# Display initial info with styling
print("=" * 80)
print("INITIAL DATA OVERVIEW")
print("=" * 80)
print(f"Total number of students: {len(df)}")

# Map columns using list indexing since column names have special characters
name_col_idx = 3
email_col_idx = 4
country_col_idx = 6
education_col_idx = 7
specialization_col_idx = 8
contribute_col_idx = 11

# Create simplified column names
df['Name'] = df.iloc[:, name_col_idx]
df['Email'] = df.iloc[:, email_col_idx]
df['Country'] = df.iloc[:, country_col_idx].str.strip()
df['Education'] = df.iloc[:, education_col_idx].str.strip()
df['Specialization'] = df.iloc[:, specialization_col_idx].str.strip()
df['Contribution'] = df.iloc[:, contribute_col_idx].str.strip()

# Normalize country names
df['Country'] = df['Country'].replace({
    'Maroc': 'Morocco',
    'France': 'France'
})

# Normalize specialization to match criteria
def normalize_specialization(spec):
    spec_lower = str(spec).lower()
    if 'data' in spec_lower:
        return 'Data'
    elif 'cyber' in spec_lower:
        return 'Cybersecurity'
    elif 'dev' in spec_lower or 'développement' in spec_lower:
        return 'Development'
    else:
        return spec

df['Normalized_Spec'] = df['Specialization'].apply(normalize_specialization)

# Define filtering criteria
print("\n" + "=" * 80)
print("SELECTION CRITERIA")
print("=" * 80)
print("""
GROUP 1 - DATA
- Main Selection: 25 students
- Waiting List: 7 students
- Education Level: BAC+3, BAC+4, BAC+5
- Country: Morocco or France
- Contribution: Yes OR "I want More details"
- Selection: RANDOM

GROUP 2 - CYBERSECURITY & DEVELOPMENT
- Main Selection: 10 students
- Waiting List: 7 students
- Education Level: BAC+3, BAC+4, BAC+5
- Country: France or Morocco
- Contribution: Yes OR "I want More details"
- Selection: RANDOM

GROUP 3 - OTHER FIELDS
- Main Selection: 10 students
- Waiting List: 7 students
- Education Level: BAC+3, BAC+4, BAC+5
- Country: France or Morocco
- Contribution: Yes OR "I want More details"
- Selection: RANDOM

Total Main Selection: 45 students
Total Waiting List: 21 students
Grand Total: 66 students
""")

# ==================== GROUP 1: DATA ====================
data_students = df[
    (df['Normalized_Spec'] == 'Data') &
    (df['Education'].isin(['BAC+3', 'BAC+4', 'BAC+5'])) &
    (df['Country'].isin(['Morocco', 'France'])) &
    (df['Contribution'].isin(['Yes', 'I want More details']))
].copy()

# RANDOM SELECTION
data_students_shuffled = data_students.sample(frac=1).reset_index(drop=True)
selected_data = data_students_shuffled.head(25)
waiting_data = data_students_shuffled.iloc[25:32]  # Next 7 students

print(f"\n✓ Eligible Data students: {len(data_students)}")
print(f"✓ RANDOMLY Selected Data students: {len(selected_data)}")
print(f"✓ Data Waiting List: {len(waiting_data)}")

# ==================== GROUP 2: CYBERSECURITY & DEVELOPMENT ====================
cyber_dev_students = df[
    (df['Normalized_Spec'].isin(['Cybersecurity', 'Development'])) &
    (df['Education'].isin(['BAC+3', 'BAC+4', 'BAC+5'])) &
    (df['Country'].isin(['Morocco', 'France'])) &
    (df['Contribution'].isin(['Yes', 'I want More details']))
].copy()

# RANDOM SELECTION
cyber_dev_students_shuffled = cyber_dev_students.sample(frac=1).reset_index(drop=True)
selected_cyber_dev = cyber_dev_students_shuffled.head(10)
waiting_cyber_dev = cyber_dev_students_shuffled.iloc[10:17]  # Next 7 students

print(f"\n✓ Eligible Cybersecurity/Development students: {len(cyber_dev_students)}")
print(f"✓ RANDOMLY Selected Cybersecurity/Development students: {len(selected_cyber_dev)}")
print(f"✓ Cybersecurity/Development Waiting List: {len(waiting_cyber_dev)}")

# ==================== GROUP 3: OTHER FIELDS ====================
other_fields_students = df[
    (~df['Normalized_Spec'].isin(['Data', 'Cybersecurity', 'Development'])) &
    (df['Education'].isin(['BAC+3', 'BAC+4', 'BAC+5'])) &
    (df['Country'].isin(['Morocco', 'France'])) &
    (df['Contribution'].isin(['Yes', 'I want More details']))
].copy()

# RANDOM SELECTION
other_fields_students_shuffled = other_fields_students.sample(frac=1).reset_index(drop=True)
selected_other = other_fields_students_shuffled.head(10)
waiting_other = other_fields_students_shuffled.iloc[10:17]  # Next 7 students

print(f"\n✓ Eligible Other Fields students: {len(other_fields_students)}")
print(f"✓ RANDOMLY Selected Other Fields students: {len(selected_other)}")
print(f"✓ Other Fields Waiting List: {len(waiting_other)}")

# ==================== COMBINE SELECTIONS ====================
# Add group and status labels
selected_data['Group'] = 'Data'
selected_data['Status'] = 'Selected'
waiting_data['Group'] = 'Data'
waiting_data['Status'] = 'Waiting List'

selected_cyber_dev['Group'] = 'Cybersecurity/Development'
selected_cyber_dev['Status'] = 'Selected'
waiting_cyber_dev['Group'] = 'Cybersecurity/Development'
waiting_cyber_dev['Status'] = 'Waiting List'

selected_other['Group'] = 'Other Fields'
selected_other['Status'] = 'Selected'
waiting_other['Group'] = 'Other Fields'
waiting_other['Status'] = 'Waiting List'

# Combine selected students
final_selection = pd.concat([selected_data, selected_cyber_dev, selected_other], ignore_index=True)

# Combine waiting list
final_waiting = pd.concat([waiting_data, waiting_cyber_dev, waiting_other], ignore_index=True)

# Combine everything
all_students = pd.concat([
    selected_data, waiting_data,
    selected_cyber_dev, waiting_cyber_dev,
    selected_other, waiting_other
], ignore_index=True)

print("\n" + "=" * 80)
print("FINAL SELECTION SUMMARY")
print("=" * 80)
print(f"Total SELECTED students: {len(final_selection)}")
print(f"  - Data: {len(selected_data)}")
print(f"  - Cybersecurity/Development: {len(selected_cyber_dev)}")
print(f"  - Other Fields: {len(selected_other)}")
print(f"\nTotal WAITING LIST students: {len(final_waiting)}")
print(f"  - Data: {len(waiting_data)}")
print(f"  - Cybersecurity/Development: {len(waiting_cyber_dev)}")
print(f"  - Other Fields: {len(waiting_other)}")
print(f"\n🎯 GRAND TOTAL: {len(all_students)} students")

# ==================== EXPORT TO CSV ====================
# Export SELECTED students
selected_export = final_selection[[
    'Name', 'Email', 'Group', 'Normalized_Spec', 'Education', 'Country', 'Contribution', 'Status'
]].copy()
selected_export.columns = ['Name', 'Email', 'Group', 'Specialization', 'Education Level', 'Country', 'Contribution Response', 'Status']
selected_export.to_csv('selected_students.csv', index=False)

# Export WAITING LIST students
waiting_export = final_waiting[[
    'Name', 'Email', 'Group', 'Normalized_Spec', 'Education', 'Country', 'Contribution', 'Status'
]].copy()
waiting_export.columns = ['Name', 'Email', 'Group', 'Specialization', 'Education Level', 'Country', 'Contribution Response', 'Status']
waiting_export.to_csv('waiting_list_students.csv', index=False)

# Export ALL students (selected + waiting)
all_export = all_students[[
    'Name', 'Email', 'Group', 'Normalized_Spec', 'Education', 'Country', 'Contribution', 'Status'
]].copy()
all_export.columns = ['Name', 'Email', 'Group', 'Specialization', 'Education Level', 'Country', 'Contribution Response', 'Status']
all_export.to_csv('all_students_selected_and_waiting.csv', index=False)

print("\n" + "=" * 80)
print("✅ CSV FILES CREATED SUCCESSFULLY!")
print("=" * 80)
print("✓ selected_students.csv")
print("✓ waiting_list_students.csv")
print("✓ all_students_selected_and_waiting.csv")

print("\n🎉 You can now run the Streamlit dashboard!")