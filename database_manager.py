import sqlite3 as sql

def listMotorcycle():
    con = sql.connect("/workspaces/JPI-Website-SE-Project-2025/.database/data_source.db")
    cur = con.cursor()
    data = cur.execute('SELECT * FROM motorcycles').fetchall()
    con.close()
    return data