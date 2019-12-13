from flask import flask

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def index():
    return "Hello. World from PA"

@app.route('/books/<int:id>')
def getBook(id):
    return "You want book with id"+ str(id)

if __name__ == '__main__' :
    app.run(debug= True)