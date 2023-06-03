"""Role testing files using testinfra."""


def test_vagrant_machine_is_running(host):
    command = r"""vagrant status | grep -Ec 'myvm\s*running\s\(libvirt\)'"""
    cmd = host.run(command)
    assert '1' in cmd.stdout


def test_pool_is_started(host):
    command = r"""virsh pool-list --all |
    cut -d " " -f 5 | tail -n +3 | head -n +1 | grep -Ec '^active$'"""
    with host.sudo():
        cmd = host.run(command)
        assert '1' in cmd.stdout


def test_pool_is_autostarted(host):
    command = r"""virsh pool-list --all |
    cut -d " " -f 8 | tail -n +3 | head -n +1 | grep -Ec '^yes$'"""
    with host.sudo():
        cmd = host.run(command)
        assert '1' in cmd.stdout


def test_net_is_started(host):
    command = r""" virsh net-list --all |
    cut -d " " -f 5 | tail -n +3 | head -n +1 | egrep -c '^active$'"""
    with host.sudo():
        cmd = host.run(command)
        assert '1' in cmd.stdout


def test_net_is_autostarted(host):
    command = r"""virsh net-list --all |
    cut -d " " -f 8 | tail -n +3 | head -n +1 | egrep -c '^yes$'"""
    with host.sudo():
        cmd = host.run(command)
        assert '1' in cmd.stdout
