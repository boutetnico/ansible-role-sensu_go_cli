ansible-role-sensu-go-cli
=========================

This role installs and configures [Sensuctl](https://docs.sensu.io/sensu-go/latest/sensuctl/reference/).

Requirements
------------

Ansible 2.6 or newer.

Supported Platforms
-------------------

- [Debian - 9 (Stretch)](https://wiki.debian.org/DebianStretch)
- [Debian - 10 (Buster)](https://wiki.debian.org/DebianBuster)
- [Ubuntu - 16.04 (Xenial Xerus)](http://releases.ubuntu.com/16.04/)
- [Ubuntu - 18.04 (Bionic Beaver)](http://releases.ubuntu.com/18.04/)

Role Variables
--------------

| Variable                     | Required | Default                           | Choices   | Comments                                      |
|------------------------------|----------|-----------------------------------|-----------|-----------------------------------------------|
| sensu_cli_dependencies       | true     | `[apt-transport-https,curl,gnupg]`| list      |                                               |
| sensu_cli_package_state      | true     | `present`                         | string    | Use  `latest` to upgrade.                     |
| sensu_cli_backend_url        | true     | `http://127.0.0.1:8080`           | string    | Url to sensu backend API.                     |
| sensu_cli_namespace          | true     | `default`                         | string    |                                               |
| sensu_cli_username           | true     | `admin`                           | string    | Should match username set in sensu backend.   |
| sensu_cli_password           | true     | `P@ssw0rd!`                       | string    | Should match password set in sensu backend.   |
| sensu_cli_format             | true     | `json`                            | string    | One of: tabular, wrapped-json, yaml, json.    |

Dependencies
------------

None

Example Playbook
----------------

    - hosts: all
      roles:
        - role: ansible-role-sensu-go-cli

Testing
-------

## Debian

    molecule --base-config molecule/shared/base.yml test --scenario-name debian-9
    molecule --base-config molecule/shared/base.yml test --scenario-name debian-10

## Ubuntu

    molecule --base-config molecule/shared/base.yml test --scenario-name ubuntu-1604
    molecule --base-config molecule/shared/base.yml test --scenario-name ubuntu-1804

License
-------

MIT

Author Information
------------------

[@boutetnico](https://github.com/boutetnico)
