Role Name
=========

This role is used for generating a conf file based on a generic template.

The template requires the ansible variables be named using a specific format:

prefix__confsection__confvariable: confvariablevalue

For example:

  nova_conf__DEFAULT__verbose: true

__ is the default separator, it is used to split the ansible variable into the
parts for use in the template.

Ansible variables are only allowed to contain [a-zA-Z0-9_]. In most cases that
is sufficient however there a conf files where section names contain other
characters e.g. ':' or '-'. This means there needs to be a way to allow them to
be inserted when required. The role will allow mappings to be specified for the
purpose.

An example of how an option in the swift.conf file would be handled:

  swift_conf__swift__hyphen__hash__swift_hash_path_prefix = "changeme"

The prefix is swift_conf, swift__hyphen__hash is the section in the conf file,
swift_hash_path_prefix is the option name and "chanageme" is the value.

Requirements
------------

N/A.

Role Variables
--------------

A description of the settable variables for this role should go here, including
any variables that are in defaults/main.yml, vars/main.yml, and any variables
that can/should be set via parameters to the role. Any variables that are read
from other roles and/or the global scope (ie. hostvars, group vars, etc.)
should be mentioned here as well.

config_dest - destination path for the configuration file.
config_owner - owner of the configuration file.
config_group - group of the configuration file.
config_mode - optional mode of the configuration file, defaults to 0644.
config_notify - optional handler to call when the configuration file is
                changed.
template_var_prefix - this is the variable prefix used to discover applicable
                      variables.
separator - used to separate the variable name into its constituent parts,
            defaults to '__'.
symbol_mappings - the default list should not need overriding, it is used for
                  inserting ':' or '-' into the section name.
delete_temporary_template - when debugging set this to false to view the
                            generated temporary template.

Dependencies
------------

N/A.

Example Playbook
----------------

    - hosts: nova_compute
      roles:
        - role: "ini-conf"
          config_dest: "/etc/nova/nova.conf"
          config_owner: nova
          config_group: nova
          config_notify: Restart nova services
          template_var_prefix: nova_conf

License
-------

Apache2

Author Information
------------------

N/A.
