from flask import Blueprint, request, jsonify
import flask_restful
from lib.logger_utils import get_logger
from config import config_values
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

        :endpoint:  http://localhost:5000/v1.0/customer/createuser
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
        :summary: 1. Receives a request to create user with the details present in the request data.
                  2. The PII details like email_id, dob and password are encrypted
                  3. Later a search is made in the `customer` table to check if the email_id is already present.
                  4. If the email_id is already present then we send a response saying the customer already exists.
                  5. If there is no record for the email_id, then a new record is created in the customer table
                     and the success response is sent back.

        :endpoint:  http://localhost:5000/v1.0/customer/createuser
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
            LOG.info("POST request received for authentication of customer email")
            business_logic_obj = CustomerDetailsBusinessLogics()
            response = business_logic_obj.authenticate_user(request_data)
            LOG.info("Response formulated : %s", response)
            return jsonify(response)
        except Exception as ex:
            LOG.exception("Exception occurred in POST call of /authenticate")
            flask_restful.abort(500, message="Internal Server Error")


customer_api.add_resource(CustomerDetails, '/authenticate')