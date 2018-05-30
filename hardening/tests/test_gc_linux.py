""" hardening dga-mi linux module """

import pytest

@pytest.mark.skip(reason="No way of testing motherboard or hard drive  physical protection")
def test_hw_security ():
  """ R1 """
  pass

# R2
def test_root_partition_exist (host):
  """ R2 """
  assert host.mount_point("/").exists

# R2
def test_tmp_partition_exist (host):
  """ R2 """
  assert host.mount_point("/tmp").exists

# R2
def test_home_partition_exist (host):
  """ R2 """
  assert host.mount_point("/home").exists

# R2
def test_var_partition_exist (host):
  """ R2 """
  assert host.mount_point("/var").exists

# R2
def test_var_log_partition_exist (host):
  """ R2 """
  assert host.mount_point("/var/log").exists

# R2
def test_var_log_audit_partition_exist (host):
  """ R2 """
  assert host.mount_point("/var/log/audit").exists

# R3
@pytest.mark.skip(reason="BIOS tests not covered (cf. vmx hardening tests)")
def test_bios_password ():
  """ R3 """
  pass

# R4
@pytest.mark.skip(reason="BIOS tests not covered (cf. vmx hardening tests)")
def test_bios_disable_notused_device_boot ():
  """ R4 """
  pass

# R5
@pytest.mark.skip(reason="BIOS tests not covered (cf. vmx hardening tests)")
def test_bios_disable_notused_usb_device ():
  """ R5 """
  pass

# R6
@pytest.mark.skip(reason="BIOS tests not covered (cf. vmx hardening tests)")
def test_bios_disable_pxe ():
  """ R6 """
  pass

# R7
@pytest.mark.skip(reason="BIOS tests not covered (cf. vmx hardening tests)")
def test_bios_disable_notused_usb_serial ():
  """ R7 """
  pass

# R8
def test_grub_unique_os (host):
  """ R8 """
  with host.sudo():
    other_entry=host.run("grep \"^menuentry\" /boot/grub2/grub.cfg | grep -v \"CentOS Linux\"")
    assert other_entry.stdout == ""


# R9/R10
def test_grub_password_exist (host):
  """ R9/R10 """
  with host.sudo():
    assert host.file("/boot/grub2/user.cfg").contains("grub.pbkdf2.sha512")

# R11
def test_grub_conf_owner (host):
  """ R11 """
  with host.sudo():
    owner = host.file("/boot/grub2/user.cfg").user
    assert owner in 'root'

# R12/R13
@pytest.mark.skip(reason="Non-applicable because Grub used instead of Lilo")
def test_lilo ():
  """ R12/R13 """
  pass

# R14
# N/A Installation a partir dun master minimal
@pytest.mark.skip(reason="Template with core package group only - cf. NCIRC for the removal of uncessary packages")
def test_minimal_install ():
  """ R14 """
  pass

# R15
# N/A couvert par la mise en place dun processus MCS
@pytest.mark.skip(reason="No way of testing because configure as manual- cf. security update organizational processes")
def test_security_update_tracking():
  """ R15 """
  pass

# R16
def test_password_shadow_enabled(host):
  """ R16 """
  shadow_enable=host.run("/usr/sbin/authconfig --test | grep shadow")
  assert "shadow passwords are enabled" in shadow_enable.stdout

# R17
# TODO use regex for multiple spaces in pattern
def test_password_shadow_only (host):
  """ R17 """
  shadow_config="^password.*sufficient.*pam_unix.so sha512 shadow.*try_first_pass use_authtok"
  assert host.file("/etc/pam.d/password-auth").contains(shadow_config)
  assert host.file("/etc/pam.d/system-auth").contains(shadow_config)



#R18/R19
def test_password_quality_enabled (host):
  """ R18/19 """
  pwquality_config="password.*requisite.*pam_pwquality.so local_users_only enforce_for_root retry=3"
  assert host.file("/etc/pam.d/password-auth").contains(pwquality_config)
  assert host.file("/etc/pam.d/system-auth").contains(pwquality_config)

def test_password_quality_config (host):
  """ R18/19 """
  assert host.file("/etc/security/pwquality.conf").contains('^difok = 5$')
  assert host.file("/etc/security/pwquality.conf").contains('^minlen = 14$')
  assert host.file("/etc/security/pwquality.conf").contains('^dcredit = 1$')
  assert host.file("/etc/security/pwquality.conf").contains('^ucredit = 1$')
  assert host.file("/etc/security/pwquality.conf").contains('^lcredit = 1$')
  assert host.file("/etc/security/pwquality.conf").contains('^ocredit = 1$')
  assert host.file("/etc/security/pwquality.conf").contains('^minclass = 4$')

  shadow_config="auth.*required.*pam_faillock.so preauth audit deny=3 unlock_time=900"
  assert host.file("/etc/pam.d/password-auth").contains(shadow_config)
  assert host.file("/etc/pam.d/system-auth").contains(shadow_config)

  shadow_config="password.*required.*pam_pwhistory.so enforce_for_root remember=10 use_authok"
  assert host.file("/etc/pam.d/password-auth").contains(shadow_config)
  assert host.file("/etc/pam.d/system-auth").contains(shadow_config)

# R20
def test_password_lifetime_config (host):
  """ R20 """
  assert host.file("/etc/login.defs").contains("^PASS_MAX_DAYS\s90")
  assert host.file("/etc/login.defs").contains("^PASS_MIN_DAYS\s7")
  assert host.file("/etc/login.defs").contains("^PASS_WARN_AGE\s7")

