# NOTE: detecting crosswalk algorithm
# from OpenSSL import SSL
from flask import Flask, render_template, send_file, jsonify, Response, request
from flask_graphql import GraphQLView
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> b0510df... applied uwsgi
from time import time

session = {
    'sequence': 0
}

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> b0510df... applied uwsgi
app = Flask(__name__)
=======

from 
>>>>>>> f1dd3e0... applied uwsgi
<<<<<<< HEAD
=======
from time import time

session = {
    'sequence': 0
}
>>>>>>> 0980a45... test connections
=======
app = null
>>>>>>> 0b9629c... fixed minor errors
=======
app = Flask(__name__)
>>>>>>> 3ec40bd... fixed minor errors
=======
>>>>>>> b0510df... applied uwsgi


def create_app():
    global app
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> b0510df... applied uwsgi

    # context = SSL.Con
    # app.add_url_rule(
    #     '/graphql',
    #     view_func=GraphQLView.as_view(
    #         'graphql',
    #         schema=app.schema,
    #         graphiql=True  # for having the GraphiQL interface
    #     ))
<<<<<<< HEAD
=======
    app = Flask(__name__)
>>>>>>> 0b9629c... fixed minor errors
=======
>>>>>>> 3ec40bd... fixed minor errors

    # context = SSL.Con
    # app.add_url_rule(
    #     '/graphql',
    #     view_func=GraphQLView.as_view(
    #         'graphql',
    #         schema=app.schema,
    #         graphiql=True  # for having the GraphiQL interface
    #     ))
=======

    # context = SSL.Con
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=app.schema,
            graphiql=True  # for having the GraphiQL interface
        ))
>>>>>>> b0510df... applied uwsgi

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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> b0510df... applied uwsgi
            print("-- GET --")
=======
            print("-- GET -- ")
>>>>>>> f1dd3e0... applied uwsgi
<<<<<<< HEAD
=======
            print("-- GET --")
>>>>>>> 0980a45... test connections
=======
>>>>>>> b0510df... applied uwsgi
            res.headers.add("Access-Control-Allow-Origin", "*")
            res.set_data("Done!")

        return res
        # return jsonify(msg='Hello World!')
<<<<<<< HEAD

    @app.route('/tick')
    def time_tick():
        if int(time()) % 10 < 5:
            return 1
        else:
            return 0
=======
>>>>>>> f1dd3e0... applied uwsgi
<<<<<<< HEAD

    @app.route('/tick')
    def time_tick():
        if int(time()) % 10 < 5:
            return 1
        else:
            return 0
=======
>>>>>>> b0510df... applied uwsgi

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
    return app

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> b0510df... applied uwsgi

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()


if __name__ == "__main__":
    create_app()
    app.run(host='0.0.0.0')
=======
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
>>>>>>> f1dd3e0... applied uwsgi
<<<<<<< HEAD
=======

# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()


<<<<<<< HEAD
<<<<<<< HEAD
def
>>>>>>> 0980a45... test connections
=======
def __name__ == "__main__":
=======
if __name__ == "__main__":
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> c1e6c90... fixed minor errors
=======
    global app
>>>>>>> 0b9629c... fixed minor errors
=======
>>>>>>> b509d07... fixed minor errors
=======
    create_app()
>>>>>>> 29fcfe9... fixed minor errors
    app.run(host='0.0.0.0')
>>>>>>> 7ed39aa... fixed minor errors
=======
>>>>>>> b0510df... applied uwsgi
