# -*- coding: utf-8 -*-
#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import subprocess
import so1602
import rtmidi

clear = 0x01
display_On=0x0c
display_Off=0x08
display_on_No_Cursor=0x0c
OLED_1stline=0x80
OLED_2ndline=0xa0
so1602.setaddr(0x3c) #so1602のI2Cアドレス
so1602.command(clear)
so1602.command(0x02)
so1602.command(display_On)


input_A = 4
input_B = 17
input_C = 27
input_D = 5
input_E = 6
input_F = 26
input_G = 13
input_H = 24
input_I = 23

volume = 90
mode = 0
CC2 = 0
CC1 = 0
prevolume = 0
premode = 0
preCC2 = 0
preCC1 = 0
midiCH = 0
midiPROG=  [0]*16
midiCC7=  [100]*16
midiCC11=  [127]*16
midiCC10=  [64]*16
midiCC1=  [0]*16
midiCC91=  [40]*16
midiCC93=  [0]*16
midiCC94=  [0]*16
pb1 = [0]*16
pb2 = [0x40]*16
playflag = [0]
sf2used = [0]
pbcounter =[0]*16

GPIO.setmode(GPIO.BCM)
GPIO.setup(input_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_C, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_D, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_E, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_F, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_G, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_H, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_I, GPIO.IN, pull_up_down=GPIO.PUD_UP)
rock_flag = 1

def rotaryDeal_1():
  global volume, Last_input_C_Status, Current_input_C_Status, rock_flag
  Last_input_C_Status = GPIO.input(input_C)
  flag1 = 0
  while GPIO.input(input_B) ==0 and (GPIO.input(input_D) !=0 or GPIO.input(input_F) !=0 or GPIO.input(input_H) !=0):
    Current_input_C_Status = GPIO.input(input_C)
    flag1 = 1
  if flag1 == 1 :
     flag1 = 0
     if (Last_input_C_Status == 0) and (Current_input_C_Status == 1):
        volume += 1
     if (Last_input_C_Status == 1) and (Current_input_C_Status == 0):
        volume -= 1

def rotaryDeal_2():
  global mode, Last_input_E_Status, Current_input_E_Status, rock_flag
  Last_input_E_Status = GPIO.input(input_E)
  flag2 = 0
  while GPIO.input(input_D) ==0 and (GPIO.input(input_B) !=0 or GPIO.input(input_F) !=0 or GPIO.input(input_H) !=0):
    Current_input_E_Status = GPIO.input(input_E)
    flag2 = 1
  if flag2 == 1:
    flag2 = 0
    if (Last_input_E_Status == 0) and (Current_input_E_Status == 1):
      mode += 1
    if (Last_input_E_Status == 1) and (Current_input_E_Status == 0):
      mode -=1

def rotaryDeal_3():
  global CC2, Last_input_G_Status, Current_input_G_Status, rock_flag
  Last_input_G_Status = GPIO.input(input_G)
  flag3 = 0
  while GPIO.input(input_F) ==0 and (GPIO.input(input_B) !=0 or GPIO.input(input_D) !=0 or GPIO.input(input_H) !=0) :
    Current_input_G_Status = GPIO.input(input_G)
    flag3 = 1
  if flag3 == 1:
    flag3 = 0
    if (Last_input_G_Status == 0) and (Current_input_G_Status == 1):
      CC2 = CC2 + 1
    if (Last_input_G_Status == 1) and (Current_input_G_Status == 0):
      CC2 = CC2 -1

def rotaryDeal_4():
  global CC1, Last_input_I_Status, Current_input_I_Status, rock_flag
  Last_input_I_Status = GPIO.input(input_I)
  flag4 = 0
  while GPIO.input(input_H)== 0 and (GPIO.input(input_B) !=0 or GPIO.input(input_F) !=0 or GPIO.input(input_D) !=0):
    Current_input_I_Status = GPIO.input(input_I)
    flag4 = 1
  if flag4 == 1:
    flag4 = 0
    if (Last_input_I_Status == 0) and (Current_input_I_Status == 1):
      CC1 = CC1 + 1
    if (Last_input_I_Status == 1) and (Current_input_I_Status == 0):
      CC1 = CC1 -1

