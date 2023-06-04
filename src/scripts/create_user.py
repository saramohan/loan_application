import requests
from config import config_values


def create_user(first_name, last_name, date_of_birth, email_id, password):
    """
    This method takes in the customer details and posts to the FLASK API
    /customer/createuser to create a customer record.
    :param first_name:
    :param last_name:
    :param date_of_birth:
    :param email_id:
    :param password:
    :return: NA
    """
    request = {
        'first_name': first_name,
        'last_name': last_name,
        'date_of_birth': date_of_birth,
        'email_id': email_id,
        'password': password
    }
    response = requests.post(config_values.CUSTOMER_CREATE_URL, json=request)
    if response.status_code == 200:
        response_data = response.json()
        if request['first_name'] == "admin":
            print("\n")
            print("----------------------------------------------------------------------------------------------")
            print("Admin user created successfully")
            print("----------------------------------------------------------------------------------------------")
            print("Email ID: ", request['email_id'])
            print("Password: ", request['password'])
            print("Pleas use the ADMIN credentials to access details regarding the admin")
            print("\n")
        else:
            print("\n")
            print("----------------------------------------------------------------------------------------------")
            print("New User created successfully!")
            print("----------------------------------------------------------------------------------------------")
            print("Customer ID:", response_data['customer_id'])
            print("Email ID:", request['email_id'])
            print("Password:", request['password'])
            print("Please use the customer email_id and password created to apply a loan/make repayments etc")
            print("\n")
    else:
        print("Error creating user:", response.text)


if __name__ == "__main__":
    create_user("Hermoine", "Granger", "1979-09-19", "hermoine_granger@example.com", "$@mplep@$$wrd!")
    create_user("Harry", "Potter", "1980-07-31", "harry_potter@example.com", "$@mplep@$$wrd@")
    create_user("admin", "", "1971-01-01", "admin@example.com", "@dminp@$$!")
