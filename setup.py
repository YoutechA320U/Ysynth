# -*- coding: utf-8 -*-
import subprocess
subprocess.call('sudo mkdir /mnt/g_mass_storage' ,shell=True)
subprocess.call('dd if=/dev/zero of=/home/pi/g_mass_storage.img bs=64M count=64' ,shell=True)
subprocess.call('sudo losetup /dev/loop0 /home/pi/g_mass_storage.img' ,shell=True)
subprocess.call('sudo parted /dev/loop0 -s mklabel msdos mkpart primary fat32 2048s 100%' ,shell=True)
subprocess.call('sudo mkfs.vfat /dev/loop0p1' ,shell=True)
subprocess.call('sudo losetup -d /dev/loop0' ,shell=True)
subprocess.call('sudo mount -t vfat -o uid=pi,iocharset=utf8,loop,offset=1048576 /home/pi/g_mass_storage.img /mnt/g_mass_storage/' ,shell=True)
subprocess.call('sudo apt-get install -y libasound2-dev git build-essential python3-dev libpython3.5-dev libjack-jackd2-dev cython3 python3-setuptools i2c-tools python3-smbus python3-rpi.gpio python3-pip timidity fluid-soundfont-gm' ,shell=True)
subprocess.call('sudo mkdir /mnt/g_mass_storage/sf2' ,shell=True)
subprocess.call('sudo mkdir /mnt/g_mass_storage/midi' ,shell=True)
subprocess.call('mkdir /home/pi/timidity_cfg' ,shell=True)
subprocess.call('sudo chown -R pi:pi /home/pi/' ,shell=True)
subprocess.call('sudo apt-get remove -y timidity-daemon' ,shell=True)
subprocess.call('sudo systemctl disable timidity.service' ,shell=True)
subprocess.call('sudo pip3 install python-rtmidi' ,shell=True)
subprocess.call('sudo cp /usr/share/sounds/sf2/*.sf2 /mnt/g_mass_storage/sf2' ,shell=True)
subprocess.call('sudo rm /usr/share/sounds/sf2/*.sf2' ,shell=True)
subprocess.call('sudo raspi-config nonint do_i2c 0' ,shell=True)
subprocess.call('chmod +x /home/pi/Ysynth/cfgforsf' ,shell=True)
script = '''
# For more options and information see
# http://rpf.io/configtxt
# Some settings may impact device functionality. See link above for details

# uncomment if you get no picture on HDMI for a default "safe" mode
#hdmi_safe=1

# uncomment this if your display has a black border of unused pixels visible
# and your display can output without overscan
#disable_overscan=1

# uncomment the following to adjust overscan. Use positive numbers if console
# goes off screen, and negative if there is too much border
#overscan_left=16
#overscan_right=16
#overscan_top=16
#overscan_bottom=16

# uncomment to force a console size. By default it will be display's size minus
# overscan.
#framebuffer_width=1280
#framebuffer_height=720

# uncomment if hdmi display is not detected and composite is being output
#hdmi_force_hotplug=1

# uncomment to force a specific HDMI mode (this will force VGA)
#hdmi_group=1
#hdmi_mode=1

# uncomment to force a HDMI mode rather than DVI. This can make audio work in
# DMT (computer monitor) modes
#hdmi_drive=2

# uncomment to increase signal to HDMI, if you have interference, blanking, or
# no display
#config_hdmi_boost=4

# uncomment for composite PAL
#sdtv_mode=2

#uncomment to overclock the arm. 700 MHz is the default.
#arm_freq=800

# Uncomment some or all of these to enable the optional hardware interfaces
dtparam=i2c_arm=on
dtparam=i2s=on
#dtparam=spi=on

# Uncomment this to enable the lirc-rpi module
#dtoverlay=lirc-rpi

# Additional overlays and parameters are documented /boot/overlays/README

# Enable audio (loads snd_bcm2835)
#dtparam=audio=on
dtoverlay=iqaudio-dacplus
dtoverlay=dwc2
'''
f=open("/boot/config.txt","wt")
f.write(script)
f.close()
script = '''
@audio - rtprio 95
@audio memlock unlimited
@audio -nice -19
'''
f=open("/etc/security/limits.d/audio.conf","wt")
f.write(script)
f.close()
script = '''
options snd slots=snd_soc_iqaudio_dac, usb_f_midi
options snd_soc_iqaudio_dac index=0
options usb_f_midi index=1
'''
f=open("/etc/modprobe.d/alsa-base.conf","wt")
f.write(script)
f.close()
script = '''
# Instrument configuration file for timidity
# $Id: timidity.cfg,v 1.7 2005/09/03 19:26:03 hmh Exp $

# You can change just about every option in TiMidity++ using
# This config file.  Please refer to the timidity.cfg(5) manpage
# for more details

## If you have a slow CPU, uncomment these:
#opt EFresamp=d         #disable resampling
#opt EFvlpf=d           #disable VLPF
#opt EFreverb=d         #disable reverb
#opt EFchorus=d         #disable chorus
#opt EFdelay=d          #disable delay
#opt anti-alias=d       #disable sample anti-aliasing
#opt EWPVSETOZ          #disable all Midi Controls
#opt p32a               #default to 32 voices with auto reduction
#opt s32kHz             #default sample frequency to 32kHz
#opt fast-decay         #fast decay notes

## If you have a moderate CPU, try these:
#opt EFresamp=l
#opt EFreverb=g,42
#opt EFchorus=s
#opt s32kHz
#opt p64a

opt iA
opt Os
opt --sequencer-ports=1
opt --realtime-priority=90
opt B2,8
opt q0-0
opt s32kHz
opt -EFresamp=1
opt -EFreverb=1
opt -EFchorus=1
opt p64a

# Disabling some of the Midi Controls can help with the CPU usage a lot.
# The same goes to the VLPF, sample anti-aliasing and effects such as
# reverb and chorus

# By default, try to use the instrument patches from freepats:
#source /etc/timidity/freepats.cfg

# alternatively, you can use the fluid-soundfont:
#source /etc/timidity/fluidr3_gm.cfg
#source /etc/timidity/fluidr3_gs.cfg
'''
f=open("/etc/timidity/timidity.cfg","wt")
f.write(script)
f.close()
script = '''
[Unit]
Description = Ysynth

[Service]
ExecStart = /usr/bin/python3.5 /home/pi/Ysynth/ysynth.py
Restart = always
Type = simple

[Install]
WantedBy = multi-user.target
'''
f=open("/etc/systemd/system/ysynth.service","wt")
f.write(script)
f.close()
subprocess.call('sudo systemctl enable ysynth.service' ,shell=True)
script = '''
ACTION=="add", \
SUBSYSTEMS=="usb", \
RUN+="/bin/bash /home/pi/Ysynth/midiconnect.sh"
'''
f=open("/etc/udev/rules.d/90-usbmidiconnect.rules","wt")
f.write(script)
f.close()

subprocess.call('sudo reboot' ,shell=True)
