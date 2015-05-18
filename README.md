# Foreman SSH

A tool to trigger SSH commands against a host list retrieved via the Foreman API.

Caution: currently loads one API request / host to retrieve the IP address of the host, can be very greedy.

# Usage

Start the binary and give it the path to the Foreman API as argument.

````
$ foreman-api http://foreman.domain/api --user user --password password
````

Send a Foreman query:

````
$ foreman-api http://foreman.domain/api --user user --password password --search "foreman query"
````

# Development 

Ensure you have a Python 2.7 environment running.

Install the dependencies:

````
$ pip install -r requirements.txt
````

Create the binary:

````
pip install --editable .
````

