import requests
from config import config_values


def check_authentication(email_id, password):
    """
    Checks if the admin has provided the proper credentials to login.
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
            print("Admin is authenticated!!")
            print("----------------------------------------------------------------------------------------------")
            return True
        else:
            return False
    else:
        return False


def change_application_status(app_details, new_status):
    """
    This method changes the state of the pending application to either APPROVED or DECLINED.
    If the application status is moved to APPROVED then a loan is created.
    :param app_details:
    :param new_status:
    :return:
    """
    request = {'customer_id': app_details['customer_id'],
               'application_id': app_details['application_id'],
               'new_application_status': new_status}
    response = requests.put(config_values.APPLICATION_BASE_URL, json=request)
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get('status') == "success":
            print("Status of the application is changed to : ", new_status)
            if new_status == "APPROVED":
                create_loan_request = {'application_id': app_details.get('application_id'),
                                       'customer_id': app_details.get('customer_id'),
                                       'loan_duration': app_details.get('requested_loan_duration'),
                                       'loan_amount': app_details.get('requested_loan_amount')}
                loan_response = requests.post(config_values.LOAN_CREATE_URL, json=create_loan_request)
                if loan_response.status_code == 200:
                    loan_response_data = loan_response.json()
                    if loan_response_data.get('loan_creation_status') == "success":
                        print("New Loan is Created : ", loan_response_data.get('loan_id'))
                else:
                    print("\n")
                    print("Exception occurred while creating a loan!!")
    else:
        print("\n")
        print("Exception occurred in changing the pending application status!!")


def process_pending_applications():
    """
    This method allows the admin to process all the pending applications.
    :return:
    """
    pending_app_response = requests.get(config_values.APPLICATION_PENDING_URL + str(0) + '/')
    if pending_app_response.status_code == 200:
        response_data = pending_app_response.json()
        if response_data.get('status') == 'success' and response_data.get('pending_app_details'):
            for app_details in response_data.get('pending_app_details'):
                print("The Pending Application Details are as Follows :: ")
                print("Application ID :: ", app_details['application_id'])
                print("Customer ID :: ", app_details['customer_id'])
                print("Requested Loan Duration :: ", app_details['requested_loan_duration'])
                print("Requested Loan Amount :: ", app_details['requested_loan_amount'])
                print("Application Status :: ", app_details['application_status'])
                print("Application Created Datetime :: ", app_details['created_datetime'])
                new_application_status = input("***** Can this Application be APPROVED or DECLINED ::  ")
                change_application_status(app_details, new_application_status)
                print("----------------------------------------------------------------------------------------------")
    else:
        print("\n")
        print("Exception occurred while fetching the pending applications in the system !!")
    print("----------------------------------------------------------------------------------------------")


if __name__ == "__main__":
    print("----------------------------------------------------------------------------------------------")
    email_id = input("Enter Email-id to Login :  ")
    password = input("Enter Password to Login :  ")
    if check_authentication(email_id, password):
        process_pending_applications()
    else:
        print("----------------------------------------------------------------------------------------------")
        print("Admin details(email-id or password) provided are not correct!!")
        print("----------------------------------------------------------------------------------------------")
