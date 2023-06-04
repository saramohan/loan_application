class LoanApplicationDAO(object):

    def __init__(self, db_conn_obj):
        self.conn = db_conn_obj

    def create_application(self, application_details):
        """
        This method creates a record in the loan_application table for the customer_id
        :param application_details:
        :return: Primary key ID is returned
        """
        query = "insert into loan_application(customer_id, requested_loan_duration, " \
                "requested_loan_amount, application_status, created_datetime) " \
                "values (%s, %s, %s, 'PENDING', now())"
        query_args = (application_details['customer_id'], application_details['requested_loan_duration'],
                      application_details['requested_loan_amount'])
        id_value = self.conn.process_query(query, arguments=query_args, fetch=False, returnprikey=True)
        return id_value

    def get_pending_application(self, customer_id, application_state="PENDING"):
        """
        This method gets all pending application related to a customer_id. If customer_id is
        NULL then it gets all pending applications in the system.
        :param customer_id:
        :param application_state:
        :return: List of Dic containing the application details
        """
        query = "select * from loan_application where application_status = %s"
        query_args = (application_state, )
        if customer_id:
            query = query + " and customer_id = %s"
            query_args = (application_state, customer_id)
        result = self.conn.process_query(query, arguments=query_args, fetch=True)
        return result

    def update_application_status(self, application_data):
        """
        This method updates the status of the application in the loan_application table
        :param application_data: Dict containing all the data
        :return: NA
        """
        query = "update loan_application set application_status = %s where application_id = %s"
        query_args = (application_data['new_application_status'], application_data['application_id'])
        self.conn.process_query(query, arguments=query_args, fetch=False)

    def get_application(self, application_id):
        """
        This method fetches the details for a particular application_id
        :param application_id:
        :return: Dict containing all the application details
        """
        query = "select * from loan_application where application_id = %s"
        query_args = (application_id,)
        result = self.conn.process_query(query, arguments=query_args, fetch=True, count=1)
        return result
