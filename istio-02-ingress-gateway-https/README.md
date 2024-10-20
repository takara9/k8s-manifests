# Istio Gateway のTLS利用

HTTPS(TLS)暗号化通信の設定を実施する。

参考資料
[1] Secure Gateways, https://istio.io/latest/docs/tasks/traffic-management/ingress/secure-ingress/




プライベート認証局証明書作成
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -subj '/O=labo. /CN=labo.local' -keyout labo.local.key -out labo.local.crt

サーバー証明要求
openssl req -out httpbin.labo.local.csr -newkey rsa:2048 -nodes -keyout httpbin.labo.local.key -subj "/CN=istio-ingressgateway.istio-system.k8s1.labo.local/O=httpbin organization"

認証局署名
openssl x509 -req -days 365 -CA labo.local.crt -CAkey labo.local.key -set_serial 0 -in httpbin.labo.local.csr -out httpbin.labo.local.crt

シークレット作成
kubectl create -n istio-system secret tls httpbin-credential --key=httpbin.labo.local.key --cert=httpbin.labo.local.crt

アプリデプロイ
kubectl apply -f httpbin.yaml

Istio GW,VS のデプロイ
kubectl apply -f istio-gwvs.yaml




テスト（プライベートCA証明書付き)
curl -v https://istio-ingressgateway.istio-system.k8s1.labo.local/delay/2 --cacert labo.local.crt


テスト（CA証明書なし）
curl -k -v https://istio-ingressgateway.istio-system.k8s1.labs.local/delay/2



