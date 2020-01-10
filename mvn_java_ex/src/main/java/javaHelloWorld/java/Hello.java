
package javaHelloWorld.java;

import com.google.gson.JsonObject;

/**
 * This is a hello world example of a maven project built to be used as a
 * function as a service in a serverless platform
 * 
 * @author Joe Osborn
 *
 */
public class Hello {
	public static JsonObject main(JsonObject args) {
		String name = "stranger";

		if (args.has("name"))
			name = args.getAsJsonPrimitive("name").getAsString();

		JsonObject response = new JsonObject();
		String msg = "Hello " + name + "! This is a Java FaaS";
		response.addProperty("greeting", msg);
		response.addProperty("body", "<html><body><h3>" + msg + "</h3></body></html>");
		return response;

	}

}
