package com.example.appl1.dao;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.stereotype.Repository;
import com.example.appl1.model.Person;

/*
 * インタフェースクラスを実装するクラスであり、データベースによって
 * このクラスは差し替える必要がある。 
 * そのため、@Repositoryにタグを設定して、サービス（ビジネスロジック）で
 * タグを指定して、実装クラスを変更できるようにする。
 */
// Spring DAO等のDBアクセスを行うクラスであることを意味づける
@Repository("fakeDao")
public class FakePersonDataAccessService implements PersonDao {

	private static List<Person> DB = new ArrayList<>();
	
	@Override
	public int insertPerson(UUID id, Person person) {
		DB.add(new Person(id, person.getName()));
		return 1;
	}

	@Override
	public List<Person> selectAllPeople() {
		return DB;
	}

	@Override
	public Optional<Person> selectPersonById(UUID id) {
		return DB.stream()
				.filter(person -> person.getId().equals(id))
				.findFirst();
	}

	@Override
	public int deletePersonById(UUID id) {
		Optional<Person> personMeybe = this.selectPersonById(id);
		if (personMeybe.isEmpty()) {
			return 0;
		}
		DB.remove(personMeybe.get());
		return 1;
	}

	@Override
	public int updatePersonById(UUID id, Person personToUpdate) {
		return this.selectPersonById(id)
				.map(person -> {
					int indexOfPersonToUpdate = DB.indexOf(person);
					if (indexOfPersonToUpdate >= 0) {
						DB.set(indexOfPersonToUpdate,new Person(id, personToUpdate.getName()));
						return 1;
					}  
					return 0;
				})
				.orElse(0);
	}
	
}
