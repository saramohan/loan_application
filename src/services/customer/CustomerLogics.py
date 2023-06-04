import hashlib

from lib.logger_utils import get_logger
from lib.db_utils import DBConnectionUtils
from services.customer.CustomerDAO import CustomerDetailsDAO

LOG = get_logger(__name__)


class CustomerDetailsBusinessLogics(object):

    def __init__(self):
        """
        Constructor for the class Customer
        """
        self.db_conn = DBConnectionUtils()
        self.customer_dao = CustomerDetailsDAO(self.db_conn)

    @staticmethod
    def encrypt(input_text):
        """
        This method is used to hash the customer's pii information.
        :param input_text: string
        :return: string - return encrypted text
        """
        sha = hashlib.sha256()
        sha.update(input_text.encode('utf-8'))
        return sha.hexdigest()

    def create_user(self, request_data):
        """
        This method checks if the request details received for creating a new customer
        are already present in the `customer` table. If the details are not present they are
        inserted into the table. The customer_id is responded back to identify the customer.
        :param request_data:
        :return:
        """
        try:
            customer_details_dict = dict(request_data)
            hashed_pii_dict = {
                'date_of_birth': CustomerDetailsBusinessLogics.encrypt(request_data['date_of_birth']),
                'email_id': CustomerDetailsBusinessLogics.encrypt(request_data['email_id'].lower()),
                'password': CustomerDetailsBusinessLogics.encrypt(request_data['password'])
            }
            customer_details_dict.update(hashed_pii_dict)
            customer_exists = self.customer_dao.check_if_customer_exists(customer_details_dict['email_id'])
            if customer_exists.get('customer_id'):
                LOG.info("Customer already exists in the records!!")
                return {'status': 'success', 'message': 'Customer already exists',
                        'customer_id': customer_exists.get('customer_id')}
            else:
                LOG.info("Creating a record for the customer in the database.")
                customer_id = self.customer_dao.insert_new_customer(customer_details_dict)
                self.db_conn.save_db_changes()
                return {'status': 'success', 'customer_id': customer_id}
        except Exception as ex:
            LOG.exception("An exception had occurred while creating a user : %s", ex)
            self.db_conn.revert_db_changes()
            raise
        finally:
            self.db_conn.close_db_connection()

    def authenticate_user(self, request_dict):
        """
        This method is used to authenticate the customer details email_id and password.
        If the customer email_id is present in the table then check if the password from
        the request matches with password from the table. If the password matches then the
        customer is authenticated. Else the appropriate messaging is sent as response.
        :param request_dict:
        :return: response_dict - dict containing the authentication_status of the request
        """
        try:
            authentication_dict = dict(request_dict)
            hashed_email_id = CustomerDetailsBusinessLogics.encrypt(authentication_dict['email_id'].lower())
            hashed_password = CustomerDetailsBusinessLogics.encrypt(authentication_dict['password'])
            customer_exists = self.customer_dao.check_if_customer_exists(hashed_email_id)
            if customer_exists.get('customer_id') and customer_exists.get('password') == hashed_password:
                LOG.info("The customer with customer_id %s is authenticated", customer_exists.get('customer_id'))
                return {'authentication_status': 'success',
                        'customer_id': customer_exists.get('customer_id')}
            elif customer_exists.get('customer_id') and customer_exists.get('password') != hashed_password:
                LOG.info("The customer with customer_id %s exists but authentication is failed",
                         customer_exists.get('customer_id'))
                return {'authentication_status': 'failure'}
            else:
                LOG.info("The customer does not exists!!")
                return {'authentication_status': 'failure'}
        except Exception as ex:
            LOG.exception("An exception had occurred while authenticating a user : %s", ex)
            self.db_conn.revert_db_changes()
            raise
        finally:
            self.db_conn.close_db_connection()
