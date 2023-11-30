from flask import Flask, render_template
from flask_frozen import Freezer

app = Flask(__name__, template_folder='templates', static_folder='static')
freezer = Freezer(app)

@app.route('/index')  # Adjust the route as needed
def index():
    return render_template('app/index.html')

if __name__ == '__main__':
    app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
    freezer.freeze()