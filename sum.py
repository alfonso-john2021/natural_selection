import pandas as pd
import os

# Directory containing the Excel files
directory = 'D:/xxx'  # Update this path to your folder
merged_data = []

# Iterate through all Excel files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(directory, filename)
        df = pd.read_excel(file_path)
        df['Source File'] = filename  # Optional: Add a column to indicate the source file
        merged_data.append(df)

# Concatenate all DataFrames into one
merged_df = pd.concat(merged_data, ignore_index=True)

# Save the merged DataFrame to a new Excel file
merged_df.to_excel('merged_data.xlsx', index=False)

print("Merging complete. Merged data saved as 'merged_data.xlsx'.")
