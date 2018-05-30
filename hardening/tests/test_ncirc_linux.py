""" hardening ncirc module """
import pytest
from pytest import fixture


# increase shadow and gshadow chmod from 0644 to 0000 
def test_perm_passwd_security (host):
  with host.sudo():
    assert host.file("/etc/passwd").user in 'root'
    assert host.file("/etc/group").user in 'root'
    assert host.file("/etc/shadow").user in 'root'
    assert host.file("/etc/gshadow").user in 'root'
    assert oct(host.file("/etc/passwd").mode) == '0644'
    assert oct(host.file("/etc/group").mode) == '0644'
    assert oct(host.file("/etc/shadow").mode) == '0'
    assert oct(host.file("/etc/gshadow").mode) == '0'

def test_perm_set_umask (host):
    assert host.file("/etc/sysconfig/init").contains("^umask 027")

def test_exec_shield (host):
    # kernel-exec-shield is enabled by default in RHEL7 (no more sysctl vars)
    assert host.file("/etc/sysctl.conf").contains("^kernel.randomize_va_space=2")

def test_core_dumps (host):
    assert host.file("/etc/sysctl.conf").contains("^fs.suid_dumpable=0")
    assert host.file("/etc/security/limits.conf").contains("^*\s*hard\s*core\s*0$")

def test_restrict_root_login (host):
  assert host.file("/etc/securetty").size == 0

def test_restrict_su (host):
  with host.sudo():
    assert host.file("/etc/pam.d/su").contains("^auth           required        pam_wheel.so use_uid")

def test_user_umask (host):
    assert host.file("/etc/login.defs").contains( "^UMASK\s*077$")

def test_password_quality (host):
  pwquality_config="password    requisite     pam_pwquality.so local_users_only enforce_for_root retry=3"
  assert host.file("/etc/pam.d/password-auth").contains(pwquality_config)
  assert host.file("/etc/pam.d/system-auth").contains(pwquality_config)
  assert host.file("/etc/security/pwquality.conf").contains('^difok = 5$')
  assert host.file("/etc/security/pwquality.conf").contains('^minlen = 14$')
  assert host.file("/etc/security/pwquality.conf").contains('^dcredit = 1$')
  assert host.file("/etc/security/pwquality.conf").contains('^ucredit = 1$')
  assert host.file("/etc/security/pwquality.conf").contains('^lcredit = 1$')
  assert host.file("/etc/security/pwquality.conf").contains('^ocredit = 1$')
  assert host.file("/etc/security/pwquality.conf").contains('^minclass = 4$')

def test_password_history (host):
  shadow_config="password    required      pam_pwhistory.so enforce_for_root remember=10 use_authok"
  assert host.file("/etc/pam.d/password-auth").contains(shadow_config)
  assert host.file("/etc/pam.d/system-auth").contains(shadow_config)

def test_password_min_age (host):
  assert host.file("/etc/login.defs").contains("^PASS_MIN_DAYS\s7")

def test_password_max_age (host):
  assert host.file("/etc/login.defs").contains("^PASS_MAX_DAYS\s90")

def test_password_change_warning (host):
  assert host.file("/etc/login.defs").contains("^PASS_WARN_AGE\s7")

def test_disable_usb_storage (host):
  # No more modprobe.conf in RHEL7
  file_exist = host.file("/etc/modprobe.d/disable-usb-storage.conf").exists
  if (file_exist):
    assert file_exist.contains("^install usb-storage /bin/true$")
  else:
    assert file_exist

def test_grub_password (host):
  with host.sudo():
    assert host.file("/boot/grub2/user.cfg").contains("grub.pbkdf2.sha512")

def test_disable_interactive_boot (host):
    assert host.file("/etc/sysconfig/init").contains("^PROMPT=no")

@pytest.mark.skip(reason="No GUI installed")
def test_gui_screen_locking():
  pass

