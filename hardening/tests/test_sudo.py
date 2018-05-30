import time

""" hardening sudo module """

def test_log_sudo_actions (host):
  """ run the privileged command \'sudo hostname'\ and test if a log exists with \'sudo journalctl -f\' """
  with host.sudo():
    action = host.run("hostname")
    time.sleep(3)
    action_log = host.run("journalctl --since \"1 minute ago\" -t sudo | grep /bin/hostname")
    assert action_log.stdout

def test_log_auth_failure (host):
  """ run the privileged command \'sudo hostname'\ with a wrong password and test if a failure log exists with \'sudo journalctl -f\' """
  auth = host.run("echo \"wrong_password\" | sudo -S hostname")
  with host.sudo():
    time.sleep(3)
    authfailure_log = host.run("journalctl --since \"10 seconds ago\" | grep \"incorrect password attempt\"")
  assert authfailure_log.stdout
