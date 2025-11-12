"""
Main entry point for the Chart Suggester application.
This file initializes the application and starts the UI.
"""

import tkinter as tk
from ui import create_main_window, setup_styles

def main():
    """Main function to start the application."""
    root = tk.Tk()
    root.title("Chart Suggester")
    root.geometry("1200x800")
    
    # Set up styles and create the main window
    setup_styles(root)
    create_main_window(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()