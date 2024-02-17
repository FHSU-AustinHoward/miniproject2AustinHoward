# INF601 - Advanced Programming in Python
# Austin Howard
# Mini Project 1

"""
(5/5 points) Initial comments with your name, class and project at the top of your .py file.
(5/5 points) Proper import of packages used.
(20/20 points) Using a data source of your choice, such as data from data.gov or using the Faker package, generate or
            retrieve some data for creating basic statistics on. This will generally come in as json data, etc.
            Think of some question you would like to solve such as:
            "How many homes in the US have access to 100Mbps Internet or more?"
            "How many movies that Ridley Scott directed is on Netflix?" -
            https://www.kaggle.com/datasets/shivamb/netflix-shows
            Here are some other great datasets: https://www.kaggle.com/datasets
(10/10 points) Store this information in Pandas dataframe. These should be 2D data as a dataframe, meaning the data is
            labeled tabular data.
(10/10 points) Using matplotlib, graph this data in a way that will visually represent the data. Really try to build
            some fancy charts here as it will greatly help you in future homework assignments and in the final project.
(10/10 points) Save these graphs in a folder called charts as PNG files. Do not upload these to your project folder, the
            project should save these when it executes. You may want to add this folder to your .gitignore file.
(10/10 points) There should be a minimum of 5 commits on your project, be sure to commit often!
(10/10 points) I will be checking out the main branch of your project. Please be sure to include a requirements.txt file
            which contains all the packages that need installed. You can create this fille with the output of pip freeze
            at the terminal prompt.
(20/20 points) There should be a README.md file in your project that explains what your project is, how to install the
            pip requirements, and how to execute the program. Please use the GitHub flavor of Markdown. Be thorough on
            the explanations.
"""
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def make_dir():
    # Attempt to make a directory for the charts...
    try:
        Path('charts').mkdir()
    # ...unless it already exists
    except FileExistsError:
        pass


def retrieve_clean_data():
    # Load the dataset
    cars = pd.read_csv("Sport car price.csv", index_col=0)
    print(cars.dtypes)

    # Remove commas and convert 'Price (in USD)' column to numeric, if it can't: NaN
    cars['Price (in USD)'] = pd.to_numeric(cars['Price (in USD)'].str.replace(',', ''), errors='coerce')

    # Convert the other columns to numeric, if it can't: NaN
    numeric_columns = ['Year', 'Engine Size (L)', 'Horsepower', 'Torque (lb-ft)', '0-60 MPH Time (seconds)']
    for col in numeric_columns:
        cars[col] = pd.to_numeric(cars[col], errors='coerce')

    return cars


def cheap_performance_scatterplot(cars):
    # Select the 25 cheapest unique car models
    selected_cars = cars.sort_values(by='Price (in USD)').drop_duplicates('Car Model').head(25)

    # Scatterplot
    plt.figure(figsize=(12, 8))
    plt.scatter(selected_cars['Horsepower'], selected_cars['Price (in USD)'], s=50, alpha=0.8)

    # Add data labels with Car Model and Year information
    for i, row in selected_cars.iterrows():
        label = f"{row['Car Model']} ({row['Year']})"
        plt.text(row['Horsepower'], row['Price (in USD)'], label, fontsize=8, ha='right', va='bottom')

    # Title and labels
    plt.title('Scatterplot of Horsepower vs. Cost for 25 Cheapest Car Models')
    plt.xlabel('Horsepower')
    plt.ylabel('Price (in USD)')

    # Set the number of ticks and labels on both axes
    plt.xticks(np.arange(100,
                         max(selected_cars['Horsepower']) + 100,
                         100)
               )
    plt.yticks(np.arange(min(selected_cars['Price (in USD)'] - 5000),
                         max(selected_cars['Price (in USD)']) + 5000,
                         5000)
               )

    # Show grid
    plt.grid(True)

    return plt

def new_car_hp_linechart(cars):
    # Filter for the past 25 years
    selected_cars = cars[cars['Year'] >= cars['Year'].max() - 25]

    # Group by Year and find the maximum Horsepower for each year
    max_hp_per_year = selected_cars.groupby('Year')['Horsepower'].max()

    # Line chart
    plt.figure(figsize=(12, 8))
    plt.plot(max_hp_per_year.index, max_hp_per_year.values, marker='o', linestyle='-', color='b')

    # Add data labels with Car Model information
    for year, horsepower in max_hp_per_year.items():
        max_hp_model = selected_cars.loc[
            (selected_cars['Year'] == year) & (selected_cars['Horsepower'] == horsepower), 'Car Model'].values[0]
        plt.text(year, horsepower, f"{max_hp_model}", fontsize=8, ha='left', va='bottom')

    # Title and labels
    plt.title('Most powerful new car releases')
    plt.xlabel('Year')
    plt.ylabel('Horsepower')

    # Show grid
    plt.grid(True)

    return plt


def power_per_liter_barchart(cars):
    pass
    # return plt

def save_chart(data, filename):
    # Save the plot in the "charts" folder
    full_filename = f"charts/{filename}.png"
    data.savefig(full_filename)
    plt.clf()  # Clear the current figure


# Main Function
def main():
    # Make the charts directory
    make_dir()

    # Retrieve sanitized data from the sports cars data_set
    cars = retrieve_clean_data()

    # Call different methods to create the charts and save them
    cheap_performance_scatterplot(cars)
    save_chart(plt, "cheap_performance_cars")

    new_car_hp_linechart(cars)
    save_chart(plt, "best_horsepower_per_model_year")

    power_per_liter_barchart(cars)
    save_chart(plt, "most_power_per_liter")

# Only run main as stand-alone (not as a module)
if __name__ == "__main__":
    main()