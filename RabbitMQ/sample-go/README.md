# RabbitMQの送信テスト


~~~
$ kubectl -n default get secret rmq-default-user -o jsonpath="{.data.username}" | base64 --decode;echo
default_user__D39UYlVnhe54QtlAPI

$ kubectl -n default get secret rmq-default-user -o jsonpath="{.data.password}" | base64 --decode;echo
NNs_aZqdatta0sc89WtEoP4QllKtDzeI
~~~


~~~
$ mkdir golib
$ export GOPATH=`pwd`/golib
$ go mod init rmq
$ go mod tidy
~~~

~~~
$ go run send.go
~~~

~~~
$ go run receive.go
~~



ゴールチンを使用したデータの受信

~~~
    /*
    forever := make(chan bool)
      go func() {
          for d := range msgs {
              log.Printf("Received a message: %s", d.Body)
          }
      }()
      log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
    <-forever
    */
~~~
