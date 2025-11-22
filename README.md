# Chart Suggester

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Data Visualization](https://img.shields.io/badge/Data-Visualization-FF6B35?logo=chartdotjs&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-4DA51F?logo=opensourceinitiative&logoColor=white)

Chart Suggester is a desktop application built with Python and Tkinter that simplifies the process of data visualization. By automatically analyzing your dataset's structure and content, it recommends the most suitable chart types and generates them with just a few clicks.


<img width="1920" height="1017" alt="image" src="https://github.com/user-attachments/assets/756fdc69-1dbe-430e-a39b-1275f33226b7" />


## Features
- Multi-format Data Support: Load data from CSV, Excel, JSON, text files, and SQLite databases

- Smart Data Analysis: Automatic detection of column types (numeric, categorical, datetime, boolean, text)

- Intelligent Chart Suggestions: Context-aware recommendations based on selected columns and data types

- Wide Variety of Charts: Support for 30+ chart types including:

- Basic charts: Bar, Line, Scatter, Pie

- Statistical charts: Histogram, Box Plot, Violin Plot, Density Plot

- Advanced charts: Heatmaps, Facet Grids, Pair Plots, Word Clouds

- Time series charts: Area charts, Event timelines

- Interactive UI: User-friendly interface with real-time chart generation

- Export Capabilities: Save charts as PNG or PDF files

## How It Works
1. Upload Data: Load your dataset from various file formats

2. Analyze: The app automatically detects column types and provides statistics

3. Select Columns: Choose columns for visualization (X-axis and optional Y-axis)

4. Get Suggestions: Receive intelligent chart recommendations based on your selection

5. Generate & Export: Create charts instantly and save them in high quality
<img width="896" height="63" alt="Untitled Diagram drawio" src="https://github.com/user-attachments/assets/524effa6-e76a-4d1c-a750-24b18f8138e9" />

## Project Screenshots

### Main Interface
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/1510b0d9-a843-4df3-be18-ed1aa113cb27" />


### Chart Gallery
| Bar Chart | Scatter Plot | Heatmap |
|-----------|-------------|---------|
| <img width="2965" height="1763" alt="bar chart" src="https://github.com/user-attachments/assets/213794eb-7d52-469b-86c3-b867f198980a" /> | <img width="2965" height="1762" alt="scatter plot" src="https://github.com/user-attachments/assets/cc4df266-3396-439b-b9c7-27b4607842f8" /> | <img width="2721" height="1763" alt="heatmap" src="https://github.com/user-attachments/assets/42e31945-ea8f-4356-be73-cbe6053769a6" /> |


## Technical Architecture
The application is organized into modular components:

- main.py: Application entry point

- ui.py: User interface implementation using Tkinter

- data_loader.py: Handles data loading from multiple file formats

- chart_logic.py: Contains data analysis and chart suggestion algorithms

- chart_plotter.py: Implements chart generation using Matplotlib and Seaborn

- utils.py: Utility functions for data type detection and statistics

### Supported Data Types
- Numeric: Integer and floating-point numbers

- Categorical: Limited unique values (categories)

- Datetime: Date and time values

- Boolean: True/False values

- Text: Longer string content

- Other: Unrecognized or mixed data types

## Install required dependencies
```cmd
pip install -r requirements.txt
```
## Usage
Run the application:

```bash
python main.py
```


## Requirements
Python 3.6+

pandas
numpy
matplotlib
seaborn
pillow
tkinter (usually included with Python)


## License
This project is open source and available under the MIT License.
