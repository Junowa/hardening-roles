### Variable to be define


# Additional VG/LV (size in mb) created with additional vmdk
vg_list:
    - vg_name : vg_opt
      vg_disk : /dev/sdb

      lv_list:
        - lv_name: part3
          lv_fstype: ext4
          lv_fsopts: nobarrier
          lv_mountpoint: /opt/part3
          lv_mountopts: nodev,nosuid,noexec
          lv_size: 512
