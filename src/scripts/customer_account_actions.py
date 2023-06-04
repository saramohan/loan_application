import requests
from config import config_values


class ProcessLoanApplication(object):
    def __init__(self):
        self.customer_id = None

    def check_customer_authenticated(self, email_id, password):
        """
        Checks if the customer is present in the system and authenticates the customer.
        This method emulates the login functionality of a web-app.
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
                print("Customer ID is : ", response_data.get('customer_id'))
                self.customer_id = response_data.get('customer_id')
                print("----------------------------------------------------------------------------------------------")
                return True
            else:
                return False
        else:
            return False

    def loan_repayment(self, loan_id):
        repayment_details = requests.get(config_values.LOAN_REPAYMENTS_DETAILS_URL + str(loan_id) + '/')
        if repayment_details.status_code == 200:
            response_data = repayment_details.json()
            if response_data.get('status') == "success":
                print("---------------------------------------------------------")
                print("Loan Repayment Details")
                print("Upcoming Pay Date :: ", response_data.get('upcoming_pay_date'))
                print("Upcoming Due Amount :: ", response_data.get('upcoming_due_amount'))
                print("Past Due Amount :: ", response_data.get('past_due_amount'))
                print("Outstanding Principal Balance :: ", response_data.get('outstanding_principal_balance'))
                repay_amount = input("********* Enter the amount to be repaid ::  ")
                repay_request = {'loan_id': loan_id, 'repay_amount': repay_amount}
                repay_response = requests.post(config_values.LOAN_REPAYMENTS_URL, json=repay_request)
                if repay_response.status_code == 200:
                    response_data = repay_response.json()
                    if response_data.get('status') == "success":
                        print("Repayment Amount has been adjusted to the loan schedule!!")
                        print("Current Outstanding Principal Balance :: ",
                              response_data.get('outstanding_principal_balance'))
                else:
                    print("\n")
                    print("Exception occurred in adjusting the reapyment amount!!")
        else:
            print("\n")
            print("Exception occurred in while loan repayment details!!")

    def customer_has_loans(self):
        open_loan_response = requests.get(config_values.LOAN_BASE_URL + '/' + str(self.customer_id) + '/')
        if open_loan_response.status_code == 200:
            response_data = open_loan_response.json()
            if response_data.get('status') == 'success' and response_data.get('loan_id'):
                print("Customer Has an Open Loan : ", response_data.get('loan_id'))
                print("Loan Details : ")
                print("Loan ID :: ", response_data.get('loan_id'))
                print("Customer ID :: ", response_data.get('customer_id'))
                print("Loan Duration :: ", response_data.get('loan_duration'))
                print("Loan Amount :: ", response_data.get('loan_amount'))
                print("Repayment Frequency :: ", response_data.get('repayment_frequency'))
                print("Loan Status :: ", response_data.get('loan_status'))
                print("Loan created datetime :: ", response_data.get('created_datetime'))
                self.loan_repayment(response_data.get('loan_id'))
                print("----------------------------------------------------------------------------------------------")
                return True
        else:
            print("\n")
            print("Exception occurred in while getting open loan details!!")
        return False

    def customer_has_pending_applications(self):
        """
        This method checks if the customer has a pending application and displays the same.
        It emulates a functionality of the customer's account section!!
        :return: boolean denoting if the customer has a pending application or not
        """
        pending_app_response = requests.get(config_values.APPLICATION_PENDING_URL + str(self.customer_id) + '/')
        if pending_app_response.status_code == 200:
            response_data = pending_app_response.json()
            if response_data.get('status') == 'success' and response_data.get('pending_app_details'):
                print("Pending Application Found for the customer id ", self.customer_id)
                print("The Application Details are as Follows :: ")
                print("Application ID :: ", response_data.get('pending_app_details')[0]['application_id'])
                print("Customer ID :: ", response_data.get('pending_app_details')[0]['customer_id'])
                print("Requested Loan Duration :: ",
                      response_data.get('pending_app_details')[0]['requested_loan_duration'])
                print("Requested Loan Amount :: ",
                      response_data.get('pending_app_details')[0]['requested_loan_amount'])
                print("Application Status :: ", response_data.get('pending_app_details')[0]['application_status'])
                print("Application Created Datetime :: ",
                      response_data.get('pending_app_details')[0]['created_datetime'])
                print("----------------------------------------------------------------------------------------------")
                return True
        else:
            print("\n")
            print("Exception occurred in while getting the pending application details!!")
        return False

    def create_loan_application(self):
        """
        This method is used to create a loan application for a customer-id.
        :return: None
        """
        print("Creating Loan Application for the customer_id : ", self.customer_id)
        loan_duration = input("Enter the Duration of Loan required :  ")
        loan_amount = input("Enter the Loan Amount Required :  ")
        app_request = {
            'customer_id': self.customer_id,
            'requested_loan_amount': loan_amount,
            'requested_loan_duration': loan_duration}
        response = requests.post(config_values.APPLICATION_BASE_URL, json=app_request)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('status') == "success":
                print("\n")
                print("Application is created successfully for the customer!!")
                print("Application ID : ", response_data.get('application_id'))
                print("Current Status of the Application : ", response_data.get('application_status'))
        else:
            print("\n")
            print("Exception occurred in creating the application for the customer!!")
        print("----------------------------------------------------------------------------------------------")


def process_request():
    print("----------------------------------------------------------------------------------------------")
    email_id = input("Enter Email-id to Login :  ")
    password = input("Enter Password to Login :  ")
    process_loan_obj = ProcessLoanApplication()
    if process_loan_obj.check_customer_authenticated(email_id, password):
        if process_loan_obj.customer_has_loans() is False:
            customer_has_pending_application = process_loan_obj.customer_has_pending_applications()
            if customer_has_pending_application is False:
                process_loan_obj.create_loan_application()
    else:
        print("----------------------------------------------------------------------------------------------")
        print("Customer details(email-id or password) provided are not correct!!")
        print("----------------------------------------------------------------------------------------------")


if __name__ == "__main__":
    process_request()
