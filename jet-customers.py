# JetCustomers - Find Common jet clients with ease
#
# Easly identify common customers by your own notes.
#
# powered by python
# Written by Noam Alum
#
# GitHub page at https://github.com/Noam-Alum/Jet-Customers/
#
# © Ncode. All rights reserved
# Visit ncode.codes for more scripts like this :)

## IMPORTS
import sqlite3
import os

## CONFIGURATION
# DATABASE
DB_location="/var/lib/jet-customers/"
DB_name="Jet_Customers_db"

## FUNCTIONS
# RUN QUERY
def sqlite(query):
    # define sqlite
    connection = sqlite3.connect(DB_location + DB_name)
    cursor = connection.cursor()

    # run query
    cursor.execute(query)

    # fetch result
    result = cursor.fetchall()

    # commit changes and close connection
    connection.commit()
    connection.close()

    return result

# add
def sqlite_add():
    client_info = ['full_name', 'company', 'mail', 'phone', 'url', 'note']
    user_inputs = {}

    for info in client_info:
        user_input = input(f"Clients {info} [skip for unknown] : ")
        if user_input.strip() and (info != 'phone' or user_input.strip().isdigit()):
            user_inputs[info] = user_input
        else:
            user_inputs[info] = "NULL"

    sqlite(f"INSERT INTO customers (\
        full_name, company, mail, phone, url, note\
    ) VALUES (\
        '{user_inputs['full_name']}',\
        '{user_inputs['company']}',\
        '{user_inputs['mail']}',\
        '{user_inputs['phone']}',\
        '{user_inputs['url']}',\
        '{user_inputs['note']}'\
    );")

# search
def sqlite_search():
    table_schema = ['full_name', 'company', 'mail', 'phone', 'url', 'note']

    filters = []
    while len(filters) < 5:
        filter = input(f"What information would you like to get? (DONE to exit) [Current: {filters}] : ")
        if filter == "DONE":
            break
        elif filter == "*":
            filters.append(filter)
            break
        elif filter not in table_schema:
            print(f"\nFilter does not exist, choose from this selection: \n{table_schema}\n")
        elif filter:
            filters.append(filter)

    search = ""
    while not search:
        search = input("What would you like to search for? : ")
        if search not in table_schema:
            print(f"\nSearch does not exist, choose from this selection: \n{table_schema}\n")
            search=""

    what2find = ""
    while not what2find:
        what2find = input(f"What would you like to search for in {search}? : ")

    res = sqlite(f"SELECT {', '.join(filters)} FROM customers WHERE {search} LIKE '%{what2find}%'")

    if res:
        print(f"\nResults:\n{', '.join(filters)}")
        for row in res:
            print(row)
    else:
        print("\nNo matching records found.")

# remove
def sqlite_remove():
    table_schema = ['full_name', 'company', 'mail', 'phone', 'url', 'note']

    search = ""
    while not search:
        search = input("What would identify what you are trying to remove? : ")
        if search not in table_schema:
            print(f"\nSearch does not exist, choose from this selection: \n{table_schema}\n")
            search=""

    what2find = ""
    while not what2find:
        what2find = input(f"What would you like to search for in {search}? : ")

    sqlite(f"DELETE FROM customers WHERE {search} = '{what2find}';")

    # Verifying removal
    res = sqlite(f"SELECT * FROM customers WHERE {search} = '{what2find}';")

    if not res:
        print(f"\nSuccessfully removed {what2find} or it does not exist.")
    else:
        print(f"\nFailed to remove {what2find}. Record still exists.")

## MAIN
# create dir if not exist
os.makedirs(DB_location, exist_ok=True)

# create db & table if not exist
sqlite("CREATE TABLE IF NOT EXISTS customers (\
    id INTEGER PRIMARY KEY,\
    full_name TEXT NOT NULL,\
    company TEXT NOT NULL,\
    mail TEXT NOT NULL,\
    phone INTEGER,\
    url TEXT NOT NULL,\
    note TEXT\
);")

# loop
while True:

    # get actiom
    actions = ['add', 'remove', 'search']
    action=""
    while not action:
        action = input("What action would you like to take? : ")
        if action not in actions:
            print(f"\nPlease choose from the following actions:\n{actions}\n")
            action = ""

    # run action
    if action == "add":
        sqlite_add()
    elif action == "remove":
        sqlite_remove()
    else:
        sqlite_search()
