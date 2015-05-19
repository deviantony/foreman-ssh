# Foreman SSH

A tool to trigger SSH commands against a host list retrieved via the Foreman API (it will force the use of the API version 2).

# Usage

Use the binary to request a list of host against the Foreman API and run a command against them. By default, it will retrieve the 50 first hosts sorted by alphabetical order.

The following will execute the command "ls /tmp" against the 50 first hosts sorted by alphabetical order:

````
$ foreman-ssh http://foreman.domain/api "ls /tmp" --foreman-user user --foreman-password password
````

## Dry-run

You can specify the `--dry-run` flag to specify that you do not want to execute the command on the host list. Instead it will print the list of targeted hosts, use this if you want to be sure of the host list.

````
$ foreman-ssh http://foreman.domain/api "ls /tmp" --foreman-user user --foreman-password password --dry-run
````

## Foreman related options

You can specify a search query (using the syntax you would use in the Foreman UI):

````
$ foreman-ssh http://foreman.domain/api "ls /tmp" --foreman-user user --foreman-password password --foreman-search "hostgroup_fullname  = myHostGroup"
````

## SSH related options

By default, SSH will use the user who started the binary to run distant commands.

### Authentication

You can specify another user/password for the SSH authentication:

````
$ foreman-ssh http://foreman.domain/api "ls /tmp" --foreman-user user --foreman-password password --foreman-search "hostgroup_fullname  = myHostGroup" --ssh-user myUser --ssh-password myPassword
````

### Connection retries

In case of connection error, the binary will retry to connect to the host up to three 3 times. Use the `--ssh-retry` option to change that value:

````
$ foreman-ssh http://foreman.domain/api "ls /tmp" --foreman-user user --foreman-password password --foreman-search "hostgroup_fullname  = myHostGroup" --ssh-user myUser --ssh-password myPassword --ssh-retry 1
````

### Timeout

Any SSH connection will timeout after 5 secs, you can change this value using the `--ssh-timeout` option:

````
$ foreman-ssh http://foreman.domain/api "ls /tmp" --foreman-user user --foreman-password password --foreman-search "hostgroup_fullname  = myHostGroup" --ssh-user myUser --ssh-password myPassword --ssh-retry 1 --ssh-timeout 10
````

### Command parallelization

The SSH client will run command in parallel using a pool of 10 hosts by default. You can update this value using the `--ssh-parallel-count` option:

````
$ foreman-ssh http://foreman.domain/api "ls /tmp" --foreman-user user --foreman-password password --foreman-search "hostgroup_fullname  = myHostGroup" --ssh-user myUser --ssh-password myPassword --ssh-retry 1 --ssh-timeout 10 --ssh-parallel-count 50
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

# Limitations

This tool has been tested on the following OSes:

* Ubuntu 12.04
* Ubuntu 14.04

It supports the following Python versions:

* 2.7

