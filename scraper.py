import requests
from bs4 import BeautifulSoup
import csv
from flask import Flask, jsonify
from flask_cors import CORS
import time
data = []

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

from flask import request

@app.route('/api/scrape-menu', methods=['POST'])
def scrape_menu(url):

    
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    food_items = soup.find_all(class_='menu-items') 

    food_data = []
    temp = 0
    
    for item in food_items:
        food_name = item.find(class_='item-title').text.replace("\n", "")
        food_price = item.find(class_='item-price').text.replace("\n", "").replace(" ", "")
        food_description = item.find(class_='description').text.replace("\n", "")

        food_dict = {
            'name': food_name,
            'price': food_price,
            'description': food_description,
        }

        food_data.append(food_dict)

    return food_data

def grab_links(location):

    count = 0
    url = 'https://www.allmenus.com/ca/' + location + '/-/'
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    restaurants = soup.find_all(class_="restaurant-list-item clearfix")
    all_data = []

    field_names = ['restaurant_name', 'cuisine', 'location', 'menu_item']

    for restaurant in restaurants:
        name = restaurant.find(class_="name")
        info = name.find('a')
        if info:
            href = info['href']
            rest_name = name.text
         

        cuisine_list = restaurant.find(class_='cuisine-list')
        if cuisine_list:
            cuisine_list = cuisine_list.text
            

        address_lines = restaurant.find(class_="address-container s-hidden-sm s-col-sm-4")
        address_lines = address_lines.find_all('p', class_="address")
        location = ""
        if address_lines:
            for address in address_lines:
                location += address.text
                location += " "

        restaurant_data = {
            'restaurant_name': rest_name,
            'cuisine': cuisine_list,
            'location': location
        }

       
        href = "https://www.allmenus.com/ca/" + location + "/" + href
        # Now let's scrape the menu for this restaurant
        menu_data = scrape_menu(href)
        
        for food_item in menu_data:
            food_item['restaurant_name'] = rest_name
            food_item['cuisine'] = cuisine_list
            food_item['location'] = location
            menu_name = food_item.pop('name')
            menu_price = food_item.pop('price')
            menu_description = food_item.pop('description')
            food_item['restaurant_name'] = rest_name
            food_item['menu_item'] = f"{menu_price}: {menu_name}, {menu_description}"

        all_data.extend(menu_data)
        
        if(count % 50 == 0): print(count)
        if(count > 400): break
        count = count + 1

    # Write all data to CSV
    csv_file_path = '/Users/samabdel/project/restaurant_menu.csv'

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        for food_item in all_data:
            writer.writerow(food_item)


    return all_data

# Call the grab_links function to execute the scraping and CSV writing
grab_links('santa-clara')
grab_links('san-francisco')
grab_links('san-jose')

FILENAME = '/Users/samabdel/project/restaurant_menu.csv'
DELETE_LINE_NUMBER = 5

# Load the data from the file
with open(FILENAME) as f:
    data = f.read().splitlines()  # Read csv file

# Remove the specified line
updated_data = data[:DELETE_LINE_NUMBER] + data[DELETE_LINE_NUMBER+1:]

# Write the updated data back to the file
with open(FILENAME, 'w') as g:
    g.write('\n'.join(updated_data))  # Write to file