midicounter = 0
sf2counter = 0
so1602.command(OLED_1stline)
so1602.write("     Ysynth")
so1602.command(OLED_2ndline)
so1602.write("     Rev3.0")
time.sleep(2.0)
so1602.command(clear)
so1602.command(OLED_1stline)
so1602.write("       by")
time.sleep(1.0)
so1602.command(OLED_2ndline)
so1602.write("  YoutechA320U")
time.sleep(2.0)
subprocess.call('sudo mount -t vfat -o uid=pi,iocharset=utf8,loop,offset=1048576 /home/pi/g_mass_storage.img /mnt/g_mass_storage/' ,shell=True)
try:
  midi = subprocess.check_output('ls -v /mnt/g_mass_storage/midi/*.mid' ,shell=True).decode('utf-8').strip().replace('/mnt/g_mass_storage/midi/', '').replace('.mid', '').split('\n')
  playflag = [0]*len(midi)
except:
 midi= ["midi_None"]
try:
 sf2 = subprocess.check_output('ls -v /mnt/g_mass_storage/sf2/*.sf2' ,shell=True).decode('utf-8').strip().replace('/mnt/g_mass_storage/sf2/', '').replace('.sf2', '').split('\n')
 sf2used = [0]*len(sf2)
except:
 sf2 = ["sf2_None"]
 rock_flag = 0
try:
 cfg = subprocess.check_output('ls -v /home/pi/timidity_cfg/*.cfg' ,shell=True).decode('utf-8').strip().replace('/home/pi/timidity_cfg/', '').replace('.cfg', '').split('\n')
except:
 cfg = [ ]
if (sf2 != cfg) and (sf2[0] != "sf2_None"):
 so1602.command(clear)
 so1602.command(OLED_1stline)
 so1602.write("making")
 so1602.command(OLED_2ndline)
 so1602.write("sf2_config")
 list_difference = list(set(cfg) - set(sf2))
 list_difference = [l.replace(' ', '\ ') for l in list_difference]
 for x in range(len(list_difference)):
  print(list_difference[x])
  subprocess.call('sudo rm /home/pi/timidity_cfg/{}.cfg' .format(list_difference[x])  ,shell=True)
 list_difference = list(set(sf2) - set(cfg))
 list_difference = [l.replace(' ', '\ ') for l in list_difference]
 for x in range(len(list_difference)):
  so1602.write(".")
  subprocess.call("sudo /home/pi/Ysynth/cfgforsf -C /mnt/g_mass_storage/sf2/{sf2name}.sf2 | sed -e 's/(null)//' -e 's/^[ ]*//g' -e '/(null)#/d'  -e /^#/d | grep -C 1 % | sed -e '/--/d' -e /^$/d > /home/pi/timidity_cfg/{sf2name}.cfg" .format(sf2name=list_difference[x])  ,shell=True)
 subprocess.call('sudo chown -R pi:pi /home/pi/timidity_cfg' ,shell=True)
if sf2[0] == "sf2_None":
   subprocess.call('sudo rm /home/pi/timidity_cfg/*.cfg' ,shell=True)
otg_mode = subprocess.check_output("lsmod | grep g_ |head -1| awk '{print $1}'" ,shell=True).decode('utf-8').strip().split('\n')
midiout = rtmidi.MidiOut()
midiout.open_virtual_port("Ysynth_out") # 仮想MIDI出力ポートの名前
time.sleep(1.0)
midiin = rtmidi.MidiIn()
midiin.open_virtual_port("Ysynth_in") # 仮想MIDI入力ポートの名前
midiin.ignore_types(sysex=False)
def allnoteoff():
    a = 0xb0
    while (a < 0xbf ):
        midiout.send_message([a, 0x78, 0x00])
        a += 1
so1602.command(clear)
subprocess.call('amixer cset numid=1 90% > /dev/null', shell=True)
##初期設定ここまで##
if rock_flag == 0:
   so1602.write('CH:'+str("{0:02}".format(midiCH + 1))+"     ")
   so1602.command(OLED_2ndline)
   so1602.write('PC:'+str("{0:03d}".format(midiPROG[midiCH] + 1))+"     ")
   subprocess.call("sh /home/pi/Ysynth/midiconnect.sh" , shell = True)
if rock_flag == 1:
   so1602.command(OLED_1stline)
   so1602.write("SF2:     ")
   so1602.command(OLED_2ndline)
   so1602.write(str("{0:02}" .format(sf2counter + 1))+":"+sf2[sf2counter])
