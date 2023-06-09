class CustomerDetailsDAO(object):

    def __init__(self, db_conn_obj):
        self.conn = db_conn_obj

    def check_if_customer_exists(self, email_id):
        """
        This method reads from the customer table using the hashed email_id value.
        :param email_id:
        :return: Dict containing all the details
        """
        query = "select * from customer where email_id = %s"
        query_args = (email_id,)
        result = self.conn.process_query(query, arguments=query_args, fetch=True, count=1)
        return result

    def insert_new_customer(self, customer_dict):
        """
        This method is used to insert the customer details received into the `customer` table
        :param customer_dict:
        :return: Primary key ID is returned
        """
        query = "insert into customer(first_name, last_name, date_of_birth, email_id, password, created_datetime) " \
                "values (%s, %s, %s, %s, %s, now())"
        query_args = (customer_dict['first_name'], customer_dict['last_name'],
                      customer_dict['date_of_birth'], customer_dict['email_id'],
                      customer_dict['password'])
        id_value = self.conn.process_query(query, arguments=query_args, fetch=False, returnprikey=True)
        return id_value
