from pssh import (ParallelSSHClient,
                  AuthenticationException,
                  UnknownHostException,
                  ConnectionErrorException)
import click
import requests
import logging


@click.command()
@click.argument('foreman-api-url')
@click.argument('command')
@click.option('--foreman-user',
              help="Username used to authenticate against the Foreman API.")
@click.option('--foreman-password',
              help="Password used to authenticate against the Foreman API.")
@click.option('--foreman-search',
              help="Foreman search string.")
@click.option('--ssh-user',
              help="SSH username used to authenticate against hosts.")
@click.option('--ssh-password',
              help="SSH password used to authenticate against hosts.")
@click.option('--ssh-timeout',
              default=5,
              type=int,
              help="Number of seconds to timeout SSH connection attempts.",
              show_default=True)
@click.option('--ssh-parallel-count',
              default=10,
              type=int,
              help="Number of parallel SSH tasks.",
              show_default=True)
@click.option('--ssh-retry',
              default=3,
              type=int,
              help="Number of retries for connection attempts.",
              show_default=True)
@click.option('--dry-run',
              help="Trigger a dry-run. Will print the hosts \
              information without running the command.",
              is_flag=True)
def main(foreman_api_url, command,
         foreman_user, foreman_password, foreman_search,
         ssh_user, ssh_password, ssh_timeout, ssh_parallel_count, ssh_retry,
         dry_run):
    setupLogging()
    foreman_authentication = createForemanAuthentication(
        foreman_user,
        foreman_password)
    hosts = retrieveHostsFromForeman(foreman_api_url,
                                     foreman_authentication,
                                     foreman_search)
    if dry_run:
        displayHostsInfo(hosts)
    else:
        runCommandOnHostList(hosts, command, ssh_timeout,
                             ssh_parallel_count, ssh_retry)


def createForemanAuthentication(foreman_user, foreman_password):
    foreman_authentication = None
    if foreman_user and foreman_password:
        foreman_authentication = (foreman_user, foreman_password)
    return foreman_authentication


def retrieveHostsFromForeman(foreman_api_url,
                             foreman_authentication,
                             foreman_search):
    hosts = []
    parameters = {'search': foreman_search}
    foreman_hosts_endpoint = ''.join([foreman_api_url, '/hosts'])
    r = requests.get(foreman_hosts_endpoint,
                     auth=foreman_authentication,
                     params=parameters)
    response_json = r.json()
    if r.status_code == 200:
        for element in response_json:
            host_id = element["host"]["id"]
            host_information = retrieveHostInformationFromForeman(
                foreman_api_url,
                foreman_authentication,
                host_id)
            hosts.append(host_information["ip"])
    return hosts


def retrieveHostInformationFromForeman(foreman_api_url,
                                       foreman_authentication,
                                       host_id):
    foreman_host_endpoint = ''.join([foreman_api_url,
                                     '/hosts/',
                                     str(host_id)])
    r = requests.get(foreman_host_endpoint,
                     auth=foreman_authentication)
    response_json = r.json()
    if r.status_code == 200:
        host_ip = response_json["host"]["ip"]
        host_information = {'ip': host_ip}
        return host_information


def runCommandOnHostList(hosts, command,
                         ssh_timeout, ssh_parallel_count, ssh_retry):
    client = ParallelSSHClient(hosts,
                               timeout=ssh_timeout,
                               pool_size=ssh_parallel_count,
                               num_retries=ssh_retry)
    try:
        output = client.run_command(command)
        for host in output:
            for line in output[host]['stdout']:
                print(line)
    except (AuthenticationException,
            UnknownHostException,
            ConnectionErrorException):
        print("SSH Exception")


def setupLogging():
    pssh_logger = logging.getLogger('pssh')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    pssh_logger.addHandler(ch)


def displayHostsInfo(hosts):
    print("Targeting %i hosts:" % len(hosts))
    for host in hosts:
        print(host)
