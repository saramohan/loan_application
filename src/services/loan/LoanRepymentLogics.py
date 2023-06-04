from decimal import Decimal
from lib.logger_utils import get_logger
from lib.db_utils import DBConnectionUtils
from config import config_values
from services.loan.LoanDAO import LoanActivityDAO

LOG = get_logger(__name__)


class LoanRepaymentBusinessLogic(object):

    def __init__(self):
        """
        Constructor for the class LoanRepaymentBusinessLogic
        """
        self.db_conn = DBConnectionUtils()
        self.loan_dao = LoanActivityDAO(self.db_conn)

    def get_repayment_details(self, loan_id):
        """
        This method gets the repayment details for the given loan_id
        :param loan_id:
        :return: Dict containing all the repayment details
        """
        try:
            response_dict = {'loan_id': loan_id}
            upcoming_pay_cycle_details = self.loan_dao.get_upcoming_pay_schedule(loan_id)
            response_dict['upcoming_pay_date'] = upcoming_pay_cycle_details.get('pay_date')
            response_dict['upcoming_due_amount'] = upcoming_pay_cycle_details.get('upcoming_due_amount', 0)
            past_due_amount = self.loan_dao.get_pay_cycles_due_amount(loan_id)
            response_dict['past_due_amount'] = past_due_amount.get('past_due_amount', 0)
            response_dict['outstanding_principal_balance'] = self.loan_dao.get_opb(loan_id).get('opb', 0)
            response_dict['status'] = "success"
            return response_dict
        except Exception as ex:
            LOG.exception("An exception had occurred while getting the repayment details : %s", ex)
            raise
        finally:
            self.db_conn.close_db_connection()


    def account_repayment_amount(self, request_data):
        """
        This method accounts the repayment amount received in the request to the payment schedule of the loan_id
        :param request_data:
        :return: Dict containing the status and the current OPB
        """
        try:
            response_dict = {}
            loan_id = request_data['loan_id']
            repayment_amount = Decimal(request_data['repay_amount'])
            loan_schedule_details = self.loan_dao.get_loan_schedule(loan_id)
            remaining_amount = repayment_amount
            for schedule_row in loan_schedule_details:
                if remaining_amount >= (schedule_row['amount_due']-schedule_row['amount_paid']):
                    remaining_amount -= (schedule_row['amount_due']-schedule_row['amount_paid'])
                    amount_paid = schedule_row['amount_due']
                    repayment_status = "COMPLETED"
                    self.loan_dao.update_schedule_row(schedule_row['repayment_id'], amount_paid, repayment_status)
                else:
                    amount_paid = remaining_amount
                    repayment_status = "PENDING"
                    self.loan_dao.update_schedule_row(schedule_row['repayment_id'], amount_paid, repayment_status)
                    break
            self.db_conn.save_db_changes()
            response_dict['outstanding_principal_balance'] = self.loan_dao.get_opb(loan_id).get('opb', 0)
            if response_dict['outstanding_principal_balance'] is None:
                self.loan_dao.update_loan_status(loan_id, config_values.CLOSED_LOAN_STATUS)
            self.db_conn.save_db_changes()
            response_dict['status'] = "success"
            return response_dict
        except Exception as ex:
            LOG.exception("An exception had occurred while accounting the repayment details : %s", ex)
            self.db_conn.revert_db_changes()
            raise
        finally:
            self.db_conn.close_db_connection()
