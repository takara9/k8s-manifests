package com.example.servingwebcontent;

import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.availability.AvailabilityChangeEvent;
import org.springframework.boot.availability.ReadinessState;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Controller;

@Controller
public class ReadinessController {

	@Autowired
	private ApplicationEventPublisher eventPublisher;
	
	/*
	 * コンストラクタ内にタイマーをセットして、30秒後に、リクエストトラフィックを開始するように、
	 * Readiness プローブの設定を変更する。
	 * 
	 * 実際のアプリケーションでは、アプリの初期化処理が完了したところで、状態を変更する。
	 */
    public ReadinessController() {
        ScheduledExecutorService scheduled = Executors.newSingleThreadScheduledExecutor();
        scheduled.schedule(() -> {
        	 AvailabilityChangeEvent.publish(eventPublisher, "event source.", ReadinessState.ACCEPTING_TRAFFIC);
        }, 30, TimeUnit.SECONDS);
    }

}
