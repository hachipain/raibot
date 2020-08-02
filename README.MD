# 雑談linebot
自然言語処理API「catplus」使用、AWS lambdaデプロイ  


####環境変数設定必須
LINE_CHANNEL_SECRET  
LINE_CHANNEL_ACCESS_TOKEN  
CHAPLUS_API_KEY  

####デプロイ方法
zip圧縮したファイルをAWS lambdaにアップロードしてデプロイ  
`zip -r line-bot-rai .`