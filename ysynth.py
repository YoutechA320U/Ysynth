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
so1602.setaddr(0x3c)
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
mode = 6
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
playflag = 0

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
syokai = 1
def rotaryDeal_1():
  global volume, Last_input_C_Status, Current_input_C_Status, syokai
  Last_input_C_Status = GPIO.input(input_C)
  flag1 = 0
  while (not GPIO.input(input_B)):
    Current_input_C_Status = GPIO.input(input_C)
    flag1 = 1
  if flag1 == 1:
    flag1 = 0
    if (Last_input_C_Status == 0) and (Current_input_C_Status == 1):
      volume = volume + 1
    if (Last_input_C_Status == 1) and (Current_input_C_Status == 0):
      volume = volume -1

def rotaryDeal_2():
  global mode, Last_input_E_Status, Current_input_E_Status, syokai
  Last_input_E_Status = GPIO.input(input_E)
  flag2 = 0
  while (not GPIO.input(input_D)):
    Current_input_E_Status = GPIO.input(input_E)
    flag2 = 1
  if flag2 == 1:
    flag2 = 0
    if (Last_input_E_Status == 0) and (Current_input_E_Status == 1):
      mode = mode + 1
    if (Last_input_E_Status == 1) and (Current_input_E_Status == 0):
      mode = mode -1

def rotaryDeal_3():
  global CC2, Last_input_G_Status, Current_input_G_Status, syokai
  Last_input_G_Status = GPIO.input(input_G)
  flag3 = 0
  while (not GPIO.input(input_F)):
    Current_input_G_Status = GPIO.input(input_G)
    flag3 = 1
  if flag3 == 1:
    flag3 = 0
    if (Last_input_G_Status == 0) and (Current_input_G_Status == 1):
      CC2 = CC2 + 1
    if (Last_input_G_Status == 1) and (Current_input_G_Status == 0):
      CC2 = CC2 -1

def rotaryDeal_4():
  global CC1, Last_input_I_Status, Current_input_I_Status, syokai
  Last_input_I_Status = GPIO.input(input_I)
  flag4 = 0
  while (not GPIO.input(input_H)):
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
midiquant = int(subprocess.check_output('ls -U1 /home/pi/midi/*.mid | wc -l' ,shell=True))
midi = subprocess.check_output('ls /home/pi/midi/*.mid' ,shell=True).decode('utf-8').strip().replace('/home/pi/midi/', '').replace('.mid', '').split('\n')
sf2quant = int(subprocess.check_output('ls -U1 /home/pi/timidity_cfg/*.cfg | wc -l' ,shell=True))
sf2 = subprocess.check_output('ls /home/pi/timidity_cfg/*.cfg' ,shell=True).decode('utf-8').strip().replace('/home/pi/timidity_cfg/', '').replace('.cfg', '').split('\n')
midiout = rtmidi.MidiOut()
midiout.open_virtual_port("Ysynth_out") # 仮想MIDIポートの名前
def GM1_System_ON():
        midiout.send_message([0xF0, 0x7E, 0x7F])
        midiout.send_message([0x09, 0x01, 0xF7])
def allnoteoff():
    a = 0xb0
    while (a < 0xbf ):
        midiout.send_message([a, 0x78, 0x00])
        a += 1
