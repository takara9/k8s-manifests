# メモ

コンテナのビルドとデプロイ先が必要


kubectl create ns dex
kubectl create secret tls dex.labo.local.tls \
  --cert=certs/dex.labo.local.crt \
  --key=certs/dex.labo.local.key \
  -n dex
kubectl apply -k k8s



GitHub OAuth
Client ID: f0b88fbfc24a0b4e9395
Secret: 8fd4056adbfdd032f5ad605f2f8a7c34a26abf69

