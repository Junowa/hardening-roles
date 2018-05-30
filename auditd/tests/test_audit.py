""" auditd module """

def test_host_file_audit(host):
  """ Modify /etc/hosts and test if a log exists by running \'sudo journalctl -f\'"""
  with host.sudo():
    host.run("touch /etc/hosts")
    audit_log = host.run("journalctl -u auditd --since \"10 seconds  ago\" | grep \"/etc/hosts\"")
    assert audit_log.stdout

def test_sudoers_audit(host):
  """ Modify /etc/sudoers and test if a log exists by running \'sudo journalctl -f\'"""
  with host.sudo():
    sudoers_access = host.run("touch /etc/sudoers")
    audit_log = host.run("journalctl -u auditd --since \"10 seconds  ago\" | grep \"/etc/sudoers\"")
    assert audit_log.stdout
