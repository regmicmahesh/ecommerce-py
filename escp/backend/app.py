from flask import Flask, Response, make_response, render_template, request
from flask_apscheduler import APScheduler
from sqlmodel import Session, create_engine

from escp.crons.syncFromDB import syncFromDB
from escp.models.Product import Product, parseResponseFromURL
from escp.utils.db import engine


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)

scheduler = APScheduler()

scheduler.init_app(app)
app.config.from_object(Config())

scheduler.task('cron', id='do_job_1', hour='22', minute='27')(syncFromDB)
scheduler.start()


def is_valid(url):
    if url.startswith("https://www.daraz.com.np"):
        return url.split(".html")[0] + ".html"
        return url


@app.route('/', methods=['GET', 'POST'])
def post_link():
    if request.method == 'POST':
        url = request.form.get('url', "")
        if not is_valid(url):
            return Response(status=400)

        try:
            product, product_price = parseResponseFromURL(url)
        except:
            return Response(status=400)

        with Session(engine) as session:
            try:
                session.add(product)
                session.commit()
                session.refresh(product)

                product_price.product_id = product.id
                session.add(product_price)
                session.commit()

            except:
                return Response(status=400)

        return Response(status=200)

    if request.method == 'GET':
        return render_template("index.html")


if __name__ == '__main__':
    app.run()
