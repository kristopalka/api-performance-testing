import random
import logging

from flask import Flask, jsonify
from flask_restful import Api, Resource

from src.database import db, Message
from src.fibonacci import generate_fibonacci

app = Flask(__name__)

log = logging.getLogger('werkzeug')
# log.setLevel(logging.WARNING)

app.config['SQLALCHEMY_DATABASE_URI'] = "mariadb+mariadbconnector://user:password@mariadb:3306/database"
db.init_app(app)
api = Api(app)


class Hello(Resource):
    def get(self):
        return jsonify({"message": "Hello World!"})


class Fibonacci(Resource):
    def get(self, n):
        if n < 0:
            return {"error": "Invalid input, n must be a non-negative integer"}, 400

        value = generate_fibonacci(n)
        return jsonify({"number": n, "value": value})


class Database(Resource):
    def get(self):
        random_id = random.randint(1, 25)
        message = Message.query.get(random_id)

        if not message:
            return {"error": "Message not found"}, 404

        return jsonify({"message": message.val})


# Add routes
api.add_resource(Hello, '/hello')
api.add_resource(Fibonacci, '/fibonacci/<int:n>')
api.add_resource(Database, '/database')

if __name__ == '__main__':
    app.run(debug=False, port=8080)