so1602.command(OLED_1stline)
so1602.write("     コンニチハ!")
so1602.command(OLED_2ndline)
so1602.write("     Ysynth")
time.sleep(4.0)
so1602.command(clear)
##初期設定ここまで##
so1602.command(OLED_1stline)
so1602.write("サウンドフォント:     ")
so1602.command(OLED_2ndline)
so1602.write(str("{0:02}" .format(sf2counter + 1))+":"+sf2[sf2counter])
msg = 0
timer = time.time()
while True:
    if syokai == 0:
       msg = midiin.get_message()
    if msg and syokai == 0:
       message, deltatime = msg
       timer += deltatime
       for x in range(16):
        if message[0] == 192+x :
           midiPROG[x] = message[1]
           if mode == 0:
              so1602.command(OLED_2ndline)
              so1602.write('インストゥルメント:'+str("{0:03d}".format(midiPROG[midiCH] + 1))+"     ")
       for x in range(16):
        if message[0] == 176+x and message[1] ==7:
           midiCC7[x] = message[2]
           if mode == 1:
              so1602.command(OLED_1stline)
              so1602.write('ボリューム:'+str("{0:03d}".format(midiCC7[midiCH]))+"     ")
       for x in range(16):
        if message[0] == 176+x and message[1] ==11:
           midiCC11[x] = message[2]
           if mode == 1:
              so1602.command(OLED_2ndline)
              so1602.write('エクスプレッション:'+str("{0:03d}".format(midiCC11[midiCH]))+"     ")
       for x in range(16):
        if message[0] == 176+x and message[1] ==10:
           midiCC10[x] = message[2]
           if mode == 2:
              so1602.command(OLED_1stline)
              so1602.write('パン:'+str("{0:03d}".format(midiCC10[midiCH]-64))+"     ")
       for x in range(16):
        if message[0] == 176+x and message[1] ==1:
           midiCC1[x] = message[2]
           if mode == 2:
              so1602.command(OLED_2ndline)
              so1602.write('モジュレーション:'+str("{0:03d}".format(midiCC1[midiCH]))+"     ")
       for x in range(16):
        if message[0] == 176+x and message[1] ==91:
           midiCC91[x] = message[2]
           if mode == 3:
              so1602.command(OLED_1stline)
              so1602.write('リバーブ:'+str("{0:03d}".format(midiCC91[midiCH]))+"     ")
       for x in range(16):
        if message[0] == 176+x and message[1] ==93:
           midiCC93[x] = message[2]
           if mode == 3:
              so1602.command(OLED_2ndline)
              so1602.write('コーラス:'+str("{0:03d}".format(midiCC93[midiCH]))+"     ")
       for x in range(16):
        if message[0] == 176+x and message[1] ==94:
           midiCC94[x] = message[2]
           if mode == 4:
              so1602.command(OLED_1stline)
              so1602.write('ディレイ:'+str("{0:03d}".format(midiCC94[midiCH]))+"     ")
       for x in range(16):
        if message[0] == 0xe0+x :
           pb1[x] = message[1]
           pb2[x] = message[2]
           if mode == 4:
              so1602.command(OLED_2ndline)
              so1602.write('ピッチベンド:'+str("{0:04d}".format(0x80*pb2[midiCH]+pb1[midiCH]-8192))+"     ")
       #print (message)
    if GPIO.input(4) == 0:
       if mode == 0 :
          allnoteoff()
       if mode == 5 and playflag == 0 and syokai == 0 :
          playmidi = midi[midicounter]
          subprocess.call(['sudo', 'killall', 'aplaymidi'])
          allnoteoff()
          so1602.command(0x80+0x05)
          so1602.write("サイセイ")
          subprocess.Popen('aplaymidi -p 129:0 /home/pi/midi/{}.mid' .format(playmidi), shell = True)
          playflag = 1
          while (GPIO.input(4) == 0):
             pass
       if GPIO.input(4) == 0 and mode == 5 and playflag == 1 and syokai == 0: 
          so1602.command(0x80+0x05)
          so1602.write("テイシ ")
          allnoteoff()
          subprocess.call(['sudo', 'killall', 'aplaymidi'])
          allnoteoff()
          playflag = 0
          while (GPIO.input(4) == 0):
             pass

       if mode == 6 or syokai == 1:
          timidity_cfg = sf2[sf2counter]
          subprocess.call(['sudo', 'killall', 'aplaymidi'])
          subprocess.call(['sudo', 'killall', 'timidity'])
          allnoteoff()
          so1602.command(OLED_1stline)
          so1602.command(0x80+0x0a)
          subprocess.Popen('timidity -c /home/pi/timidity_cfg/{}.cfg' .format(timidity_cfg), shell = True)
          time.sleep(1.5)
          subprocess.call("sh /home/pi/Ysynth/midiconnect.sh" , shell = True)
          so1602.write("OK")
          time.sleep(2.0)
          while (GPIO.input(4) == 0):
             pass
          if syokai == 1:
             midiin = rtmidi.MidiIn()
             midiin.open_virtual_port("Ysynth_in") # 仮想MIDIポートの名前
             midiin.ignore_types(sysex=False, timing=False, active_sense=False)
             syokai = 0
          time.sleep(1)
          subprocess.call(['aconnect', '20:0', '130:0'])
          subprocess.call(['aconnect', '24:0', '130:0'])
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
          so1602.command(clear)
          so1602.command(OLED_1stline)
          so1602.write('チャンネル:'+str("{0:02}".format(midiCH + 1))+"     ")
          so1602.command(OLED_2ndline)
          so1602.write('インストゥルメント:'+str("{0:03d}".format(midiPROG[midiCH] + 1))+"     ")
       if mode == 7 and syokai == 0:
          so1602.command(OLED_2ndline)
          so1602.write("マタネ!")
          subprocess.call(['sudo', 'killall', 'timidity'])
          subprocess.call('amixer cset numid=1 90% > /dev/null', shell=True)
          time.sleep(3.0)
          so1602.command(clear)
          so1602.command(display_Off)
          subprocess.call(["sudo", "shutdown", "-h", "now"])
       if mode == 8 and syokai == 0:
          so1602.command(OLED_2ndline)
          so1602.write("Reload")
          time.sleep(3.0)
          so1602.command(clear)
          so1602.command(display_Off)
          subprocess.call('sudo systemctl restart ysynth.service', shell=True)
