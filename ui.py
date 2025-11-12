"""
UI module for the Chart Suggester application.
This module contains all the UI-related functions and components.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Import other modules
from data_loader import load_data
from chart_logic import analyze_data, suggest_chart_for_columns
from chart_plotter import plot_chart
from utils import get_file_extension, reset_app

# Global variables to store application state
current_df = None
current_chart_type = None
chart_suggestions = []
file_path = None
selected_columns = []

def setup_styles(root):
    """Set up the styles for the application."""
    # Configure styles
    root.configure(bg="#f5f5f5")
    
    # Set the theme color
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure styles for buttons
    style.configure('TButton', font=('Helvetica', 10), borderwidth=0)
    style.map('TButton', 
              foreground=[('pressed', 'white'), ('active', 'white')],
              background=[('pressed', '#4a6fa5'), ('active', '#5a7fb5')])
    
    # Configure styles for frames
    style.configure('TFrame', background='#f5f5f5')
    
    # Configure styles for labels
    style.configure('TLabel', background='#f5f5f5', font=('Helvetica', 10))
    
    # Configure styles for headers
    style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), background='#f5f5f5')
    
    # Configure styles for section headers
    style.configure('SectionHeader.TLabel', font=('Helvetica', 12, 'bold'), background='#f5f5f5')

def create_main_window(root):
    """Create the main window layout."""
    # Create main container
    main_container = ttk.Frame(root)
    main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    # Create header
    header_frame = ttk.Frame(main_container)
    header_frame.pack(fill=tk.X, pady=(0, 15))
    
    # Try to load the icon
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
        icon_image = Image.open(icon_path)
        icon_image = icon_image.resize((40, 40), Image.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_image)
        root.iconphoto(False, icon_photo)
        
        icon_label = ttk.Label(header_frame, image=icon_photo)
        icon_label.image = icon_photo  # Keep a reference
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
    except:
        # If icon can't be loaded, continue without it
        pass
    
    title_label = ttk.Label(header_frame, text="Chart Suggester", style='Header.TLabel')
    title_label.pack(side=tk.LEFT)
    
    # Create content area with sidebar and main display
    content_frame = ttk.Frame(main_container)
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create sidebar
    sidebar_frame = ttk.Frame(content_frame, width=300)
    sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
    
    # Create main display area
    display_frame = ttk.Frame(content_frame)
    display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Populate sidebar
    create_sidebar(sidebar_frame)
    
    # Populate main display area
    create_display_area(display_frame)

def create_sidebar(parent):
    """Create the sidebar with controls."""
    # File upload section
    file_frame = ttk.LabelFrame(parent, text="Data Source", padding=5)
    file_frame.pack(fill=tk.X, pady=(0, 5))
    
    upload_button = ttk.Button(file_frame, text="Upload File", command=upload_file)
    upload_button.pack(fill=tk.X, pady=(0, 5))
    
    # File info label
    global file_info_label
    file_info_label = ttk.Label(file_frame, text="No file selected", wraplength=280)
    file_info_label.pack(fill=tk.X)
    
    # Analysis section
    analysis_frame = ttk.LabelFrame(parent, text="Data Analysis", padding=10)
    analysis_frame.pack(fill=tk.X, pady=(0, 5))
    
    analyze_button = ttk.Button(analysis_frame, text="Analyze Data", command=analyze_data_ui)
    analyze_button.pack(fill=tk.X, pady=(0, 5))
    
    # Data info text
    global data_info_text
    data_info_text = tk.Text(analysis_frame, height=12, width=30, wrap=tk.WORD, bg="#f9f9f9")
    data_info_text.pack(fill=tk.X)
    data_info_text.config(state=tk.DISABLED)
    
    # Column selection section
    column_frame = ttk.LabelFrame(parent, text="Column Selection", padding=5)
    column_frame.pack(fill=tk.X, pady=(0, 5))
    
    # X-axis column dropdown
    ttk.Label(column_frame, text="X-axis:").pack(anchor=tk.W)
    global x_column_var
    x_column_var = tk.StringVar()
    global x_column_dropdown
    x_column_dropdown = ttk.Combobox(column_frame, textvariable=x_column_var, state="readonly")
    x_column_dropdown.pack(fill=tk.X, pady=(0, 5))
    x_column_dropdown.bind("<<ComboboxSelected>>", on_x_column_selected)
    
    # Y-axis column dropdown
    ttk.Label(column_frame, text="Y-axis (optional):").pack(anchor=tk.W)
    global y_column_var
    y_column_var = tk.StringVar()
    global y_column_dropdown
    y_column_dropdown = ttk.Combobox(column_frame, textvariable=y_column_var, state="readonly")
    y_column_dropdown.pack(fill=tk.X, pady=(0, 5))
    y_column_dropdown.bind("<<ComboboxSelected>>", on_y_column_selected)
    
    # Chart selection section
    chart_frame = ttk.LabelFrame(parent, text="Chart Selection", padding=10)
    chart_frame.pack(fill=tk.X, pady=(0, 5))
    
    # Chart type dropdown
    global chart_type_var
    chart_type_var = tk.StringVar()
    chart_type_var.set("Select chart type")
    
    global chart_type_dropdown
    chart_type_dropdown = ttk.Combobox(chart_frame, textvariable=chart_type_var, state="readonly")
    chart_type_dropdown.pack(fill=tk.X, pady=(0, 5))
    chart_type_dropdown.bind("<<ComboboxSelected>>", on_chart_type_selected)
    
    # Generate chart button
    generate_button = ttk.Button(chart_frame, text="Generate Chart", command=generate_chart)
    generate_button.pack(fill=tk.X, pady=(0, 5))
    
    # Save chart button
    save_button = ttk.Button(chart_frame, text="Save Chart", command=save_chart)
    save_button.pack(fill=tk.X, pady=(0, 5))
    
    # Reset button
    reset_button = ttk.Button(chart_frame, text="Reset", command=reset_app_ui)
    reset_button.pack(fill=tk.X)

def create_display_area(parent):
    """Create the main display area for charts."""
    # Create a frame for the chart
    global chart_frame
    chart_frame = ttk.Frame(parent)
    chart_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create a placeholder label
    global placeholder_label
    placeholder_label = ttk.Label(chart_frame, text="Upload a file and analyze data to generate charts", 
                                  font=('Helvetica', 12), anchor=tk.CENTER)
    placeholder_label.pack(expand=True)

def upload_file():
    """Handle file upload."""
    global file_path, current_df
    
    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select a data file",
        filetypes=[
            ("All supported files", "*.csv;*.xlsx;*.xls;*.json;*.txt;*.db"),
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx;*.xls"),
            ("JSON files", "*.json"),
            ("Text files", "*.txt"),
            ("SQLite files", "*.db")
        ]
    )
    
    if not file_path:
        return
    
    # Update file info label
    file_name = os.path.basename(file_path)
    file_info_label.config(text=f"Selected: {file_name}")
    
    try:
        # Load the data
        current_df = load_data(file_path)
        messagebox.showinfo("Success", f"File '{file_name}' loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {str(e)}")
        current_df = None
        file_info_label.config(text="No file selected")

def format_number(value):
    """Format a number with thousands separators, handling None and non-numeric values."""
    if value is None:
        return "N/A"
    
    try:
        if isinstance(value, (int, float)):
            if isinstance(value, int) or value.is_integer():
                return f"{int(value):,}"
            else:
                return f"{value:,.2f}"
        return str(value)
    except:
        return str(value)

def analyze_data_ui():
    """Handle data analysis in the UI."""
    global current_df
    
    if current_df is None:
        messagebox.showwarning("Warning", "Please upload a file first!")
        return
    
    try:
        # Analyze the data
        data_info = analyze_data(current_df)
        
        # Update data info text
        data_info_text.config(state=tk.NORMAL)
        data_info_text.delete(1.0, tk.END)
        
        # Format data info
        info_text = f"Rows: {format_number(data_info['num_rows'])}\n"
        info_text += f"Columns: {format_number(data_info['num_columns'])}\n\n"
        info_text += "Column Types:\n"
        
        for col, col_info in data_info['column_info'].items():
            col_type = col_info['type']
            stats = col_info['statistics']
            
            info_text += f"\n{col} ({col_type}):\n"
            info_text += f"  - Values: {format_number(stats['count'])}\n"
            info_text += f"  - Null: {format_number(stats['null_count'])} ({format_number(stats['null_percentage'])}%)\n"
            info_text += f"  - Unique: {format_number(stats['unique_count'])} ({format_number(stats['unique_percentage'])}%)\n"
            
            # Add type-specific statistics
            if col_type == 'numeric':
                info_text += f"  - Min: {format_number(stats['min'])}\n"
                info_text += f"  - Max: {format_number(stats['max'])}\n"
                info_text += f"  - Mean: {format_number(stats['mean'])}\n"
                info_text += f"  - Median: {format_number(stats['median'])}\n"
                info_text += f"  - Std Dev: {format_number(stats['std'])}\n"
            elif col_type == 'categorical':
                info_text += f"  - Most common: {stats['most_common']} ({format_number(stats['most_common_count'])})\n"
                info_text += f"  - Least common: {stats['least_common']} ({format_number(stats['least_common_count'])})\n"
            elif col_type == 'datetime':
                try:
                    info_text += f"  - Min date: {stats['min_date'].strftime('%Y-%m-%d')}\n"
                    info_text += f"  - Max date: {stats['max_date'].strftime('%Y-%m-%d')}\n"
                    info_text += f"  - Date range: {format_number(stats['date_range'])} days\n"
                except:
                    info_text += f"  - Date information unavailable\n"
            elif col_type == 'boolean':
                info_text += f"  - True: {format_number(stats['true_count'])} ({format_number(stats['true_percentage'])}%)\n"
                info_text += f"  - False: {format_number(stats['false_count'])}\n"
            elif col_type == 'text':
                info_text += f"  - Min length: {format_number(stats['min_length'])}\n"
                info_text += f"  - Max length: {format_number(stats['max_length'])}\n"
                info_text += f"  - Avg length: {format_number(stats['avg_length'])}\n"
        
        data_info_text.insert(1.0, info_text)
        data_info_text.config(state=tk.DISABLED)
        
        # Update column dropdowns
        columns = list(current_df.columns)
        x_column_dropdown['values'] = columns
        y_column_dropdown['values'] = ["None"] + columns  # Add "None" option for single-column charts
        
        messagebox.showinfo("Analysis Complete", "Data analysis completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to analyze data: {str(e)}")

def on_x_column_selected(event):
    """Handle X-axis column selection."""
    global selected_columns
    
    # Get selected X column
    x_col = x_column_var.get()
    
    if not x_col:
        return
    
    # Reset Y column selection
    y_column_var.set("None")
    
    # Update selected columns
    selected_columns = [x_col]
    
    # Update chart suggestions based on selected X column only
    update_chart_suggestions()

def on_y_column_selected(event):
    """Handle Y-axis column selection."""
    global selected_columns
    
    # Get selected columns
    x_col = x_column_var.get()
    y_col = y_column_var.get()
    
    if not x_col:
        messagebox.showwarning("Warning", "Please select an X-axis column first!")
        y_column_var.set("None")
        return
    
    if y_col == "None":
        # Only X column is selected
        selected_columns = [x_col]
    else:
        # Both X and Y columns are selected
        selected_columns = [x_col, y_col]
    
    # Update chart suggestions based on selected columns
    update_chart_suggestions()

def update_chart_suggestions():
    """Update chart suggestions based on selected columns."""
    global current_df, selected_columns, chart_suggestions
    
    if current_df is None or not selected_columns:
        return
    
    try:
        # Get new chart suggestions based on selected columns
        chart_suggestions = suggest_chart_for_columns(current_df, selected_columns)
        
        # Update chart type dropdown
        chart_type_dropdown['values'] = chart_suggestions
        if chart_suggestions:
            chart_type_var.set(chart_suggestions[0])  # Set first suggestion as default
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update chart suggestions: {str(e)}")

def on_chart_type_selected(event):
    """Handle chart type selection."""
    global current_chart_type
    current_chart_type = chart_type_var.get()

def generate_chart():
    """Generate the selected chart."""
    global current_df, current_chart_type, selected_columns
    
    if current_df is None:
        messagebox.showwarning("Warning", "Please upload a file first!")
        return
    
    if not current_chart_type:
        messagebox.showwarning("Warning", "Please select a chart type!")
        return
    
    if not selected_columns:
        messagebox.showwarning("Warning", "Please select at least one column!")
        return
    
    try:
        # Clear the placeholder if it exists
        if placeholder_label:
            placeholder_label.pack_forget()
        
        # Clear previous chart
        for widget in chart_frame.winfo_children():
            widget.destroy()
        
        # Create a subset dataframe with only selected columns
        subset_df = current_df[selected_columns]
        
        # Create the chart
        fig = plot_chart(subset_df, current_chart_type)
        
        # Embed the chart in the UI
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(canvas, chart_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate chart: {str(e)}")

def save_chart():
    """Save the current chart as PNG or PDF."""
    if current_df is None or not current_chart_type or not selected_columns:
        messagebox.showwarning("Warning", "Please generate a chart first!")
        return
    
    # Ask for file path
    file_path = filedialog.asksaveasfilename(
        title="Save Chart",
        defaultextension=".png",
        filetypes=[
            ("PNG files", "*.png"),
            ("PDF files", "*.pdf")
        ]
    )
    
    if not file_path:
        return
    
    try:
        # Create a subset dataframe with only selected columns
        subset_df = current_df[selected_columns]
        
        # Create the chart
        fig = plot_chart(subset_df, current_chart_type)
        
        # Save the chart
        file_ext = get_file_extension(file_path)
        if file_ext == '.png':
            fig.savefig(file_path, dpi=300, bbox_inches='tight')
        elif file_ext == '.pdf':
            fig.savefig(file_path, format='pdf', bbox_inches='tight')
        
        messagebox.showinfo("Success", f"Chart saved successfully to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save chart: {str(e)}")

def reset_app_ui():
    """Reset the application to its initial state."""
    global current_df, current_chart_type, chart_suggestions, file_path, selected_columns
    
    # Reset global variables
    current_df = None
    current_chart_type = None
    chart_suggestions = []
    file_path = None
    selected_columns = []
    
    # Reset UI elements
    file_info_label.config(text="No file selected")
    x_column_var.set("")
    y_column_var.set("")
    x_column_dropdown['values'] = []
    y_column_dropdown['values'] = []
    chart_type_var.set("Select chart type")
    chart_type_dropdown['values'] = []
    
    # Clear data info text
    data_info_text.config(state=tk.NORMAL)
    data_info_text.delete(1.0, tk.END)
    data_info_text.config(state=tk.DISABLED)
    
    # Clear chart area
    for widget in chart_frame.winfo_children():
        widget.destroy()
    
    # Show placeholder
    placeholder_label.pack(expand=True)
    
    messagebox.showinfo("Reset", "Application has been reset successfully!")