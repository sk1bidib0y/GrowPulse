from st_on_hover_tabs import on_hover_tabs
import streamlit as ui
import pandas as pandas
import numpy as numpy
import plotly.express as px
import subprocess
import random
from datetime import timedelta
import time

# Initialize the Streamlit page with a wide layout and a custom title
ui.set_page_config(layout="wide", page_title="GrowPulse OS", page_icon="PlantData/PulseLogoFavicon.png")
    
@ui.cache_data
def load_data():
    # Trying to read the file normally
    try:
        return pandas.read_csv('PlantData/greenhouse_telemetry.csv')
    # Error handling if the file is missing or empty.
    except (FileNotFoundError, pandas.errors.EmptyDataError):
        # If missing or blank, trigger the generator script.
        data_file = open('PlantData/greenhouse_telemetry.csv', 'w')  # Create an empty file to avoid FileNotFoundError during subprocess execution
        data_file.close()
        subprocess.run(['python', 'data_generate.py'])
        # Read file now that it's successfully built
        return pandas.read_csv('PlantData/greenhouse_telemetry.csv')
skibidi = load_data()

# User interface styling and loading custom CSS.
ui.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

with ui.sidebar:
    with ui.container():
        ui.container(height=190, border=False)
    tabs = on_hover_tabs(
        tabName=['Dashboard', 'Canopy Vision', 'Controls', 'Export Data'], 
        iconName=['dashboard', 'visibility', 'settings', 'download'], 
        default_choice=0,
        styles={
            'navtab': {
                'background-color': 'transparent !important',
                'color': '#818181',
                'font-size': '16px',
                'transition': '.3s',
                'white-space': 'nowrap',
                'text-transform': 'capitalize'
            },
            'tabStyle': {
                'list-style-type': 'none',
                'margin-bottom': '25px',
                'padding-left': '25px',
                ':hover :hover': {
                    'color': '#FF4B4B', 
                    'cursor': 'pointer'
                }
            },
            'iconStyle': {
                'position': 'fixed',
                'left': '7.5px',
                'text-align': 'left'
            }
        },
        key="growpulse_nav"
    )

#ui.markdown("""""", unsafe_allow_html=True)

# Page routing to desired content based on the selected tab in the sidebar.
# Dashboard tab for real-time metrics and statistical visualizations.
if tabs == 'Dashboard':
    ui.title("Core Dashboard")

    def random_temp():
        return round(random.uniform(20.0, 30.0), 2)
    def random_humidity():
        return round(random.uniform(40.0, 80.0), 2)
    def random_soil_moisture():
        return round(random.uniform(40.0, 80.0), 2)
    def random_sprinkler_status():
        return random.choice(["ON", "OFF"])
    
    current_status = random_sprinkler_status()

    if (current_status == "ON"):
        working_status = "working"
        color = "green"
    elif (current_status == "OFF"):
        working_status = "offline"
        color = "red"
    else:
        working_status = "unknown"

    ui.markdown("### Real-time metrics.")
    temp, humidity, soil_moisture, sprinkler_status = ui.columns(4)
    temp.metric(
        "Temperature", 
        f"{random_temp()}°C", 
        "-2°C", 
        border=True
    )
    humidity.metric(
        "Humidity", 
        f"{random_humidity()}%", 
        "3%", 
        border=True
    )
    soil_moisture.metric(
        "Soil Moisture", 
        f"{random_soil_moisture()}%", 
        "5%", 
        border=True
    )
    sprinkler_status.metric(
        "Sprinkler Status", 
        f"{current_status}", 
        working_status, 
        border=True, 
        delta_arrow="off",
        delta_color=f"{color}"
    )

    ui.write("### Statistical metric data")
    
    # Create a horizontal control bar for field selection and chart style.
    control_col1, control_col2, control_col3, control_col4 = ui.columns(4)
    
    with control_col1:
        x_metric = ui.selectbox("X-Axis Field", options=skibidi.columns, index=4) # Default: Timestamp
        
    with control_col2:
        y_metric = ui.selectbox("Y-Axis Field", options=skibidi.columns, index=1) # Default: Temperature_C
        
    with control_col3:
        # Let's filter or group colors by metadata categories like Crop_Type
        group_metric = ui.selectbox("Group / Color By", options=[None] + list(skibidi.columns), index=2) # Default: Crop_Type
        
    with control_col4:
        chart_style = ui.selectbox(
            "Visualization Style", 
            options=["Line Graph", "Scatter Plot", "Bar Chart", "Box Plot"], 
            index=3
        )

    # Build the Plotly figure on the fly based on selections
    if chart_style == "Box Plot":
        fig = px.box(skibidi, x=x_metric, y=y_metric, color=group_metric, template="plotly_dark")
    elif chart_style == "Line Graph":
        fig = px.line(skibidi, x=x_metric, y=y_metric, color=group_metric, template="plotly_dark")
    elif chart_style == "Scatter Plot":
        fig = px.scatter(skibidi, x=x_metric, y=y_metric, color=group_metric, template="plotly_dark")
    elif chart_style == "Bar Chart":
        fig = px.bar(skibidi, x=x_metric, y=y_metric, color=group_metric, template="plotly_dark")
    
    # Style improvements.
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=20, b=10)
    )
    
    # Display the beautiful interactive chart
    ui.plotly_chart(fig, width='stretch')

