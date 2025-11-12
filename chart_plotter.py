"""
Chart plotter module for the Chart Suggester application.
This module contains functions to generate various types of charts.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from utils import detect_column_type

def plot_chart(df, chart_type):
    """
    Generate a chart based on the dataframe and chart type.
    
    Args:
        df (pandas.DataFrame): The dataframe to plot
        chart_type (str): The type of chart to generate
        
    Returns:
        matplotlib.figure.Figure: The generated figure
    """
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.facecolor'] = 'white'
    
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
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Generate the appropriate chart based on the chart type
    if chart_type == 'Histogram':
        if numeric_cols:
            sns.histplot(data=df, x=numeric_cols[0], kde=True, ax=ax)
            ax.set_title(f'Histogram of {numeric_cols[0]}')
    
    elif chart_type == 'Box Plot':
        if numeric_cols:
            sns.boxplot(data=df, y=numeric_cols[0], ax=ax)
            ax.set_title(f'Box Plot of {numeric_cols[0]}')
    
    elif chart_type == 'Density Plot':
        if numeric_cols:
            sns.kdeplot(data=df, x=numeric_cols[0], ax=ax)
            ax.set_title(f'Density Plot of {numeric_cols[0]}')
    
    elif chart_type == 'Violin Plot':
        if numeric_cols:
            sns.violinplot(data=df, y=numeric_cols[0], ax=ax)
            ax.set_title(f'Violin Plot of {numeric_cols[0]}')
    
    elif chart_type == 'Bar Chart':
        if categorical_cols and numeric_cols:
            # Group by categorical column and aggregate numeric column
            grouped = df.groupby(categorical_cols[0])[numeric_cols[0]].mean().reset_index()
            sns.barplot(data=grouped, x=categorical_cols[0], y=numeric_cols[0], ax=ax)
            ax.set_title(f'Bar Chart: {numeric_cols[0]} by {categorical_cols[0]}')
            plt.xticks(rotation=45)
        elif categorical_cols:
            # Count of categorical values
            counts = df[categorical_cols[0]].value_counts().reset_index()
            counts.columns = [categorical_cols[0], 'count']
            sns.barplot(data=counts, x=categorical_cols[0], y='count', ax=ax)
            ax.set_title(f'Bar Chart: Count of {categorical_cols[0]}')
            plt.xticks(rotation=45)
        elif boolean_cols:
            # Count of boolean values
            counts = df[boolean_cols[0]].value_counts().reset_index()
            counts.columns = [boolean_cols[0], 'count']
            sns.barplot(data=counts, x=boolean_cols[0], y='count', ax=ax)
            ax.set_title(f'Bar Chart: Count of {boolean_cols[0]}')
    
    elif chart_type == 'Pie Chart':
        if categorical_cols and numeric_cols:
            # Group by categorical column and aggregate numeric column
            grouped = df.groupby(categorical_cols[0])[numeric_cols[0]].sum().reset_index()
            ax.pie(grouped[numeric_cols[0]], labels=grouped[categorical_cols[0]], autopct='%1.1f%%')
            ax.set_title(f'Pie Chart: {numeric_cols[0]} by {categorical_cols[0]}')
        elif categorical_cols:
            # Count of categorical values
            counts = df[categorical_cols[0]].value_counts()
            ax.pie(counts, labels=counts.index, autopct='%1.1f%%')
            ax.set_title(f'Pie Chart: Distribution of {categorical_cols[0]}')
        elif boolean_cols:
            # Count of boolean values
            counts = df[boolean_cols[0]].value_counts()
            ax.pie(counts, labels=counts.index, autopct='%1.1f%%')
            ax.set_title(f'Pie Chart: Distribution of {boolean_cols[0]}')
    
    elif chart_type == 'Count Plot':
        if categorical_cols:
            sns.countplot(data=df, x=categorical_cols[0], ax=ax)
            ax.set_title(f'Count Plot of {categorical_cols[0]}')
            plt.xticks(rotation=45)
        elif boolean_cols:
            sns.countplot(data=df, x=boolean_cols[0], ax=ax)
            ax.set_title(f'Count Plot of {boolean_cols[0]}')
    
    elif chart_type == 'Scatter Plot':
        if len(numeric_cols) >= 2:
            if categorical_cols:
                sns.scatterplot(data=df, x=numeric_cols[0], y=numeric_cols[1], hue=categorical_cols[0], ax=ax)
                ax.set_title(f'Scatter Plot: {numeric_cols[0]} vs {numeric_cols[1]} (by {categorical_cols[0]})')
            else:
                sns.scatterplot(data=df, x=numeric_cols[0], y=numeric_cols[1], ax=ax)
                ax.set_title(f'Scatter Plot: {numeric_cols[0]} vs {numeric_cols[1]}')
    
    elif chart_type == 'Scatter Plot (with hue)':
        if len(numeric_cols) >= 2 and categorical_cols:
            sns.scatterplot(data=df, x=numeric_cols[0], y=numeric_cols[1], hue=categorical_cols[0], ax=ax)
            ax.set_title(f'Scatter Plot: {numeric_cols[0]} vs {numeric_cols[1]} (by {categorical_cols[0]})')
    
    elif chart_type == 'Line Chart':
        if len(numeric_cols) >= 2:
            if categorical_cols:
                sns.lineplot(data=df, x=numeric_cols[0], y=numeric_cols[1], hue=categorical_cols[0], ax=ax)
                ax.set_title(f'Line Chart: {numeric_cols[0]} vs {numeric_cols[1]} (by {categorical_cols[0]})')
            else:
                sns.lineplot(data=df, x=numeric_cols[0], y=numeric_cols[1], ax=ax)
                ax.set_title(f'Line Chart: {numeric_cols[0]} vs {numeric_cols[1]}')
        elif datetime_cols and numeric_cols:
            sns.lineplot(data=df, x=datetime_cols[0], y=numeric_cols[0], ax=ax)
            ax.set_title(f'Line Chart: {numeric_cols[0]} over Time')
            plt.xticks(rotation=45)
    
    elif chart_type == 'Line Chart (with hue)':
        if len(numeric_cols) >= 2 and categorical_cols:
            sns.lineplot(data=df, x=numeric_cols[0], y=numeric_cols[1], hue=categorical_cols[0], ax=ax)
            ax.set_title(f'Line Chart: {numeric_cols[0]} vs {numeric_cols[1]} (by {categorical_cols[0]})')
    
    elif chart_type == 'Hexbin Plot':
        if len(numeric_cols) >= 2:
            ax.hexbin(df[numeric_cols[0]], df[numeric_cols[1]], gridsize=20, cmap='viridis')
            ax.set_title(f'Hexbin Plot: {numeric_cols[0]} vs {numeric_cols[1]}')
            ax.set_xlabel(numeric_cols[0])
            ax.set_ylabel(numeric_cols[1])
            plt.colorbar(ax.collections[0], ax=ax, label='count')
    
    elif chart_type == 'Bubble Chart':
        if len(numeric_cols) >= 3:
            scatter = ax.scatter(df[numeric_cols[0]], df[numeric_cols[1]], s=df[numeric_cols[2]]*10, alpha=0.5)
            ax.set_title(f'Bubble Chart: {numeric_cols[0]} vs {numeric_cols[1]} (size: {numeric_cols[2]})')
            ax.set_xlabel(numeric_cols[0])
            ax.set_ylabel(numeric_cols[1])
            plt.colorbar(scatter, ax=ax, label=numeric_cols[2])
    
    elif chart_type == 'Area Chart':
        if datetime_cols and numeric_cols:
            df_sorted = df.sort_values(datetime_cols[0])
            ax.fill_between(df_sorted[datetime_cols[0]], df_sorted[numeric_cols[0]], alpha=0.4)
            ax.plot(df_sorted[datetime_cols[0]], df_sorted[numeric_cols[0]])
            ax.set_title(f'Area Chart: {numeric_cols[0]} over Time')
            plt.xticks(rotation=45)
    
    elif chart_type == 'Swarm Plot':
        if categorical_cols and numeric_cols:
            sns.swarmplot(data=df, x=categorical_cols[0], y=numeric_cols[0], ax=ax)
            ax.set_title(f'Swarm Plot: {numeric_cols[0]} by {categorical_cols[0]}')
            plt.xticks(rotation=45)
    
    elif chart_type == 'Strip Plot':
        if categorical_cols and numeric_cols:
            sns.stripplot(data=df, x=categorical_cols[0], y=numeric_cols[0], ax=ax)
            ax.set_title(f'Strip Plot: {numeric_cols[0]} by {categorical_cols[0]}')
            plt.xticks(rotation=45)
    
    elif chart_type == 'Heatmap':
        if len(categorical_cols) >= 2:
            # Create a contingency table
            contingency_table = pd.crosstab(df[categorical_cols[0]], df[categorical_cols[1]])
            sns.heatmap(contingency_table, annot=True, fmt='d', cmap='viridis', ax=ax)
            ax.set_title(f'Heatmap: {categorical_cols[0]} vs {categorical_cols[1]}')
            plt.xticks(rotation=45)
            plt.yticks(rotation=0)
        elif len(boolean_cols) >= 1 and len(categorical_cols) >= 1:
            # Create a contingency table for boolean and categorical
            contingency_table = pd.crosstab(df[boolean_cols[0]], df[categorical_cols[0]])
            sns.heatmap(contingency_table, annot=True, fmt='d', cmap='viridis', ax=ax)
            ax.set_title(f'Heatmap: {boolean_cols[0]} vs {categorical_cols[0]}')
            plt.xticks(rotation=45)
            plt.yticks(rotation=0)
    
    elif chart_type == 'Stacked Bar Chart':
        if len(categorical_cols) >= 2:
            # Create a contingency table
            contingency_table = pd.crosstab(df[categorical_cols[0]], df[categorical_cols[1]])
            contingency_table.plot(kind='bar', stacked=True, ax=ax)
            ax.set_title(f'Stacked Bar Chart: {categorical_cols[0]} vs {categorical_cols[1]}')
            plt.xticks(rotation=45)
            plt.legend(title=categorical_cols[1])
        elif len(boolean_cols) >= 1 and len(categorical_cols) >= 1:
            # Create a contingency table for boolean and categorical
            contingency_table = pd.crosstab(df[categorical_cols[0]], df[boolean_cols[0]])
            contingency_table.plot(kind='bar', stacked=True, ax=ax)
            ax.set_title(f'Stacked Bar Chart: {categorical_cols[0]} vs {boolean_cols[0]}')
            plt.xticks(rotation=45)
            plt.legend(title=boolean_cols[0])
    
    elif chart_type == 'Time Series Plot':
        if datetime_cols:
            if numeric_cols:
                for num_col in numeric_cols:
                    ax.plot(df[datetime_cols[0]], df[num_col], label=num_col)
                ax.set_title(f'Time Series Plot of Numeric Variables')
                ax.set_xlabel(datetime_cols[0])
                ax.legend()
                plt.xticks(rotation=45)
            else:
                # If no numeric columns, count occurrences over time
                counts = df.groupby(datetime_cols[0]).size().reset_index(name='count')
                ax.plot(counts[datetime_cols[0]], counts['count'])
                ax.set_title(f'Time Series Plot: Count over Time')
                ax.set_xlabel(datetime_cols[0])
                ax.set_ylabel('Count')
                plt.xticks(rotation=45)
    
    elif chart_type == 'Bar Chart over Time':
        if datetime_cols and categorical_cols:
            # Group by time period and category
            df_copy = df.copy()
            # Extract time period (e.g., year, month) based on data range
            date_range = (df[datetime_cols[0]].max() - df[datetime_cols[0]].min()).days
            if date_range > 365 * 5:  # More than 5 years, group by year
                df_copy['time_period'] = df_copy[datetime_cols[0]].dt.year
                period_name = 'Year'
            elif date_range > 60:  # More than 2 months, group by month
                df_copy['time_period'] = df_copy[datetime_cols[0]].dt.to_period('M').astype(str)
                period_name = 'Month'
            else:  # Less than 2 months, group by day
                df_copy['time_period'] = df_copy[datetime_cols[0]].dt.date
                period_name = 'Day'
            
            # Count occurrences by time period and category
            counts = df_copy.groupby(['time_period', categorical_cols[0]]).size().reset_index(name='count')
            
            # Create bar chart
            sns.barplot(data=counts, x='time_period', y='count', hue=categorical_cols[0], ax=ax)
            ax.set_title(f'Bar Chart: {categorical_cols[0]} over Time (by {period_name})')
            ax.set_xlabel(period_name)
            plt.xticks(rotation=45)
    
    elif chart_type == 'Joint Plot':
        if len(numeric_cols) >= 2:
            # Create a joint plot using seaborn
            joint_plot = sns.jointplot(data=df, x=numeric_cols[0], y=numeric_cols[1], kind='scatter')
            joint_plot.fig.suptitle(f'Joint Plot: {numeric_cols[0]} vs {numeric_cols[1]}', y=1.02)
            return joint_plot.fig
    
    elif chart_type == 'Pair Plot':
        if len(numeric_cols) >= 2:
            # Create a pair plot using seaborn
            pair_plot = sns.pairplot(df[numeric_cols])
            pair_plot.fig.suptitle('Pair Plot of Numeric Variables', y=1.02)
            return pair_plot.fig
    
    elif chart_type == 'Facet Grid':
        if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
            # Create a facet grid using seaborn
            g = sns.FacetGrid(df, col=categorical_cols[0])
            g.map(plt.hist, numeric_cols[0])
            g.fig.suptitle(f'Facet Grid: {numeric_cols[0]} by {categorical_cols[0]}', y=1.02)
            return g.fig
    
    elif chart_type == 'Text Length Histogram':
        if text_cols:
            # Calculate text lengths
            text_lengths = df[text_cols[0]].astype(str).str.len()
            sns.histplot(text_lengths, kde=True, ax=ax)
            ax.set_title(f'Text Length Histogram of {text_cols[0]}')
            ax.set_xlabel('Text Length')
    
    elif chart_type == 'Text Length Comparison':
        if len(text_cols) >= 2:
            # Calculate text lengths for both columns
            df_melted = pd.melt(
                df[text_cols].apply(lambda col: col.astype(str).str.len()).reset_index(),
                id_vars=['index'],
                value_vars=text_cols,
                var_name='column',
                value_name='length'
            )
            sns.boxplot(data=df_melted, x='column', y='length', ax=ax)
            ax.set_title('Text Length Comparison')
            plt.xticks(rotation=45)
    
    elif chart_type == 'Word Cloud':
        if text_cols:
            try:
                from wordcloud import WordCloud
                
                # Combine all text
                text = ' '.join(df[text_cols[0]].astype(str))
                
                # Generate word cloud
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
                
                # Display word cloud
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                ax.set_title(f'Word Cloud of {text_cols[0]}')
            except ImportError:
                # If wordcloud is not installed, show a message
                ax.text(0.5, 0.5, 'Word Cloud requires the "wordcloud" package.\nInstall it with: pip install wordcloud', 
                       ha='center', va='center', fontsize=12)
                ax.axis('off')
    
    elif chart_type == 'Word Cloud Comparison':
        if len(text_cols) >= 2:
            try:
                from wordcloud import WordCloud
                
                # Create subplots
                fig, axes = plt.subplots(1, len(text_cols), figsize=(15, 6))
                if len(text_cols) == 1:
                    axes = [axes]  # Make it iterable
                
                for i, col in enumerate(text_cols):
                    # Combine all text
                    text = ' '.join(df[col].astype(str))
                    
                    # Generate word cloud
                    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
                    
                    # Display word cloud
                    axes[i].imshow(wordcloud, interpolation='bilinear')
                    axes[i].axis('off')
                    axes[i].set_title(f'Word Cloud of {col}')
                
                plt.tight_layout()
                return fig
            except ImportError:
                # If wordcloud is not installed, show a message
                ax.text(0.5, 0.5, 'Word Cloud requires the "wordcloud" package.\nInstall it with: pip install wordcloud', 
                       ha='center', va='center', fontsize=12)
                ax.axis('off')
    
    elif chart_type == 'Event Timeline':
        if datetime_cols:
            # Create a timeline of events
            df_sorted = df.sort_values(datetime_cols[0])
            
            # Create a scatter plot with y-values as 1 for all points
            ax.scatter(df_sorted[datetime_cols[0]], [1] * len(df_sorted), alpha=0.5)
            
            # Add labels if there's a text column
            if text_cols:
                for i, row in df_sorted.iterrows():
                    ax.text(row[datetime_cols[0]], 1.02, str(row[text_cols[0]])[:20] + '...', 
                           rotation=45, ha='left', va='bottom', fontsize=8)
            
            ax.set_title('Event Timeline')
            ax.set_xlabel(datetime_cols[0])
            ax.set_yticks([])
            plt.xticks(rotation=45)
    
    elif chart_type == 'Table View':
        ax.axis('off')
        table = ax.table(cellText=df.head(10).values, 
                         colLabels=df.columns, 
                         cellLoc='center', 
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.5)
        ax.set_title('Data Table View (First 10 Rows)')
    
    else:
        # Default to a simple bar chart of the first column
        if df.columns:
            col = df.columns[0]
            if column_types[col] == 'numeric':
                sns.histplot(data=df, x=col, ax=ax)
            else:
                counts = df[col].value_counts().reset_index()
                counts.columns = [col, 'count']
                sns.barplot(data=counts, x=col, y='count', ax=ax)
                plt.xticks(rotation=45)
            ax.set_title(f'Chart of {col}')
    
    # Adjust layout
    plt.tight_layout()
    
    return fig