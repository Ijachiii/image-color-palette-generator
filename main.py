from flask import Flask, render_template, url_for, redirect, request, session
import os
from werkzeug.utils import secure_filename
from PIL import Image
import webcolors
from colorthief import ColorThief

UPLOAD_FOLDER = os.path.join("static", "images")
app = Flask(__name__, static_folder="static")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "daveisdagoat"

colors = []


@app.route("/", methods=["GET", "POST"])
def home():
    global img_filename
    if request.method == "POST":
        image = request.files["img"]
        img_filename = secure_filename(image.filename)
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))
        session["image_file_path"] = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
        return redirect(url_for("show"))
    return render_template("index.html")


@app.route("/show")
def show():
    img_file_path = f"static/images/{img_filename}"
    with open(img_file_path, "r+b") as f:
        with Image.open(f) as image:
            color_thief = ColorThief(img_file_path)
            color_palette = color_thief.get_palette(color_count=10, quality=10)
            for color in color_palette:
                colors.append(webcolors.rgb_to_hex(color))
            top_colors = colors[:10]
    return render_template("colors.html", user_image=img_file_path, colors=top_colors)


if __name__ == "__main__":
    app.run(debug=True)