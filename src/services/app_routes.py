from flask import Flask
from services.customer.CustomerController import customer_blueprint
from services.application.ApplicationController import application_blueprint
from services.loan.LoanController import loan_blueprint

app = Flask(__name__)

app.register_blueprint(customer_blueprint)
app.register_blueprint(application_blueprint)
app.register_blueprint(loan_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
