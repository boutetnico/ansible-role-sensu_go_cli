import pytest

import os

import json

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('name', [
  ('sensu-go-cli'),
])
def test_packages_are_installed(host, name):
    package = host.package(name)
    assert package.is_installed


@pytest.mark.parametrize('api_url,format,namespace,username', [
  ('http://127.0.0.1:8080', 'json', 'default', 'admin'),
])
def test_sensuctl_is_configured(host, api_url, format, namespace, username):
    json_data = host.check_output('sensuctl config view')
    config = json.loads(json_data)
    assert config['api-url'] == api_url
    assert config['format'] == format
    assert config['namespace'] == namespace
    assert config['username'] == username


@pytest.mark.parametrize('name', [
  ('sensu-plugins/sensu-plugins-cpu-checks'),
  ('sensu-slack-handler'),
])
def test_assets_are_installed(host, name):
    json_data = host.check_output('sensuctl asset list')
    assets = json.loads(json_data)
    for asset in assets:
        if asset['metadata']['name'] == name:
            assert True
            break
    else:
        assert False
