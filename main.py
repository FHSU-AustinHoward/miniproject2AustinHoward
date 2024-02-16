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

    # Remove commas and convert 'Price (in USD)' column to numeric, if it can't: NaN
    cars['Price (in USD)'] = pd.to_numeric(cars['Price (in USD)'].str.replace(',', ''), errors='coerce')

    # Convert the other columns to numeric, if it can't: NaN
    numeric_columns = ['Year', 'Engine Size (L)', 'Horsepower', 'Torque (lb-ft)', '0-60 MPH Time (seconds)']
    for col in numeric_columns:
        cars[col] = pd.to_numeric(cars[col], errors='coerce')

    return cars


def hp_per_dollar_scatterplot(cars):
    # Select the 25 cheapest unique car models
    selected_cars = cars.sort_values(by='Price (in USD)').drop_duplicates('Car Model').head(25)

    # Print selection for debugging
    print(selected_cars)

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

    # Increase the number of ticks and labels on both axes
    plt.xticks(np.arange(100, max(selected_cars['Horsepower']) + 100, 100))
    plt.yticks(np.arange(min(selected_cars['Price (in USD)'] - 5000), max(selected_cars['Price (in USD)']) + 5000, 5000))

    # Show grid
    plt.grid(True)

    # Show the plot
    plt.show()


def save_plot(graph):

# Main Function
def main():
    make_dir()
    cars = retrieve_clean_data()
    graphs = []
    graphs.append(hp_per_dollar_scatterplot(cars))
    for graph in graphs:
        save_plot(graph)


# Only run main as stand-alone (not as a module)
if __name__ == "__main__":
    main()