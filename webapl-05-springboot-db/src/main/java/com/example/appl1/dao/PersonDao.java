package com.example.appl1.dao;

import java.util.List;
import java.util.Optional;
import java.util.UUID;
import com.example.appl1.model.Person;

/*
 * データベースアクセスのためのインタフェースクラス
 * 
 * データベースを変更しても、ビジネスロジックに変更を及ぼさないために、
 * 実装から分離してインタフェースを規定しておく
 * 
 */

public interface PersonDao {
	
	int insertPerson(UUID id, Person person);
	default int insertPerson(Person person) {
		UUID id = UUID.randomUUID();
		return insertPerson(id, person);
	}
	List<Person> selectAllPeople();	
	Optional<Person> selectPersonById(UUID id);
	int deletePersonById(UUID id);
	int updatePersonById(UUID id, Person pesron);
}
