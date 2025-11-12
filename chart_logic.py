"""
Chart logic module for the Chart Suggester application.
This module contains functions to analyze data and suggest appropriate chart types.
"""

import pandas as pd
import numpy as np
from utils import detect_column_type, get_column_statistics

def analyze_data(df):
    """
    Analyze the dataset and return information about columns and types.
    
    Args:
        df (pandas.DataFrame): The dataframe to analyze
        
    Returns:
        dict: A dictionary containing analysis results
    """
    # Get basic info
    num_rows, num_columns = df.shape
    
    # Detect column types and get statistics
    column_info = {}
    for col in df.columns:
        data_type = detect_column_type(df[col])
        statistics = get_column_statistics(df[col], data_type)
        
        column_info[col] = {
            'type': data_type,
            'statistics': statistics
        }
    
    # Count columns by type
    type_counts = {
        'numeric': 0,
        'categorical': 0,
        'datetime': 0,
        'boolean': 0,
        'text': 0,
        'other': 0
    }
    
    for col_info in column_info.values():
        col_type = col_info['type']
        if col_type in type_counts:
            type_counts[col_type] += 1
    
    # Return analysis results
    return {
        'num_rows': num_rows,
        'num_columns': num_columns,
        'column_info': column_info,
        'type_counts': type_counts
    }

def suggest_chart(df):
    """
    Suggest appropriate chart types based on the data.
    
    Args:
        df (pandas.DataFrame): The dataframe to analyze
        
    Returns:
        list: A list of suggested chart types
    """
    # Get column types
    column_types = {}
    for col in df.columns:
        column_types[col] = detect_column_type(df[col])
    
    # Count columns by type
    numeric_cols = [col for col, dtype in column_types.items() if dtype == 'numeric']
    categorical_cols = [col for col, dtype in column_types.items() if dtype == 'categorical']
    datetime_cols = [col for col, dtype in column_types.items() if dtype == 'datetime']
    boolean_cols = [col for col, dtype in column_types.items() if dtype == 'boolean']
    text_cols = [col for col, dtype in column_types.items() if dtype == 'text']
    
    suggestions = []
    
    # Case 1: Single numeric column
    if len(numeric_cols) == 1 and len(categorical_cols) == 0 and len(datetime_cols) == 0:
        suggestions.extend(['Histogram', 'Box Plot', 'Density Plot', 'Violin Plot'])
    
    # Case 2: Single categorical column
    elif len(categorical_cols) == 1 and len(numeric_cols) == 0 and len(datetime_cols) == 0:
        suggestions.extend(['Bar Chart', 'Pie Chart', 'Count Plot'])
    
    # Case 3: Single boolean column
    elif len(boolean_cols) == 1 and len(numeric_cols) == 0 and len(categorical_cols) == 0 and len(datetime_cols) == 0:
        suggestions.extend(['Bar Chart', 'Pie Chart'])
    
    # Case 4: Single datetime column
    elif len(datetime_cols) == 1 and len(numeric_cols) == 0 and len(categorical_cols) == 0:
        suggestions.extend(['Time Series Plot', 'Histogram'])
    
    # Case 5: Two numeric columns
    elif len(numeric_cols) >= 2 and len(categorical_cols) == 0 and len(datetime_cols) == 0:
        suggestions.extend(['Scatter Plot', 'Line Chart', 'Hexbin Plot', 'Joint Plot'])
        if len(numeric_cols) >= 3:
            suggestions.append('Bubble Chart')
    
    # Case 6: One categorical and one numeric column
    elif len(categorical_cols) >= 1 and len(numeric_cols) >= 1 and len(datetime_cols) == 0:
        suggestions.extend(['Bar Chart', 'Box Plot', 'Violin Plot', 'Swarm Plot', 'Strip Plot'])
        if len(categorical_cols) == 1 and len(numeric_cols) == 1:
            suggestions.append('Pie Chart')
    
    # Case 7: Datetime and numeric columns
    elif len(datetime_cols) >= 1 and len(numeric_cols) >= 1:
        suggestions.extend(['Line Chart', 'Area Chart', 'Time Series Plot'])
    
    # Case 8: Boolean and numeric columns
    elif len(boolean_cols) >= 1 and len(numeric_cols) >= 1:
        suggestions.extend(['Box Plot', 'Violin Plot', 'Bar Chart'])
    
    # Case 9: Categorical and boolean columns
    elif len(categorical_cols) >= 1 and len(boolean_cols) >= 1:
        suggestions.extend(['Bar Chart', 'Heatmap', 'Stacked Bar Chart'])
    
    # Case 10: Datetime and categorical columns
    elif len(datetime_cols) >= 1 and len(categorical_cols) >= 1:
        suggestions.extend(['Line Chart', 'Bar Chart over Time'])
    
    # Case 11: Multiple columns of mixed types
    elif len(numeric_cols) >= 2 and len(categorical_cols) >= 1:
        suggestions.extend(['Scatter Plot (with hue)', 'Line Chart (with hue)', 'Pair Plot', 'Facet Grid'])
    
    # Case 12: Text columns
    elif len(text_cols) >= 1:
        if len(text_cols) == 1:
            suggestions.extend(['Word Cloud', 'Text Length Histogram'])
        elif len(text_cols) >= 2:
            suggestions.extend(['Word Cloud Comparison', 'Text Length Comparison'])
    
    # Case 13: Only datetime columns
    elif len(datetime_cols) >= 1 and len(numeric_cols) == 0:
        suggestions.extend(['Time Series Plot', 'Event Timeline'])
    
    # Default case
    else:
        suggestions.extend(['Table View'])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_suggestions = []
    for suggestion in suggestions:
        if suggestion not in seen:
            seen.add(suggestion)
            unique_suggestions.append(suggestion)
    
    return unique_suggestions

