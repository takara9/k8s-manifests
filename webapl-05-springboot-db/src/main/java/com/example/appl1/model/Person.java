package com.example.appl1.model;

import java.util.UUID;
import com.fasterxml.jackson.annotation.JsonProperty;

/*
 * Person のデータモデル／エンティティクラス
 * メソッド間のPersonデータの受け渡しに使われる
 */
public class Person {
	private final UUID id;
	private final String name;
	
	public Person(@JsonProperty("id") UUID id,
			      @JsonProperty("name") String name) {
		this.id = id;
		this.name = name;
	}
	
	public UUID getId() {
		return id;
	}

	public String getName() {
		return name;
	}
}
