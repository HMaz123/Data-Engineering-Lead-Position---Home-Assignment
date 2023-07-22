        # -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 17:14:59 2023

This script scrapes character information from the TV show Vikings and saves it in a PostgreSQL database.
It also downloads the character images and stores them in a local "images" folder.

Please note that the database connection details are hardcoded in this script for demonstration purposes only.
In a real-world scenario, it's better to store sensitive information like database credentials in a secure manner.


Make sure you have set up a PostgreSQL database with a table named "characters" with appropriate columns:
CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    character_name VARCHAR(255) NOT NULL,
    actor_name VARCHAR(255) NOT NULL,
    image_path VARCHAR(255) NOT NULL
);

Author: Maz
"""
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import psycopg2

def scrape_imdb_characters(url):
    """
    Scrapes character information from an IMDb TV show page.

    Args:
    url (str): The URL of the IMDb TV show page.

    Returns:
    A list of dictionaries containing character data (character_name, actor_name, image_path).
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    characters_data = []

    # Find all the character divs
    character_divs = soup.find_all("div", {"data-testid": "title-cast-item"})
    for character_div in character_divs:
        # Extract character name
        character_name = character_div.select_one(".title-cast-item__char").text.strip()

        # Extract actor name
        actor_name = character_div.select_one(".title-cast-item__actor").text.strip()

        # Extract image URL and download the image
        image_url = character_div.select_one(".ipc-avatar__avatar-image")["src"]
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image = Image.open(BytesIO(image_response.content))

            # Save image
            image_path = f"images/{character_name.replace(' ', '_')}.jpg"
            image.save(image_path)
        else:
            print(f"Failed to fetch the image for {character_name}. Status code: {image_response.status_code}")
            continue

        characters_data.append({
            "character_name": character_name,
            "actor_name": actor_name,
            "image_path": image_path
        })

    return characters_data

def insert_data_into_database(character_data):
    """
    Inserts character data into the PostgreSQL database.

    Args:
    character_data: A list of dictionaries containing character data.

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
        INSERT INTO characters (character_name, actor_name, image_path)
        VALUES (%(character_name)s, %(actor_name)s, %(image_path)s)
    """

    cursor.executemany(insert_query, character_data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    imdb_url = "https://www.imdb.com/title/tt5905354/"
    characters_info = scrape_imdb_characters(imdb_url)

    for character_info in characters_info:
        print(f"Character: {character_info['character_name']}")
        print(f"Actor: {character_info['actor_name']}")
        print(f"Image saved to: {character_info['image_path']}")
        print("---")

    # Save the data to the PostgreSQL database
    insert_data_into_database(characters_info)

    print("Scraped data and images saved successfully and data added to the database.")