def suggest_chart_for_columns(df, selected_columns):
    """
    Suggest appropriate chart types based on the selected columns.
    
    Args:
        df (pandas.DataFrame): The dataframe to analyze
        selected_columns (list): List of selected column names
        
    Returns:
        list: A list of suggested chart types
    """
    # Create a subset dataframe with only selected columns
    subset_df = df[selected_columns]
    
    # Get column types for selected columns
    column_types = {}
    for col in selected_columns:
        column_types[col] = detect_column_type(df[col])
    
    # Count columns by type
    numeric_cols = [col for col, dtype in column_types.items() if dtype == 'numeric']
    categorical_cols = [col for col, dtype in column_types.items() if dtype == 'categorical']
    datetime_cols = [col for col, dtype in column_types.items() if dtype == 'datetime']
    boolean_cols = [col for col, dtype in column_types.items() if dtype == 'boolean']
    text_cols = [col for col, dtype in column_types.items() if dtype == 'text']
    
    suggestions = []
    
    # Case 1: Only one column selected
    if len(selected_columns) == 1:
        col_type = column_types[selected_columns[0]]
        
        if col_type == 'numeric':
            suggestions.extend(['Histogram', 'Box Plot', 'Density Plot', 'Violin Plot'])
        elif col_type == 'categorical':
            suggestions.extend(['Bar Chart', 'Pie Chart', 'Count Plot'])
        elif col_type == 'datetime':
            suggestions.extend(['Time Series Plot', 'Histogram'])
        elif col_type == 'boolean':
            suggestions.extend(['Bar Chart', 'Pie Chart'])
        elif col_type == 'text':
            suggestions.extend(['Word Cloud', 'Text Length Histogram'])
        else:
            suggestions.extend(['Table View'])
    
    # Case 2: Two columns selected
    elif len(selected_columns) == 2:
        x_col, y_col = selected_columns
        x_type = column_types[x_col]
        y_type = column_types[y_col]
        
        # Numeric vs Numeric
        if x_type == 'numeric' and y_type == 'numeric':
            suggestions.extend(['Scatter Plot', 'Line Chart', 'Hexbin Plot', 'Joint Plot'])
        
        # Categorical vs Numeric
        elif (x_type == 'categorical' and y_type == 'numeric') or (x_type == 'numeric' and y_type == 'categorical'):
            suggestions.extend(['Bar Chart', 'Box Plot', 'Violin Plot', 'Swarm Plot', 'Strip Plot'])
        
        # Categorical vs Categorical
        elif x_type == 'categorical' and y_type == 'categorical':
            suggestions.extend(['Bar Chart', 'Heatmap', 'Stacked Bar Chart'])
        
        # Datetime vs Numeric
        elif (x_type == 'datetime' and y_type == 'numeric') or (x_type == 'numeric' and y_type == 'datetime'):
            suggestions.extend(['Line Chart', 'Area Chart', 'Time Series Plot'])
        
        # Datetime vs Categorical
        elif (x_type == 'datetime' and y_type == 'categorical') or (x_type == 'categorical' and y_type == 'datetime'):
            suggestions.extend(['Line Chart', 'Bar Chart over Time'])
        
        # Boolean vs Numeric
        elif (x_type == 'boolean' and y_type == 'numeric') or (x_type == 'numeric' and y_type == 'boolean'):
            suggestions.extend(['Box Plot', 'Violin Plot', 'Bar Chart'])
        
        # Boolean vs Categorical
        elif (x_type == 'boolean' and y_type == 'categorical') or (x_type == 'categorical' and y_type == 'boolean'):
            suggestions.extend(['Bar Chart', 'Heatmap', 'Stacked Bar Chart'])
        
        # Text vs Numeric
        elif (x_type == 'text' and y_type == 'numeric') or (x_type == 'numeric' and y_type == 'text'):
            suggestions.extend(['Bar Chart', 'Scatter Plot'])
        
        # Text vs Categorical
        elif (x_type == 'text' and y_type == 'categorical') or (x_type == 'categorical' and y_type == 'text'):
            suggestions.extend(['Bar Chart', 'Heatmap'])
        
        # Other combinations
        else:
            suggestions.extend(['Table View'])
    
    # Case 3: More than two columns selected
    else:
        # If we have at least two numeric columns
        if len(numeric_cols) >= 2:
            suggestions.extend(['Scatter Plot', 'Line Chart'])
            
            # If we also have a categorical column
            if categorical_cols:
                suggestions.extend(['Scatter Plot (with hue)', 'Line Chart (with hue)'])
            
            # If we have three numeric columns
            if len(numeric_cols) >= 3:
                suggestions.append('Bubble Chart')
        
        # If we have at least one categorical and one numeric
        elif categorical_cols and numeric_cols:
            suggestions.extend(['Bar Chart', 'Box Plot', 'Violin Plot', 'Swarm Plot'])
        
        # If we have datetime columns
        elif datetime_cols:
            if numeric_cols:
                suggestions.extend(['Line Chart', 'Area Chart'])
            elif categorical_cols:
                suggestions.extend(['Line Chart', 'Bar Chart over Time'])
            else:
                suggestions.extend(['Time Series Plot'])
        
        # If we have boolean columns
        elif boolean_cols:
            if numeric_cols:
                suggestions.extend(['Box Plot', 'Violin Plot', 'Bar Chart'])
            elif categorical_cols:
                suggestions.extend(['Bar Chart', 'Heatmap', 'Stacked Bar Chart'])
        
        # If we have text columns
        elif text_cols:
            if len(text_cols) == 1:
                suggestions.extend(['Word Cloud', 'Text Length Histogram'])
            else:
                suggestions.extend(['Word Cloud Comparison', 'Text Length Comparison'])
        
        # Default case
        else:
            suggestions.extend(['Table View'])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_suggestions = []
    for suggestion in suggestions:
        if suggestion not in seen:
            seen.add(suggestion)
            unique_suggestions.append(suggestion)
    
    return unique_suggestions