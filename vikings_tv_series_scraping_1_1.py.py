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
    image_url TEXT NOT NULL
);

Author: Maz
"""
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2

def scrape_vikings_cast_info():
    """
    Scrapes character information from the Vikings website.

    Returns:
    A list of dictionaries containing character data.
    """
    url = "https://www.history.com/shows/vikings/cast"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    character_data = []

    character_elements = soup.find_all("div", class_="details")
    for character_element in character_elements:
        character_name = character_element.find("strong").text.strip()
        actor_name = character_element.find("small").text.strip()
        image_url = character_element.find_previous("img")["src"]

        character_data.append({
            "Character": character_name,
            "Actor": actor_name,
            "Image URL": image_url,
        })

    return character_data

def save_images(character_data):
    """
    Downloads and saves character images to a local "images" folder.

    Args:
    character_data: A list of dictionaries containing character data with image URLs.
    """
    os.makedirs("images", exist_ok=True)
    for data in character_data:
        image_url = data["Image URL"]
        image_name = image_url.split("/")[-1].split("?")[0]  # Remove query string
        image_path = os.path.join("images", image_name)

        with open(image_path, "wb") as f:
            response = requests.get(image_url)
            f.write(response.content)

def create_table(character_data):
    """
    Converts the character data into a pandas DataFrame.

    Args:
    character_data: A list of dictionaries containing character data.

    Returns:
    A pandas DataFrame with the character information.
    """
    df = pd.DataFrame(character_data)
    return df

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
        INSERT INTO characters (character_name, actor_name, image_url)
        VALUES (%(Character)s, %(Actor)s, %(Image URL)s)
    """

    cursor.executemany(insert_query, character_data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    character_data = scrape_vikings_cast_info()
    save_images(character_data)
    df = create_table(character_data)
    # Save the DataFrame to a CSV file for later use if needed
    df.to_csv("vikings_characters.csv", index=False)

    # Save the data to the PostgreSQL database
    insert_data_into_database(character_data)

    print("Scraped data and images saved successfully and data added to the database.")