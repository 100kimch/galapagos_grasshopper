# NOTE: detecting crosswalk algorithm
# from OpenSSL import SSL
from flask import Flask, render_template, send_file, jsonify, Response, request
from flask_graphql import GraphQLView
from time import time

session = {
    'sequence': 0
}

app = Flask(__name__)


# def create_app():
#     global app

# context = SSL.Con
# app.add_url_rule(
#     '/graphql',
#     view_func=GraphQLView.as_view(
#         'graphql',
#         schema=app.schema,
#         graphiql=True  # for having the GraphiQL interface
#     ))
@app.route('/test')
def hello_world():
    res = Response()

    http_method = request.method

    if http_method == "OPTIONS":
        print("-- Preflight Request --")
        res.headers.add("Access-Control-Allow_Origin", "*")
        res.headers.add("Access-Control-Allow-Headers", "*")
        res.headers.add("Access-Control-Allow-Methods", "GET,DELETE")
    elif http_method == "GET":
        print("-- GET --")
        res.headers.add("Access-Control-Allow-Origin", "*")
        res.set_data("Done!")

    return res
    # return jsonify(msg='Hello World!')


@app.route('/tick')
def time_tick():
    if int(time()) % 10 < 5:
        return jsonify(msg="Successfully received a tick.", val="1")
    else:
        return jsonify(msg="Successfully received a tick.", val="0")


@app.route('/')
def index():
    return render_template(
        'index.html',
        title='testing',
        testing='Hello!',
        image_file='images/sample.png',
        has_image=True
    )

# @app.route('/get_image')
# def get_image():
#     if Flask.request.args.get('type') == 1:
# return app


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()

if __name__ == "__main__":
    # create_app()
    app.run(host='0.0.0.0')
