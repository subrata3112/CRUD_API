from django.shortcuts import render
from passlib.hash import argon2
import psycopg2


def connect_to_db():

    connection = psycopg2.connect(

        host = "john.db.elephantsql.com",
        user = "iqxodjwg",
        password = "mi8fWdkQ2Ut6RhgZ_xi5lCWpehj6lnKl",
        database = "iqxodjwg",
        port = "5432"
    )
    return connection

def query_exec(query):

    connection = connect_to_db()
    # connection.autocommit(True)
    # print(connection)
    cursor = connection.cursor()

    cursor.execute(query)
    # result = cursor.fetchone()
    connection.commit()

def query_fetch(query):

    connection = connect_to_db()
    # print(connection)
    cursor = connection.cursor()

    cursor.execute(query)
    result = cursor.fetchone()
    connection.commit()
    return result

def encryptor(password):
    hashed = argon2.hash(password)
    return hashed

def pass_verify(string,hashed):
    return argon2.verify(string,hashed)