#ロータリーエンコーダをループで処理
    prevolume = volume
    premode = mode
    preCC2 = CC2
    preCC1 = CC1
    rotaryDeal_1()
    rotaryDeal_2()
    rotaryDeal_3()
    rotaryDeal_4()
#右から1番目でボリューム、モード関係なしで変化。
    if (prevolume != volume):
      if volume >= 101:
         volume = 100
      if volume <= 0:
         volume = 0
      subprocess.call('amixer cset numid=1 {}% > /dev/null' .format(volume), shell = True)
      if mode == 5 or mode == 6 or mode == 7 : #特定のモードでOLEDに表示
         so1602.command(OLED_2ndline)
         so1602.write("システムボリューム:"+str("{0:02}".format(volume))+"   ")

#右から2番目でモードチェンジ、モード関係なしで変化。
    if (premode != mode) and syokai == 0:
      so1602.command(clear)
      if mode > 8:
         mode = 0
      if mode < 0:
         mode = 8
      if mode == 0 and syokai == 0:
         so1602.command(OLED_1stline)
         so1602.write('チャンネル:'+str("{0:02}".format(midiCH + 1))+"     ")
         so1602.command(OLED_2ndline)
         so1602.write('インストゥルメント:'+str("{0:03d}".format(midiPROG[midiCH] + 1))+"     ")
      if mode == 1 and syokai == 0: 
         so1602.command(OLED_1stline)
         so1602.write('ボリューム:'+str("{0:03d}".format(midiCC7[midiCH]))+"     ")
         so1602.command(OLED_2ndline)
         so1602.write('エクスプレッション:'+str("{0:03d}".format(midiCC11[midiCH]))+"     ")
      if mode == 2 and syokai == 0:
         so1602.command(OLED_1stline)
         so1602.write('パン:'+str("{0:03d}".format(midiCC10[midiCH]-64))+"     ")
         so1602.command(OLED_2ndline)
         so1602.write('モジュレーション:'+str("{0:03d}".format(midiCC1[midiCH]))+"  ")
      if mode == 3 and syokai == 0:
         so1602.command(OLED_1stline)
         so1602.write('リバーブ:'+str("{0:03d}".format(midiCC91[midiCH]))+"     ")
         so1602.command(OLED_2ndline)
         so1602.write('コーラス:'+str("{0:03d}".format(midiCC93[midiCH]))+"     ")
      if mode == 4 and syokai == 0:
         so1602.command(OLED_1stline)
         so1602.write('ディレイ:'+str("{0:03d}".format(midiCC94[midiCH]))+"     ")
         so1602.command(OLED_2ndline)
         so1602.write('ピッチベンド:'+str("{0:04d}".format(0x80*pb2[midiCH]+pb1[midiCH]-8192))+"     ")
      if mode == 5 and syokai == 0:
         so1602.command(OLED_1stline)
         so1602.write("MIDI:     ")
         so1602.command(OLED_2ndline)
         so1602.write(str("{0:02}" .format(midicounter + 1))+":"+midi[midicounter])
      if mode == 6 or syokai == 1:
         so1602.command(OLED_1stline)
         so1602.write("サウンドフォント:     ")
         so1602.command(OLED_2ndline)
         so1602.write(str("{0:02}" .format(sf2counter + 1))+":"+sf2[sf2counter])
      if mode == 7 and syokai == 0:
         so1602.command(OLED_1stline)
         so1602.write("シャットダウン_シマスカ?   ")
         so1602.command(OLED_2ndline)
         so1602.write("              ")
      if mode == 8 and syokai == 0:
         so1602.command(OLED_1stline)
         so1602.write("リロード_シマスカ?        ")
         so1602.command(OLED_2ndline)
         so1602.write("              ")
