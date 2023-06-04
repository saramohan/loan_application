import requests
from config import config_values


class ProcessLoanApplication(object):
    def __init__(self):
        self.customer_id = None

    def check_customer_authenticated(self, email_id, password):
        """
        Checks if the customer is present in the system
        :param email_id:
        :param password:
        :return: boolean
        """
        authentication_request = {
            'email_id': email_id,
            'password': password
        }
        response = requests.post(config_values.CUSTOMER_AUTH_URL, json=authentication_request)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('authentication_status') == "success":
                print("----------------------------------------------------------------------------------------------")
                print("Customer is authenticated!!")
                print("Customer ID is : %s", response_data.get('customer_id'))
                self.customer_id = response_data.get('customer_id')
                print("----------------------------------------------------------------------------------------------")
                return True
            else:
                return False
        else:
            return False


def process_request():
    email_id = input("Enter Email-id to Login :  ")
    password = input("Enter Password to Login :  ")
    process_loan_obj = ProcessLoanApplication()
    if process_loan_obj.check_customer_authenticated(email_id, password):
        pass
    else:
        print("----------------------------------------------------------------------------------------------")
        print("Customer details(email-id or password) provided are not correct!!")
        print("----------------------------------------------------------------------------------------------")


if __name__ == "__main__":
    process_request()
