import pandas as pandas
import numpy as numpy
from datetime import datetime, timedelta

# Randomly generate a synthetic dataset for greenhouse telemetry timestamps
num_rows = 1000
start_time = datetime.now() - timedelta(days=10)
timestamps = [start_time + timedelta(minutes=15 * i) for i in range(num_rows)]

# Set seed value for random number generation.
numpy.random.seed(42)

# Generate synthetic telemetry data for temperature, humidity, soil moisture, and sprinkler status
time_axis = numpy.linspace(0, 4 * numpy.pi, num_rows)
temperatures = 24 + 5 * numpy.sin(time_axis) + numpy.random.normal(0, 0.5, num_rows)
humidity = 60 - 10 * numpy.sin(time_axis) + numpy.random.normal(0, 1.2, num_rows)

soil_moisture = []
current_moist = 75.0
for i in range(num_rows):
    current_moist -= numpy.random.uniform(0.05, 0.2)
    if current_moist < 45.0: 
        current_moist = 80.0
    soil_moisture.append(current_moist)

sprinkler_status = [1 if m > 78 else 0 for m in soil_moisture]
crop_types = numpy.random.choice(['Tomato', 'Lettuce', 'Cucumber'], size=num_rows)

growth_rates = []
for temp in temperatures:
    base_growth = 5.0 + numpy.random.normal(0, 0.3)
    if 22 <= temp <= 26:
        base_growth += 2.5  
    growth_rates.append(round(base_growth, 2))

# Create a DataFrame to hold the synthetic greenhouse telemetry data
df = pandas.DataFrame({
    'Timestamp': timestamps,
    'Crop_Type': crop_types,
    'Temperature_C': numpy.round(temperatures, 1),
    'Humidity_Percent': numpy.round(humidity, 1),
    'Growth_Rate_cm_month': growth_rates,  
    'Soil_Moisture_Percent': numpy.round(soil_moisture, 1),
    'Sprinkler_Active': sprinkler_status
})

try:
    df.to_csv('PlantData\greenhouse_telemetry.csv', index=False)
except PermissionError:
    print("Lack of file permissions")