timer = time.time()
msg = 0
while True:
##MIDI入力をディスプレイに反映する処理
    if rock_flag == 0:
       msg = midiin.get_message()
    if msg and rock_flag == 0:
       message, deltatime = msg
       timer += deltatime
       try:
        if message == ([240, 65, 16, 66, 18, 64, 0, 127, 0, 65, 247]) or message ==( [240, 67, 16, 76, 0, 0, 126, 0, 247]) or message == ([240, 126, 127, 9, 1, 247]) or message == ([240, 126, 127, 9, 3, 247]) :
           midiPROG= [0]*16
           midiCC7=  [100]*16
           midiCC11=  [127]*16
           midiCC10=  [64]*16
           midiCC1=  [0]*16
           midiCC91=  [40]*16
           midiCC93=  [0]*16
           midiCC94=  [0]*16
           pb1 = [0]*16
           pb2 = [0x40]*16
           if mode == 0:
              so1602.command(OLED_2ndline)
              so1602.write('PC:'+str("{0:03d}".format(midiPROG[midiCH] + 1))+"     ")
           if mode == 1:
              so1602.command(OLED_1stline)
              so1602.write('Vol:'+str("{0:03d}".format(midiCC7[midiCH]))+"     ")
              so1602.command(OLED_2ndline)
              so1602.write('Exp:'+str("{0:03d}".format(midiCC11[midiCH]))+"     ")
           if mode == 2:
              so1602.command(OLED_1stline)
              so1602.write('Pan:'+str("{0:03d}".format(midiCC10[midiCH]-64))+"     ")
              so1602.command(OLED_2ndline)
              so1602.write('Mod:'+str("{0:03d}".format(midiCC1[midiCH]))+"     ")
           if mode == 3:
              so1602.command(OLED_1stline)
              so1602.write('Rev:'+str("{0:03d}".format(midiCC91[midiCH]))+"     ")
              so1602.command(OLED_2ndline)
              so1602.write('Cho:'+str("{0:03d}".format(midiCC93[midiCH]))+"     ")
           if mode == 4:
              so1602.command(OLED_1stline)
              so1602.write('Dly:'+str("{0:03d}".format(midiCC94[midiCH]))+"     ")
              so1602.command(OLED_2ndline)
              so1602.write('P.Bend:'+str("{0:04d}".format(0x80*pb2[midiCH]+pb1[midiCH]-8192))+"     ")
       except :
        continue
       for x in range(16):
        if message[0] == 192+x :
           midiPROG[x] = message[1]
           if mode == 0:
              so1602.command(OLED_2ndline)
              so1602.write('PC:'+str("{0:03d}".format(midiPROG[midiCH] + 1))+"     ")
        if message[0] == 176+x and message[1] ==7:
           midiCC7[x] = message[2]
           if mode == 1:
              so1602.command(OLED_1stline)
              so1602.write('Vol:'+str("{0:03d}".format(midiCC7[midiCH]))+"     ")
        if message[0] == 176+x and message[1] ==11:
           midiCC11[x] = message[2]
           if mode == 1:
              so1602.command(OLED_2ndline)
              so1602.write('Exp:'+str("{0:03d}".format(midiCC11[midiCH]))+"     ")
        if message[0] == 176+x and message[1] ==10:
           midiCC10[x] = message[2]
           if mode == 2:
              so1602.command(OLED_1stline)
              so1602.write('Pan:'+str("{0:03d}".format(midiCC10[midiCH]-64))+"     ")
        if message[0] == 176+x and message[1] ==1:
           midiCC1[x] = message[2]
           if mode == 2:
              so1602.command(OLED_2ndline)
              so1602.write('Mod:'+str("{0:03d}".format(midiCC1[midiCH]))+"     ")
        if message[0] == 176+x and message[1] ==91:
           midiCC91[x] = message[2]
           if mode == 3:
              so1602.command(OLED_1stline)
              so1602.write('Rev:'+str("{0:03d}".format(midiCC91[midiCH]))+"     ")
        if message[0] == 176+x and message[1] ==93:
           midiCC93[x] = message[2]
           if mode == 3:
              so1602.command(OLED_2ndline)
              so1602.write('Cho:'+str("{0:03d}".format(midiCC93[midiCH]))+"     ")
        if message[0] == 176+x and message[1] ==94:
           midiCC94[x] = message[2]
           if mode == 4:
              so1602.command(OLED_1stline)
              so1602.write('Dly:'+str("{0:03d}".format(midiCC94[midiCH]))+"     ")
        if message[0] == 0xe0+x :
           pb1[x] = message[1]
           pb2[x] = message[2]
           if mode == 4:
              so1602.command(OLED_2ndline)
              so1602.write('P.Bend:'+str("{0:04d}".format(0x80*pb2[midiCH]+pb1[midiCH]-8192))+"     ")
