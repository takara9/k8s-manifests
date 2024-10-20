package io.openliberty.guides.rest;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import org.json.JSONArray;
import org.json.JSONObject;


@Path("personList")
public class PersonList {

    @GET
    @Produces(MediaType.APPLICATION_JSON)    
    public String getPersonArray() {        
        JSONArray personArray = new JSONArray();

        JSONObject firstPerson = new JSONObject();
        firstPerson.put("name", "アムロ レイ");
        personArray.put(firstPerson);	
        
        JSONObject secondPerson = new JSONObject();
        secondPerson.put("name", "セイラ マス");
        personArray.put(secondPerson);	

	return personArray.toString();
    }
    
}
