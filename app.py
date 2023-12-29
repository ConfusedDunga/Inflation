## app.py or app.ipynb

import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
import matplotlib as plt
import openpyxl


def run_inflation_analysis():
    # Specify the path to the Excel file
    excel_file_path = 'NRB_Data.xlsx'

    # Read the Excel file into a Pandas DataFrame
    excel_data = pd.ExcelFile(excel_file_path)
    # Read the 'Inflation' sheet into a DataFrame
    df = pd.read_excel(excel_file_path, sheet_name='Inflation', engine='openpyxl')

    # Get the current year
    current_year = pd.to_datetime('now').year

   # Get the latest inflation rate and previous month's inflation rate
    latest_inflation = df.loc[df['Date'].idxmax(), 'Inflation']
    previous_month_date = df['Date'].max() - pd.DateOffset(months=1)
    previous_month_inflation = df.loc[df['Date'] == previous_month_date, 'Inflation'].squeeze()
    # Get the change from the previous year, same month
    previous_year_date = df['Date'].max() - pd.DateOffset(years=1)
    previous_year_same_month_inflation = df.loc[df['Date'] == previous_year_date, 'Inflation'].squeeze()

   
    # Get the latest available month from the DataFrame
    latest_month = df['Date'].max().strftime('%B %Y')  # Format: Month Year



    # Display the gauge chart with the latest inflation rate and change from the previous month
    col1, col2, col3 = st.columns(3)
    # Display the three metrics: Latest Inflation Rate, Change from Previous Month, Change from Previous Year
    col1.metric(f"{latest_month} Inflation Rate", f"{latest_inflation:.2f}%", help="Latest available month's inflation rate")
    col2.metric("Change from Previous Month", f"{latest_inflation - previous_month_inflation:.2f}%", help="Change from the previous month")
    col3.metric("Change from Previous Year (Same Month)", f"{latest_inflation - previous_year_same_month_inflation:.2f}%", help="Change from the previous year, same month")

    # Filter data based on selected years
    selected_years = st.sidebar.multiselect("Select Years", df['Date'].dt.year.unique(), default=[current_year])

      # Create separate 'Year' and 'Month' columns
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    
    # Create a line chart for the selected years using Plotly Express
    fig = px.line(
        df[df['Date'].dt.year.isin(selected_years)],
        x='Month',
        y='Inflation',
        color='Year',
        labels={'Inflation': 'Inflation (%)'},
        title='Inflation Data Analysis',
        height=400,
        width=800,
    )

    # Configure chart properties
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Inflation (%)')

     # Create separate 'Year' and 'Month' columns
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()

    # Create a line chart for the selected years using Plotly Express
    fig = px.line(
        df[df['Date'].dt.year.isin(selected_years)],
        x='Month',
        y='Inflation',
        color='Year',
        labels={'Inflation': 'Inflation (%)'},
        title='Inflation Data Analysis',
        line_shape='spline',
        markers=True,
    )

    # Configure chart properties
    fig.update_xaxes(title_text='Month')
    fig.update_yaxes(title_text='Inflation (%)')

    # Display the Plotly chart with automatic container width
    st.plotly_chart(fig, use_container_width=True)

    # Create a pivot table with months as columns and years as rows
    pivot_table = pd.pivot_table(
        df, 
        values='Inflation', 
        index=df['Date'].dt.year, 
        columns=df['Date'].dt.month_name(), 
        aggfunc='mean'
    )

    # Rename the columns to use three-letter month abbreviations
    pivot_table.columns = pd.to_datetime(pivot_table.columns, format='%B').strftime('%b')

    # Sort the columns in chronological order
    sorted_columns = pd.to_datetime(pivot_table.columns, format='%b').sort_values().strftime('%b')
    pivot_table = pivot_table[sorted_columns]

    # Format the values as percentages and add % sign
    pivot_table = pivot_table.applymap(lambda x: f"{x:.2f}%" if not pd.isna(x) else '-')

    # Format the index (year) without commas
    pivot_table.index = pivot_table.index.map(lambda x: f"{x:,.0f}")

    # Display the modified pivot table
    st.write(pivot_table)

def show_main_page():
    st.title("NRB Data")
    st.write("Welcome to the data presentation app. Select an analysis from the sidebar.")
    st.write("Developed by Parash Shrestha")
def main():
    # Display the title and introduction
    show_main_page()

    # Get the names of all sheets in the Excel file
    excel_file_path = 'NRB_Data.xlsx'
    excel_data = pd.ExcelFile(excel_file_path)
    sheet_names = excel_data.sheet_names

    # Allow the user to select an analysis
    selected_analysis = st.sidebar.selectbox("Select Indicator", ["Main Page", "Inflation Analysis"])

    # Run the selected analysis
    if selected_analysis == "Inflation Analysis":
        run_inflation_analysis()

if __name__ == "__main__":
    main()