##MIDI入力をディスプレイに反映する処理ここまで
##押しボタンスイッチの処理
    try:
     if aplaymidi.poll() is not None:
        if mode == 5 and playflag[midicounter] == 1:
           so1602.command(0x80+0x05)
           so1602.write(" ")
        playflag = [0]*len(midi)
    except:
     pass
    if GPIO.input(input_A) == 0:
       if 0 <=mode <=3 and rock_flag == 0:
          allnoteoff()
       if mode == 5 and rock_flag == 0 and midi[0] != "midi_None":
          if GPIO.input(input_A) == 0 and playflag[midicounter] == 0:
             subprocess.call(['sudo', 'killall', 'aplaymidi'])
             allnoteoff()
             so1602.command(0x80+0x05)
             so1602.write("▶")
             midi = [s.replace(' ', '\ ') for s in midi]
             aplaymidi = subprocess.Popen('aplaymidi -p 14:0 /mnt/g_mass_storage/midi/{}.mid' .format(midi[midicounter]), shell = True)
             midi = [s.replace('\ ', ' ') for s in midi]
             playflag = [0]*len(midi)
             playflag[midicounter] = 1
             while (GPIO.input(4) == 0):
                pass
          if GPIO.input(input_A) == 0 and playflag[midicounter] == 1:
             so1602.command(0x80+0x05)
             so1602.write(" ")
             allnoteoff()
             subprocess.call(['sudo', 'killall', 'aplaymidi'])
             allnoteoff()
             playflag = [0]*len(midi)
             while (GPIO.input(4) == 0):
                pass      
       if (mode == 6 or rock_flag == 1) :
          so1602.command(OLED_1stline)
          so1602.command(0x80+0x04)
          so1602.write("Wait..")
          subprocess.call(['sudo', 'killall', 'aplaymidi'])
          subprocess.call(['sudo', 'killall', 'timidity'])
          allnoteoff()
          so1602.command(OLED_1stline)
          so1602.command(0x80+0x04)
          sf2 = [s.replace(' ', '\ ') for s in sf2]
          subprocess.Popen('timidity -c /home/pi/timidity_cfg/{}.cfg' .format(sf2[sf2counter]), shell = True)
          sf2 = [s.replace('\ ', ' ') for s in sf2]
          time.sleep(1.5)
          subprocess.call("sh /home/pi/Ysynth/midiconnect01.sh" , shell = True)
          time.sleep(0.5)
          while (GPIO.input(4) == 0):
             pass
          so1602.write("OK    ")
          subprocess.call("sh /home/pi/Ysynth/midiconnect02.sh" , shell = True)
          time.sleep(2)
          sf2used = [0]*len(sf2)
          sf2used[sf2counter] = 1
          mode = 0
          midiCH = 0
          midiPROG=  [0]*16
          midiCC7=  [100]*16
          midiCC11=  [127]*16
          midiCC10=  [64]*16
          midiCC1=  [0]*16
          midiCC91=  [40]*16
          midiCC93=  [0]*16
          midiCC94=  [0]*16
          pb1 = [0]*16
          pb2 = [0x40]*16
          rock_flag = 0
          so1602.command(clear)
          so1602.command(OLED_1stline)
          so1602.write('CH:'+str("{0:02}".format(midiCH + 1))+"     ")
          so1602.command(OLED_2ndline)
          so1602.write('PC:'+str("{0:03d}".format(midiPROG[midiCH] + 1))+"     ")
       if mode == 7 and rock_flag == 0:
          so1602.command(OLED_2ndline)
          so1602.write("マタネ!")
          subprocess.call(['sudo', 'killall', 'timidity'])
          subprocess.call('amixer cset numid=1 90% > /dev/null', shell=True)
          time.sleep(3.0)
          so1602.command(clear)
          so1602.command(display_Off)
          subprocess.call(["sudo", "shutdown", "-h", "now"])
       if (mode == 8 and rock_flag == 0) or rock_flag == 2:
          if otg_mode[0] == 'g_midi':
             subprocess.call('sudo modprobe -r g_midi', shell=True)
             allnoteoff()
             subprocess.call(['sudo', 'killall', 'aplaymidi'])
             subprocess.call(['sudo', 'killall', 'timidity'])
             subprocess.call('sudo umount  /mnt/g_mass_storage/', shell=True)
             subprocess.call('sudo modprobe g_mass_storage removable=1 file=/home/pi/g_mass_storage.img', shell=True)
             otg_mode = subprocess.check_output("lsmod | grep g_ |head -1| awk '{print $1}'" ,shell=True).decode('utf-8').strip().split('\n')
             rock_flag = 2
             so1602.command(OLED_2ndline)
             so1602.write("mass_storage")
             while (GPIO.input(4) == 0):
                   pass
          if GPIO.input(4) == 0:
             if otg_mode[0] == 'g_mass_storage':
                subprocess.call('sudo modprobe -r g_mass_storage', shell=True)
                subprocess.call('sudo umount /mnt/g_mass_storage/', shell=True)
                so1602.command(OLED_2ndline)
                so1602.write("Ysynth_Restart")
                subprocess.call('sudo modprobe g_midi', shell=True)
                subprocess.call('sudo systemctl restart ysynth.service', shell=True)
