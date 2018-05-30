""" active directory client module """
# these accounts must be defined in AD (to test all Vms with same accounts) :
#
## admin_account in Administrateurs Fonctionnel, Administrateurs Reseau, Administrateurs Systeme, Administrateurs Securite
#
## sup_account in Superviseurs Reseau, Superviseurs Systeme, Superviseurs Securite
#
## other_account in no group
#
#
# --> parameters must be defined here :
#
#

admin_account = "test1"
admin_password = "Descartes@2016"

sup_account = "test2"
sup_password = "Descartes@2016"

other_account = "test3"
other_password = "Descartes@2016"

def test_ad_join(host):
        """ Test if realmd is installed and the current domain with \'sudo realmd list\' """
	with host.sudo():
		assert host.package("realmd").is_installed
		realm = host.run("realm list")
		domain = host.ansible.get_variables()["domain"]
		assert realm.rc == 0
		assert domain in realm.stdout #domain joined

def test_ad_kerberos(host):
        """ Test if the machine is a kerberos-member with \'sudo realmd list\' """
	with host.sudo():
		assert host.package("realmd").is_installed
		realm = host.run("realm list")
		assert realm.rc == 0
		assert "kerberos-member" in realm.stdout #join with kerberos

def test_ad_admin_login(host):
        """ Test admin test user account login uis sucessfull """
	with host.sudo():
		pamtester = host.run("pamtester login " + admin_account + " acct_mgmt")
		assert pamtester.rc == 0 
		assert "done" in pamtester.stdout #login ok

def test_ad_admin_sudo(host):		
        """ Test a sudo for the admin test user is sucessfull """
	with host.sudo(admin_account):
		assert host.check_output("whoami") == admin_account
		sudo_right = host.run("echo '" + admin_password + "' | sudo -S -l")
		assert sudo_right.rc == 0
		assert "may run the following commands on this host" in sudo_right.stdout #have sudo right

def test_ad_sup_login(host):
        """ Test supervisor test user account login is successfull """
	with host.sudo():
		pamtester = host.run("pamtester login " + sup_account + " acct_mgmt")
		assert pamtester.rc == 0 
		assert "done" in pamtester.stdout #login ok

def test_ad_sup_sudo(host):		
        """ Test a sudo for the supervisor test user is unsucessfull """
	with host.sudo(sup_account):
		assert host.check_output("whoami") == sup_account
		sudo_right = host.run("echo '" + sup_password + "' | sudo -S -l")
		assert sudo_right.rc == 0
		assert "may run the following commands on this host" not in sudo_right.stdout #not have sudo right

def test_ad_other_login(host):
        """ Test a test user account in no group login is unsuccessfull"""
	with host.sudo():
		pamtester = host.run("pamtester login " + other_account + " acct_mgmt")
		assert pamtester.rc == 1 
		assert "Permission denied" in pamtester.stderr #login ko

def test_ad_other_sudo(host):
        """ Test a sudo for the no group test user is unsucessfull """
	with host.sudo(other_account):
		assert host.check_output("whoami") == other_account
		sudo_right = host.run("echo '" + other_password + "' | sudo -S -l")
		assert sudo_right.rc == 0
		assert "may run the following commands on this host" not in sudo_right.stdout #not have sudo right

def test_ad_access_rights(host):
        """ Test a no group test user can not list files with \'ls /root \' """
	with host.sudo(admin_account):
		ls = host.run("ls /root")
		assert ls.rc != 0
		assert "Permission non accord" in ls.stderr
