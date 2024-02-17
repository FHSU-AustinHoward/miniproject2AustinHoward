# INF601 - Advanced Programming in Python
# Austin Howard
# Mini Project 1

"""
(DONE) Initial comments with your name, class and project at the top of your .py file.
(DONE) Proper import of packages used.
(DONE) Using a data source of your choice, such as data from data.gov or using the Faker package, generate or
            retrieve some data for creating basic statistics on. This will generally come in as json data, etc.
            Think of some question you would like to solve such as:
            "How many homes in the US have access to 100Mbps Internet or more?"
            "How many movies that Ridley Scott directed is on Netflix?" -
            https://www.kaggle.com/datasets/shivamb/netflix-shows
            Here are some other great datasets: https://www.kaggle.com/datasets
(DONE) Store this information in Pandas dataframe. These should be 2D data as a dataframe, meaning the data is
            labeled tabular data.
(DONE) Using matplotlib, graph this data in a way that will visually represent the data. Really try to build
            some fancy charts here as it will greatly help you in future homework assignments and in the final project.
(DONE) Save these graphs in a folder called charts as PNG files. Do not upload these to your project folder, the
            project should save these when it executes. You may want to add this folder to your .gitignore file.
(DONE) There should be a minimum of 5 commits on your project, be sure to commit often!
(DONE) I will be checking out the main branch of your project. Please be sure to include a requirements.txt file
            which contains all the packages that need installed. You can create this fille with the output of pip freeze
            at the terminal prompt.
(20/20 points) There should be a README.md file in your project that explains what your project is, how to install the
            pip requirements, and how to execute the program. Please use the GitHub flavor of Markdown. Be thorough on
            the explanations.
"""

# Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path


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

    # Convert the other columns to numeric
    numeric_columns = ['Year',
                       'Engine Size (L)',
                       'Horsepower',
                       'Torque (lb-ft)',
                       '0-60 MPH Time (seconds)']

    # If converting to numeric throws an error, return 'NaN'
    for col in numeric_columns:
        cars[col] = pd.to_numeric(cars[col], errors='coerce')

    return cars


def cheap_performance_scatterplot(cars):
    # Select the 25 cheapest unique car models
    selected_cars = (cars.sort_values(by='Price (in USD)')
                    .drop_duplicates('Car Model')
                    .head(25))

    # Scatterplot size and data included within it
    plt.figure(figsize=(12, 8))
    plt.scatter(selected_cars['Horsepower'],
                selected_cars['Price (in USD)'],
                s=50,
                alpha=0.8)

    # Add data labels with Car Model and Year information
    for i, row in selected_cars.iterrows():
        label = f"{row['Car Model']} ({row['Year']})"
        plt.text(row['Horsepower'],
                 row['Price (in USD)'],
                 label, fontsize=8,
                 ha='right',
                 va='bottom')

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

    # Line chart properties
    plt.figure(figsize=(12, 8))
    plt.plot(max_hp_per_year.index, max_hp_per_year.values, marker='o', linestyle='-', color='b')

    for year, horsepower in max_hp_per_year.items():
        # Calculate the highest horsepower for that model year
        max_hp_model = selected_cars.loc[(selected_cars['Year'] == year)
                        & (selected_cars['Horsepower'] == horsepower), 'Car Model'].values[0]

        # Add data labels with Car Model information
        plt.text(year, horsepower, f"{max_hp_model}", fontsize=8, ha='left', va='bottom')

    # Title and labels
    plt.title('Most powerful new car releases')
    plt.xlabel('Year')
    plt.ylabel('Horsepower')

    # Show grid
    plt.grid(True)

    return plt


def power_per_liter_barchart(cars):
    # Calculate HP/l
    cars['Horsepower per Liter'] = cars['Horsepower'] / cars['Engine Size (L)']

    # Sort the DataFrame by HP/l in descending order
    top_10_cars = (cars.drop_duplicates('Car Model')
                   .sort_values(by='Horsepower per Liter', ascending=False)
                   .head(10))

    # Create a bar chart
    plt.figure(figsize=(12, 8))
    plt.bar(top_10_cars['Car Model'], top_10_cars['Horsepower per Liter'])
    plt.xlabel('Car Model')
    plt.xticks(rotation=30, ha='right')
    plt.ylabel('Horsepower per Liter')
    plt.title('Top 10 Cars with the Best Horsepower per Liter')
    plt.grid(True)

    return plt