##押しボタンスイッチの処理ここまで
##ロータリーエンコーダをループの処理
    prevolume = volume
    premode = mode
    preCC2 = CC2
    preCC1 = CC1
    rotaryDeal_1()
    rotaryDeal_2()
    rotaryDeal_3()
    rotaryDeal_4()
###ロータリーエンコーダ4の処理。Vol、モード関係なしで変化。
    if (prevolume != volume) and rock_flag == 0:
      if volume > 100:
         volume = 0
         #volume = 100
      if volume < 0:
         volume = 100
         #volume = 0
      subprocess.Popen(['amixer', 'cset', 'numid=1', '{}%'.format(volume)])
      if 7<=mode <= 8: #特定のモードでOLEDに表示
         so1602.command(OLED_2ndline)
         so1602.write("SystemVol:"+str("{0:02}".format(volume))+"   ")
###ロータリーエンコーダ4の処理ここまで
###ロータリーエンコーダ3の処理。右から2番目でモードチェンジ、モード関係なしで変化。
    if (premode != mode) and rock_flag == 0:
      so1602.command(clear)
      if mode > 8:
         mode = 0
      if mode < 0:
         mode = 8
      if mode == 0 and rock_flag == 0:
         so1602.command(OLED_1stline)
         so1602.write('CH:'+str("{0:02}".format(midiCH + 1))+"     ")
         so1602.command(OLED_2ndline)
         so1602.write('PC:'+str("{0:03d}".format(midiPROG[midiCH] + 1))+"     ")
      if mode == 1 and rock_flag == 0: 
         so1602.command(OLED_1stline)
         so1602.write('Vol:'+str("{0:03d}".format(midiCC7[midiCH]))+"     ")
         so1602.command(OLED_2ndline)
         so1602.write('Exp:'+str("{0:03d}".format(midiCC11[midiCH]))+"     ")
      if mode == 2 and rock_flag == 0:
         so1602.command(OLED_1stline)
         so1602.write('Pan:'+str("{0:03d}".format(midiCC10[midiCH]-64))+"     ")
         so1602.command(OLED_2ndline)
         so1602.write('Mod:'+str("{0:03d}".format(midiCC1[midiCH]))+"  ")
      if mode == 3 and rock_flag == 0:
         so1602.command(OLED_1stline)
         so1602.write('Rev:'+str("{0:03d}".format(midiCC91[midiCH]))+"     ")
         so1602.command(OLED_2ndline)
         so1602.write('Cho:'+str("{0:03d}".format(midiCC93[midiCH]))+"     ")
      if mode == 4 and rock_flag == 0:
         so1602.command(OLED_1stline)
         so1602.write('Dly:'+str("{0:03d}".format(midiCC94[midiCH]))+"     ")
         so1602.command(OLED_2ndline)
         so1602.write('P.Bend:'+str("{0:04d}".format(0x80*pb2[midiCH]+pb1[midiCH]-8192))+"     ")
      if mode == 5 and rock_flag == 0:
         so1602.command(OLED_1stline)
         so1602.write("MIDI:     ")
         if playflag[midicounter] == 1 and midi[0] != "midi_None":
            so1602.command(0x80+0x05)
            so1602.write("▶")
         if playflag[midicounter] == 0 and midi[0] != "midi_None":
            so1602.command(0x80+0x05)
            so1602.write(" ")
         so1602.command(OLED_2ndline)
         so1602.write(str("{0:02}" .format(midicounter + 1))+":"+midi[midicounter])
      if mode == 6 or rock_flag == 1:
         so1602.command(OLED_1stline)
         so1602.write("SF2:     ")
         if sf2used[sf2counter] == 1 and sf2[0] != "sf2_None":
            so1602.command(0x80+0x04)
            so1602.write("♪")
         if sf2used[sf2counter] == 0 and sf2[0] != "sf2_None":
            so1602.command(0x80+0x04)
            so1602.write(" ")
         so1602.command(OLED_2ndline)
         so1602.write(str("{0:02}" .format(sf2counter + 1))+":"+sf2[sf2counter])
      if mode == 7 and rock_flag == 0:
         so1602.command(OLED_1stline)
         so1602.write("シャットダウン_シマスカ?   ")
         so1602.command(OLED_2ndline)
         so1602.write("              ")
      if mode == 8 and rock_flag == 0:
         so1602.command(OLED_1stline)
         so1602.write("OTG_Mode_Change?        ")
         so1602.command(OLED_2ndline)
         so1602.write("              ")
