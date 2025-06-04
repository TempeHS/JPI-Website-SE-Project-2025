import sqlite3

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

