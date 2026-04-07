from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from extensions import db, ma
from routes.task_routes import tasks_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(tasks_bp)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
