# originallly from https://github.com/techytushar/random-memer
import requests
from flask import Flask, send_file, render_template, jsonify, redirect
import random
from io import BytesIO
from PIL import Image
import json

app = Flask(__name__, static_url_path="/pages")

s = requests.Session()


def get_repo_images(a, b, c):
    url = f"https://api.github.com/repos/{a}/{b}/contents/{c}"
    print(url)
    data = json.loads(s.get(url).content)
    imgs = []
    for i in data:
        try:
            if i["download_url"].split(".")[-1] in ["jpg", "png", "jpeg"]:
                imgs.append(i["download_url"])
        except:
            print(">> Error")
            print(">> Redirecting to home")
            return redirect("/")
    return imgs


def serve_pil_image(pil_img):
    img_io = BytesIO()
    if pil_img.mode in ("RGBA", "P"):
        print(">> Converting to RGB")
        pil_img = pil_img.convert("RGB")
    pil_img.save(img_io, "JPEG", quality=80)
    img_io.seek(0)
    return send_file(img_io, mimetype="image/jpeg")


@app.after_request
def set_response_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route("/", methods=["GET"])
def homie():
    return render_template("index.html")


@app.route("/<a>/<b>/<c>/list", methods=["GET"])
def return_img_list(a, b, c):
    img_urls = get_repo_images(a, b, c)
    return jsonify(img_urls)


@app.route("/<a>/<b>/<c>", methods=["GET"])
def return_img(a, b, c):
    img_urls = random.choice(get_repo_images(a, b, c))
    res = s.get(img_urls, stream=True)
    res.raw.decode_content = True
    img = Image.open(res.raw)
    return serve_pil_image(img)


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")
