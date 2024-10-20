package com.example.servingwebcontent;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.availability.AvailabilityChangeEvent;
import org.springframework.boot.availability.ReadinessState;
import org.springframework.context.ConfigurableApplicationContext;

@SpringBootApplication
public class ServingWebContentApplication {

    public static void main(String[] args) {
    	
    	/*
    	 * Spring Boot のアプリケーション開始
    	 */
    	ConfigurableApplicationContext app = SpringApplication.run(ServingWebContentApplication.class, args);
    	
    	/*
    	 * 起動直後は、リクエストを受け付けない。
    	 * データベースやメッセージシステムとの接続が完了して、リクエストを受けても良い状態になってから、
    	 * 
    	 */
        AvailabilityChangeEvent.publish(app, "event source.", ReadinessState.REFUSING_TRAFFIC);
    }

}
