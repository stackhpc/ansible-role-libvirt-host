Libvirt Host
============

This role configures a host as a Libvirt/KVM hypervisor. It can also configure
storage pools and networks on the host.

Requirements
------------

The host should have Virtualization Technology (VT) enabled.

Role Variables
--------------

`libvirt_host_pools` is a list of pools to define and start. Each item
should be a dict containing the following items:
- `name` The name of the pool.
- `type` The type of the pool, currently only `dir`, `logical` and `rbd` are
  supported. `lvm2` is supported as an alias for `logical`, but this alias is
  deprecated and will be removed in a future release.
- `capacity`  The capacity, in bytes, of the pool. (optional)
- `path` The absolute path to the pool's backing directory.
- `mode` The access mode of the pool. N.B.: This should be specified as an
  integer **without** a leading zero; for example: `mode: 755`. (only `dir`)
- `owner` The owner of the pool. (only `dir`)
- `group` The group of the pool. (only `dir`)
- `source` The name of the volume group (when type is `logical`) or RBD pool
  (when type is `rbd`).
- `pvs` A list of physical volumes the volume group consists of. (only when
  type is `logical`)
- `hosts` The list of the Ceph monitors IPs or hostnames. (only `rbd`)
- `username` The username used for RADOS authentification. (only `rbd`)
- `passphrase` The passphrase used for RADOS authentification. (only `rbd`)

`libvirt_host_networks` is a list of networks to define and start. Each item
should be a dict containing the following items:
- `name` The name of the network.
- `mode` The forwarding mode of the network, `bridge`, `route` and `nat` are
  supported.
- `bridge` The name of the bridge interface for this network.
- `zone` the firewalld zone for the bridge (defaults to public)  
- `ip` IP address of the virtual bridge, mandatory for `route` and `nat` mode.
- `netmask` Netmask of the virtual bridge, mandatory for `route` and `nat` mode.
- `domain` DNS domain name for `route` and `nat` mode, default to the network
   name (optional).
- `dhcp_start` First IP of the DHCP range in `route` or `nat` mode (optional).
- `dhcp_end` Last IP of the DHCP range in `route` or `nat` mode (optional).
- `routes` Optional list of additionals routes defined as following:
  - `address` Address of the route, required.
  - `prefix` Prefix of the route, required.
  - `gateway` Gateway of the route, required.
  - `metric` Metric of the route (optional).
- `ipv6` IPv6 address of the virtual bridge (optional).
- `ipv6_prefix` IPv6 prefix of the virtual bridge (optional).
- `routesv6` Optional list of additionals IPv6 routes defined as following:
  - `address` IPv6 address of the route, required.
  - `prefix` IPv6 previx of the route, required.
  - `gateway` gateway of the route, required.
  - `metric` metric of the route (optional).

`libvirt_host_require_vt` is whether to require that Intel Virtualisation
Technology (VT) is enabled in order to run this role. While this provides
better VM performance, it may not be available in certain environments. The
default value is `true`.

`libvirt_host_qemu_emulators`: List of architectures for which to install QEMU
system emulators, e.g.  `x86`. The default value is `['x86']` if

`libvirt_host_require_vt` is `false`, otherwise the default value is an empty
list.

`libvirt_host_enable_efi_support`: Whether to enable EFI support. This defaults 
to false as extra packages need to be installed.

`libvirt_host_var_prefix`: This determines The directory under /var/run that libvirt
uses to store state, e.g unix domain sockets, as well as the default name of the 
PID file. Override this if you have a conflict with the default socket e.g it 
could be in use by the nova_libvirt container. Defaults to `""`.

`libvirt_host_socket_dir`: Where the libvirtd socket is created. Defaults to
`/var/run/{{ libvirt_host_var_prefix }}` if `libvirt_host_var_prefix` is set,
otherwise `""`.

`libvirt_host_pid_path`: Path to PID file which prevents multiple instances of
the daemon from spawning. Defaults to `/var/run/{{ libvirt_host_var_prefix }}.pid` 
if `libvirt_host_var_prefix` is set, otherwise `""`.

`libvirt_host_libvirtd_args`: Command line arguments passed to libvirtd by the
init system when libvirtd is started - quotes will be added

`libvirt_host_uri`: The libvirt connnection URI. Defaults to 
`qemu+unix:///system?socket={{ libvirt_host_socket_dir }}/libvirt-sock` if
`libvirt_host_var_prefix` is set, otherwise `""`. If set to a falsey value,
an explicit connection URI will not be set when calling virsh or any of
the virt_ ansible modules.

`libvirt_host_python3`: Whether the python3 version of the libvirt python
bindings should be installed. If `false`, the python 2 bindings will be
installed.

`libvirt_host_install_daemon`: Whether to install and enable the libvirt
daemon. Default is `true`.

`libvirt_host_install_client`: Whether to install and enable the libvirt
client. Default is `true`.

`libvirt_host_extra_daemon_packages`: List of additional packages to install on
libvirt daemon hosts.

