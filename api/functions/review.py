import time
from flask import Flask
from flask_restplus import Resource, Api, fields, reqparse, inputs
import sqlite3
import json
import pandas as pd
from pandas.io import sql
from requests import get
import re
import hashlib

# Insert new value into users database
# CONSIDER: better way of getting the user_id from a token?
# How do we know the user_id from the request


def newReview(user_id, movie_id, comment, score):
    # check that the movie_id exists in the movie db
    if not movieIdExists(movie_id):
        raise ValueError(f"No movie with id: {movie_id} exists in the database")

    # check that the user_id exists in the user db
    if not userIdExists(user_id):
        raise ValueError(f"No user with id: {user_id} exists in the database")

    if score < 0:
        raise ValueError("Score cannot be negative")
    elif score > 10:
        raise ValueError("Score cannot be greater than 10")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(f"select * from users where user_id = {user_id}")

    cur.execute("select * from review;")
    review_id = len(cur.fetchall()) + 1
    cur.execute(
        f"""
        INSERT INTO review(review_id, user_id, movie_id, comment, score, num_likes)
        VALUES ({review_id}, {user_id}, {movie_id}, "{comment}", {score}, 0);
        """
    )
    conn.commit()
    conn.close()

    return {"success": "True"}


def editReview(review_id, comment, score):
    if not reviewIdExists(review_id):
        raise ValueError(f"No review with id: {review_id} exists in the database")
    if score < 0:
        raise ValueError("Score cannot be negative")
    elif score > 10:
        raise ValueError("Score cannot be greater than 10")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(
        f'UPDATE review SET comment = "{comment}", score = {score} where review_id = {review_id};'
    )
    conn.commit()
    conn.close()
    return {"success": "True"}


# Increment the review num likes by 1
def incrementLikes(review_id):
    if not reviewIdExists(review_id):
        raise ValueError(f"No review with id: {review_id} exists in the database")
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(f"select * from review where review_id = {review_id};")
    num_likes = cur.fetchone()[5] + 1
    cur.execute(
        f"UPDATE review SET num_likes = {num_likes} where review_id = {review_id};"
    )
    conn.commit()
    conn.close()
    return {"success": "True"}


def movieIdExists(movie_id):
    movie_conn = sqlite3.connect("movieDB.db")
    movie_cur = movie_conn.cursor()
    movie_cur.execute(f"select * from movie where movie_id = {movie_id};")
    if len(movie_cur.fetchall()) == 0:
        return False
    movie_conn.close()
    return True


def userIdExists(user_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(f"select * from users where user_id = {user_id}")
    if len(cur.fetchall()) == 0:
        return False
    conn.close()
    return True


def reviewIdExists(review_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(f"select * from review where review_id = {review_id}")
    if len(cur.fetchall()) == 0:
        return False
    conn.close()
    return True