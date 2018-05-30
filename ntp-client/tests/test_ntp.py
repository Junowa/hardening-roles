""" ntp module """

def test_ntp_is_installed(host):
  """ test if ntpd is installed with \'systemctl status ntpd\'"""
  ntp = host.package("ntp")
  assert ntp.is_installed

def test_ntp_running_and_enabled(host):
  """ test if ntpd is running and enabled with \'systemctl status ntpd\'"""
  ntp = host.service("ntpd")
  assert ntp.is_running
  assert ntp.is_enabled

def test_ntp_is_synchronous(host):
  """ test if ntpd is synchronized by running ntpstat command"""
  ntpstat = host.run("ntpstat | head -n 1")
  assert ntpstat.stdout[0:12] == "synchronized"

def test_deny_user_time_changes(host):
  """ test if an unpriviled user can set time by trying to run date, timedatectl and hwclock commands """
  cmd1 = host.run("date --s 15:00:00")
  cmd2 = host.run("timedatectl set-time 15:00:00")
  cmd3 = host.run("hwclock --set --date \"21 Oct 2014 21:17\" --utc")

  assert cmd1.stderr
  assert cmd2.stderr
  assert cmd3.stderr
