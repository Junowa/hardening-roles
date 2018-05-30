param(
  [string]$vcenter_hostname,
  [string]$vcenter_username,
  [string]$vcenter_password,
  [string]$inventory_hostname
)

Get-Module -ListAvailable PowerCLI* | Import-Module

$vmx_options = @{}
$vmx_options.add('tools.syncTime', '0')
$vmx_options.add('time.synchronize.continue', '0')
$vmx_options.add('time.synchronize.restore', '0')
$vmx_options.add('time.synchronize.resume.disk', '0')
$vmx_options.add('time.synchronize.shrink', '0')
$vmx_options.add('time.synchronize.tools.startup', '0')
$vmx_options.add('time.synchronize.tools.enable', '0')
$vmx_options.add('time.synchronize.resume.host', '0')

Connect-VIServer -Server $vcenter_hostname -User $vcenter_username -Password $vcenter_password | Out-Null

$vm =Get-View -ViewType VirtualMachine -Filter @{"Name"= $inventory_hostname}
$vmConfigSpec = New-Object VMWare.Vim.VirtualMachineConfigSpec
$vmConfigSpec.extraconfig += New-Object VMware.Vim.optionvalue

$vmx_options.Keys | % {

  $vmConfigSpec = New-Object VMWare.Vim.VirtualMachineConfigSpec
  $vmConfigSpec.extraconfig += New-Object VMware.Vim.optionvalue
  $vmConfigSpec.extraconfig[0].Key = $_
  $vmConfigSpec.extraconfig[0].value = $vmx_options.Item($_)
  $vm.ReconfigVM($vmConfigSpec)

}


Disconnect-VIServer -Server $vcenter_hostname -Confirm:$false | Out-Null
#End
