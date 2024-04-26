import streamlit as st
import sqlite3
import json
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables and initialize OpenAI
load_dotenv('secrets.env')
openai_api_key = os.getenv("API_KEY")
client = openai.OpenAI(api_key=openai_api_key)


# Initialize session state for selected restaurant and messages
if 'selected_restaurant_id' not in st.session_state:
    st.session_state['selected_restaurant_id'] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []

def wrap_text(text, width):
    """
    A simple function to wrap text at a given width.
    """
    if len(text) <= width:
        return text
    else:
        # Find the nearest space before the cutoff point
        wrap_index = text.rfind(' ', 0, width)
        if wrap_index > -1:
            # If a space is found, break at that space
            return text[:wrap_index] + '\n' + wrap_text(text[wrap_index+1:], width)
        else:
            # If no space is found, hard break at the width
            return text[:width] + '\n' + wrap_text(text[width:], width)


# Define the function to search restaurants in the database
# def search_restaurants(search_term):
#     conn = sqlite3.connect('restaurants.db')
#     conn.row_factory = sqlite3.Row
#     cur = conn.execute("SELECT * FROM restaurants WHERE restaurant_name LIKE ?", ('%' + search_term + '%',))
#     results = cur.fetchall()
#     conn.close()
#     return results
    
def search_restaurants(search_term):
    conn = sqlite3.connect('restaurants.db')
    conn.row_factory = sqlite3.Row
    # Update the SQL query to search within restaurant_name, cuisine, and address
    cur = conn.execute("""
        SELECT * FROM restaurants 
        WHERE restaurant_name LIKE ? 
        OR cuisine LIKE ? 
        OR address LIKE ?
        """, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
    results = cur.fetchall()
    conn.close()
    return results


# Function to fetch the menu of the selected restaurant
def get_menu(restaurant_id):
    """Fetch menu data for the given restaurant ID."""
    conn = sqlite3.connect('restaurants.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT menu_data FROM restaurants WHERE restaurant_id = ?", (restaurant_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return json.loads(row['menu_data'])
    else:
        return None

# Function to interact with the OpenAI API
def interact_with_openai(user_prompt, restaurant_id):
    menu_data = get_menu(restaurant_id)
    menu_str = ', '.join(menu_data) if menu_data else "Menu not found for the specified restaurant."
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=st.session_state.messages + [
                {"role": "system", "content": f"Roleplay as a helpful server at a restaurant and answer any questions about the menu provided: {menu_str}. Be knowledgeable about the previous conversation history."},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


# UI for restaurant search
if not st.session_state['selected_restaurant_id']:
    st.title('RagU Restaurant Search')
    search_term = st.text_input('Search for a restaurant')
    
    if search_term:
        results = search_restaurants(search_term)
        if results:
            for row in results:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.subheader(row['restaurant_name'])
                    st.write(f"Address: {row['address']}")
                    st.write(f"Cuisine: {row['cuisine']}")
                with col2:
                    select_btn = st.button("Select", key=row['restaurant_id'])
                    if select_btn:
                        st.session_state['selected_restaurant_id'] = row['restaurant_id']
                        st.session_state['messages'] = [{"role": "assistant", "content": "Hello! How can I assist you with our menu today?"}]
                        #st.experimental_rerun()
                        st.rerun()
                        break  # Break the loop to refresh the page and move to chat interface

        else:
            st.write('No restaurants found.')


# Chatbot interface
if st.session_state['selected_restaurant_id']:
    st.title("RagU")
    st.caption("A chatbot designed to be your personal waiter")
    st.caption("RagU can make mistakes. Consider checking important information.")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    menu_data = get_menu(st.session_state['selected_restaurant_id'])

    with st.sidebar:
        if st.session_state['selected_restaurant_id'] is not None:
            if st.button("Search Another Restaurant"):
                st.session_state['selected_restaurant_id'] = None
                st.session_state['messages'] = []
                st.rerun()

    st.sidebar.header("Menu:")

    for item in menu_data:
        parts = item.split(':')
        name = parts[0]
        price = parts[1] if len(parts) > 1 and parts[1] else "Price upon request"
        description = parts[2] if len(parts) > 2 else "No description available."

        if price and price != "Price upon request":
            st.sidebar.markdown(f"**{name} : {price}**")
        else:
            st.sidebar.markdown(f"**{name}**")

        st.sidebar.text(description)

    if 'user_prompt' not in st.session_state:
        st.session_state['user_prompt'] = ""


    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        msg = interact_with_openai(prompt,st.session_state['selected_restaurant_id'])
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        print(st.session_state.messages)

    
