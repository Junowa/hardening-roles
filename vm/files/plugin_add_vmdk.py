#!/usr/bin/env python

from pyVmomi import vim
from pyVmomi import vmodl
from pyVim.connect import SmartConnect, Disconnect
import atexit
import argparse
import getpass
import sys


def add_disk(vm, si, disk_size, disk_type): 
    spec = vim.vm.ConfigSpec()
    unit_number=0
    controller=vim.vm.device.VirtualDevice()
    # get all disks on a VM, set unit_number to the next available
    for dev in vm.config.hardware.device:
        if hasattr(dev.backing, 'fileName'):
            unit_number = int(dev.unitNumber) + 1
           # unit_number 7 reserved for scsi controller
            if unit_number == 7:
                unit_number += 1
            if unit_number >= 16:
                print "we don't support this many disks"
                return
        if isinstance(dev, vim.vm.device.VirtualSCSIController):
            controller = dev
    ''' add disk here'''
    dev_changes = []
    new_disk_kb = int(disk_size) * 1024 * 1024
    disk_spec = vim.vm.device.VirtualDeviceSpec()
    disk_spec.fileOperation = "create"
    disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
    disk_spec.device = vim.vm.device.VirtualDisk()
    disk_spec.device.backing = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
    if disk_type == 'thin':
        disk_spec.device.backing.thinProvisioned = True
    else:
      pass
    disk_spec.device.backing.diskMode = 'persistent'
    disk_spec.device.unitNumber = unit_number
    disk_spec.device.capacityInKB = new_disk_kb
    disk_spec.device.controllerKey = controller.key
    dev_changes.append(disk_spec)
    spec.deviceChange = dev_changes
    vm.ReconfigVM_Task(spec=spec)
    print "%sGB disk added to %s" % (disk_size, vm.config.name)


def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def main():
    si = SmartConnect(
        host=host,
        user=user,
        pwd=pwd)
    vm = None
    if vm_name:
        content = si.RetrieveContent()
        vm = get_obj(content, [vim.VirtualMachine], vm_name)
    if vm:
        add_disk(vm, si, disk_size, disk_type)
    else:
        print "VM not found"


# start this thing
if __name__ == "__main__":
    host=sys.argv[1]
    user=sys.argv[2]
    pwd=sys.argv[3]
    vm_name=sys.argv[4]
    disk_type=sys.argv[5]
    disk_size=sys.argv[6]

    main()