# Canopy Vision tab for displaying computer vision analytics on plant health and nutrient deficiencies.
elif tabs == 'Canopy Vision':
    with ui.spinner("Loading Canopy Vision Analytics..."):
        time.sleep(1.5)  # Simulate a delay for loading analytics
    ui.title("Computer Vision & Canopy Analytics")
    columnOne, columnTwo = ui.columns(2)
    with columnOne:
        ui.markdown("## Plants detected with nitrogen deficiency.")
        ui.image(
            "PlantData/nitrogen_deficiency_photoshopped.png", 
            caption="Canopy Vision: Nitrogen Deficiency Detection", 
            width='content'
            )
    
    with columnTwo:
        ui.markdown("## Plants detected with phosphorus deficiency.")
        ui.image(
            "PlantData/phosphorus_deficiency_edited.png", 
            caption="Canopy Vision: Phosphorus Deficiency Detection", 
            width='content'
            )
    
    ui.markdown("## Plants detected with potassium deficiency.")
    ui.image(
        "PlantData/potassium_deficiency_edited.png", 
        caption="Canopy Vision: Potassium Deficiency Detection", 
        width='content'
        )
# Control tab for adjusting actuator settings like sprinklers, nutrient input, and temperature ranges.
elif tabs == 'Controls':
    with ui.spinner("Loading Actuator Control Panel..."):
        time.sleep(1.5)  # Simulate a delay for loading controls
    ui.title("Performance & Actuator Overrides")
    sprinkler, soil_nutrients, temperature = ui.columns(3, border=True)
    with sprinkler:
        ui.write("### Sprinkler Control")
        ui.write("Select timine to turn sprinklers on/off.")
        ui.time_input("Turn on at: ", value=None, key="sprinkler_schedule", step=timedelta(hours=1))
        ui.time_input("Turn off at: ", value=None, key="sprinkler_schedule_off", step=timedelta(hours=1))
    with soil_nutrients:
        ui.write("### Soil Nutrient Control")
        ui.write("Select nutrient input levels for soil/aquaponics.")
        ui.slider("Nitrogen Input Level", min_value=0, max_value=100, value=50, step=1, key="nitrogen_input")
        ui.slider("Phosphorus Input Level", min_value=0, max_value=100, value=50, step=1, key="phosphorus_input")
        ui.slider("Potassium Input Level", min_value=0, max_value=100, value=50, step=1, key="potassium_input")
    with temperature:
        ui.write("### Temperature Control")
        ui.write("Select temperature range for greenhouse.")
        ui.slider("Minimum Temperature (°C)", min_value=10, max_value=40, value=20, step=1, key="min_temp")
        ui.slider("Maximum Temperature (°C)", min_value=10, max_value=40, value=30, step=1, key="max_temp")

# Export Data tab for downloading datasets based on user-selected criteria.
elif tabs == 'Export Data':
    with ui.spinner("Loading Data Export Options..."):
        time.sleep(1.5)  # Simulate a delay for loading export options
    ui.title("Corporate Telemetry Exports.")
    ui.write("#### Download the greenhouse telemetry dataset for further analysis or reporting.")
    export_choice = ui.get_options = ui.selectbox("Export Options", options=["Please select an option" ,"All Data", "Monthly Export", "Crop Type", "Custom Growth Range"], index=0, key="export_options")

    if export_choice == "All Data":
        with ui.spinner("Preparing full dataset for download..."):
            time.sleep(2.5)  # Simulate a delay for dataset preparation
        ui.button(label="Download Full Dataset")
    elif export_choice == "Monthly Export":
        month_number = ui.slider(
            "Select month number to export:", 
            min_value=1, max_value=12, value=None,
            step=1, 
            key="monthly_export"
        )
        with ui.spinner(f"Preparing dataset for month {month_number}..."):
            time.sleep(2.5)  # Simulate a delay for dataset preparation
        ui.button(label=f"Download Month {month_number} Dataset")
    elif export_choice == "Crop Type":
        crop_type = ui.selectbox(
            "Select Crop Type to export:", 
            options=["Tomato", "Lettuce", "Cucumber"], 
            index=0, 
            key="crop_type_export"
        )
        with ui.spinner(f"Preparing dataset for crop type: {crop_type}..."):
            time.sleep(2.5)  # Simulate a delay for dataset preparation
        ui.button(label=f"Download {crop_type} Dataset")
    elif export_choice == "Custom Growth Range":
        growth_range = ui.slider(
            "Select Growth Rate Range (cm/month):", 
            min_value=0, max_value=10, value=(0, 10),
            step=1, 
            key="growth_range_export"
        )
        with ui.spinner(f"Preparing dataset for growth rate range: {growth_range[0]} - {growth_range[1]} cm/month..."):
            time.sleep(2.5)  # Simulate a delay for dataset preparation
        ui.button(label=f"Download Growth Rate Range Dataset")