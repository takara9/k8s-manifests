package io.openliberty.guides.rest;

import javax.json.Json;
import javax.json.JsonObject;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import java.math.BigDecimal;

@Path("person")
public class Person {
 
    @GET
        public String getJsonText() {
            JsonObject json = Json.createObjectBuilder()
            .add("name", "Falco")
            .add("age", BigDecimal.valueOf(3))
            .add("biteable", Boolean.FALSE).build();
        String result = json.toString();
        System.out.println(result);
        return result;
    }
    

}
