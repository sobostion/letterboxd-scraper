# Retrieve film ratings from profile and display them in a table

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

# Get username for ratings
username = input("Enter Letterboxd username: ")

url = "https://letterboxd.com/{}/films/".format(username)

# Send a GET request to retrieve the page content
response = requests.get(url)
html_content = response.content

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Find the list containing the movie ratings
rating_list = soup.find_all("li", class_="poster-container")

# Create empty dict to store the movie details
ratings = {}

# Create function for printing table

def printTable(ratings):
    print("\n {} Film Ratings:".format(username + "'s"))
    print("----------------------------------------------------")
    print("| {:<40} | {:>10} |".format("Film Name", "Rating"))
    print("----------------------------------------------------")
    
    for film_name, film_rating in ratings:
        print("| {:<40} | {:>10} |".format(film_name, film_rating))
    
    print("----------------------------------------------------")

# we need numeric ratings for sorting
def convert_rating_to_numeric(rating):
    if rating == 'N/A':
        return -1
    elif rating == '½':
        return 0.5
    elif rating == '★':
        return 1
    else:
        return int(rating.count('★'))


# Extract movie titles and ratings from the list
for item in rating_list:
    try:
        title = item.find("img")["alt"].strip()
        rating = item.find("span", class_="rating").text
    except AttributeError as err: # not all films have rating so do exception catch
        rating = "N/A"

    ratings[title] = rating

table_data = []
for film, rating in ratings.items():
    table_data.append([film, rating])

sorted_table_data = sorted(table_data, key=lambda x: convert_rating_to_numeric(x[1]), reverse=True)

headers = ["Film", "Rating"]
table = tabulate(sorted_table_data, headers, tablefmt="pretty")
print("\n {} film ratings:".format(username + "'s"))
print(table)
