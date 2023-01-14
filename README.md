# jpgXyuv.exe v0.1.0.0
本プログラムはJPEG形式のファイルを任意のYUV形式ファイルに一括変換するプログラムです

配布されているファイルは現時点でWindows 10のみの対応です

ダウンロードはこちらの[リンク](https://github.com/7ra4no/jpgXyuv/releases)より

Assetsのプルダウンより`jpgXyuv.zip`をダウンロードしてください

注意事項をよく読んでご利用ください

## 使い方
1. 変換対象のJPEG形式ファイルを`image_original`ディレクトリに移動
2. 変換したいYUV形式が記述されている`bat`形式ファイルを実行
3. 指定のYUV形式に変更されたファイルが`image_yuv`ディレクトリに書き出される

## 機能
#### 入力 :
* JPEG(RGB888)
#### 出力:
* YUV444 (4:4:4)
* YUV422 (4:2:2)
* YUV420 (4:2:0)
* YUV400 (4:0:0)

YUV440，YUV411，YUV410については開発中のため使用不可
