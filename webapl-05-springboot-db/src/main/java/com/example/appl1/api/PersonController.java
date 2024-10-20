package com.example.appl1.api;

import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.appl1.model.Person;
import com.example.appl1.service.PersonService;

/*
 * REST API として公開する部分のコントロールを担当
 * ビジネスロジックを担当する PersonService をコールする
 */

@RequestMapping("/api/v1/person")
@RestController
public class PersonController {
	
	private PersonService personService = null;
	
	@Autowired
	public PersonController(PersonService personService) {
		this.personService = personService;
	}

	/*
	 * 結果を返すものだけ return をいれる。
	 * それ以外は、HTTPリクエストの応答コードに反映される。
	 */
	@PostMapping
	public void addPerson(@RequestBody Person person) {
		personService.addPerson(person);
	}
	
	@GetMapping
	public List<Person> getAllPeople() {
		return personService.getAllPeople();
	}
	
	@GetMapping("/{id}")
	public Person getPersonById(@PathVariable("id") UUID id) {
		return personService.getPersonById(id).orElse(null);
	}
	
	@DeleteMapping("/{id}")
	public void deletePersonById(@PathVariable("id") UUID id) {
		personService.deletePersonById(id);
	}
	
	@PutMapping("/{id}")
	public void updatePersonById(@PathVariable("id") UUID id, @RequestBody Person personToUpdate) {
		personService.updatePersonById(id, personToUpdate);
	}
	
}
