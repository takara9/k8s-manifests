package com.example.appl1.service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

import com.example.appl1.dao.PersonDao;
import com.example.appl1.model.Person;

/*
 * REST APIなどのプレゼンテーション層から、
 * リクエストを受け取るビジネスロジック層 
 */

// @Service は業務処理すなわちビジネスロジックの提供を意味する。
@Service
public class PersonService {

	// コンストラクタの中で、DAOの実装クラスをインスタンス化のでここで宣言
	// ビジネスロジックとして複数のDAOを利用する時は複数書いておく。
	private PersonDao personDao = null;
	
	// @Autowiredを指定することで、必要なインスタンス化を実行してくれる
	// fakeDao または postgres の選択がある
	@Autowired
	public PersonService(@Qualifier("fakeDao")PersonDao personDao) {
		this.personDao = personDao;
	}

	
	/*
	 * ここから下は、DAOのラップの様になっているが、
	 * ビジネスロジックの実装となる。
	 */
	public int addPerson(Person person) {
		Person personToAdd = new Person(
				UUID.randomUUID(),
				person.getName());
		return personDao.insertPerson(personToAdd);
	}

	public List<Person> getAllPeople() {
		return personDao.selectAllPeople();
	}
	
	public Optional<Person> getPersonById(UUID id) {
		return personDao.selectPersonById(id);
	}
	
	public int deletePersonById(UUID id) {
		return personDao.deletePersonById(id);
	}
	
	public int updatePersonById(UUID id, Person newPerson) {
		return personDao.updatePersonById(id, newPerson);
	}
	
	
}
