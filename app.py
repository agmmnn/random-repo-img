# originally from: https://github.com/techytushar/random-memer
import requests
from flask import Flask, send_file, render_template, jsonify, redirect
from random import choice
from io import BytesIO
from PIL import Image

app = Flask(__name__, static_url_path="/pages")

GH_API_KEY = ""
s = requests.Session()

# https://random-repo-img.herokuapp.com/agmmnn/random-repo-img/sample_imgs
# https://api.github.com/repos/agmmnn/random-repo-img/contents/sample_imgs
def get_repo_images(a, b, c):
    url = f"https://api.github.com/repos/{a}/{b}/contents/{c}"
    headers = {"Authorization": "token " + GH_API_KEY}
    data = s.get(url, headers=headers).json()
    imgs = []

    for i in data:
        try:
            if i["download_url"].split(".")[-1] in ["jpg", "png", "jpeg"]:
                imgs.append(i["download_url"])
        except:
            return False
    print(url)
    print(imgs)
    print(len(imgs))
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
    img_urls = get_repo_images(a, b, c)
    if img_urls == False:
        print(">> Error!\n>> Redirecting to home")
        return redirect("/")
    r_img_urls = choice(get_repo_images(a, b, c))
    res = s.get(r_img_urls, stream=True)
    res.raw.decode_content = True
    img = Image.open(res.raw)
    return serve_pil_image(img)


@app.errorhandler(404)
def page_not_found(e):
    print(">> 404!\n>> Redirecting to home")
    return redirect("/")
