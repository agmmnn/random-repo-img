# originally from: https://github.com/techytushar/random-memer
import os
import requests
from flask import Flask, send_file, render_template, jsonify, redirect
from random import choice
from io import BytesIO
from PIL import Image
from typing import List, Optional
from dotenv import dotenv_values


secrets = dotenv_values(".env")

app = Flask(__name__, static_url_path="/pages")
s = requests.Session()

# https://randomrepoimg.fly.dev/agmmnn/random-repo-img/sample_imgs
# https://api.github.com/repos/agmmnn/random-repo-img/contents/sample_imgs
def get_repo_images(owner: str, repo: str, path: str) -> Optional[List[str]]:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": "token " + secrets["GH_API_KEY"]}
    data = s.get(url, headers=headers).json()
    print(data)
    img_urls = [
        i["download_url"]
        for i in data
        if i["download_url"].split(".")[-1] in ["jpg", "png", "jpeg"]
    ]
    return img_urls or None


def serve_pil_image(pil_img: Image) -> send_file:
    img_io = BytesIO()
    if pil_img.mode in ("RGBA", "P"):
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
def index() -> str:
    return render_template("index.html")


@app.route("/<owner>/<repo>/<path>/list", methods=["GET"])
def return_img_list(owner: str, repo: str, path: str) -> jsonify:
    img_urls = get_repo_images(owner, repo, path)
    return (
        jsonify(img_urls)
        if img_urls
        else print(">> Cannot get images from github api!")
    )


@app.route("/<owner>/<repo>/<path>", methods=["GET"])
def return_img(owner: str, repo: str, path: str) -> send_file:
    img_urls = get_repo_images(owner, repo, path)
    if img_urls:
        r_img_url = choice(img_urls)
        res = s.get(r_img_url, stream=True)
        res.raw.decode_content = True
        img = Image.open(res.raw)
        return serve_pil_image(img)
    else:
        return redirect("/")


@app.errorhandler(404)
def page_not_found(e) -> jsonify:
    return jsonify({"404": "not found"})
