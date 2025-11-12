"""
Utils module for the Chart Suggester application.
This module contains helper functions used across the application.
"""

import pandas as pd
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox
import re
from datetime import datetime

def get_file_extension(file_path):
    """
    Get the file extension from a file path.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: The file extension including the dot (e.g., '.csv')
    """
    return os.path.splitext(file_path)[1].lower()

def is_numeric(series):
    """
    Check if a series contains numeric data.
    
    Args:
        series (pandas.Series): The series to check
        
    Returns:
        bool: True if the series is numeric
    """
    # First check if the dtype is already numeric
    if np.issubdtype(series.dtype, np.number):
        return True
    
    # Try to convert to numeric
    try:
        pd.to_numeric(series, errors='raise')
        return True
    except:
        return False

def is_datetime(series):
    """
    Check if a series contains datetime data.
    
    Args:
        series (pandas.Series): The series to check.
        
    Returns:
        bool: True if the series is datetime
    """
    # First check if the dtype is already datetime
    if np.issubdtype(series.dtype, np.datetime64):
        return True
    
    # Try to convert to datetime
    try:
        pd.to_datetime(series, errors='raise')
        return True
    except:
        return False

def is_categorical(series):
    """
    Check if a series contains categorical data.
    
    Args:
        series (pandas.Series): The series to check
        
    Returns:
        bool: True if the series is categorical
    """
    # If it's numeric or datetime, it's not categorical
    if is_numeric(series) or is_datetime(series):
        return False
    
    # Check if it's a string type
    if pd.api.types.is_string_dtype(series):
        # Check if the number of unique values is small compared to the total number of values
        unique_count = series.nunique()
        total_count = len(series)
        
        # If there are many unique values, but they're all short strings, it might still be categorical
        if unique_count > 10:
            avg_length = series.astype(str).str.len().mean()
            if avg_length <= 10:
                return True
        
        # If the ratio of unique values to total values is small, it's likely categorical
        if unique_count / total_count < 0.05 or unique_count <= 20:
            return True
    
    # Check if it's already a categorical type
    if pd.api.types.is_categorical_dtype(series):
        return True
    
    return False

def is_boolean(series):
    """
    Check if a series contains boolean data.
    
    Args:
        series (pandas.Series): The series to check
        
    Returns:
        bool: True if the series is boolean
    """
    # Check if it's already a boolean type
    if pd.api.types.is_bool_dtype(series):
        return True
    
    # Check if the values are all boolean-like
    unique_values = set(series.dropna().unique())
    boolean_values = {True, False, 'true', 'false', 'yes', 'no', 'y', 'n', '1', '0'}
    
    # If all unique values are in the boolean values set, it's likely boolean
    if unique_values.issubset(boolean_values):
        return True
    
    return False

def is_text(series):
    """
    Check if a series contains text data.
    
    Args:
        series (pandas.Series): The series to check
        
    Returns:
        bool: True if the series is text
    """
    # If it's already identified as another type, it's not text
    if is_numeric(series) or is_datetime(series) or is_categorical(series) or is_boolean(series):
        return False
    
    # Check if it's a string type
    if pd.api.types.is_string_dtype(series):
        # Check if the values are typically longer strings
        avg_length = series.astype(str).str.len().mean()
        if avg_length > 10:
            return True
    
    return False

def detect_column_type(series):
    """
    Detect the type of a column (numeric, categorical, datetime, boolean, text, etc.).
    
    Args:
        series (pandas.Series): The column to analyze
        
    Returns:
        str: The detected type ('numeric', 'categorical', 'datetime', 'boolean', 'text', or 'other')
    """
    # Check for boolean first (most specific)
    if is_boolean(series):
        return 'boolean'
    
    # Check for numeric
    if is_numeric(series):
        # Check if it's actually categorical (few unique values)
        unique_count = series.nunique()
        if unique_count <= 10 and unique_count / len(series) < 0.05:
            return 'categorical'
        return 'numeric'
    
    # Check for datetime
    if is_datetime(series):
        return 'datetime'
    
    # Check for categorical
    if is_categorical(series):
        return 'categorical'
    
    # Check for text
    if is_text(series):
        return 'text'
    
    # Default to 'other'
    return 'other'

