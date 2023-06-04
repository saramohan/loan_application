class LoanActivityDAO(object):

    def __init__(self, db_conn_obj):
        self.conn = db_conn_obj

    def insert_loan_details(self, loan_details):
        """
        This method creates a record in the loan_details table for the customer_id
        :param loan_details:
        :return: Primary key ID is returned
        """
        query = "insert into loan_details(application_id, customer_id, loan_duration, " \
                "loan_amount, repayment_frequency, loan_status, created_datetime) " \
                "values (%s, %s, %s, %s, %s, %s, now())"
        query_args = (loan_details['application_id'], loan_details['customer_id'],
                      loan_details['loan_duration'], loan_details['loan_amount'],
                      loan_details['repayment_frequency'], loan_details['loan_status'])
        id_value = self.conn.process_query(query, arguments=query_args, fetch=False, returnprikey=True)
        return id_value

    def create_loan_repayment_schedule(self, loan_id, schedule_details):
        """
        This method saves the repayment schedule of the loan in the repayment_calendar table
        :param loan_id:
        :param schedule_details:
        :return: NA
        """
        query = "insert into repayment_calendar(loan_id, cycle, pay_date, " \
                "amount_due, repayment_status, created_datetime) " \
                "values (%s, %s, %s, %s, 'PENDING', now())"
        for schedule_row in schedule_details:
            query_args = (loan_id, schedule_row['cycle'], schedule_row['pay_date'],
                          schedule_row['amount_due'])
            self.conn.process_query(query, arguments=query_args, fetch=False)

    def get_loan_details(self, customer_id):
        """
        This method get the open loan present for a particular customer_id
        :param customer_id:
        :return: Dict containing the open loan details
        """
        query = "select * from loan_details where customer_id = %s and loan_status = 'ACTIVE'"
        query_args = (customer_id,)
        result = self.conn.process_query(query, arguments=query_args, fetch=True, count=1)
        return result

    def get_upcoming_pay_schedule(self, loan_id):
        """
        This method get the upcoming repayment cycles details
        :param loan_id:
        :return: Dict containing the repayment details
        """
        query = "select pay_date, (amount_due-amount_paid) upcoming_due_amount from repayment_calendar " \
                "where loan_id = %s and pay_date > curdate() and repayment_status = 'PENDING' " \
                "and is_record_valid order by cycle limit 1"
        query_args = (loan_id,)
        result = self.conn.process_query(query, arguments=query_args, fetch=True, count=1)
        return result

    def get_pay_cycles_due_amount(self, loan_id):
        """
        This method get the past repayment cycles due amount details
        :param loan_id:
        :return: Dict containing the repayment details
        """
        query = "select sum(amount_due-amount_paid) past_due_amount from repayment_calendar where " \
                "loan_id = %s and pay_date < curdate() and repayment_status = 'PENDING' and is_record_valid"
        query_args = (loan_id,)
        result = self.conn.process_query(query, arguments=query_args, fetch=True, count=1)
        return result

    def get_opb(self, loan_id):
        """
        This method get outstanding principal balance for the given loan_id
        :param loan_id:
        :return: Dict containing the repayment details
        """
        query = "select sum(amount_due-amount_paid) opb from repayment_calendar " \
                "where loan_id = %s and repayment_status = 'PENDING' and is_record_valid"
        query_args = (loan_id,)
        result = self.conn.process_query(query, arguments=query_args, fetch=True, count=1)
        return result

    def get_loan_schedule(self, loan_id):
        """
        This method get loan schedule for a loan_id
        :param loan_id:
        :return: List of Dict containing the repayment schedule
        """
        query = "select * from repayment_calendar where loan_id = %s and repayment_status = 'PENDING' " \
                "and is_record_valid"
        query_args = (loan_id,)
        result = self.conn.process_query(query, arguments=query_args, fetch=True)
        return result

    def update_schedule_row(self, repayment_id, amount_paid, repayment_status):
        """
        This method updates the loan schedule row with the latest details
        :param repayment_id:
        :param amount_paid:
        :param repayment_status:
        :return: NA
        """
        query = "update repayment_calendar set amount_paid = %s, repayment_status = %s where repayment_id = %s"
        query_args = (amount_paid, repayment_status, repayment_id)
        self.conn.process_query(query, arguments=query_args, fetch=False)

    def update_loan_status(self, loan_id, loan_status):
        """
        This method updates the status of the loan
        :param loan_id:
        :param loan_status:
        :return: NA
        """
        query = "update loan_details set loan_status = %s where loan_id = %s"
        query_args = (loan_status, loan_id)
        self.conn.process_query(query, arguments=query_args, fetch=False)