# R21
def test_logindefs_owner (host):
  """ R21 """
  with host.sudo():
    owner = host.file("/etc/login.defs").user
    assert owner in 'root'
  
# R22
def test_passwd_owner (host):
  """ R22 """
  with host.sudo():
    owner = host.file("/etc/passwd").user
    assert owner in 'root'

# R23
def test_shadow_owner (host):
  """ R23 """
  with host.sudo():
    owner = host.file("/etc/shadow").user
    assert owner in 'root'

# R24
def test_disable_local_root_login (host):
  """ R24 """
  assert host.file("/etc/securetty").size == 0

# R25
def test_securetty_chmod (host):
  """ R25 """
  assert oct(host.file("/etc/securetty").mode) == '0600'

# R26
def test_disable_ssh_root_login (host):
  """ R26 """
  with host.sudo():
    assert host.file("/etc/ssh/sshd_config").contains("^PermitRootLogin no$")

# R27
def test_sshdconfig_chmod (host):
  """ R27 """
  assert oct(host.file("/etc/ssh/sshd_config").mode) == '0600'

# R28
def test_restrict_su_users (host):
  """ R28 """
  assert oct(host.file("/etc/ssh/sshd_config").mode) == '0600'
  with host.sudo():
    assert host.file("/etc/pam.d/su").contains("^auth           required        pam_wheel.so use_uid")

# R29
def test_group_chmod (host):
  """ R29 """
  assert oct(host.file("/etc/ssh/sshd_config").mode) == '0600'
  assert oct(host.file("/etc/group").mode) == '0644'

# R30
def test_restrict_root_login (host):
  """ R30 """
  assert oct(host.file("/etc/ssh/sshd_config").mode) == '0600'
  assert host.file("/etc/securetty").size == 0

# R31
def test_restrict_su (host):
  """ R31 """
  assert oct(host.file("/etc/ssh/sshd_config").mode) == '0600'
  with host.sudo():
    assert host.file("/etc/pam.d/su").contains("^auth           required        pam_wheel.so use_uid")

# R32/R33/R34
def test_part_nosuid_nodev_noexec (host):
  """ R32/R33/R34 """
  assert oct(host.file("/etc/ssh/sshd_config").mode) == '0600'
  assert host.file("/etc/fstab").contains("/home.*nodev,nosuid,noexec")
  assert host.file("/etc/fstab").contains("/tmp.*nodev,nosuid,noexec")
  assert host.file("/etc/fstab").contains("/var.*nodev,nosuid,noexec")

# R35
def test_fstab_chmod_owner (host):
  """ R35 """
  assert oct(host.file("/etc/ssh/sshd_config").mode) == '0600'
  with host.sudo():
    assert host.file("/etc/fstab").user in 'root'
    assert oct(host.file("/etc/fstab").mode) == '0644'

# R36
# Note: increase required chmod from 644 to 444
def test_mtab_chmod_owner (host):
  """ R36 """
  with host.sudo():
    assert host.file("/proc/self/mounts").user in 'root'
    assert oct(host.file("/proc/self/mounts").mode) == '0444'

# R37
def test_var_log_chmod (host):
  """ R37 """
  with host.sudo():
    assert oct(host.file("/var/log").mode) == '0755'

# R38
def test_var_log_wtmp_chmod (host):
  """ R38 """
  with host.sudo():
    assert host.file("/var/log/wtmp").user in 'root'
    assert oct(host.file("/var/log/wtmp").mode) == '0644'

# R39
def test_var_run_utmp_chmod (host):
  """ R39 """
  with host.sudo():
    assert host.file("/var/run/utmp").user in 'root'
    assert oct(host.file("/var/run/utmp").mode) == '0644'

# R40
def test_find_free_access_file (host):
   """ R40 """
   with host.sudo():
     free_access_files=host.run("find / -perm 2 ! -type l -ls ")
     assert free_access_files.stdout == ""

# R41
def test_find_free_owner_file (host):
   """ R41 """
   with host.sudo():
     free_owner_files=host.run("find / \( -nouser -o -nogroup \) -print")
     assert free_owner_files.stdout == ""

# R42
@pytest.mark.skip(reason="Non-applicable on servers")
def test_working_hours_policy ():
  """ R42 """
  pass

# R43
def test_securitytime_chmod_owner (host):
  """ R43 """
  with host.sudo():
    assert host.file("/etc/security/time.conf").user in 'root'
    assert oct(host.file("/etc/security/time.conf").mode) == '0644'

# R44
@pytest.mark.skip(reason="Non-applicable because obsolete with systemd")
def test_services_hardening ():
  """ R44 """
  pass

# R45
def test_services_chmod_owner (host):
  """ R45 """
  with host.sudo():
    assert host.file("/etc/services").user in 'root'
    assert oct(host.file("/etc/services").mode) == '0644'

# R46
def test_unecessary_packages_removed (host):
  """ R46 """
  with host.sudo():
    assert not host.package("telnet").is_installed
    assert not host.package("rsh").is_installed

# R47
def test_firewall_enabled (host):
  """ R47 """
  service = host.service('firewalld')
  assert service.is_running
  assert service.is_enabled

# R48-R50
# N/A: fichier obsolete

# TODO R51-R55

# R56-R69
# N/A: service non deployes

