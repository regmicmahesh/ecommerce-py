from flask import Flask, request, render_template
from escp.models.Product import Product, parseResponseFromURL

app = Flask(__name__)


def is_valid(url):
    if url.startswith("https://www.daraz.com.np"):
        return True

@app.route('/', methods=['GET', 'POST'])

def post_link():
    if request.method == 'POST':
        data = dict(request.form)
        url = data['url']
        if is_valid(url):
            product = parseResponseFromURL(url)
            print(product)

    if request.method == 'GET':
        return render_template("index.html")


if __name__ == '__main__':
    app.run()