
oauth2-proxy用にDNS名とTLS証明書を取得する


kubectl create ns oauth2-proxy

kubectl create -f op-service.yaml

kubectl create secret tls oauth2-proxy.tls \
  --cert=certs/oauth2-proxy.labo.local.crt \
  --key=certs/oauth2-proxy.labo.local.key \
  -n oauth2-proxy

kubectl apply -k .

