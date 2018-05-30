""" firewalld module """

def test_firewall_ssh(host):
        """ Run \'firewall-cmd --list-all-zones\' and check if command runs successfully and ssh is opened"""
	with host.sudo():
		all_zones = host.run("firewall-cmd --list-all-zones")
		assert host.ansible("command", "echo foo", check=False)["stdout"] == "foo" #ssh working
		assert all_zones.rc == 0
		assert "22/tcp" or "ssh" in all_zones.stdout # ssh open in firewall


def test_firewalld_package(host):
        """ Check if firewalld is installed with \'yum info firewalld\'"""
	with host.sudo():
		firewalld = host.package('firewalld')
		assert firewalld.is_installed


def test_firewall_service(host):
        """ Check if firewalld is running and enabled with \'systemctl status firewalld\'"""
	with host.sudo():
		firewalld = host.service('firewalld')
		assert firewalld.is_running
		assert firewalld.is_enabled

def test_firewall_default_zone_drop(host):
        """ Check firewalld default zone is drop with \'firewall-cmd --get-default-zone\'"""
	with host.sudo():
		default_zone = host.run("firewall-cmd --get-default-zone")
		assert default_zone.stdout == "drop"
		assert default_zone.rc == 0


def test_firewall_default_zone_target_DROP(host):
        """ Check firewalld default zone target is DROP with \'firewall-cmd --permanent --zone=drop --get-target\'"""
	with host.sudo():
		default_zone = host.run("firewall-cmd --permanent --zone=drop --get-target")
		assert default_zone.stdout == "DROP"
		assert default_zone.rc == 0


def test_firewall_other_zones_defined(host):
        """ Check firewalld zone definition and if source ranges are defined \'firewall-cmd --permanent --get-zones\'"""
	with host.sudo():
		fw_zones = host.ansible.get_variables()["fw_zones"]
		#@pytest.mark.parametrize("zone",fw_zones)
		zone_list = host.run("firewall-cmd --permanent --get-zones")
		assert zone_list.rc == 0
		for zone in fw_zones:
			assert zone["name"] in zone_list.stdout #zone is defined in firewalld
			ip_sources = host.run("firewall-cmd --list-sources --zone=" + zone["name"])
			#ip_sources = host.run("firewall-cmd --list-sources --zone=drop")
			assert ip_sources.rc == 0
			assert ip_sources.stdout #ip sources are bound to zone

