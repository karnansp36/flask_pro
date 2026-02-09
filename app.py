from flask import Flask, render_template
from flask_cors import CORS
from routes import api_bp
from ai import ai_bp
app = Flask(__name__)
CORS(app)
app.register_blueprint(api_bp)
app.register_blueprint(ai_bp, url_prefix='/ai')

@app.route('/hello', methods=["POST"])
def hello():

    return render_template('index.html', )


if __name__ == '__main__':
    app.run(debug=True)
