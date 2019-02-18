from flask_site import app

@app.route('/')
def show_entries():
    return "Hello World!"