def pricerange_performance_boxplot(cars):
    # Filter for cars over $1,000,000
    expensive_cars = (cars[cars['Price (in USD)'] > 1000000]
                      .drop_duplicates('Car Model')
                      .sort_values(by='0-60 MPH Time (seconds)', ascending=False))

    # Filter for cars between $100,000 and $1,000,000
    midrange_cars = (cars[(cars['Price (in USD)'] > 100000) & (cars['Price (in USD)'] <= 1000000)]
                     .drop_duplicates('Car Model')
                     .sort_values(by='0-60 MPH Time (seconds)', ascending=False))

    # Filter for cars under $100,000
    affordable_cars = (cars[cars['Price (in USD)'] <= 100000]
                       .drop_duplicates('Car Model')
                       .sort_values(by='0-60 MPH Time (seconds)', ascending=False))

    # Calculate overall y-axis limits
    overall_y_limits = (
        min(affordable_cars['0-60 MPH Time (seconds)'].min(),
            midrange_cars['0-60 MPH Time (seconds)'].min(),
            expensive_cars['0-60 MPH Time (seconds)'].min()),
        max(affordable_cars['0-60 MPH Time (seconds)'].max(),
            midrange_cars['0-60 MPH Time (seconds)'].max(),
            expensive_cars['0-60 MPH Time (seconds)'].max())
    )

    # Box plot for affordable cars
    plt.figure(figsize=(18, 8))

    plt.subplot(1, 3, 1)
    plt.boxplot(affordable_cars['0-60 MPH Time (seconds)'], vert=True, showfliers=True)
    plt.xticks([1], ['Under $100,000'])
    plt.title('Under $100,000')
    plt.grid(True)
    plt.ylim(overall_y_limits)

    # Add describe() summary statistics
    summary_stats_affordable = affordable_cars['0-60 MPH Time (seconds)'].describe()
    plt.text(0.1, 0.5, summary_stats_affordable.to_string(), fontsize=8, transform=plt.gca().transAxes)

    # Box plot for midrange cars
    plt.subplot(1, 3, 2)
    plt.boxplot(midrange_cars['0-60 MPH Time (seconds)'], vert=True, showfliers=True)
    plt.xticks([1], ['$100,000 - $1,000,000'])
    plt.title('$100,000 - $1,000,000')
    plt.grid(True)
    plt.ylim(overall_y_limits)

    # Add describe() summary statistics
    summary_stats_midrange = midrange_cars['0-60 MPH Time (seconds)'].describe()
    plt.text(0.1, 0.5, summary_stats_midrange.to_string(), fontsize=8, transform=plt.gca().transAxes)

    # Box plot for expensive cars
    plt.subplot(1, 3, 3)
    plt.boxplot(expensive_cars['0-60 MPH Time (seconds)'], vert=True, showfliers=True)
    plt.xticks([1], ['Over $1,000,000'])
    plt.title('Over $1,000,000')
    plt.grid(True)
    plt.ylim(overall_y_limits)

    # Add describe() summary statistics
    summary_stats_expensive = expensive_cars['0-60 MPH Time (seconds)'].describe()
    plt.text(0.1, 0.5, summary_stats_expensive.to_string(), fontsize=8, transform=plt.gca().transAxes)

    # Common title and labels
    plt.suptitle('Box Plot of 0-60 Performance for Different Price Ranges')
    plt.ylabel('0-60 MPH Time (seconds)')

    return plt


def save_chart(data, filename):
    # Save the plot in the "charts" folder
    full_filename = f"charts/{filename}.png"
    data.savefig(full_filename)

    # Clear the current figure
    plt.clf()


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
    save_chart(plt, "most_horsepower_per_liter")

    pricerange_performance_boxplot(cars)
    save_chart(plt, "0-60_performance_per_price_range")


# Only run main as stand-alone (not as a module)
if __name__ == "__main__":
    main()