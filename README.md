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
`libvirt_host_enable_efi_support`: Whether to enable EFI support. This defaults 
to false as extra packages need to be installed.

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
