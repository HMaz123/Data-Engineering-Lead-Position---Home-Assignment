# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 00:47:37 2023

@author: Maz
"""
from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# Database connection
connection = psycopg2.connect(
    dbname="Home Assignment",
    user="postgres",
    password="test1",
    host="localhost",
    port="5432",
)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/players", methods=["GET"])
def get_players():
    # Get filter criteria from request parameters
    name = request.args.get("name", default="", type=str)
    position = request.args.get("position", default="", type=str)
    age = request.args.get("age", default="", type=int)

    # Build the SQL query based on the filter criteria
    query = "SELECT * FROM players WHERE 1=1"
    params = []
    if name:
        query += " AND name LIKE %s"
        params.append(f"%{name}%")
    if position:
        query += " AND position = %s"
        params.append(position)
    if age:
        query += " AND age = %s"
        params.append(age)

    cursor = connection.cursor()
    cursor.execute(query, params)
    players = cursor.fetchall()
    cursor.close()

    return jsonify(players)

if __name__ == "__main__":
    app.run(debug=True)