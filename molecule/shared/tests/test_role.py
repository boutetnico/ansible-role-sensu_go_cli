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


@pytest.mark.parametrize('api_url,opt_out', [
  ('http://127.0.0.1:8080', 'true'),
])
def test_tessen_is_configured(host, opt_out):
    json_data = host.check_output('sensuctl tessen info')
    config = json.loads(json_data)
    assert config['opt_out'] == opt_out


@pytest.mark.parametrize('name,version', [
  ('sensu-plugins-cpu-checks', '4.1.0'),
  ('sensu-ruby-runtime', '0.0.10'),
  ('sensu/sensu-slack-handler', '1.0.3'),
  ('sensu-plugins/sensu-plugins-http', '6.0.0'),
])
def test_assets_are_installed(host, name, version):
    json_data = host.check_output('sensuctl asset list')
    assets = json.loads(json_data)
    for asset in assets:
        metadata = asset['metadata']
        if metadata['name'] == name:
            annotations = metadata['annotations']
            assert annotations['io.sensu.bonsai.version'] == version
            break
    else:
        assert False


@pytest.mark.parametrize('name', [
  ('filter_interval_60_hourly'),
])
def test_filters_are_installed(host, name):
    json_data = host.check_output('sensuctl filter list')
    checks = json.loads(json_data)
    for check in checks:
        metadata = check['metadata']
        if metadata['name'] == name:
            assert True
            break
    else:
        assert False


@pytest.mark.parametrize('name,type', [
  ('slack', 'pipe'),
  ('tcp_handler', 'tcp'),
  ('keepalive', 'set'),
])
def test_handlers_are_installed(host, name, type):
    json_data = host.check_output('sensuctl handler list')
    handlers = json.loads(json_data)
    for handler in handlers:
        metadata = handler['metadata']
        if metadata['name'] == name:
            assert handler['type'] == type
            break
    else:
        assert False


@pytest.mark.parametrize('name', [
  ('check-cpu-interval'),
  ('check-cpu-cron'),
  ('check-cpu-ad-hoc'),
  ('check-http-proxy'),
])
def test_checks_are_installed(host, name):
    json_data = host.check_output('sensuctl check list')
    checks = json.loads(json_data)
    for check in checks:
        metadata = check['metadata']
        if metadata['name'] == name:
            assert True
            break
    else:
        assert False


@pytest.mark.parametrize('name', [
  ('awesome_username'),
  ('user_with_hashed_password'),
])
def test_users_exist(host, name):
    json_data = host.check_output('sensuctl user list')
    users = json.loads(json_data)
    for user in users:
        if user['username'] == name:
            assert True
            break
    else:
        assert False


@pytest.mark.parametrize('name', [
  ('dev_and_testing'),
  ('org-admins'),
])
def test_role_bindings_exist(host, name):
    json_data = host.check_output('sensuctl role-binding list')
    role_bindings = json.loads(json_data)
    for role_binding in role_bindings:
        metadata = role_binding['metadata']
        if metadata['name'] == name:
            assert True
            break
    else:
        assert False
