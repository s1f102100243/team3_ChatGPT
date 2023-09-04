
  // HTTPでファイルを読み込む
  let xhr = new XMLHttpRequest(); 
  //取得するファイルの設定
   xhr.open("GET",'TestData.csv',true);
  //リクエストの要求送信
   xhr.send(null);
