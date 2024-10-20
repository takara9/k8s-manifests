# 起動方法


セッションストアにRedisを利用するケース
./oauth2-proxy --config=oauth2-proxy-github.cfg --redis-connection-url=redis://127.0.0.1:6379 --session-store-type=redis


セッションにクッキーを使うケース
./oauth2-proxy --config=oauth2-proxy-github.cfg


