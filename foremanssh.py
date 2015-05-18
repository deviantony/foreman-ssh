import click
import requests
from pssh import ParallelSSHClient


@click.command()
@click.argument('foreman-api')
@click.argument('command')
@click.option('--user', help="User used to authenticate against Foreman.")
@click.option('--password',
              help="Password used to authenticate against Foreman.")
@click.option('--search', help="Foreman search string")
def main(foreman_api, command, user, password, search):
    if user and password:
        authentication = (user, password)
    else:
        authentication = None
    hosts = []
    parameters = {'search': search}
    foreman_api_host_endpoint = ''.join([foreman_api, '/hosts'])
    r = requests.get(foreman_api_host_endpoint,
                     auth=authentication,
                     params=parameters)
    response_json = r.json()
    if r.status_code == 200:
        for element in response_json:
            host_id = element["host"]["id"]
            process_host(foreman_api_host_endpoint,
                         authentication,
                         hosts,
                         host_id)
            break
    else:
        print(response_json)
    if len(hosts) > 0:
        run(hosts, command)
    else:
        print("No hosts")


def process_host(base_url, authentication, hosts, host_id):
    print("HostID: %s" % host_id)
    foreman_host_api_url = ''.join([base_url,
                                    '/',
                                    str(host_id)])
    r = requests.get(foreman_host_api_url,
                     auth=authentication)
    response_json = r.json()
    if r.status_code == 200:
        host_ip = response_json["host"]["ip"]
        print("IP: %s" % host_ip)
        hosts.append(host_ip)
    else:
        print(response_json)


def run(hosts, command):
    client = ParallelSSHClient(hosts)
    output = client.run_command(command)
    for host in output:
        for line in output[host]['stdout']:
            print(line)
