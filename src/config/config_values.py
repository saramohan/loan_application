MYSQL_DB_CREDENTIALS = dict(user='aspireapp', passwd='@$p!repa55w0rD!',
                            host='127.0.0.1', database='mini_aspire_app')

MYSQL_CONNECTION_RETRIES = 3

CUSTOMER_BASE_URL = 'http://localhost:5000/v1.0/customer'
CUSTOMER_CREATE_URL = CUSTOMER_BASE_URL + '/createuser'
CUSTOMER_AUTH_URL = CUSTOMER_BASE_URL + '/authenticate'

APPLICATION_BASE_URL = 'http://localhost:5000/v1.0/application/'
APPLICATION_PENDING_URL = APPLICATION_BASE_URL + 'pending/'

LOAN_BASE_URL = 'http://localhost:5000/v1.0/loan'
LOAN_CREATE_URL = LOAN_BASE_URL + '/create'
LOAN_REPAYMENTS_URL = LOAN_BASE_URL + '/repayments'
LOAN_REPAYMENTS_DETAILS_URL = LOAN_BASE_URL + '/repaymentdetails/'

DEFAULT_REPAYMENT_FREQUENCY = "weekly"
ACTIVE_LOAN_STATUS = "ACTIVE"
CLOSED_LOAN_STATUS = "CLOSED-OFF"
