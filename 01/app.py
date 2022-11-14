from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>sus mogus</h1>'
    # return "hello cruel world"

@app.route( '/user/<name>' )
def user(name):
    return '<h1>Witaj {}!'.format(name)

# app.add_url_rule('/', 'index', index) <- zastąpic app.route
if __name__ == '__main__':
    # app.run(host='0.0.0.0') # może być uruchomiony w lanie
    app.run()