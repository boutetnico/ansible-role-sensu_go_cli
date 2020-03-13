ansible-role-sensu-go-cli
=========================

This role installs and configures [Sensuctl](https://docs.sensu.io/sensu-go/latest/sensuctl/reference/).

Requirements
------------

Ansible 2.9 or newer.
Python 3.6 or newer.

Supported Platforms
-------------------

- [Debian - 10 (Buster)](https://wiki.debian.org/DebianBuster)
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
| sensu_cli_assets             | true     | `[]`                              | list      | Assets to install from Bonsai.                |
| sensu_cli_checks             | true     | `[]`                              | list      | Configure checks.                             |

Dependencies
------------

This role relies on modules from [Sensu Go Ansible Collection](https://sensu.github.io/sensu-go-ansible/installation.html). You can install this collection using the following command:

    ansible-galaxy collection install sensu.sensu_go

Example Playbook
----------------

    - hosts: all
      roles:
        - role: ansible-role-sensu-go-cli
          sensu_cli_assets:
            - name: sensu/sensu-slack-handler:1.0.3
              rename: sensu-slack-handler
            - name: sensu-plugins/sensu-plugins-cpu-checks
          sensu_cli_checks:
            - name: check-cpu
              command: check-cpu.rb -w 75 -c 90
              interval: 60
              subscriptions:
                - system
              assets:
                - cpu-checks-plugins
                - sensu-ruby-runtime


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
