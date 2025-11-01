from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.chatbot_routes import chatbot_bp


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "CleanCity Portal Backend Running 🚀"})

app.register_blueprint(chatbot_bp)


if __name__ == '__main__':
    app.run(debug=True)
