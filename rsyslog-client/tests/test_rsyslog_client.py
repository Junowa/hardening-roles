""" rsyslog module """

import random, string

config_syslog_rotate = '/var/log/messages\n/var/log/secure\n{\n    rotate 5\n    hourly\n    size 100M\n    compress\n}'


def test_rsyslog_local_logging(host):
  """ Log a random string with the command \'logger'\. Check the string log with \'journalctl -f'\ """
  payload = ''.join(random.choice(string.lowercase) for i in range(50))
  command = "logger " +payload
  host.run(command)
  command2 = "journalctl | grep " +payload
  with host.sudo():
    result = host.run(command2)

  assert payload in result.stdout 

def test_rsyslog_remote_logging(host):
  """ Check if a remote rsyslogd connection is established with the command \'netstat -tunap | grep rsyslogd\' """

  remote_syslog_server_hostname = host.ansible.get_variables()['tls_log_server_hostname']
  remote_syslog_server_port = host.ansible.get_variables()['tls_log_server_tcpport']

  hostname_and_port = str(remote_syslog_server_hostname)
  hostname_and_port += ":"
  hostname_and_port += str(remote_syslog_server_port)


  with host.sudo():
    rsyslog_remote_connection = host.run("netstat -tunap | grep rsyslogd | grep ESTABLISHED")

  assert hostname_and_port in rsyslog_remote_connection.stdout

def test_rsyslog_default_filtering(host):
  """ Check if syslog filtering is available in /etc/rsyslog.conf """
  assert host.file("/etc/rsyslog.conf").contains("^\*.info;mail.none;authpriv.none;cron.none                /var/log/messages")
  assert host.file("/etc/rsyslog.conf").contains("^authpriv.info                                           /var/log/secure")

def test_logrotate_config(host):
  """ Check the logrotate configuration in /etc/logrotate.d/syslog """
  syslog_rotate = host.file("/etc/logrotate.d/syslog").content_string
  assert config_syslog_rotate in syslog_rotate
