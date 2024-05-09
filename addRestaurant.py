import sqlite3
import csv
import json

# Connect to the SQLite database
conn = sqlite3.connect('restaurants.db')

# Create the restaurants table
create_table_sql = '''
CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id INTEGER PRIMARY KEY,
    restaurant_name TEXT NOT NULL,
    address TEXT NOT NULL,
    cuisine TEXT NOT NULL,
    menu_data TEXT NOT NULL
);
'''

# Execute the SQL statement to create the table
conn.execute(create_table_sql)

# Path to your CSV file
csv_file_path = 'restaurant_menu.csv'

# Initialize a dictionary to hold restaurant data
restaurants = {}

# Read the CSV file
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        restaurant_name = row['restaurant_name']
        cuisine = row['cuisine']
        location = row['location']
        menu_item = row['menu_item']
        
        # Parse the menu item into the desired format: item name:price:description
                # Parse the menu item into the desired format: item name:price:description
        #print(menu_item)
        price, item_description = menu_item.split(': ', 1)
        item_parts = item_description.split(', ', 1)
        if len(item_parts) == 2:
            item_name, description = item_parts
        else:
            item_name = item_parts[0]
            description = ""  # Default to empty if no description is provided
        formatted_item = f"{item_name}:{price}:{description}"

        
        # If the restaurant is already in the dictionary, append the new menu item
        if restaurant_name in restaurants:
            restaurants[restaurant_name]['menu_data'].append(formatted_item)
        else:
            # Otherwise, add the restaurant and its first menu item
            restaurants[restaurant_name] = {
                'cuisine': cuisine,
                'address': location,
                'menu_data': [formatted_item]
            }

# Insert data into the database
for name, info in restaurants.items():
    # Convert the list of menu items into a JSON string
    menu_data_json = json.dumps(info['menu_data'])
    # Prepare the insert statement
    insert_sql = '''INSERT INTO restaurants (restaurant_name, address, cuisine, menu_data) VALUES (?, ?, ?, ?)'''
    # Execute the insert statement
    conn.execute(insert_sql, (name, info['address'], info['cuisine'], menu_data_json))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data imported successfully.")
