# article_ID_TROPOMI
TROPOMIのSO2データの解析から地図上にプロット（描画）するコードの解説をしています。


### 元の記事

## 構成
- NISHINOSHIMA_Plot.ipynb
    - TROPOMIのSO2データの解析から地図上に描画するコードです。
- conv_NC4files.ipybn
    - 読み込んだ.ncファイルのlongitude、latitude、qa_value、time_secなどを抽出する関数が書かれています。
    - ファイル内のconv_s5p_csv関数は、プロットするためにカラムの体裁を整える関数です。
    - longitude、latitude、qa_value、time_secなどのカラムがプロットに必要なカラムです。
    - この関数で処理されたデータをcsv形式で出力します。
    
## 注意点
- このコードはanacondaのインストールが必須です。
- TROPOMIのデータは下記のURLからダウンロードできます。
-  https://disc.gsfc.nasa.gov/earthdata-login
-　データをダウンロードする際は、アカウントの登録が必要です。

## ライセンス、利用規約

## 貢献方法
プルリクエストや Issue はいつでも歓迎します。
