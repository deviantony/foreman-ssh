import click
import requests


@click.command()
@click.argument('foreman-api')
@click.option('--search', help="Foreman search string")
def main(foreman_api, search):
    """ Usage: foreman-api http://foreman.wit.prod/api/hosts """
    parameters = {'search': search}
    foreman_api_host_endpoint = ''.join([foreman_api, '/hosts'])
    r = requests.get(foreman_api_host_endpoint,
                     auth=('user', 'password'),
                     params=parameters)
    response_json = r.json()
    print(foreman_api_host_endpoint)
    for element in response_json:
        host_id = element["host"]["id"]
        process_host(foreman_api_host_endpoint, host_id)


def process_host(base_url, host_id):
    print("HostID: %s" % host_id)
    foreman_host_api_url = ''.join([base_url,
                                    '/',
                                    str(host_id)])
    r2 = requests.get(foreman_host_api_url,
                      auth=('user', 'password'))
    r2_json = r2.json()
    print("IP: %s" % r2_json["host"]["ip"])
