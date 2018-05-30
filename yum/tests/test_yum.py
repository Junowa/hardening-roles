""" yum module """

def test_centos_repo(host):
  """ Check the enabled repository with the command \'yum repolist\' """
  repolist = host.run("yum repolist")
  assert 'base' in repolist.stdout
  assert 'updates' in repolist.stdout
  assert 'epel' in repolist.stdout

def test_yum_logging(host):
  """ Install/remove a package \'yum install|remove tmux\' and check the log with '\journalctl -f\' """
  with host.sudo():
    tmux_is_installed = host.run("rpm -qa | grep tmux")

    if tmux_is_installed:
      yum_remove = host.run("yum -y remove tmux")
      yum_remove_log = host.run("journalctl --since \"10 seconds  ago\" | grep \"Erased: tmux\"")
      assert 'tmux' in yum_remove_log.stdout

      yum_install = host.run("yum -y install tmux")
      yum_install_log = host.run("journalctl --since \"10 seconds  ago\" | grep \"Installed: tmux\"")
      assert 'tmux' in yum_install_log.stdout

    else:
      yum_install = host.run("yum -y install tmux")
      yum_install_log = host.run("journalctl --since \"10 seconds  ago\" | grep \"Installed: tmux\"")
      assert 'tmux' in yum_install_log.stdout

      yum_remove = host.run("yum -y remove tmux")
      yum_remove_log = host.run("journalctl --since \"10 seconds  ago\" | grep \"Erased: tmux\"")
      assert 'tmux' in yum_remove_log.stdout
