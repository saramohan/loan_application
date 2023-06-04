import re
import mysql.connector
from lib.logger_utils import get_logger
from config import config_values

LOGGER = get_logger(__name__)


class DBConnectionUtils(object):

    def __init__(self, cursor_type=None):
        """
        Constructor for the class DBConnectionUtils
        :param cursor_type:
        """
        self.connection_id = None
        self.cursor_type = cursor_type
        self.conn = self.get_db_connection()

    def get_db_connection(self):
        """
        This method gets the MySQL database connection object.
        This connection object is further used in all transactions related to the database.
        :return: mysql connection object
        """
        db_credentials = dict(config_values.MYSQL_DB_CREDENTIALS)
        db_credentials.update({'autocommit': False})
        retry = config_values.MYSQL_CONNECTION_RETRIES
        for trial in range(int(retry)):
            try:
                db_conn = mysql.connector.connect(**db_credentials)
                self.connection_id = db_conn.connection_id
                LOGGER.info("Connection id: %s", self.connection_id)
                return db_conn
            except Exception as ex:
                LOGGER.exception(" Exception Occurred in creating Connection. exception no: %s", ex)
                if trial == int(retry) - 1:
                    LOGGER.exception("Database Retry Limit Exceeded!!")
                    raise Exception("Database connection retry exceeded")

    def get_cursor(self):
        """
        This method gets the DB cursor based on the cursor_type.
        :return: cursor object
        """
        if self.conn:
            if self.cursor_type == "TUPLE_CURSOR":
                return self.conn.cursor()
            return self.conn.cursor(dictionary=True)

    def is_connected(self):
        """
        This method checks if the DB connection is still alive
        :return: boolean
        """
        if self.conn.is_connected():
            return True
        else:
            return False

    def close_db_connection(self):
        """
        This method closes the open MySQL connection.
        :return:
        """
        self.conn.close()

    def save_db_changes(self):
        """
        This method commits the database changes.
        :return:
        """
        self.conn.commit()

    def revert_db_changes(self):
        """
        This method roll's back the database changes in case of an exception.
        :return:
        """
        self.conn.rollback()

    def __formatargs(self, query, arguments):
        """
        This method is to format the query and the arguments to be executed.
        :param query:
        :param arguments:
        :return:
        """
        if isinstance(arguments, tuple):
            arguments = list(arguments)
        res_args = []
        if isinstance(arguments, list):
            end_idx = 0
            query = re.sub('\([ ]*%[ ]*s[ ]*\)', '(%s)', query)
            for i, value in enumerate(arguments):
                if isinstance(value, tuple) or isinstance(value, list):
                    len_ = len(value)
                    find_idx = query.index('(%s)', end_idx)
                    end_idx = find_idx + len("(%s)")
                    query = list(query)
                    query[find_idx:end_idx] = '(%s' + ', %s' * (len_ - 1) + ')'
                    query = ''.join(query)
                    for ele in value:
                        res_args.append(ele)
                else:
                    res_args.append(value)
        else:
            pass

        if not res_args:
            res_args = arguments
        return query, res_args

    def process_query(self, query, count=0, arguments=None, fetch=True, returnprikey=0):
        """
        This method execute the given query respective of given argument.
        :param query: query to execute
        :param count: if select query, number of rows to return
        :param arguments: arguments for the query
        :param fetch: select query - True , update/insert query - False
        :param returnprikey: insert query - 1, update query - 0
        :return: result from the database
        """
        query_success = False
        try:
            curs = self.get_cursor()
            if arguments:
                query, arguments = self.__formatargs(query, arguments)
            curs.execute(query, arguments)
            query_success = True
            if fetch:
                result_set = curs.fetchall()
                if count == 1 and len(result_set) >= count:
                    final_result_set = result_set[0]
                elif count == 1 and len(result_set) < count:
                    final_result_set = {}
                elif len(result_set) >= count > 1:
                    final_result_set = result_set[0:count]
                else:
                    final_result_set = result_set
            else:
                if returnprikey:
                    final_result_set = curs.lastrowid
                else:
                    final_result_set = curs.rowcount
            curs.close()
            return final_result_set
        except (mysql.connector.DataError,
                mysql.connector.IntegrityError,
                mysql.connector.NotSupportedError,
                mysql.connector.ProgrammingError) as ex:
            LOGGER.exception("ConnectionID :: " +
                             str(self.connection_id) +
                             " Exception Occurred while executing the query : %s", ex)
            raise Exception('Exception while executing the Query::%s' % ex)
        except (mysql.connector.DatabaseError,
                mysql.connector.InterfaceError,
                mysql.connector.InternalError,
                mysql.connector.OperationalError,
                mysql.connector.PoolError) as ex:
            LOGGER.exception("ConnectionID :: " +
                             str(self.connection_id) +
                             " Exception Occurred in creating Connection : %s", ex)
            raise Exception('DB Connection creation Error::%s' % ex)
        except ValueError as ex:
            LOGGER.exception("ConnectionID :: " +
                             str(self.connection_id) +
                             " Value Error Occurred while executing the query : %s", ex)
            raise Exception('Exception while executing the Query::%s' % ex)
        except Exception as ex:
            LOGGER.exception("ConnectionID :: " +
                             str(self.connection_id) +
                             " Un-handled exception in DB Manager process query")
            raise Exception('Un-handled exception in DB Manager process query::%s' % ex)
