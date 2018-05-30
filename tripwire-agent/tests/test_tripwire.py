""" tripwire module """

def test_tripwire_is_installed(host):
  """ Check if tripwire is installed """
  tripwire = host.package("tripwire")
  assert tripwire.is_installed

def test_tripwire_is_enabled(host):
  """ Check if tripwire is enabled with the command \'sudo crontab -l\' """
  with host.sudo():
    tripwire_cron = host.run("crontab -l | grep \"tripwire --check\"")
    assert tripwire_cron

def test_tripwire_log(host):
  """ Check tripwire log by running \'tripwire --check\' and checking the journal with \'journalctl -f'\ """
  with host.sudo():
    tripwire_check = host.run("tripwire --check")
    tripwire_log = host.run("journalctl --since \"10 seconds  ago\" | grep \"Integrity Check Complete\"")
    assert tripwire_log.stdout
