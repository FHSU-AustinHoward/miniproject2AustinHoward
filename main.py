# INF601 - Advanced Programming in Python
# Austin Howard
# Mini Project 1

'''
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
'''

import pandas as pd
import matplotlib.pyplot as plt


def retrieve_clean_data():
    # Load the dataset
    cars = pd.read_csv("Sport car price.csv", index_col=0)

    # Convert 'Price (in USD)' column to numeric values
    cars['Price (in USD)'] = pd.to_numeric(cars['Price (in USD)'].str.replace(',', ''))

    return cars


def hp_per_dollar_scatterplot(cars):
    # Select a sample of 24 cars from the dataset, drop duplicate car models, and sort by 'Price (in USD)'
    sample_cars = cars.drop_duplicates(subset='Car Model').sample(24).sort_values(by=['Price (in USD)'])

    # Print the sorted DataFrame
    print(sample_cars)


# Main Function
def main():
    cars = retrieve_clean_data()
    hp_per_dollar_scatterplot(cars)


# Only run main as stand-alone (not as a module)
if __name__ == "__main__":
    main()