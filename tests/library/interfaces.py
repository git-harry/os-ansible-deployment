#!/usr/bin/env python
import collections
import re
import subprocess


class NetworkInterfacesFilesFacts(object):
    def __init__(self, module):
        self.state_change = False
        self.module = module
        self.params = self.module.params

    def gather_facts(self):
        """Get information about RPC release."""
        config = self.run_command(
            ['cat', '/etc/network/interfaces'])
        ifaces = collections.defaultdict(list)
        f = open('/tmp/foobar', 'w')
        for line in config.split('\n'):
            f.write(line)
            line = line.strip()
            if not line or line.startswith('#'):
               continue
            if (line.startswith('auto') or
                   line.startswith('allow-auto') or
                   line.startswith('allow-hotplug')):
               # assume everything is auto
               continue
            if line.startswith('source'):
                # assume no additional files need reading
                continue
            match = re.match(r'^iface\s+(?P<name>\S+)\s+(?P<address_family>\S+)\s+(?P<method>\S+)', line)
            if match:
                ifaces[match.group('name')].append({'address_family': match.group('address_family'),
                                               'method': match.group('method'),
                                               'options': collections.defaultdict(list)})
                current_iface = match.group('name')
                continue
            option, value = line.split(None, 1)
            ifaces[current_iface][-1]['options'][option].append(value)

        self.module.exit_json(
            ansible_facts={'network_interface_files': ifaces})

    def run_command(self, cmd):
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

        except subprocess.CalledProcessError as e:
            message = ('Network interfaces file(s) fact collection failed: "%s".' %
                       e.output.strip())
            self.module.fail_json(msg=message)
        else:
            return output.strip()


def main():
    module = AnsibleModule(
        argument_spec={
        },
        supports_check_mode=False
    )
    iface_facts = NetworkInterfacesFilesFacts(module)
    iface_facts.gather_facts()

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
