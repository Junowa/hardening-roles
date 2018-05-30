param(
  [string]$vcenter_hostname,
  [string]$vcenter_username,
  [string]$vcenter_password,
  [string]$template_dir,
  [string]$template,
  [string]$compute,
  [string]$datastore,
  [string]$cluster
)

Get-Module -ListAvailable PowerCLI* | Import-Module
Connect-VIServer -Server $vcenter_hostname -User $vcenter_username -Password $vcenter_password | Out-Null

$mycluster=Get-Cluster -Name $cluster
$myHost=Get-VMHost -Name $compute
$myDatastore=Get-Datastore -Name $datastore

$tmplSuffix=$cluster -replace '\s',''
Import-VApp -Source $template_dir/$template.ova -VMHost $myHost -Datastore $myDatastore -Name $template-$tmplSuffix

Disconnect-VIServer -Server $vcenter_hostname -Confirm:$false | Out-Null
#End
