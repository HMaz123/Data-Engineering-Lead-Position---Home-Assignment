# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 21:32:27 2023

This script fetches player roster information from the Vikings NFL Team website and inserts it into a PostgreSQL database.

Please note that the database connection details are hardcoded in this script for demonstration purposes only.
In a real-world scenario, it's better to store sensitive information like database credentials in a secure manner.

@author: Maz
"""
import requests
from bs4 import BeautifulSoup
import psycopg2

# Function to insert data into PostgreSQL
def insert_player_data(data):
    """
    Inserts player data into a PostgreSQL database.

    Args:
    data (list): A list of dictionaries containing player information.

    Returns:
    None
    """
    conn = psycopg2.connect(
        database="Home Assignment",
        user="postgres",
        password="test1",
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()
    insert_query = """
        INSERT INTO players (name, jersey_number, position, height, weight, age, experience, college, photo_url)
        VALUES (%(name)s, %(jersey_number)s, %(position)s, %(height)s, %(weight)s, %(age)s, %(experience)s, %(college)s, %(photo_url)s)
    """

    cursor.executemany(insert_query, data)
    conn.commit()
    conn.close()


url = "https://www.vikings.com/team/players-roster/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

roster_data = []

players = soup.find_all("tr")
for player in players:
    player_info = player.find_all("td")

    if len(player_info) == 8:
        name = player_info[0].find("a").text.strip()
        jersey_number = int(player_info[1].text.strip())
        position = player_info[2].text.strip()
        height = player_info[3].text.strip()
        weight = int(player_info[4].text.strip())
        age = int(player_info[5].text.strip())
        experience = player_info[6].text.strip()
        college = player_info[7].text.strip()

        # You can also extract the player's photo URL using the "img" tag inside the "picture" tag.
        photo_url = player_info[0].find("img")["src"]

        player_data = {
            "name": name,
            "jersey_number": jersey_number,
            "position": position,
            "height": height,
            "weight": weight,
            "age": age,
            "experience": experience,
            "college": college,
            "photo_url": photo_url,
        }

        roster_data.append(player_data)

# After processing the roster_data, call the insert function to store data in the database.
insert_player_data(roster_data)