from flask import Flask
from services.customer.CustomerController import customer_blueprint


app = Flask(__name__)

app.register_blueprint(customer_blueprint)


if __name__ == '__main__':
    app.run(debug=True)