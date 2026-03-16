import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

def is_numeric(col):      # check column is numeric
  return pd.api.types.is_numeric_dtype(col)

def parse_date_column(df, col):
  try:
    df[col] = pd.to_datetime(df[col])
    return True
  except:
    return False

# CSV file - reads and validation 

def process_csv_file(filename):
  filepath = os.path.join("uploads", filename)

  if not os.path.exists(filepath):
    raise FileNotFoundError(f"File {filename} not found in uploads folder")

  try:
    df = pd.read_csv(filepath)
  except  Exception as e:
    raise  ValueError(f"Failed to read CSV: {str(e)}")

  if df.empty:
    raise ValueError("CSV file is empty")


  column_info = []
  for col in df.columns:
    col_type = "numeric" if is_numeric(df[col]) else "categorical"
    column_info.append({
      "name" : col,
      "type" : col_type,
      "null_count" : int(df[col].isnull().sum()),
      "unique_count" : int(df[col].nunique())
    })

  return{
    "dataframe": df,
    "total_rows": len(df),
    "total_columns": len(df.columns),
    "columns": column_info
  }



# multiple Filters to dataframes 


def Apply_filters(df, filters):
  df_filtered = df.copy()


  for filter_config in filters:
    filter_type = filter_config.get("type")
    column = filter_config.get("column")

    if column not in df_filtered.columns:
      continue    
    