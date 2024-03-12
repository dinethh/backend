from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_cors import CORS,cross_origin
from models import db, Users

app = Flask(__name__)

# Configure the database URI and suppress SQLAlchemy track modifications warning
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root1234@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

CORS(app,supports_credentials=True)
# Initialize the database with the Flask app
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Initialize Marshmallow for serialization
ma = Marshmallow(app)


# Define the UserSchema for serialization
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address', 'salary')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Define routes
@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/users')
def get_users():
    all_users = Users.query.all()
    result = users_schema.dump(all_users)
    return jsonify(users=result)


@app.route('/details/<int:id>')
def get_user(id):
    user = Users.query.get(id)
    return user_schema.jsonify(user)


@app.route('/save', methods=['POST'])
def save_user():
    name = request.json.get('name')
    address = request.json.get('address')
    salary = request.json.get('salary')

    if name and address and salary:
        user = Users(name=name, address=address, salary=salary)
        db.session.add(user)
        db.session.commit()
        return user_schema.jsonify(user)
    else:
        return jsonify(message="Incomplete data provided"), 400


@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    user = Users.query.get(id)

    name = request.json.get('name')
    address = request.json.get('address')
    salary = request.json.get('salary')

    if name and address and salary:
        user.name = name
        user.address = address
        user.salary = salary
        db.session.commit()
        return user_schema.jsonify(user)


@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    user = Users.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)
