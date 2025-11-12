"""
Data loader module for the Chart Suggester application.
This module contains functions to load data from various file formats.
"""
import pandas as pd
import json
import sqlite3
from utils import get_file_extension

def load_data(file_path):
    """
    Load data from a file based on its extension.
    
    Args:
        file_path (str): Path to the data file
        
    Returns:
        pandas.DataFrame: The loaded dataframe
        
    Raises:
        Exception: If the file cannot be loaded
    """
    file_ext = get_file_extension(file_path)
    
    if file_ext == '.csv':
        return load_csv(file_path)
    elif file_ext in ['.xlsx', '.xls']:
        return load_excel(file_path)
    elif file_ext == '.json':
        return load_json(file_path)
    elif file_ext == '.txt':
        return load_txt(file_path)
    elif file_ext == '.db':
        return load_sqlite(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {file_ext}")

def load_csv(file_path):
    """Load data from a CSV file."""
    try:
        # Try to detect the delimiter
        with open(file_path, 'r') as f:
            first_line = f.readline()
        
        if '\t' in first_line:
            delimiter = '\t'
        elif ';' in first_line:
            delimiter = ';'
        else:
            delimiter = ','
        
        return pd.read_csv(file_path, delimiter=delimiter)
    except Exception as e:
        raise Exception(f"Failed to load CSV file: {str(e)}")

def load_excel(file_path):
    """Load data from an Excel file."""
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        raise Exception(f"Failed to load Excel file: {str(e)}")

def load_json(file_path):
    """Load data from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Convert to DataFrame based on JSON structure
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            # If it's a dictionary of dictionaries, try to normalize
            try:
                return pd.json_normalize(data)
            except:
                return pd.DataFrame([data])
        else:
            raise ValueError("Unsupported JSON structure")
    except Exception as e:
        raise Exception(f"Failed to load JSON file: {str(e)}")

def load_txt(file_path):
    """Load data from a text file."""
    try:
        # Try to detect the delimiter
        with open(file_path, 'r') as f:
            first_line = f.readline()
        
        if '\t' in first_line:
            delimiter = '\t'
        elif ';' in first_line:
            delimiter = ';'
        elif ',' in first_line:
            delimiter = ','
        else:
            delimiter = ' '  # Default to space
        
        return pd.read_csv(file_path, delimiter=delimiter)
    except Exception as e:
        raise Exception(f"Failed to load text file: {str(e)}")

def load_sqlite(file_path):
    """Load data from a SQLite database."""
    try:
        conn = sqlite3.connect(file_path)
        
        # Get list of tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            raise ValueError("No tables found in the SQLite database")
        
        # For simplicity, use the first table
        table_name = tables[0][0]
        
        # Load the table into a DataFrame
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        
        conn.close()
        return df
    except Exception as e:
        raise Exception(f"Failed to load SQLite database: {str(e)}")