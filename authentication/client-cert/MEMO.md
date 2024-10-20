# 証明書作成によるユーザー管理

このKubernetesのCAで署名されたデジタル証明書とキーをkubeconfigに設定して
CNで指定したユーザー名のRBAC設定で、ユーザー認証と認可が可能になる。

~~~
$ openssl x509 -in user001.crt -noout -text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            11:49:02:69:00:ed:17:bd:56:44:d6:21:34:f2:fa:c5
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN = kubernetes
        Validity
            Not Before: Jun 25 07:22:56 2022 GMT
            Not After : Jun 26 07:22:56 2022 GMT
        Subject: C = AU, ST = Some-State, O = system:authenticated, CN = user001
        Subject Public Key Info:
~~~

