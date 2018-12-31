## Ysynth

RaspberryPiとTimidity++を核にしたハードウェアシンセサイザーです。GM/GS/エクスクルーシブのメッセージが使えます。

## 概要
RaspberryPi Zeroで動作するハードウェアシンセサイザーです。チャンネルごとにデータを送信、OLEDに表示するMIDIコントローラとしての機能と、チャンネルごとにデータを受信、OLEDに表示し、任意のサウンドフォント(.sf2)を鳴らせるMIDI音源としての機能、任意のMIDIファイルを自身や外部音源で演奏できるMIDIシーケンサとしての機能を持ちます。

## スペック
    ※GM/GS/エクスクルーシブメッセージ対応
    パート数:16
    最大同時発音数:64
    音源:サウンドフォント(.sf2)※任意ファイルを追加可能
    サンプリングレート:32000Hz
    本体でコントロールできるコントロールチェンジ:
    ディスプレイ:16x2有機ELディスプレイ
    接続端子:microUSBTypeB-MIDI端子(OTG接続可)、3.5mmオーディオ出力端子、スピーカーアンプ(1W級)
    電源:DC5V1A(RaspberryPiのmicroUSBTypeB)

## 開発環境
    OS : Raspbian stretch Lite
    RaspberryPi : RaspberryPi ZeroWH,RaspberryPi 3B+
    Python : ver2.7 and ver3.5
    
## 回路図
![SS](https://github.com/YoutechA320U/Ysynth/blob/master/Ysynth.png "回路図")

## 必要な部品
※基板やピンソケット、つまみは除く

|部品名|型番など|数量|
|:---|:--:|---:|
|RaspberryPi|[RaspberryPiZeroWH](http://akizukidenshi.com/catalog/g/gM-12961/)|1|
|I2S接続オーディオDAC|Pi-DAC+相当のDAC[(Pi-DAC Zeroなど)](http://akizukidenshi.com/catalog/g/gM-13306/)|1|
|I2C接続16x2有機ELディスプレイ|[SO1602](http://akizukidenshi.com/catalog/g/gP-08277/)|1|
|ロータリーエンコーダ|[EC12E2420801](http://akizukidenshi.com/catalog/g/gP-06357/)|4|
|タクトスイッチ|[TVGP01-G73BBなど](http://akizukidenshi.com/catalog/g/gP-09826/)|1|
|小型スピーカー |[8Ω](http://akizukidenshi.com/catalog/g/gP-12587/)|1|
|アンプモジュール|[PAM8012使用2ワットD級アンプモジュール](http://akizukidenshi.com/catalog/g/gK-08217/)|1|
|半固定抵抗|[10kΩ](http://akizukidenshi.com/catalog/g/gP-03277/)|1|
|ミニジャック|[3.5mmステレオ](http://akizukidenshi.com/catalog/g/gC-08958/)|1|
## インストール方法
※OSはRaspbian stretch Lite前提です。インストールの時のみ、より高性能なRaspberryPi 3B+を使うことを強くおすすめします。

1.まず以下のコマンドを実行します。

    sudo apt-get update
    sudo apt-get upgrade -y
    sudo apt-get install -y git
    git clone https://github.com/YoutechA320U/Ysynth.git

2.何らかのエディタで`/boot/cmdline.txt`の末尾に改行せずに`modules-load=dwc2,g_midi`を追加します。

3.`cd /home/pi/Ysynth`でカレントディレクトリを`Ysynth`に移動します。

4.`sudo python setup.py`でセットアップスクリプトを実行します。完了すると自動的に再起動します。

5.有機ELディスプレイにメッセージが表示されたら完了です。

## 使い方
作成中

## 備考
作成中

### 参考コード・資料
 * <http://artteknika.hatenablog.com/entry/2017/04/28/185444>  
 * <https://hawksnowlog.blogspot.com/2017/01/raspberrypi-with-rotaryencoder-python.html>
 * <https://www.denshi.club/pc/raspi/i2caqmlcdarduinode1-aqm0802-3.html>  
 * <https://github.com/SpotlightKid/python-rtmidi>  
## 履歴
    [2018/10/11] - リポジトリ立ち上げ
