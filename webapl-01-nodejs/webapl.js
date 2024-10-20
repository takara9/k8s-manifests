// 模擬アプリケーション
//
const express = require('express')
const path = require('path');
const app = express()

var start = Date.now()

// 静的ファイルのルーティング
app.use(express.static(path.join(__dirname, 'public')));


// Livenessプローブのハンドラー
// 模擬障害として、起動から40秒を超えると、HTTP 500内部エラーを返します。
// 40秒までは、HTTP 200 OKを返します。
// つまり、40秒を超えると、Livenessプローブが失敗して、コンテナが再起動します。
//
app.get('/healthz', function(request, response) {
    var msec = Date.now() - start
    var code = 200
    /*
    if (msec > 40000 ) {
	code = 500
    }
    */
    console.log('GET /healthz ' + code)
    response.status(code).send('OK')
})

// Redinessプローブのハンドラー
// アプリケーションの初期化をシミュレーションして、
// 起動してから20秒経過後、HTTP 200を返します。 
// それまでは、HTTPS 200 OKを返します。
app.get('/ready', function(request, response) {
    var msec = Date.now() - start
    /*
    var code = 500
    if (msec > 20000 ) {
	code = 200
    }
    */
    code = 200
    console.log('GET /ready ' + code)
    response.status(code).send('OK')
})


// トップページ
app.get('/test', function(request, response) {
    console.log('GET /')
    response.send('Hello from Node.js')
})



// その他のリクエストに対する404エラー
//app.use((req, res) => {
//  res.sendStatus(404);
//});


// サーバーポート番号 TCP
app.listen(3000, () => {
  console.log('Running at Port 3000...');
});

