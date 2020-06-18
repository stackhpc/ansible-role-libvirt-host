"""Role testing files using testinfra."""


def test_vagrant_machine_is_fully_up(host):
    command = """cat myvm.log | grep -c 'myvm: SSH auth method: private key'"""
    cmd = host.run(command)
    assert '1' in cmd.stdout


def test_vagrant_machine_is_running(host):
    command = r"""vagrant status | egrep -c 'myvm\s*running\s\(libvirt\)'"""
    cmd = host.run(command)
    assert '1' in cmd.stdout


def test_pool_is_started(host):
    command = r""" sudo virsh pool-list --all |
    cut -d " " -f 5 | tail -n +3 | head -n +1 | egrep -c '^active$'"""
    cmd = host.run(command)
    assert '1' in cmd.stdout


def test_pool_is_autostarted(host):
    command = r""" sudo virsh pool-list --all |
    cut -d " " -f 8 | tail -n +3 | head -n +1 | egrep -c '^yes$'"""
    cmd = host.run(command)
    assert '1' in cmd.stdout


def test_net_is_started(host):
    command = r""" sudo virsh net-list --all |
    cut -d " " -f 5 | tail -n +3 | head -n +1 | egrep -c '^active$'"""
    cmd = host.run(command)
    assert '1' in cmd.stdout


def test_net_is_autostarted(host):
    command = r""" sudo virsh net-list --all |
    cut -d " " -f 8 | tail -n +3 | head -n +1 | egrep -c '^yes$'"""
    cmd = host.run(command)
    assert '1' in cmd.stdout
