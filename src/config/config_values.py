# MYSQL_DB_CREDENTIALS = dict(user='aspireapp', passwd='@$p!repa55w0rD!',
#                             host='product.singlebox.net', database='mini_aspire_app')

MYSQL_DB_CREDENTIALS = dict(user='root', passwd='Global!23',
                            host='product.singlebox.net', database='mini_aspire_app')
# 127.0.0.1
MYSQL_CONNECTION_RETRIES = 3

CUSTOMER_BASE_URL = 'http://localhost:5000/v1.0/customer'
CUSTOMER_CREATE_URL = CUSTOMER_BASE_URL + '/createuser'
CUSTOMER_AUTH_URL = CUSTOMER_BASE_URL + '/authenticate'

application_post_url = ''
