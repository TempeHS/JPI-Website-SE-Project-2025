from flask import Flask, redirect, render_template, url_for, request, session
from flask import flash  
from flask import jsonify
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import os
from werkzeug.utils import secure_filename
import pyotp
import qrcode

import database_manager as dbHandler
from sv_user import sanitize_input

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

app = Flask(__name__)
app.secret_key = "L_l~qr=s(kp~mSZ2Ova$7hX?DXV?R5q"
## csrf = CSRFProtect(app)

##WTF_CSRF_ENABLED = False

UPLOAD_FOLDER = 'static/images/motorcycles'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = sanitize_input(request.form.get("username"))
        password = request.form.get("password")
        if dbHandler.authenticate_user(username, password):
            session["username"] = username

            # Get or create TOTP secret for this user
            secret = dbHandler.get_user_totp_secret(username)
            if not secret:
                secret = pyotp.random_base32()
                dbHandler.set_user_totp_secret(username, secret)
            session["secret"] = secret
            session["user_id"] = username
            return redirect(url_for("show_qr"))
        else:
            error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route('/show_qr', methods=['GET', 'POST'])
def show_qr():
    if request.method == 'POST':
        otp = request.form.get('otp')
        secret = session.get('secret')
        totp = pyotp.TOTP(secret)
        if otp and totp.verify(otp):
            session.pop('secret', None)
            return redirect(url_for('userhome'))
        else:
            flash('Incorrect Code')
            return redirect(url_for('show_qr'))
    
    secret = session.get('secret')
    email = session.get('user_id')
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=email, issuer_name="Jim Parker Indian Motorcycles")
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    
    # Save QR code to a temporary file
    img_path = os.path.join('static', 'qr_code.png')
    img.save(img_path)
    
    return render_template('qrcode.html', qr_code_url=url_for('static', filename='qr_code.png'))



@app.route("/cards", methods=["GET", "POST"])
def cards():
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        about = request.form.get("description")
        location = request.form.get("location")
        year = request.form.get("year")
        contact = request.form.get("contact")
        images = request.files.getlist("images")
        motorcycle_id = dbHandler.addMotorcycle(name, price, about, location, year, contact)
        for image in images:
            if image and image.filename:
                filename = secure_filename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(save_path)
                dbHandler.addMotorcycleImage(motorcycle_id, save_path)
        return redirect(url_for('cards', success=1))
    success = request.args.get('success')
    return render_template("cards.html", success=success)

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

@app.route("/sold.html", methods=["GET"])
def sold():
    sold_content = dbHandler.listSoldMotorcycles()
    return render_template('sold.html', sold_content=sold_content)

@app.route("/sold_motorcycle/<int:product_id>")
def sold_motorcycle_detail(product_id):
    product = dbHandler.getSoldMotorcycleById(product_id)
    images = dbHandler.getSoldMotorcycleImages(product_id)
    return render_template("sold_detail.html", product=product, images=images)


# Endpoint for logging CSP violations
@app.route("/csp_report", methods=["POST"])
##@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"


@app.route("/add_admin", methods=["GET", "POST"])
def adduser():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not username or not email or not password:
            error = "All fields are required."
        else:
            success = dbHandler.add_user(username, email, password)
            if success:
                return redirect(url_for('/add_admin'))
            else:
                error = "Username or email already exists."
    return render_template("adduser.html", error=error)

@app.route("/userhome", methods=["GET"])
def userhome():
    return render_template("userhome.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
