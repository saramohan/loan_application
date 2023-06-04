import flask_restful
from flask import Blueprint, request, jsonify
from lib.logger_utils import get_logger
from lib.db_utils import DBConnectionUtils
from services.loan.LoanCreationLogics import LoanCreationBusinessLogic
from services.loan.LoanRepymentLogics import LoanRepaymentBusinessLogic
from services.loan.LoanDAO import LoanActivityDAO

LOG = get_logger(__name__)

loan_blueprint = Blueprint('loan', __name__, url_prefix='/v1.0/loan')
loan_api = flask_restful.Api(loan_blueprint)


class CreateLoan(flask_restful.Resource):

    def post(self):
        """
        :summary: 1. Receives a request to create an loan for a loan_id.
                  2. The request contains the loan_id along with information required to open a loan.
                  3. The details received are stored in the loan_details table with the loan status as ACTIVE.
                  4. A weekly loan schedule is also generated for the loan and stored in the repayment_calendar table
        :endpoint: POST call to http://localhost:5000/v1.0/loan/create
        :request_data: {'customer_id': 12,
                        'application_id' : 33
                        'loan_amount': 1320,
                        'loan_duration': 7}
        :response : 1. Successful creation of loan
                            {'loan_creation_status': 'success', 'loan_id': 55}
        : Any exception will throw 500 Internal server Error!!
        """
        try:
            request_data = request.get_json()
            LOG.info("POST request received for creation of loan for the application_id : %s",
                     request_data.get('application_id'))
            business_logic_obj = LoanCreationBusinessLogic()
            response = business_logic_obj.create_loan(request_data)
            LOG.info("Response formulated : %s", response)
            return jsonify(response)
        except Exception as ex:
            LOG.exception("Exception occurred in POST call of /create")
            flask_restful.abort(500, message="Internal Server Error")


loan_api.add_resource(CreateLoan, '/create')


class GetLoanDetails(flask_restful.Resource):

    def get(self, customer_id):
        """
        :summary: 1. Receives a request to create get any open loans associated with the customer_id.
                  2. Checks the loan_details table for ACTIVE loans for the customer_id.
                  3. If loan details are present then the same is communicated in the response
                     else only the status is sent.
        :endpoint: GET call to http://localhost:5000/v1.0/loan/1/
        :response : 1. Successful response if customer_id has open loan
                            {'status': 'success',
                            'loan_id': 1,
                            'application_id': 1,
                            'customer_id': 1,
                            'loan_duration': 8,
                            'loan_amount': Decimal('1550.00'),
                            'repayment_frequency': 'weekly',
                            'loan_status': 'ACTIVE',
                            'created_datetime': datetime.datetime(2023, 6, 4, 18, 45, 16)}
        : Any exception will throw 500 Internal server Error!!
        """
        try:
            LOG.info("GET request received for loan_id : %s", customer_id)
            db_conn = DBConnectionUtils()
            loan_dao = LoanActivityDAO(db_conn)
            active_loan_details = loan_dao.get_loan_details(customer_id)
            LOG.info("Active Loan details : %s", active_loan_details)
            response = {'status': 'success'}
            response.update(active_loan_details)
            LOG.info("Response formed : %s", response)
            return jsonify(response)
        except Exception as ex:
            LOG.exception("Exception occurred in GET call of loan/")
            db_conn.revert_db_changes()
            flask_restful.abort(500, message="Internal Server Error")
        finally:
            db_conn.close_db_connection()


loan_api.add_resource(GetLoanDetails, '/<int:customer_id>/')


class LoanRepaymentsDetails(flask_restful.Resource):

    def get(self, loan_id):
        """
        :summary: 1. Receives a request to create get the repayment details for a loan_id
        :endpoint: GET call to http://localhost:5000/v1.0/loan/repaymentdetails/1/
        :response : 1. Successful response with the repayment details
                            {'loan_id': 2,
                            'upcoming_pay_date': datetime.date(2023, 6, 11),
                            'upcoming_due_amount': Decimal('3.33'),
                            'past_due_amount': Decimal('3.2'),
                            'outstanding_principal_balance': Decimal('10.00'),
                            'status': 'success'}
        : Any exception will throw 500 Internal server Error!!
        """
        try:
            LOG.info("GET request received for getting the repayment details associated with a loan_id : %s", loan_id)
            business_logic_obj = LoanRepaymentBusinessLogic()
            response = business_logic_obj.get_repayment_details(loan_id)
            LOG.info("Response formulated for repayment details : %s", response)
            return jsonify(response)
        except Exception as ex:
            LOG.exception("Exception occurred in POST call of /create")
            flask_restful.abort(500, message="Internal Server Error")


loan_api.add_resource(LoanRepaymentsDetails, '/repaymentdetails/<int:loan_id>/')


class LoanRepayments(flask_restful.Resource):

    def post(self):
        """
        :summary: 1. Receives a request to account a repayment amount in the loan schedule calendar.
                  2. The received repaytment amount is accounted properly in the repayment_calendar for the loan
        :endpoint: POST call to http://localhost:5000/v1.0/loan/repayments
        :request_data: {'loan_id': 12,
                        'repay_amount' : '330'}
        :response : 1. Successful accounting
                            {'outstanding_principal_balance': Decimal('190.94'), 'status': 'success'}
        : Any exception will throw 500 Internal server Error!!
        """
        try:
            request_data = request.get_json()
            LOG.info("POST request received for adjusting the repayment amount for loan_id : %s",
                     request_data)
            business_logic_obj = LoanRepaymentBusinessLogic()
            response = business_logic_obj.account_repayment_amount(request_data)
            LOG.info("Response formulated for accounting repayment amount: %s", response)
            return jsonify(response)
        except Exception as ex:
            LOG.exception("Exception occurred in POST call of /repayments")
            flask_restful.abort(500, message="Internal Server Error")


loan_api.add_resource(LoanRepayments, '/repayments')
