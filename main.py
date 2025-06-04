from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import sqlite3

import database_manager as dbHandler

# Code snippet for logging a message
# app.logger.critical("message")

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

# Generate a unique basic 16 key: https://acte.ltd/utils/randomkeygen
app = Flask(__name__)
app.secret_key = b"_53oi3uriq9pifpff;apl"
csrf = CSRFProtect(app)


# Redirect index.html to domain root for consistent UX
@app.route("/index", methods=["GET"])
@app.route("/index.htm", methods=["GET"])
@app.route("/index.asp", methods=["GET"])
@app.route("/index.php", methods=["GET"])
@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)


@app.route("/", methods=["POST", "GET"])
@csp_header(
    {
        # Server Side CSP is consistent with meta CSP in layout.html
        "base-uri": "'self'",
        "default-src": "'self'",
        "style-src": "'self'",
        "script-src": "'self'",
        "img-src": "'self' data:",
        "media-src": "'self'",
        "font-src": "'self'",
        "object-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "worker-src": "'self'",
        "report-uri": "/csp_report",
        "frame-ancestors": "'none'",
        "form-action": "'self'",
        "frame-src": "'none'",
    }
)
def index():
    data = dbHandler.listMotorcycle()
    return render_template('/index.html', content=data)


@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")


@app.route("/forsale.html", methods=["GET"])
def forsale():
    motorcycles = dbHandler.listMotorcycle()
    return render_template("forsale.html", content=motorcycles)

@app.route('/gallery', methods=["GET"])
def gallery():
    gallery_content = dbHandler.listGallery()
    return render_template('gallery.html', gallery_content=gallery_content)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = dbHandler.getMotorcycleById(product_id)
    images = dbHandler.getMotorcycleImages(product_id)
    return render_template('product_detail.html', product=product, images=images)

@app.route('/gallery/<int:gallery_id>')
def gallery_detail(gallery_id):
    import sqlite3
    conn = sqlite3.connect('.database/data_source.db')
    cur = conn.cursor()
    # Get gallery info
    cur.execute("SELECT id, name, description, year FROM gallery WHERE id = ?", (gallery_id,))
    gallery = cur.fetchone()
    # Get images for this gallery item
    cur.execute("SELECT image_path FROM gallery_images WHERE gallery_id = ?", (gallery_id,))
    images = [row[0] for row in cur.fetchall()]
    conn.close()
    return render_template('gallery_detail.html', gallery=gallery, images=images)



# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
