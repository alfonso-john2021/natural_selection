import pandas as pd
import os,time

# Directory containing the Excel files
directory = 'C:/Users/이지후/Downloads/과학수행'  # Update this path to your folder
accumulated_data = pd.DataFrame()  # Initialize an empty DataFrame

# Iterate through all Excel files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(directory, filename)
        df = pd.read_excel(file_path)
        
        # Keep only the relevant columns
        df = df[["Generation", "Black", "White"]]
        df['Source File'] = filename  # Add a source file column
        
        # Accumulate data
        if accumulated_data.empty:
            accumulated_data = df
        else:
            accumulated_data = pd.concat([accumulated_data, df])
        
# Group by "Generation" and sum "Black" and "White"
accumulated_data = accumulated_data.groupby("Generation")[["Black", "White"]].sum().reset_index()
name = "accumulated_data" + str(round(time.time())) + ".xlsx"
# Save the accumulated DataFrame to a new Excel file
accumulated_data.to_excel(name, index=False)

print("Accumulation complete. Data saved as 'accumulated_data_[time].xlsx'.")
