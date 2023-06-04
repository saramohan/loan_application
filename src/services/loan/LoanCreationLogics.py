from datetime import datetime, timedelta
from lib.logger_utils import get_logger
from lib.db_utils import DBConnectionUtils
from config import config_values
from services.loan.LoanDAO import LoanActivityDAO

LOG = get_logger(__name__)


class LoanCreationBusinessLogic(object):

    def __init__(self):
        """
        Constructor for the class LoanCreationBusinessLogic
        """
        self.db_conn = DBConnectionUtils()
        self.loan_dao = LoanActivityDAO(self.db_conn)

    @staticmethod
    def generate_repayment_schedule(current_date, loan_duration, loan_amount):
        """
        This method generates the weekly loan schedule for a loan_id.
        :param current_date: date of application approved
        :param loan_duration: number of cycles for a repayment schedule
        :param loan_amount: amount approved for the application
        :return: List of dicts containing the loan schedule
        """
        due_amount = round(loan_amount / loan_duration, 2)
        loan_schedule = []
        for i in range(1, loan_duration + 1):
            due_date = current_date + timedelta(days=i * 7)
            loan_schedule.append({
                'cycle': i,
                'pay_date': due_date,
                'amount_due': due_amount
            })
        loan_schedule[-1]['amount_due'] += round(loan_amount - (due_amount * loan_duration), 2)
        return loan_schedule

    def create_loan(self, request_data):
        """
        This method creates a loan by making entries in the loan_details and updates the
        repayment schedule in the repayment_calendar table
        :param request_data: dict containing all values necessary for creating a loan
                    - loan_id, customer_id, loan_duration, loan_amount
        :return: response based on the success of loan creation
        """
        try:
            loan_creation_details = dict(request_data)
            loan_creation_details['repayment_frequency'] = config_values.DEFAULT_REPAYMENT_FREQUENCY
            loan_creation_details['loan_status'] = config_values.ACTIVE_LOAN_STATUS
            loan_id = self.loan_dao.insert_loan_details(loan_creation_details)
            repayment_schedule = \
                LoanCreationBusinessLogic.generate_repayment_schedule(datetime.now().date(),
                                                                      loan_creation_details['loan_duration'],
                                                                      loan_creation_details['loan_amount'])
            self.loan_dao.create_loan_repayment_schedule(loan_id, repayment_schedule)
            self.db_conn.save_db_changes()
            return {'loan_creation_status': 'success', 'loan_id': loan_id}
        except Exception as ex:
            LOG.exception("An exception had occurred while creating a loan : %s", ex)
            self.db_conn.revert_db_changes()
            raise
        finally:
            self.db_conn.close_db_connection()
