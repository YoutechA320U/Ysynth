## Ysynth

RaspberryPiとTimidity++を核にしたハードウェアシンセサイザーです。GM/GS/XGのメッセージが使えます。

## 概要
RaspberryPiで動作するハードウェアシンセサイザーです

## 開発環境
    OS : Raspbian stretch Lite
    RaspberryPi : RaspberryPi ZeroWH,RaspberryPi 3B+
    Python : ver2.7 and ver3.5
    
## 回路図
作成中

## 必要な部品
※基板やピンソケット、つまみは除く

|部品名|型番など|数量|
|:---|:--:|---:|
|RaspberryPi|[RaspberryPiZeroWH](http://akizukidenshi.com/catalog/g/gM-12961/)|1|
|I2S接続オーディオDAC|[Pi-DAC+相当のDAC(Pi-DAC Zeroなど)](http://akizukidenshi.com/catalog/g/gM-13306/)|1|
|I2C接続16x2有機ELディスプレイ|[SO1602](http://akizukidenshi.com/catalog/g/gP-08277/)|1|
|ロータリーエンコーダ|[EC12E2420801](http://akizukidenshi.com/catalog/g/gP-06357/)|4|
|タクトスイッチ|[TVGP01-G73BBなど](http://akizukidenshi.com/catalog/g/gP-09826/)|1|
|小型スピーカー |[8Ω](http://akizukidenshi.com/catalog/g/gP-12587/)|1|
|アンプモジュール|[PAM8012使用2ワットD級アンプモジュール](http://akizukidenshi.com/catalog/g/gK-08217/)|1|
|半固定抵抗|[10kΩ](http://akizukidenshi.com/catalog/g/gP-03277/)|1|

## 必要なライブラリ
    rymidi smbus RPi.GPIO

## インストール方法
※OSはRaspbian stretch Lite前提です。インストールの時のみ、より高性能なRaspberryPi 3B+を使うことを強くおすすめします。

1.まず以下のコマンドを実行します。

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y git
    git clone https://github.com/YoutechA320U/Ysynth

2..何らかのエディタで`/boot/cmdline.txt`の末尾に改行せずに`modules-load=dwc2,g_midi`を追加します。

3.`cd /home/pi/Ysynth`でカレントディレクトリを`Ysynth`に移動します。

4.`sudo python setup.py`でセットアップスクリプトを実行します。完了すると自動的に再起動します。

5.有機ELディスプレイにメッセージが表示されたら完了です。

## 使い方
作成中

## 備考
作成中

### 参考コード・資料
作成中
## 履歴
    [2018/10/11] - リポジトリ立ち上げ