###ロータリーエンコーダ2
    if (preCC2 != CC2):
      if mode == 0 and syokai == 0:
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
         so1602.write('インストゥルメント:'+str("{0:03d}".format(midiPROG[midiCH] + 1))+"     ")
      if mode == 1 and syokai == 0:
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
         so1602.write('エクスプレッション:'+str("{0:03d}".format(midiCC11[midiCH]))+"  ")
      if mode == 2 and syokai == 0:
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
         so1602.write('モジュレーション:'+str("{0:03d}".format(midiCC1[midiCH]))+"  ")
      if mode == 3 and syokai == 0:
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
         so1602.write('コーラス:'+str("{0:03d}".format(midiCC93[midiCH]))+"     ")

      if mode == 4 and syokai == 0:
         if CC2 - preCC2 == 1 :
            for x in range(1):
             pb1[midiCH] += 1
             if pb1[midiCH] > 0x7f:
                pb1[midiCH] = 0
                pb2[midiCH] += 1
                if pb2[midiCH] > 0x7f:
                   pb2[midiCH] = 0
         if CC2 - preCC2 == -1 :
            for x in range(1):
             pb1[midiCH] -= 1
             if pb1[midiCH] < 0:
                pb1[midiCH] = 0x7f
                if pb2[midiCH] == 0:
                   pb1[midiCH] = 0x7f
                   pb2[midiCH] = 0x7f
                else:
                   pb2[midiCH] -= 1
         midiout.send_message([0xe0+midiCH, pb1[midiCH], pb2[midiCH]])
         so1602.command(OLED_2ndline)
         so1602.write('ピッチベンド:'+str("{0:04d}".format(0x80*pb2[midiCH]+pb1[midiCH]-8192))+"     ")
      if mode == 5 and syokai == 0:
         if CC2 - preCC2 == 1 :
            midicounter += 1
            playflag = 0
         if CC2 - preCC2 == -1 :
            midicounter -= 1
            playflag = 0
         if midicounter == midiquant:
            midicounter = 0
         if midicounter == -1:
            midicounter =  midiquant-1
         so1602.command(OLED_1stline)
         so1602.command(clear)
         so1602.write("MIDI:     ")
         so1602.command(OLED_2ndline)
         so1602.write(str("{0:02}" .format(midicounter + 1))+":"+midi[midicounter])
      if mode == 6 or syokai == 1:
         if CC2 - preCC2 == 1 :
            sf2counter += 1
         if CC2 - preCC2 == -1 :
            sf2counter -= 1
         if sf2counter == sf2quant:
            sf2counter = 0
         if sf2counter == -1:
            sf2counter =  sf2quant-1
         so1602.command(OLED_1stline)
         so1602.write("サウンドフォント:     ")
         so1602.command(OLED_2ndline)
         so1602.write(str("{0:02}" .format(sf2counter + 1))+":"+sf2[sf2counter]+"          ")
###ロータリーエンコーダ1
    if (preCC1 != CC1):
      if mode == 0 and syokai == 0:
         if CC1 - preCC1 == 1 :
            midiCH += 1
         if CC1 - preCC1 == -1 :
            midiCH -= 1
         if midiCH > 15:
            midiCH = 0
         if midiCH < 0:
            midiCH = 15
         so1602.command(OLED_1stline)
         so1602.write('チャンネル:'+str("{0:02}".format(midiCH + 1))+"     ")
         so1602.command(OLED_2ndline)
         so1602.write('インストゥルメント:'+str("{0:03d}".format(midiPROG[midiCH] + 1))+"     ")
      if mode == 1 and syokai == 0:
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
         so1602.write('ボリューム:'+str("{0:03d}".format(midiCC7[midiCH]))+"     ")
      if mode == 2 and syokai == 0:
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
         so1602.write('パン:'+str("{0:03d}".format(midiCC10[midiCH]-64))+"     ")
      if mode == 3 and syokai == 0:
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
         so1602.write('リバーブ:'+str("{0:03d}".format(midiCC91[midiCH]))+"    ")
      if mode == 4 and syokai == 0:
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
         so1602.write('ディレイ:'+str("{0:03d}".format(midiCC94[midiCH]))+"     ")