`libvirt_host_extra_client_packages`: List of additional packages to install on
libvirt client hosts.

`libvirt_host_libvirtd_conf_enabled`: Whether to configure `libvirtd.conf`.
Default is `true`.

`libvirt_host_libvirtd_conf`: Configuration for `libvirtd.conf`. Dict mapping
option names to values. Default is an empty dict.

`libvirt_host_qemu_conf_enabled`: Whether to configure `qemu.conf`. Default is
`true`.

`libvirt_host_qemu_conf`: Configuration for `qemu.conf`. Dict mapping option
names to values. Default is an empty dict.

`libvirt_host_enable_sasl_support`: Whether to enable SASL authentication
support. Default is `false`.

`libvirt_host_sasl_conf_enabled`: Whether to configure SASL authentication
(`/etc/sasl2/libvirt.conf`). Default is the same as
`libvirt_host_enable_sasl_support`.

`libvirt_host_sasl_conf`: Configuration for SASL authentication
(`/etc/sasl2/libvirt.conf`). String.

`libvirt_host_sasl_mech_list`: List of enabled libvirt SASL authentication
mechanisms. Default is `["SCRAM-SHA-256"]` when `libvirt_host_tls_listen` is
`true`, otherwise `["DIGEST-MD5"]`.

`libvirt_host_sasl_credentials`: List of SASL authentication credentials to
create.  Each item is a dict containing `username` and `password` items.
Default is a single item list containing `libvirt_host_sasl_authname` and
`libvirt_host_sasl_password`.

`libvirt_host_sasl_authname`: Username for SASL authentication. Default is
`libvirt`.

`libvirt_host_sasl_password`: Password for SASL authentication. Default is
unset.

`libvirt_host_sasl_auth_conf_enabled`: Whether to configure SASL authentication
credentials (`/etc/libvirt/auth.conf`). Default is the same as
`libvirt_host_enable_sasl_support`.

`libvirt_host_sasl_auth_conf`: Configuration for SASL authentication
credentials (`/etc/libvirt/auth.conf`). String.

`libvirt_host_sasl_auth_conf_filename`: Name of file to write SASL
authentication credentials to. Default is `"/etc/libvirt/auth.conf"`.

`libvirt_host_sasl_auth_conf_owner`: Owner of file to write SASL
authentication credentials to. Default is `"root"`.

`libvirt_host_sasl_auth_conf_group`: Group of file to write SASL
authentication credentials to. Default is `"root"`.

`libvirt_host_sasl_auth_conf_mode`: Mode of file to write SASL
authentication credentials to. Default is `"0600"`.

`libvirt_host_tcp_listen`: Whether to enable the systemd TCP socket unit.
Default is `false`.

`libvirt_host_tcp_listen_address`: Systemd TCP socket ListenStream. See man
systemd.socket for format. Default is unset.

`libvirt_host_tls_listen`: Whether to enable the systemd TLS socket unit.
Default is `false`.

`libvirt_host_tls_listen_address`: Systemd TLS socket ListenStream. See man
systemd.socket for format. Default is unset.

`libvirt_host_tls_server_cert`: TLS server certificate. Default is unset.

`libvirt_host_tls_server_key`: TLS server key. Default is unset.

`libvirt_host_tls_client_cert`: TLS client certificate. Default is unset.

`libvirt_host_tls_client_key`: TLS client key. Default is unset.

`libvirt_host_tls_cacert`: TLS CA certificate. Default is unset.

`libvirt_host_configure_apparmor`: Whether to configure AppArmor for directory
storage pools.

Dependencies
------------

* [The LVM role](https://github.com/mrlesmithjr/ansible-manage-lvm) You can install it using `ansible-galaxy install -r requirements.yml --roles-p ../community`

Example Playbook
----------------

    ---
    - name: Ensure that Libvirt is configured
      hosts: all
      roles:
        - role: stackhpc.libvirt-host
          lvm_groups: # see according properties on [The LVM role](https://github.com/mrlesmithjr/ansible-manage-lvm)
            - vgname: libvirtvg
              disks:
                - /dev/sdb1
              create: true
          libvirt_host_pools:
            - name: my-pool
              type: dir
              capacity: 1024
              path: /path/to/pool
              mode: 755
              owner: my-user
              group: my-group
            - name: lvm_pool
              type: lvm2
              source: libvirtvg
            - name: rbd-pool
              type: rbd
              source: rbd
              hosts:
                - 192.168.42.200
                - 192.168.42.204
                - 192.168.42.208
              username: admin
              passphrase: xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

          libvirt_host_networks:
            - name: br-example
              mode: bridge
              bridge: br-example
            - name: brnat-example
              mode: nat
              bridge: brnat-example
              domain: example.local
              ip: 192.168.133.254
              netmask: 255.255.255.0
              dhcp_start: 192.168.133.100
              dhcp_end: 192.168.133.200

Author Information
------------------

- Mark Goddard (<mark@stackhpc.com>)
