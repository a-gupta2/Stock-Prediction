# Advice Log Analyzer

## Overview

The Log Analyzer is a web application built with Streamlit that allows users to upload CSV or Excel files containing GRAFANA log data. The application processes the logs, computes daily statistics, and visualizes the data using interactive Plotly charts. Users can also download the visualizations as HTML files for offline viewing.

## Features

- **File Upload**: Upload multiple CSV or Excel files.
- **Data Processing**: Automatically computes average and maximum response times, total requests, and request distributions.
- **Interactive Charts**: Visualize log data using Plotly charts that allow hover information and detailed statistics.
- **HTML Export**: Save visualizations as HTML files for download.

## Requirements

- Python 3.7 or higher
- Streamlit
- Pandas
- Plotly

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone https://github.com/Intelliflo/Advice.LogAnalyzer
   
2. **Create a virtual environment:**

- bash
- Copy code
- python -m venv venv
- source venv/bin/activate  # On Windows use `venv\Scripts\activate`
- Install the required packages:

- bash
- Copy code
- pip install streamlit pandas plotly
- Usage
- Run the application:


## Usage

1. **Run the Application**:
   Open your terminal or command prompt and navigate to the directory where your application is located. Run the following command:
   ```bash
   streamlit run web.py

### 1. Run the Application

### 2. Upload Log Files

### 3. Select Files for Analysis

### 4. View the Charts

### 5. Download the Charts

### 6. Refresh the Data


## Run the docker container
```bash
docker build -t log-analyzer .
docker run -p 8501:8501 log-analyzer

### Access the Application
Open your web browser and navigate to http://localhost:8501 to access the Log Analyzer application.



**Note:** app.py is not a web application is the another way to generate dashboard in html format reading the data from 'Data/Inputs folder/'
