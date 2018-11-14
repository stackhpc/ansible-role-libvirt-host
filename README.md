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
- `type` The type of the pool, currently only `dir` is supported.
- `capacity`  The capacity, in bytes, of the pool.
- `path` The absolute path to the pool's backing directory.
- `mode` The access mode of the pool. N.B.: This should be specified as an
  integer **without** a leading zero; for example: `mode: 755`.
- `owner` The owner of the pool.
- `group` The group of the pool.

`libvirt_host_networks` is a list of networks to define and start. Each item
should be a dict containing the following items:
- `name` The name of the network.
- `mode` The forwarding mode of the network, currently only `bridge` is
  supported.
- `bridge` The name of the bridge interface for this network.

`libvirt_host_require_vt`is whether to require that Intel Virtualisation
Technology (VT) is enabled in order to run this role. While this provides
better VM performance, it may not be available in certain environments. The
default value is `true`.

`libvirt_host_qemu_emulators`: List of architectures for which to install QEMU
system emulators, e.g.  `x86`. The default value is `['x86']` if

`libvirt_host_require_vt` is `false`, otherwise the default value is an empty
list.

`libvirt_vm_enable_efi_support`: Whether to enable EFI support. This defaults 
to false as extra packages need to be installed.

`libvirt_host_var_prefix`: This determines The directory under /var/run that libvirt
uses to store state, e.g unix domain sockets, as well as the default name of the 
PID file. Override this if you have a conflict with the default socket e.g it 
could be in use by the nova_libvirt container. Defaults to `""`.

`libvirt_host_socket_dir`: Where the libvirtd socket is created. Defaults to
`/var/run/{{ libvirt_host_var_prefix }}` if `libvirt_host_var_prefix` is set,
otherwise `""`.

`libvirt_host_pid_path`: Path to PID file which prevents mulitple instances of
the daemon from spawning. Defaults to `/var/run/{{ libvirt_host_var_prefix }}.pid` 
if `libvirt_host_var_prefix` is set, otherwise `""`.
`libvirt_host_libvirtd_args`: Command line arguments passed to libvirtd by the
init system when libvirtd is started - quotes will be added

`libvirt_host_uri`: The libvirt connnection URI. Defaults to 
`qemu+unix:///system?socket={{ libvirt_host_socket_dir }}/libvirt-sock` if
`libvirt_host_var_prefix` is set, otherwise `""`. If set to a falsey value,
an explicit connection URI will not be set when calling virsh or any of
the virt_ ansible modules.

Dependencies
------------

None

Example Playbook
----------------

    ---
    - name: Ensure that Libvirt is configured
      hosts: all
      roles:
        - role: stackhpc.libvirt-host
          libvirt_host_pools:
            - name: my-pool
              type: dir
              capacity: 1024
              path: /path/to/pool
              mode: 755
              owner: my-user
              group: my-group
          libvirt_host_networks:
            - name: br-example
              mode: bridge
              bridge: br-example

Author Information
------------------

- Mark Goddard (<mark@stackhpc.com>)
