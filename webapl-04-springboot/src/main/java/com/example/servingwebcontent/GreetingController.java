package com.example.servingwebcontent;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.availability.AvailabilityChangeEvent;
import org.springframework.boot.availability.LivenessState;
import org.springframework.boot.availability.ReadinessState;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class GreetingController {

	@Autowired
	private ApplicationEventPublisher eventPublisher;
	
	/*
	 * spring-boot-starter-thymeleaf 
	 *「Thymeleaf（タイムリーフ）」とはJavaテンプレートエンジンを
	 * 利用して、ruturnで返す文字列に対応するテンプレートをレンダして
	 * 応答のページを返す。
	 */	
	@GetMapping("/greeting")
	public String greeting(@RequestParam(name="name", required=false, defaultValue="World") String name, Model model) {
		model.addAttribute("name", name);
		return "greeting";
	}

	/*
	 * バグを踏んでアプリケーションが壊れたという設定で
	 * LivnessProveの設定を変更する
	 */
	@GetMapping("/bug")
	public String broken() {
        AvailabilityChangeEvent.publish(eventPublisher, "event source.", LivenessState.BROKEN);
        return "bug";
	}

	/*
	 * アプリケーションがクラッシュする
	 * クラッシュした場合、自動的に状態が変わる訳ではないので、注意が必要
	 */
	@GetMapping("/crash")
	public void crash() {
        //AvailabilityChangeEvent.publish(eventPublisher, "event source.", LivenessState.BROKEN);
        return;
	}

}
