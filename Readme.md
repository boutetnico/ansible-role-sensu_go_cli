[![tests](https://github.com/boutetnico/ansible-role-sensu-go-cli/workflows/Test%20ansible%20role/badge.svg)](https://github.com/boutetnico/ansible-role-sensu-go-cli/actions?query=workflow%3A%22Test+ansible+role%22)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-boutetnico.sensu_go_cli-blue.svg)](https://galaxy.ansible.com/boutetnico/sensu_go_cli)

ansible-role-sensu-go-cli
=========================

This role installs and configures [Sensuctl](https://docs.sensu.io/sensu-go/latest/sensuctl/reference/).

It is part of a family of Ansible roles allowing to setup and configure Sensu Go components:

- [ansible-role-sensu-go-agent](https://github.com/boutetnico/ansible-role-sensu-go-agent)
- [ansible-role-sensu-go-cli](https://github.com/boutetnico/ansible-role-sensu-go-cli)
- [ansible-role-sensu-go-backend](https://github.com/boutetnico/ansible-role-sensu-go-backend)

Requirements
------------

Ansible 2.10 or newer.
Python 3.6 or newer.

Supported Platforms
-------------------

- [Debian - 11 (Bullseye)](https://wiki.debian.org/DebianBullseye)
- [Ubuntu - 22.04 (Jammy Jellyfish)](http://releases.ubuntu.com/22.04/)

Role Variables
--------------

| Variable                  | Req. | Default                       | Type   | Comments                                    |
|---------------------------|------|-------------------------------|--------|---------------------------------------------|
| sensu_cli_dependencies    | true | `[apt-transport-https,gnupg]` | list   |                                             |
| sensu_cli_package_state   | true | `present`                     | string | Use  `latest` to upgrade.                   |
| sensu_cli_backend_url     | true | `http://127.0.0.1:8080`       | string | Url to sensu backend API.                   |
| sensu_cli_namespace       | true | `default`                     | string |                                             |
| sensu_cli_username        | true | `admin`                       | string | Should match username set in sensu backend. |
| sensu_cli_password        | true | `P@ssw0rd!`                   | string | Should match password set in sensu backend. |
| sensu_cli_tessen_state    | true | `disabled`                    | string | `enabled` or `disabled`.                    |
| sensu_cli_format          | true | `json`                        | string | One of: tabular, wrapped-json, yaml, json.  |
| sensu_cli_assets          | true | `[]`                          | list   | Assets to install from Bonsai.              |
| sensu_cli_filters         | true | `[]`                          | list   | Configure filters.                          |
| sensu_cli_pipe_handlers   | true | `[]`                          | list   | Configure pipe handlers.                    |
| sensu_cli_socket_handlers | true | `[]`                          | list   | Configure socket handlers.                  |
| sensu_cli_handler_sets    | true | `[]`                          | list   | Configure handler sets.                     |
| sensu_cli_checks          | true | `[]`                          | list   | Configure checks.                           |
| sensu_cli_users           | true | `[]`                          | list   | Configure users.                            |
| sensu_cli_role_bindings   | true | `[]`                          | list   | Configure role bindings.                    |

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
            - name: sensu/sensu-slack-handler
              version: 1.0.3
            - name: sensu-plugins/sensu-plugins-cpu-checks
              rename: sensu-plugins-cpu-checks
              version: 4.1.0
            - name: sensu/sensu-ruby-runtime
              rename: sensu-ruby-runtime
              version: 0.0.10
            - name: sensu-plugins/sensu-plugins-http
              version: 6.0.0

          sensu_cli_filters:
            - name: filter_interval_60_hourly
              action: allow
              expressions:
                - event.check.interval == 60
                - event.check.occurrences == 1 || event.check.occurrences % 60 == 0

          sensu_cli_pipe_handlers:
            - name: slack
              env_vars:
                SLACK_WEBHOOK_URL: https://hooks.slack.com/services/T0000/B000/XXXXXXXX
              command: sensu-slack-handler --channel '#monitoring'
              runtime_assets:
                - sensu-slack-handler

          sensu_cli_socket_handlers:
            - name: tcp_handler
              type: tcp
              host: 10.0.1.99
              port: 4444

          sensu_cli_handler_sets:
            - name: keepalive
              handlers:
                - slack

          sensu_cli_checks:
            - name: check-cpu-interval
              command: check-cpu.rb -w 75 -c 90
              interval: 60
              subscriptions:
                - system
              runtime_assets:
                - cpu-checks-plugins
                - sensu-ruby-runtime
            - name: check-cpu-cron
              command: check-cpu.rb -w 75 -c 90
              cron: '* * * * *'
              subscriptions:
                - system
              runtime_assets:
                - cpu-checks-plugins
                - sensu-ruby-runtime
            - name: check-cpu-ad-hoc
              command: check-cpu.rb -w 75 -c 90
              interval: 60
              publish: false
              subscriptions:
                - system
              runtime_assets:
                - cpu-checks-plugins
                - sensu-ruby-runtime
            - name: check-http-proxy
              command: http_check.sh https://sensu.io
              interval: 60
              proxy_entity_name: sensu-site
              round_robin: true
              subscriptions:
                - system
              runtime_assets:
                - sensu-plugins-http
                - sensu-ruby-runtime

          sensu_cli_users:
            - name: awesome_username
              password: hidden_password?
              groups:
                - dev
                - prod
            - name: user_with_hashed_password
              password_hash: $5f$14$.brXRviMZpbaleSq9kjoUuwm67V/s4IziOLGHjEqxJbzPsreQAyNm
              groups:
                - dev
                - prod

          sensu_cli_role_bindings:
            - name: dev_and_testing
              role: testers_permissive
              groups:
                - testers
                - dev
                - ops
              users:
                - alice
            - name: org-admins
              cluster_role: admin
              groups:
                - team1-admins
                - team2-admins

Testing
-------

## Debian

    molecule --base-config molecule/shared/base.yml test --scenario-name debian-11

## Ubuntu

    molecule --base-config molecule/shared/base.yml test --scenario-name ubuntu-2204

License
-------

MIT

Author Information
------------------

[@boutetnico](https://github.com/boutetnico)
