package main

import (
    "log"
    "fmt"
    "os"
    amqp "github.com/rabbitmq/amqp091-go"
)

func failOnError(err error, msg string) {
	if err != nil {
		log.Panicf("%s: %s", msg, err)
	}
}

func main() {
    var message string   // 送信メッセージ

    // RabbitMQとの接続
    var rabbitmq_url string
    rabbitmq_url = "amqp://" + os.Args[1] + ":" + os.Args[2] + "@" + os.Args[3]
    conn, err := amqp.Dial( rabbitmq_url)
    failOnError(err, "Failed to connect to RabbitMQ")
    defer conn.Close()

    // チャネル確立
    ch, err := conn.Channel()
    failOnError(err, "Failed to open a channel")
    defer ch.Close()

    // キュー宣言 キュー名 hello
    q, err := ch.QueueDeclare(
        "hello", // name
	false,   // durable
	false,   // delete when unused
	false,   // exclusive
	false,   // no-wait
	nil,     // arguments
    )
    failOnError(err, "Failed to declare a queue")

    // メッセージインプットと送信ループ
    for {
        print("> ")
        fmt.Scan(&message)
        err = ch.Publish(
            "",     // exchange
            q.Name, // routing key
            false,  // mandatory
            false,  // immediate
            amqp.Publishing{
            ContentType: "text/plain",
            Body:        []byte(message),
        })
        failOnError(err, "Failed to publish a message")
        log.Printf(" [x] Sent %s\n", message)
    }
}
