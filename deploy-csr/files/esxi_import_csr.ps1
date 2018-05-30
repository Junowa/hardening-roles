param(
  [string]$vcenter_hostname,
  [string]$vcenter_username,
  [string]$vcenter_password,
  [string]$template_dir,
  [string]$template,
  [string]$compute,
  [string]$cluster,
  [string]$vmname,
  [string]$admin_vswitch,
  [string]$mgmt_ipv4_addr,
  [string]$mgmt_ipv4_gateway
)

Get-Module -ListAvailable PowerCLI* | Import-Module
Connect-VIServer -Server $vcenter_hostname -User $vcenter_username -Password $vcenter_password | Out-Null

$check_vm=""
Try { 
  $check_vm=$compute | Get-VM -Name $vmname -ErrorAction Stop
  If ($check_vm)
  {
    Write-Host "VM already exists"
    exit
  }
} 
Catch { Write-Host "Start to deploy..."}


$mycluster=Get-Cluster -Name $cluster
$myHost=Get-VMHost -Name $compute

$ovapath=$template_dir+"/"+$template+".ova"
$ovfconfig=Get-OvfConfiguration -Ovf $ovapath

$ovfconfig.NetworkMapping.GigabitEthernet1.Value = $admin_vswitch
$properties=$ovfconfig.com.cisco.csr1000v.1
$properties.hostname.Value=$vmname
$properties.mgmt_ipv4_addr.Value=$mgmt_ipv4_addr
$properties.mgmt_ipv4_gateway.Value=$mgmt_ipv4_gateway 

#Default
$properties.login_username.Value="admin" 
$properties.login_password.Value="cisco123"
$properties.mgmt_interface.Value="GigabitEthernet1"
$properties.enable_ssh_server.Value="True"
$properties.privilege_password.Value="cisco123"


Import-VApp -Source $template_dir/$template.ova -OvfConfiguration $ovfconfig -VMHost $myHost -Name $vmname

Start-VM -RunAsync -VM $vmname -Confirm:$false | Out-Null

Disconnect-VIServer -Server $vcenter_hostname -Confirm:$false | Out-Null
#End