def test_shell_inactivity (host):
  tmount1 = host.file("/etc/profile.d/tmount.sh").contains("^TMOUT=600$")
  tmount2 = host.file("/etc/profile.d/tmount.sh").contains("^readonly TMOUT$")
  tmount3 = host.file("/etc/profile.d/tmount.sh").contains("^export TMOUT$")
  assert (tmount1 and tmount2 and tmount3)

def test_etc_issue (host):
  banner = "DIFFUSION RESTREINTE" 
  assert host.file("/etc/issue").contains(banner)
  assert host.file("/etc/issue.net").contains(banner)

@pytest.mark.skip(reason="No GUI installed")
def test_gui_banner():
  pass

def test_enable_selinux (host):
  selinux1 = host.file("/etc/selinux/config").contains("^SELINUX=enforcing$")
  selinux2 = host.file("/etc/selinux/config").contains("^SELINUXTYPE=targeted$")
  assert (selinux1 and selinux2)

def test_network_disable_ip_forwarding (host):
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.ip_forward=0$")

def test_network_send_redirects (host):
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.conf.all.send_redirects=0$")
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.conf.default.send_redirects=0$")

def test_network_disable_source_routing (host):
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.conf.all.accept_source_route=0$")
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.conf.default.accept_source_route=0$")

def test_network_accept_redirects (host):
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.conf.all.accept_redirects=0$")
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.conf.default.accept_redirects=0$")
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.conf.all.secure_redirects=0$")
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.conf.default.secure_redirects=0$")

def test_network_log_martians (host):
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.conf.all.log_martians=1$")
  
def test_network_ignore_broadcasts (host):
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.icmp_echo_ignore_broadcasts=1$")

def test_network_ignore_bogus_error_messages (host):
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.icmp_ignore_bogus_error_responses=1$")

def test_network_tcp_syncookies (host):
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.tcp_syncookies=1$")

def test_network_rp_filter (host):
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.conf.all.rp_filter=1$")
  assert host.file("/etc/sysctl.conf").contains("^net.ipv4.conf.default.rp_filter=1$")

def test_disable_wireless (host):
  wireless_drivers=host.run("ls -l /lib/modules/`uname -r`/kernel/drivers/net/wireless")
  assert wireless_drivers.rc == 0

def test_iptables_policy (host):
  firewalld = host.service("firewalld")
  assert firewalld.is_running
  assert firewalld.is_enabled

@pytest.mark.skip(reason="No more ipv6 module in RHEL7")
def test_disable_ipv6 (host):
  # No more modprobe.conf in RHEL7
  pass

def test_enable_auditing (host):
  auditd = host.service("auditd")
  assert auditd.is_running
  assert auditd.is_enabled

def test_disable_avahi (host):
  avahi_daemon = host.service("avahi_daemon")
  assert not avahi_daemon.is_enabled

def test_disable_apmd (host):
  apmd = host.service("apmd")
  assert not apmd.is_enabled

def test_disable_nfs (host):
  nfs = host.service("nfs")
  assert not nfs.is_enabled

def test_disable_nfslock (host):
  nfslock = host.service("nfslock")
  assert not nfslock.is_enabled

def test_disable_rpcgssd (host):
  rpcgssd = host.service("rpcgssd")
  assert not rpcgssd.is_enabled

def test_disable_rpcimapd (host):
  rpcimapd = host.service("rpcimapd")
  assert not rpcimapd.is_enabled

def test_disable_netfs (host):
  netfs = host.service("netfs")
  assert not netfs.is_enabled

def test_disable_portmap (host):
  portmap = host.service("portmap")
  assert not portmap.is_enabled

def test_disable_cups (host):
  cups = host.service("cups")
  assert not cups.is_enabled

def test_disable_firstboot (host):
  firstboot = host.service("firstboot")
  assert not firstboot.is_enabled

def test_disable_gpm (host):
  gpm = host.service("gpm")
  assert not gpm.is_enabled

def test_disable_haldaemon (host):
  haldaemon = host.service("haldaemon")
  assert not haldaemon.is_enabled

