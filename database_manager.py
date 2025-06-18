import sqlite3
import sqlite3 as sql

def listMotorcycle():
    conn = sqlite3.connect('.database/data_source.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT m.*, (
            SELECT image_path
            FROM motorcycle_images mi
            WHERE mi.motorcycle_id = m.extID
            ORDER BY mi.id ASC
            LIMIT 1
        ) as image_path
        FROM motorcycles m
    """)
    motorcycles = cur.fetchall()
    conn.close()
    return motorcycles

def getMotorcycleById(product_id):
    conn = sqlite3.connect('.database/data_source.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM motorcycles WHERE extID = ?", (product_id,))
    product = cur.fetchone()
    conn.close()
    return product

def getMotorcycleImages(product_id):
    conn = sqlite3.connect('.database/data_source.db')
    cur = conn.cursor()
    cur.execute("SELECT image_path FROM motorcycle_images WHERE motorcycle_id = ?", (product_id,))
    images = [row[0] for row in cur.fetchall()]
    conn.close()
    return images

def listGallery():
    conn = sqlite3.connect('.database/data_source.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT g.id, g.name,
            (SELECT image_path FROM gallery_images gi WHERE gi.gallery_id = g.id ORDER BY gi.id ASC LIMIT 1) as image_path
        FROM gallery g
    """)
    gallery_content = cur.fetchall()
    conn.close()
    return gallery_content

def getSoldMotorcycleById(product_id):
    conn = sqlite3.connect('.database/data_source.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM sold_motorcycles WHERE id = ?", (product_id,))
    product = cur.fetchone()
    conn.close()
    return product

def getSoldMotorcycleImages(product_id):
    conn = sqlite3.connect('.database/data_source.db')
    cur = conn.cursor()
    cur.execute("SELECT image_path FROM sold_images WHERE sold_id = ?", (product_id,))
    images = [row[0] for row in cur.fetchall()]
    conn.close()
    return images

def listSoldMotorcycles():
    conn = sqlite3.connect('.database/data_source.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT s.*, (
            SELECT image_path
            FROM sold_images smi
            WHERE smi.sold_id = s.id
            ORDER BY smi.id ASC
            LIMIT 1
        ) as image_path
        FROM sold_motorcycles s
    """)
    sold_motorcycles = cur.fetchall()
    conn.close()
    return sold_motorcycles

def authenticate_user(username, password):
    conn = sqlite3.connect('.database/data_source.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user is not None

def addMotorcycle(name, price, about, location, year, contact):
    conn = sqlite3.connect('.database/data_source.db')
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO motorcycles (name, price, about, location, year, contact) VALUES (?, ?, ?, ?, ?, ?)",
        (name, price, about, location, year, contact)
    )
    motorcycle_id = cur.lastrowid
    conn.commit()
    conn.close()
    return motorcycle_id

def addMotorcycleImage(motorcycle_id, image_path):
    conn = sqlite3.connect('.database/data_source.db')
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO motorcycle_images (motorcycle_id, image_path) VALUES (?, ?)",
        (motorcycle_id, image_path)
    )
    conn.commit()
    conn.close()

