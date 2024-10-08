# -*- coding: utf-8 -*-
"""nt-tourism-location-based-prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VtgZ7V445MvvVUWeAu_T3rSaArhABfAo
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install -q hvplot

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import hvplot.pandas
from scipy import stats

# %matplotlib inline
sns.set_style("whitegrid")
plt.style.use("fivethirtyeight")

# Load the Tourist dataset
data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Govhack-data/Tourist-Location-based-Dataset.csv')
data

# Check basic information about the dataset
data.info()

# Check number of rows and columns in dataset
data.shape

# Get Statistical measures of the dataset
data.describe()

# Check if there are any duplicates in dataset
data.duplicated()

# Check if there is any missing data in dataset
missing = data.isnull().sum()
missing

# Location Based Tourist Prediction Data Analysis
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Initialize a dictionary to store the actual predicted numbers along with trends
future_predictions_with_numbers = {}

# Create a mapping for the location codes to their full names
location_mapping = {
    'GD': 'Greater Darwin',
    'KD': 'Katherine Daly',
    'KK': 'Kakadu Arnhem Land',
    'BA': 'Barkly',
    'LAS': 'Lasseter',
    'ASM': 'Alice Springs Macdonnell'
}

# Predict the number of tourists in 2025 for each location and show the predicted numbers along with the trend
for location in data['location'].unique():
    # Get the full name of the location
    full_location_name = location_mapping.get(location, location)

    # Filter data for the current location
    location_data = data[data['location'] == location]

    # Prepare the input features (year) and target (visitor_num)
    X = location_data['year'].values.reshape(-1, 1)
    y = location_data['visitor_num'].values

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict visitor numbers for 2025 and 2024
    prediction_2025 = model.predict(np.array([[2025]]))[0]
    prediction_2024 = model.predict(np.array([[2024]]))[0]

    # Determine the trend (increase or decrease)
    trend = "Increase" if prediction_2025 > prediction_2024 else "Decrease"

    # Store both the predicted number for 2025 and the trend
    future_predictions_with_numbers[location] = {
        "Predicted_Visitor_Num_2025": prediction_2025,
        "Tourism_Trend_2025": trend
    }

    # Plot the actual data
    plt.figure()
    plt.plot(location_data['year'], location_data['visitor_num'], marker='o', label='Actual Visitor Numbers')

    # Plot the predicted data for 2025 as a separate point
    plt.scatter([2025], prediction_2025, color='green', label='Predicted Visitor Number (2025)', zorder=5)

    # Add title and labels
    plt.title(f'Tourist Numbers and Predictions for {full_location_name}')
    plt.xlabel('Year')
    plt.ylabel('Number of Tourists')

    # Show legend and display the plot
    plt.legend()
    plt.show()

# Convert to DataFrame for better visualization
future_trend_with_numbers_df = pd.DataFrame.from_dict(future_predictions_with_numbers, orient='index').reset_index()
future_trend_with_numbers_df.columns = ['Location', 'Predicted_Visitor_Num_2025', 'Tourism_Trend_2025']

# Replace the location codes with their full names in the future trend DataFrame
future_trend_with_numbers_df['Location'] = future_trend_with_numbers_df['Location'].map(location_mapping)

# Display the predicted numbers and trends for 2025
print(future_trend_with_numbers_df)

