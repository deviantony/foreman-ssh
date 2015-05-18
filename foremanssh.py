import click
import requests


@click.command()
@click.argument('foreman-api')
@click.option('--user', help="User used to authenticate against Foreman.")
@click.option('--password',
              help="Password used to authenticate against Foreman.")
@click.option('--search', help="Foreman search string")
def main(foreman_api, user, password, search):
    """ Usage: foreman-api http://foreman.domain/api """
    if user and password:
        authentication = (user, password)
    else:
        authentication = None

    parameters = {'search': search}
    foreman_api_host_endpoint = ''.join([foreman_api, '/hosts'])
    r = requests.get(foreman_api_host_endpoint,
                     auth=authentication,
                     params=parameters)
    response_json = r.json()
    if r.status_code == 200:
        for element in response_json:
            host_id = element["host"]["id"]
            process_host(foreman_api_host_endpoint, authentication, host_id)
            break
    else:
        print(response_json)


def process_host(base_url, authentication, host_id):
    print("HostID: %s" % host_id)
    foreman_host_api_url = ''.join([base_url,
                                    '/',
                                    str(host_id)])
    r = requests.get(foreman_host_api_url,
                     auth=authentication)
    response_json = r.json()
    if r.status_code == 200:
        print("IP: %s" % response_json["host"]["ip"])
    else:
        print(response_json)
