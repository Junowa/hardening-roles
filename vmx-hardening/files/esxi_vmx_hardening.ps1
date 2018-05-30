param(
  [string]$vcenter_hostname,
  [string]$vcenter_username,
  [string]$vcenter_password,
  [string]$inventory_hostname
)

Get-Module -ListAvailable PowerCLI* | Import-Module

$vmx_options = @{}
$vmx_options.add('isolation.device.connectable.disable', 'true')
$vmx_options.add('isolation.device.edit.disable', 'true')
$vmx_options.add('isolation.tools.diskWiper.disable', 'true')
$vmx_options.add('isolation.tools.diskShrink.disable', 'true')
$vmx_options.add('isolation.tools.copy.disable', 'true')
$vmx_options.add('isolation.tools.paste.disable', 'true')
$vmx_options.add('isolation.tools.setGUIOptions.enable', 'false')
$vmx_options.add('isolation.tools.setInfo.disable', 'true')
$vmx_options.add('isolation.tools.log..disable', 'true')
$vmx_options.add('log.rotateSize', '10000')
$vmx_options.add('log.keepold', '10')
$vmx_options.add('tools.setInfo.sizeLimit', '1048576')
$vmx_options.add('vlance.noOprom', 'true')
$vmx_options.add('vmxnet.noOprom', 'true')
$vmx_options.add('RemoteDisplay.maxConnections', '1')
$vmx_options.add('vmci0.unrestricted', 'false')
$vmx_options.add('guest.commands.enabled', 'false')
$vmx_options.add('tools.guestlib.enableHostInfo', 'false')
$vmx_options.add('Ethernet0.opromsize', '0')
$vmx_options.add('Ethernet1.opromsize', '0')
$vmx_options.add('Ethernet2.opromsize', '0')
$vmx_options.add('Ethernet4.opromsize', '0')

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
