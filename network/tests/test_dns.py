""" dns module """

from pytest import fixture

def setUp(host):
  with host.sudo():
   host.run("yum -y install bind-utils")

def test_hostname(host):
  """ check machine hostname by running the command: \'hostname\'"""
  hostname = host.run("hostname")
  inventory_hostname= host.ansible.get_variables()['inventory_hostname']
  assert hostname.stdout == inventory_hostname


#def test_dns_hostname_resolution(host):
#  """ check dns short name resolution by running the command: \'nslookup `hostname`\' """
#  short_resolution = host.run("nslookup `hostname` | head -n 1")
#  assert not "SERVFAIL" in short_resolution.stdout

def test_dns_fqdn_resolution(host):
  """ check dns fqdn resolution by running the command: \'nslookup `hostname --fqdn`\' """
  fqdn_resolution = host.run("nslookup `hostname --fqdn` | head -n 1")
  assert not "SERVFAIL" in fqdn_resolution.stdout
