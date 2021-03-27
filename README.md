# article_ID_TROPOMI
TROPOMIのSO2データの解析から地図上にプロット（描画）するコードの解説をしています。


### 元の記事

## 構成
- NISHINOSHIMA_Plot.ipynb
    - TROPOMIのSO2データの解析から地図上に描画するコードです。
- conv_NC4files.py
    - 読み込んだ.ncファイルのlongitude、latitude、qa_value、time_secなどを抽出する関数が書かれています。
    - ファイル内のconv_s5p_csv関数は、プロットするためにカラムの体裁を整える関数です。
    - longitude、latitude、qa_value、time_secなどのカラムがプロットに必要なカラムです。
    - この関数で処理されたデータをcsv形式で出力します。
    
## 注意点
- このコードはanacondaのインストールが必須です。
- TROPOMIのデータは下記のURLからダウンロードできます。
-  https://disc.gsfc.nasa.gov/earthdata-login
-　データをダウンロードする際は、アカウントの登録が必要です。
- Sentinel5P衛星が西之島上空を通過する時間帯はUTC02：00-04：00頃です。
- 例）S5P_OFFL_L2__SO2____20200101T023416_20200101T041546_11488_01_010107_20200103T041459.nc
- 上記の例のようにT以降が02から始まるファイルを取得してください。T以降はUTC02時34分16秒を意味しています。

## ライセンス、利用規約

## 貢献方法
プルリクエストや Issue はいつでも歓迎します。