###ロータリーエンコーダ3の処理ここまで
###ロータリーエンコーダ2の処理
    if (preCC2 != CC2):
      if mode == 0 and rock_flag == 0:
         if CC2 - preCC2 == 1 :
            midiPROG[midiCH] += 1
         if CC2 - preCC2 == -1 :
            midiPROG[midiCH] -= 1
         if midiPROG[midiCH] > 127:
            midiPROG[midiCH] = 0
         if midiPROG[midiCH] < 0:
            midiPROG[midiCH] = 127
         midiout.send_message([0xc0+midiCH, midiPROG[midiCH]])
         so1602.command(OLED_2ndline)
         so1602.write('PC:'+str("{0:03d}".format(midiPROG[midiCH] + 1))+"     ")
      if mode == 1 and rock_flag == 0:
         if CC2 - preCC2 == 1 :
            midiCC11[midiCH] += 1
         if CC2 - preCC2 == -1 :
            midiCC11[midiCH] -= 1
         if midiCC11[midiCH] > 127:
            midiCC11[midiCH] = 0
         if midiCC11[midiCH] < 0:
            midiCC11[midiCH] = 127
         midiout.send_message([0xb0+midiCH, 11, midiCC11[midiCH]])
         so1602.command(OLED_2ndline)
         so1602.write('Exp:'+str("{0:03d}".format(midiCC11[midiCH]))+"  ")
      if mode == 2 and rock_flag == 0:
         if CC2 - preCC2 == 1 :
            midiCC1[midiCH] += 1
         if CC2 - preCC2 == -1 :
            midiCC1[midiCH] -= 1
         if midiCC1[midiCH] > 127:
            midiCC1[midiCH] = 0
         if midiCC1[midiCH] < 0:
            midiCC1[midiCH] = 127
         midiout.send_message([0xb0+midiCH, 1, midiCC1[midiCH]])
         so1602.command(OLED_2ndline)
         so1602.write('Mod:'+str("{0:03d}".format(midiCC1[midiCH]))+"  ")
      if mode == 3 and rock_flag == 0:
         if CC2 - preCC2 == 1 :
            midiCC93[midiCH] += 1
         if CC2 - preCC2 == -1 :
            midiCC93[midiCH] -= 1
         if midiCC93[midiCH] > 127:
            midiCC93[midiCH] = 0
         if midiCC93[midiCH] < 0:
            midiCC93[midiCH] = 127
         midiout.send_message([0xb0+midiCH, 93, midiCC93[midiCH]])
         so1602.command(OLED_2ndline)
         so1602.write('Cho:'+str("{0:03d}".format(midiCC93[midiCH]))+"     ")

      if mode == 4 and rock_flag == 0:
         if CC2 - preCC2 == 1 :
            if pbcounter[midiCH] == 12:
               pbcounter[midiCH] = -12
            else:
               pbcounter[midiCH] += 1            
            #for x in range(1):
             #pb1[midiCH] += 1
             #if pb1[midiCH] > 0x7f:
                #pb1[midiCH] = 0
                #pb2[midiCH] += 1
                #if pb2[midiCH] > 0x7f:
                   #pb2[midiCH] = 0
         if CC2 - preCC2 == -1 :
            if pbcounter[midiCH] == -12:
               pbcounter[midiCH] = 12
            else:
               pbcounter[midiCH] -= 1      
            #for x in range(1):
             #pb1[midiCH] -= 1
             #if pb1[midiCH] < 0:
                #pb1[midiCH] = 0x7f
                #if pb2[midiCH] == 0:
                   #pb1[midiCH] = 0x7f
                   #pb2[midiCH] = 0x7f
                #else:
                   #pb2[midiCH] -= 1
         if pbcounter[midiCH] == -12:
            pb1[midiCH] = int(0x00)
            pb2[midiCH] = int(0x00)
         if pbcounter[midiCH] == -11:
            pb1[midiCH] = int(0x2b)
            pb2[midiCH] = int(0x05)
         if pbcounter[midiCH] == -10:
            pb1[midiCH] = int(0x55)
            pb2[midiCH] = int(0x0a)
         if pbcounter[midiCH] == -9:
            pb1[midiCH] = int(0x00)
            pb2[midiCH] = int(0x10)
         if pbcounter[midiCH] == -8:
            pb1[midiCH] = int(0x2b)
            pb2[midiCH] = int(0x15)
         if pbcounter[midiCH] == -7:
            pb1[midiCH] = int(0x55)
            pb2[midiCH] = int(0x1a)
         if pbcounter[midiCH] == -6:
            pb1[midiCH] = int(0x00)
            pb2[midiCH] = int(0x20)   
         if pbcounter[midiCH] == -5:
            pb1[midiCH] = int(0x2b)
            pb2[midiCH] = int(0x25) 
         if pbcounter[midiCH] == -4:
            pb1[midiCH] = int(0x55)
            pb2[midiCH] = int(0x2a)
         if pbcounter[midiCH] == -3:
            pb1[midiCH] = int(0x00)
            pb2[midiCH] = int(0x30)
         if pbcounter[midiCH] == -2:
            pb1[midiCH] = int(0x2b)
            pb2[midiCH] = int(0x35)   
         if pbcounter[midiCH] == -1:
            pb1[midiCH] = int(0x55)
            pb2[midiCH] = int(0x3a) 
         if pbcounter[midiCH] == 0:
            pb1[midiCH] = int(0x00)
            pb2[midiCH] = int(0x40)
         if pbcounter[midiCH] == 1:
            pb1[midiCH] = int(0x2b)
            pb2[midiCH] = int(0x45)
         if pbcounter[midiCH] == 2:
            pb1[midiCH] = int(0x55)
            pb2[midiCH] = int(0x4a)   
         if pbcounter[midiCH] == 3:
            pb1[midiCH] = int(0x00)
            pb2[midiCH] = int(0x50)
         if pbcounter[midiCH] == 4:
            pb1[midiCH] = int(0x2b)
            pb2[midiCH] = int(0x55)
         if pbcounter[midiCH] == 5:
            pb1[midiCH] = int(0x55)
            pb2[midiCH] = int(0x5a)
         if pbcounter[midiCH] == 6:
            pb1[midiCH] = int(0x00)
            pb2[midiCH] = int(0x60)  
         if pbcounter[midiCH] == 7:
            pb1[midiCH] = int(0x2b)
            pb2[midiCH] = int(0x65)
         if pbcounter[midiCH] == 8:
            pb1[midiCH] = int(0x55)
            pb2[midiCH] = int(0x6a)
         if pbcounter[midiCH] == 9:
            pb1[midiCH] = int(0x00)
            pb2[midiCH] = int(0x70)
         if pbcounter[midiCH] == 10:
            pb1[midiCH] = int(0x2b)
            pb2[midiCH] = int(0x75)  
         if pbcounter[midiCH] == 11:
            pb1[midiCH] = int(0x55)
            pb2[midiCH] = int(0x7a)
         if pbcounter[midiCH] == 12:
            pb1[midiCH] = int(0x7f)
            pb2[midiCH] = int(0x7f) 
         if GPIO.input(input_A) == 0:
            pb1 = [pb1[midiCH]]*16
            pb2 = [pb2[midiCH]]*16
            for x in range(16):
                midiout.send_message([0xb0+x, 0x65, 0x00])
                midiout.send_message([0xb0+x, 0x64, 0x00])
                midiout.send_message([0xb0+x, 0x06, 0x0c])
                midiout.send_message([0xb0+x, 0x26, 0x00])
                midiout.send_message([0xe0+x, pb1[x], pb2[x]])
         else:
            midiout.send_message([0xb0+midiCH, 0x65, 0x00])
            midiout.send_message([0xb0+midiCH, 0x64, 0x00])
            midiout.send_message([0xb0+midiCH, 0x06, 0x0c])
            midiout.send_message([0xb0+midiCH, 0x26, 0x00])
            midiout.send_message([0xe0+midiCH, pb1[midiCH], pb2[midiCH]])
         so1602.command(OLED_2ndline)
         so1602.write('P.Bend:'+str("{0:04d}".format(0x80*pb2[midiCH]+pb1[midiCH]-8192))+"     ")
      if mode == 5 and rock_flag == 0:
         if CC2 - preCC2 == 1 :
            midicounter += 1
         if CC2 - preCC2 == -1 :
            midicounter -= 1
         if midicounter == len(midi):
            midicounter = 0
         if midicounter == -1:
            midicounter =  len(midi)-1
         so1602.command(OLED_1stline)
         if playflag[midicounter] == 1 and midi[0] != "midi_None":
            so1602.command(0x80+0x05)
            so1602.write("▶")
         if playflag[midicounter] == 0 and midi[0] != "midi_None":
            so1602.command(0x80+0x05)
            so1602.write(" ")
         so1602.command(OLED_2ndline)
         so1602.write("                ")
         so1602.command(OLED_2ndline)
         so1602.write(str("{0:02}" .format(midicounter + 1))+":"+midi[midicounter])
      if mode == 6 or rock_flag == 1:
         if CC2 - preCC2 == 1 :
            sf2counter += 1
         if CC2 - preCC2 == -1 :
            sf2counter -= 1
         if sf2counter == len(sf2):
            sf2counter = 0
         if sf2counter == -1:
            sf2counter =  len(sf2) -1
         so1602.command(OLED_1stline)
         if sf2used[sf2counter] == 1 and sf2[0] != "sf2_None":
            so1602.command(0x80+0x04)
            so1602.write("♪")
         if sf2used[sf2counter] == 0 and sf2[0] != "sf2_None":
            so1602.command(0x80+0x04)
            so1602.write(" ")
         so1602.command(OLED_2ndline)
         so1602.write("                ")
         so1602.command(OLED_2ndline)
         so1602.write(str("{0:02}" .format(sf2counter + 1))+":"+sf2[sf2counter])
