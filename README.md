![](cover.jpg)

# 🧤[random-repo-img](https://randomrepoimg.fly.dev/)

A simple tool to pick and return a random image from the given github repo folder.

- url structure: `randomrepoimg.fly.dev/<user>/<repo>/<folder>`

## Example Usage:

- url: [https://randomrepoimg.fly.dev/agmmnn/random-repo-img/sample_imgs](https://randomrepoimg.fly.dev/agmmnn/random-repo-img/sample_imgs)

### Preview (Refresh the page):

![random](https://randomrepoimg.fly.dev/agmmnn/random-repo-img/sample_imgs)

## Development

### Serve

```py
# using gunicorn
gunicorn --bind 127.0.0.1:5000 app:app

# using waitress
waitress-serve --listen=127.0.0.1:5000 app:app
```

### Deploy

```py
# using fly.io

flyctl deploy
```
