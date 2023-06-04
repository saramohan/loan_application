from flask import Blueprint, request, jsonify
import flask_restful
from lib.logger_utils import get_logger
from services.customer.CustomerLogics import CustomerDetailsBusinessLogics

LOG = get_logger(__name__)

customer_blueprint = Blueprint('customer', __name__, url_prefix='/v1.0/customer')
customer_api = flask_restful.Api(customer_blueprint)


class CustomerDetails(flask_restful.Resource):

    def post(self):
        """
        :summary: 1. Receives a request to create user with the details present in the request data.
                  2. The PII details like email_id, dob and password are encrypted
                  3. Later a search is made in the `customer` table to check if the email_id is already present.
                  4. If the email_id is already present then we send a response saying the customer already exists.
                  5. If there is no record for the email_id, then a new record is created in the customer table
                     and the success response is sent back.

        :endpoint: POST call to http://localhost:5000/v1.0/customer/createuser
        :request_data: {'first_name': 'Hermoine',
                        'last_name': 'Granger',
                        'date_of_birth': '13-10-1990',
                        'email_id': 'hermoine_granger@example.com',
                        'password': 'S@mpl$!'
                        }
        :response : 1. Customer already exists in the system
                            {'status': 'error', 'error_text': 'Customer already exists'}
                    2. Customer is created newly
                            {'status': 'success', 'customer_id': customer_id}
        : Any other exception will throw 500 Internal server Error!!
        """
        try:
            request_data = request.get_json()
            LOG.info("POST request received for customer first name : %s  last name : %s",
                     request_data.get('first_name'), request_data.get('last_name'))
            business_logic_obj = CustomerDetailsBusinessLogics()
            response = business_logic_obj.create_user(request_data)
            LOG.info("Response formulated : %s", response)
            return jsonify(response)
        except Exception as ex:
            LOG.exception("Exception occurred in POST call of /createuser")
            flask_restful.abort(500, message="Internal Server Error")


customer_api.add_resource(CustomerDetails, '/createuser')


class CustomerAuthentication(flask_restful.Resource):

    def post(self):
        """
        :summary: 1. Receives a request to authenticate user with the details present in the request data.
                  2. The customer details(email_id and password) are checked with the details in the
                     customer table.
                  3. If the customer details match with the details in the table then the customer
                     is authenticated.
                  4. Else the customer is not authenticated.

        :endpoint: POST call to http://localhost:5000/v1.0/customer/authenticate
        :request_data: {
                        'email_id': 'hermoine_granger@example.com',
                        'password': 'S@mpl$!'
                       }
        :response : 1. If the customer is authenticated
                           {'authentication_status': 'success', 'customer_id': 1}
                    2. Customer is not authenticated
                           {'authentication_status': 'failure'}
        : Any other exception will throw 500 Internal server Error!!
        """
        try:
            request_data = request.get_json()
            LOG.info("POST request received for authentication of customer email")
            business_logic_obj = CustomerDetailsBusinessLogics()
            response = business_logic_obj.authenticate_user(request_data)
            LOG.info("Response formulated : %s", response)
            return jsonify(response)
        except Exception:
            LOG.exception("Exception occurred in POST call of /authenticate")
            flask_restful.abort(500, message="Internal Server Error")


customer_api.add_resource(CustomerAuthentication, '/authenticate')