package main

import (
    "log"
    "os"
    amqp "github.com/rabbitmq/amqp091-go"
    //"github.com/davecgh/go-spew/spew"    // デバック用
)

func failOnError(err error, msg string) {
    if err != nil {
        log.Panicf("%s: %s", msg, err)
    }
}

func main() {

    // RabbitMQと接続
    var rabbitmq_url string
    rabbitmq_url = "amqp://" + os.Args[1] + ":" + os.Args[2] + "@" + os.Args[3]
    conn, err := amqp.Dial( rabbitmq_url)
    failOnError(err, "Failed to connect to RabbitMQ")
    defer conn.Close()

    // チャネルを開く
    ch, err := conn.Channel()
    failOnError(err, "Failed to open a channel")
    defer ch.Close()

    // キューを定義
    q, err := ch.QueueDeclare(
     	 "hello", // name
	  false,   // durable
  	  false,   // delete when unused
	  false,   // exclusive
	  false,   // no-wait
	  nil,     // arguments
    )
    failOnError(err, "Failed to declare a queue")

    // メッセージの受信設定
    msgs, err := ch.Consume(
          q.Name, // queue
          "",     // consumer
          true,   // auto-ack
          false,  // exclusive
          false,  // no-local
          false,  // no-wait
          nil,    // args
    )
    failOnError(err, "Failed to register a consumer")

    // メッセージ受信ループ
    //for d := range msgs {
    //    log.Printf("Received a message: %s", d.Body)
	//spew.Dump(d)
    //}

    forever := make(chan bool)
      go func() {
          for d := range msgs {
              log.Printf("Received a message: %s", d.Body)
          }
      }()
      log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
    <-forever


}
