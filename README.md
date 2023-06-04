Prerequisites
-------------
  * Python 3.8+ 
  * MySQL server (8.0.17+) [download link](https://dev.mysql.com/downloads/) or from [dockerimage](https://hub.docker.com/_/mysql) 
  * Application setup - please refer the upcoming section.

Application setup steps
------------

After completing the prerequisites setup follow the below steps to start using the application:

1. Download & extract or checkout the project from GitHub.
2. Navigate to the project root (loan_application) folder and install the required python libraries (preferrably from a virtual environment) 
~~~
    cd loan_application
    pip install -r requirements.txt
~~~
3. Create the user "aspireapp" with remote DB access. (Need to modify the credentials stored in config/settings.py if you are creating a user with other credentials)
~~~~
CREATE USER 'aspireapp'@'localhost' IDENTIFIED BY '@$p!repa55w0rD!';
CREATE DATABASE mini_aspire_app;
GRANT ALL ON mini_aspire_app.* TO 'aspireapp'@'localhost';
FLUSH PRIVILEGES;
~~~~
4. Login to the MySQL client and source the database schema file, present in the project root (loan_application/) 
~~~~~
source database_schema.sql
~~~~~
![data_model_image](./resources/data_model.png "Data model")

5. Set the Python path to 'src' directory.
~~~~~
cd src
export PYTHONPATH=$(pwd)
~~~~~
6. Now the Flask API server is lauched using the following comman
~~~~~
cd src
python services/app_routes.py
~~~~~
8. 

Running the application
----------

### Email syncing script ###

Email syncing script (when run without arguments) will download all the emails from your Gmail account to the MySQL database.

~~~~~
cd src/scripts
python email_download_script.py 
~~~~~
Notes:

1. When running the script for the first time, Google asks you to consent to the scopes required via a link.
After you give consent to the scopes from your Google account, a token.json file will be generated under src/config/.
![initial_perm_consent_image](./resources/initial_perm_consent.png "Initial OAuth permission link")

2. Copy the URL into a browser and give consent.
![consent_to_scopes](./resources/consent_to_scopes.png "Consent to read and modify scopes")

3. Running the above script would fetch all the emails from your Gmail account. You could make use of the available arguments to pull a subset of emails to the database.
~~~
usage: email_download_script.py [-h] [-f fetch_mode] [-m max_limit] [-s page_size] [-q querystring] [-l labels [labels ...]]

This script downloads given emails from your Gmail account. Running this script without arguments would fetch all the emails and save it to the MySQL database.

optional arguments:
  -h, --help            show this help message and exit
  -f fetch_mode         Specify the fetch mode. "full" is meant to be used for the first time synchronization or when fetching newer emails;
                        To update / refresh already stored emails, use "minimal"
  -m max_limit          Specify a maximum limit for the number of emails that should be fetched & saved.
  -s page_size          Specify the page size (when paging over a large result)
  -q querystring        Google email search query filter to be applied while fetching emails.
                         Refer https://support.google.com/mail/answer/7190?hl=en.
  -l labels [labels ...]
                        Specify one (or more) labels that should be filtered
~~~

### Rules processing script ###

Rules processing script allows you to run rules based on one or more conditions and may result in one or more actions. The script requires a mandatory argument (i.e., path to the .json rule file).
Please refer the existing rules.json (resources/rules.json) to add / modify new rules on top of an existing setup.
~~~~~
cd src/scripts
python rules_processing_script.py -r <path/to/rules.json> 
~~~~~
Note:
The script runs the rule filters on the local database and applies them to the Gmail account. It then updates the local database once the update on the Gmail account is successful.

Demo screens
----
1. Scenario: From my Gmail account, I am looking to fetch messages from "Orkut" that are older than 2015 into the database.
![search_filter_image](./resources/search_filter.png "Search filter on Gmail")

2. Running the download script with filter condition to only fetch the needed emails for demo into the DB
![download_script](./resources/download_script.png "Download script")

3. Running the count queries to verify. 
![download_queries](./resources/download_queries.png "DB queries to verify counts")

4. A snapshot of the logs corresponding to the download action. Log file is available under the /logs folder which is placed under the project root, (/emailapp). Sample log
![fetch_script_logs](./resources/fetch_script_logs.png "Log messages corresponding to the download script")

5. Configuring rules.json to remove "Apptest1" label, make the messages unread and add "Apptest2" label to the above Orkut messages, but this time using the rules processing script.
![rules_json_file](./resources/rules_json_file.png "Writing a rule to test")

6. A snapshot of the rules processing script and the logs
![running_rules_script](./resources/running_rules_script.png "Rules processing script")

7. Snapshot from my Gmail account after running the rules processor script
![gmail_after_running_rules](./resources/gmail_after_running_rules.png "Gmail snapshot after running rules")

Note to Windows users
------------
Note for Windows users: Except the directory path and the python path setting, the other steps remain the same. Use  ```set pythonpath=<path\to\src>```.

Useful Limits
-------
| Category                                                                    | Limit |
|-----------------------------------------------------------------------------|:-----:|
| Maximum email content size (including encoding)                             | 25 MB |
| Google account's username - max characters allowed                          |  30   |
| Maximum recipients per email                                                |  500  |
| Maximum characters allowed in label names                                   |  225  |
| Maximum labels allowed per user account                                     |  500  |
| Maximum retention period for a trashed message (days)                       |  30   |
| Maximum page size when listing messages (via Gmail API)                     |  500  |
| Maximum GET requests that could be added to a batch request (via Gmail API) | 1000  |
| Maximum message ids per bulk modify (via Gmail API)                         | 1000  |


Improvement areas
--------
1. Unit tests to be added.
2. Parallelism when fetching emails and processing rules.
3. Storing and indexing on to / cc values (separating alias and email ids)
4. Processing the message content (storage and searching). 
5. Support for nested rules (query builder).

Resources
-------
* Using search options in Gmail - [here](https://support.google.com/mail/answer/7190?hl=en)
* How to [batch process Google APIs](https://developers.google.com/gmail/api/guides/batch#format-of-a-batch-request)
* Quickstart Google API code for Python - [here](https://github.com/googleworkspace/python-samples/blob/main/gmail/quickstart/quickstart.py)
* [Gmail API documentation](https://developers.google.com/gmail/api/reference/rest)