def safe_divide(numerator, denominator):
    """
    Safely divide two numbers, handling division by zero.
    
    Args:
        numerator: The numerator
        denominator: The denominator
        
    Returns:
        float: The result of the division, or 0 if denominator is 0
    """
    try:
        if denominator == 0:
            return 0
        return numerator / denominator
    except:
        return 0

def get_column_statistics(series, data_type):
    """
    Get statistics for a column based on its data type.
    
    Args:
        series (pandas.Series): The column to analyze
        data_type (str): The detected data type
        
    Returns:
        dict: A dictionary of statistics
    """
    stats = {
        'count': len(series),
        'null_count': series.isnull().sum(),
        'null_percentage': safe_divide(series.isnull().sum(), len(series)) * 100,
        'unique_count': series.nunique(),
        'unique_percentage': safe_divide(series.nunique(), len(series)) * 100
    }
    
    if data_type == 'numeric':
        try:
            stats.update({
                'min': series.min(),
                'max': series.max(),
                'mean': series.mean(),
                'median': series.median(),
                'std': series.std(),
                'quartiles': {
                    '25%': series.quantile(0.25),
                    '50%': series.quantile(0.5),
                    '75%': series.quantile(0.75)
                }
            })
        except:
            stats.update({
                'min': None,
                'max': None,
                'mean': None,
                'median': None,
                'std': None,
                'quartiles': {
                    '25%': None,
                    '50%': None,
                    '75%': None
                }
            })
    
    elif data_type == 'categorical':
        try:
            # Get value counts
            value_counts = series.value_counts()
            stats.update({
                'most_common': value_counts.index[0] if len(value_counts) > 0 else None,
                'most_common_count': value_counts.iloc[0] if len(value_counts) > 0 else 0,
                'least_common': value_counts.index[-1] if len(value_counts) > 0 else None,
                'least_common_count': value_counts.iloc[-1] if len(value_counts) > 0 else 0
            })
        except:
            stats.update({
                'most_common': None,
                'most_common_count': 0,
                'least_common': None,
                'least_common_count': 0
            })
    
    elif data_type == 'datetime':
        try:
            stats.update({
                'min_date': series.min(),
                'max_date': series.max(),
                'date_range': (series.max() - series.min()).days
            })
        except:
            stats.update({
                'min_date': None,
                'max_date': None,
                'date_range': None
            })
    
    elif data_type == 'boolean':
        try:
            # Count True/False values
            true_count = series.sum() if series.dtype == bool else series.astype(bool).sum()
            false_count = len(series) - true_count - series.isnull().sum()
            stats.update({
                'true_count': true_count,
                'false_count': false_count,
                'true_percentage': safe_divide(true_count, (true_count + false_count)) * 100
            })
        except:
            stats.update({
                'true_count': 0,
                'false_count': 0,
                'true_percentage': 0
            })
    
    elif data_type == 'text':
        try:
            # Get text statistics
            text_lengths = series.astype(str).str.len()
            stats.update({
                'min_length': text_lengths.min(),
                'max_length': text_lengths.max(),
                'avg_length': text_lengths.mean(),
                'median_length': text_lengths.median()
            })
        except:
            stats.update({
                'min_length': 0,
                'max_length': 0,
                'avg_length': 0,
                'median_length': 0
            })
    
    return stats

def reset_app():
    """
    Reset the application to its initial state.
    This function is called from the UI module.
    """
    # This function is implemented in ui.py as reset_app_ui
    # It's defined here for completeness, but the actual implementation is in ui.py
    pass