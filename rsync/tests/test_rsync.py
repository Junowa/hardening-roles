""" rsync module """
def test_rsync_crontask(host):
  with host.sudo():
    rsync_job_cmd = host.run("crontab -l | grep rsync | cut -d\' \'  -f 6-")
    assert not rsync_job_cmd.stdout
    
