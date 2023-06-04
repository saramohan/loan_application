import flask_restful
from flask import Blueprint, request, jsonify
from lib.logger_utils import get_logger
from lib.db_utils import DBConnectionUtils
from services.application.ApplicationDAO import LoanApplicationDAO

LOG = get_logger(__name__)

application_blueprint = Blueprint('application', __name__, url_prefix='/v1.0/application')
application_api = flask_restful.Api(application_blueprint)


class LoanApplication(flask_restful.Resource):

    def post(self):
        """
        :summary: 1. Receives a request to create an application for a customer_id.
                  2. The request contains the customer_id along with information required to open a loan.
                  3. The details received are stored in the loan_application table with the application
                     status as 'PENDING'
                  4. The newly generated application_id is sent in the response for further use.
        :endpoint: POST call to http://localhost:5000/v1.0/application/
        :request_data: {'customer_id': 12,
                        'requested_loan_amount': 1320,
                        'requested_loan_duration': 6}
        :response : 1. Successful creation of application
                            {'status': 'success', 'application_status': 'PENDING', 'application_id': 1421}
        : Any exception will throw 500 Internal server Error!!
        """
        try:
            request_data = request.get_json()
            LOG.info("POST request received for application from customer_id : %s",
                     request_data.get('customer_id'))
            db_conn = DBConnectionUtils()
            application_dao = LoanApplicationDAO(db_conn)
            application_id = application_dao.create_application(request_data)
            response = {'status': 'success', 'application_status': 'PENDING', 'application_id': application_id}
            LOG.info("Response formulated : %s", response)
            db_conn.save_db_changes()
            return jsonify(response)
        except Exception as ex:
            LOG.exception("Exception occurred in POST call of application/")
            db_conn.revert_db_changes()
            flask_restful.abort(500, message="Internal Server Error")
        finally:
            db_conn.close_db_connection()

    def put(self):
        """
        :summary: 1. Receives a request to change the status of the application which is in PENDING.
                  2. The new application status is updated in the loan_application table for that
                     particular application_id.
        :endpoint: PUT call to http://localhost:5000/v1.0/application/
        :request_data: {'customer_id': 12,
                        'application_id': 32,
                        'new_application_status': "APPROVED"}
        :response : 1. Successful Change of application status.
                            {'status': 'success'}
        : Any exception will throw 500 Internal server Error!!
        """
        try:
            request_data = request.get_json()
            LOG.info("PUT request received for application_id : %s", request_data.get('application_id'))
            db_conn = DBConnectionUtils()
            application_dao = LoanApplicationDAO(db_conn)
            application_dao.update_application_status(request_data)
            response = {'status': 'success'}
            LOG.info("Response formulated : %s", response)
            db_conn.save_db_changes()
            return jsonify(response)
        except Exception as ex:
            LOG.exception("Exception occurred in POST call of application/")
            db_conn.revert_db_changes()
            flask_restful.abort(500, message="Internal Server Error")
        finally:
            db_conn.close_db_connection()


application_api.add_resource(LoanApplication, '/')


class PendingLoanApplicationDetails(flask_restful.Resource):

    def get(self, customer_id):
        """
        :summary: 1. Receives a request to get pending application present for a customer_id
                  2. If the customer_id is 0, then applications with status PENDING will be selected. This is
                     used for admin functionality
                  3. The response contains all details regarding to the pending application present.
        :endpoint: GET call to http://localhost:5000/v1.0/application/pending/<int:customer_id>/
        :response : 1. If pending application is present for the customer_id
                            {'status': 'success',
                            'pending_app_details': [{'application_id': 2,
                                                     'customer_id': 2,
                                                     'requested_loan_duration': 6,
                                                     'requested_loan_amount': Decimal('1000.00'),
                                                     'application_status': 'PENDING',
                                                     'created_datetime': datetime.datetime(2023, 6, 4, 13, 44, 23)}]}
                    2. If no pending application is present for the customer_id
                            {'status': 'success', 'pending_app_details': []}
        : Any exception will throw 500 Internal server Error!!
        """
        try:
            LOG.info("GET pending application request received for Customer_id : %s", customer_id)
            db_conn = DBConnectionUtils()
            application_dao = LoanApplicationDAO(db_conn)
            pending_app_details = application_dao.get_pending_application(customer_id)
            LOG.info("Number of pending application for the customer_id %s is %s", customer_id,
                     len(pending_app_details))
            response = {'status': 'success', 'pending_app_details': pending_app_details}
            LOG.info("Response formulated : %s", response)
            return jsonify(response)
        except Exception as ex:
            LOG.exception("Exception occurred in GET call of pending/")
            db_conn.revert_db_changes()
            flask_restful.abort(500, message="Internal Server Error")
        finally:
            db_conn.close_db_connection()


application_api.add_resource(PendingLoanApplicationDetails, '/pending/<int:customer_id>/')