def test_disable_hidd (host):
  hidd = host.service("hidd")
  assert not hidd.is_enabled

def test_disable_isdn (host):
  isdn = host.service("isdn")
  assert not isdn.is_enabled

def test_disable_kdump (host):
  kdump = host.service("kdump")
  assert not kdump.is_enabled

def test_disable_kudzu (host):
  kudzu = host.service("kudzu")
  assert not kudzu.is_enabled

def test_disable_mcstrans (host):
  mcstrans = host.service("mcstrans")
  assert not mcstrans.is_enabled

def test_disable_mdmonitor (host):
  mdmonitor = host.service("mdmonitor")
  assert not mdmonitor.is_enabled

def test_disable_pcscd (host):
  pcscd = host.service("pcscd")
  assert not pcscd.is_enabled

def test_disable_readahead_early (host):
  readahead_early = host.service("readahead_early")
  assert not readahead_early.is_enabled

def test_disable_readahead_later (host):
  readahead_later = host.service("readahead_later")
  assert not readahead_later.is_enabled

def test_disable_rhnsd (host):
  rhnsd = host.service("rhnsd")
  assert not rhnsd.is_enabled

def test_disable_sendmail (host):
  sendmail = host.service("sendmail")
  assert not sendmail.is_enabled

def test_disable_yum_updatesd (host):
  yum_updatesd= host.service("yum-updatesd")
  assert not yum_updatesd.is_enabled

def test_disable_xfs (host):
  xfs = host.service("xfs")
  assert not xfs.is_enabled

def test_ssh_client_hardening (host):
  with host.sudo():
    assert host.file("/etc/ssh/ssh_config").contains("^        Protocol 2$")

def test_sshd_port_22 (host):
  with host.sudo():
    assert host.file("/etc/ssh/sshd_config").contains("^Port 22$")

def test_sshd_protocol_2 (host):
  with host.sudo():
    assert host.file("/etc/ssh/sshd_config").contains("^Protocol 2$")

def test_sshd_loglevel_verbose (host):
  with host.sudo():
    assert host.file("/etc/ssh/sshd_config").contains("^LogLevel VERBOSE$")

def test_sshd_deny_root_logins (host):
  with host.sudo():
    assert host.file("/etc/ssh/sshd_config").contains("^PermitRootLogin no$")

def test_sshd_disable_rsa (host):
  with host.sudo():
    assert host.file("/etc/ssh/sshd_config").contains("^RhostsRSAAuthentication no$")

def test_sshd_disable_hostbased (host):
  with host.sudo():
    assert host.file("/etc/ssh/sshd_config").contains("^HostbasedAuthentication no$")

def test_sshd_ignore_rhosts (host):
  with host.sudo():
    assert host.file("/etc/ssh/sshd_config").contains("^IgnoreRhosts yes$")

def test_sshd_deny_empty_password (host):
  with host.sudo():
    assert host.file("/etc/ssh/sshd_config").contains("^PermitEmptyPasswords no$")

def test_sshd_banner (host):
  with host.sudo():
    assert host.file("/etc/ssh/sshd_config").contains("^Banner /etc/issue.net$")

def test_empty_password_check(host):
  with host.sudo():
    empty_passwd=host.run("getent shadow | grep -Po '^[^:]*(?=::)'")
    assert empty_passwd.stdout == ""

def test_legacy_password_check(host):
  with host.sudo():
    empty_passwd = host.run("getent shadow | grep -Po '^[^:]*(?=:x:)'")
    assert empty_passwd.stdout == ""

def test_users_with_uid_0_check(host):
   uid_0_no_root = host.run("grep 'x:0' /etc/passwd | grep -v root")
   assert uid_0_no_root.stdout == ""

#TODO
#def test_suid_sgid_check(host):
  
#TODO
#def test_unowned_check(host):
# sudo find / \( -nouser -o -nogroup \) -print

#TODO
#def test_world_writable_dirs_check

#TODO
#def test_user_home_check
 