###ロータリーエンコーダ2の処理ここまで
###ロータリーエンコーダ1の処理
    if (preCC1 != CC1):
      if mode == 0 and rock_flag == 0:
         if CC1 - preCC1 == 1 :
            midiCH += 1
         if CC1 - preCC1 == -1 :
            midiCH -= 1
         if midiCH > 15:
            midiCH = 0
         if midiCH < 0:
            midiCH = 15
         so1602.command(OLED_1stline)
         so1602.write('CH:'+str("{0:02}".format(midiCH + 1))+"     ")
         so1602.command(OLED_2ndline)
         so1602.write('PC:'+str("{0:03d}".format(midiPROG[midiCH] + 1))+"     ")
      if mode == 1 and rock_flag == 0:
         if CC1 - preCC1 == 1 :
            midiCC7[midiCH] += 1
         if CC1 - preCC1 == -1 :
            midiCC7[midiCH] -= 1
         if midiCC7[midiCH] > 127:
            midiCC7[midiCH] = 0
         if midiCC7[midiCH] < 0:
            midiCC7[midiCH] = 127
         midiout.send_message([0xb0+midiCH, 7, midiCC7[midiCH]])
         so1602.command(OLED_1stline)
         so1602.write('Vol:'+str("{0:03d}".format(midiCC7[midiCH]))+"     ")
      if mode == 2 and rock_flag == 0:
         if CC1 - preCC1 == 1 :
            midiCC10[midiCH] += 1
         if CC1 - preCC1 == -1 :
            midiCC10[midiCH] -= 1
         if midiCC10[midiCH] > 127:
            midiCC10[midiCH] = 0
         if midiCC10[midiCH] < 0:
            midiCC10[midiCH] = 127
         midiout.send_message([0xb0+midiCH, 10, midiCC10[midiCH]])
         so1602.command(OLED_1stline)
         so1602.write('Pan:'+str("{0:03d}".format(midiCC10[midiCH]-64))+"     ")
      if mode == 3 and rock_flag == 0:
         if CC1 - preCC1 == 1 :
            midiCC91[midiCH] += 1
         if CC1 - preCC1 == -1 :
            midiCC91[midiCH] -= 1
         if midiCC91[midiCH] > 127:
            midiCC91[midiCH] = 0
         if midiCC91[midiCH] < 0:
            midiCC91[midiCH] = 127
         midiout.send_message([0xb0+midiCH, 91, midiCC91[midiCH]])
         so1602.command(OLED_1stline)
         so1602.write('Rev:'+str("{0:03d}".format(midiCC91[midiCH]))+"    ")
      if mode == 4 and rock_flag == 0:
         if CC1 - preCC1 == 1 :
            midiCC94[midiCH] += 1
         if CC1 - preCC1 == -1 :
            midiCC94[midiCH] -= 1
         if midiCC94[midiCH] > 127:
            midiCC94[midiCH] = 0
         if midiCC94[midiCH] < 0:
            midiCC94[midiCH] = 127
         midiout.send_message([0xb0+midiCH, 94, midiCC94[midiCH]])
         so1602.command(OLED_1stline)
         so1602.write('Dly:'+str("{0:03d}".format(midiCC94[midiCH]))+"     ")
###ロータリーエンコーダ1の処理ここまで
