from edge_server import app

if __name__ == "__main__":
    app.create_app()
    app.run(host='0.0.0.0')
