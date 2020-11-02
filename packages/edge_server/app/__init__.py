# NOTE: detecting crosswalk algorithm
from flask import Flask, render_template, send_file, jsonify


def create_app():
    app = Flask(__name__)

    @app.route('/test')
    def hello_world():
        return jsonify(msg='Hello World!')

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
