import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

public class SimpleBooksAPITest {

    private static String BASE_URL = "https://simple-books-api.glitch.me";
    private static String TOKEN;
    
    @BeforeClass
    public void setup() {
        RestAssured.baseURI = BASE_URL;
        
        // Register API Client and get token
        Response response = given()
                .contentType(ContentType.JSON)
                .body("{" +
                        "\"clientName\": \"TestClient\"," +
                        "\"clientEmail\": \"testclient@example.com\"}" )
                .when()
                .post("/api-clients/")
                .then()
                .statusCode(201)
                .extract().response();
        
        TOKEN = response.path("accessToken");
    }

    @Test
    public void testGetStatus() {
        given()
            .when()
            .get("/status")
            .then()
            .statusCode(200)
            .body("status", equalTo("OK"));
    }

    @Test
    public void testGetBooks() {
        given()
            .when()
            .get("/books")
            .then()
            .statusCode(200)
            .body("size()", greaterThan(0));
    }
    
    @Test
    public void testSubmitOrder() {
        given()
            .contentType(ContentType.JSON)
            .header("Authorization", "Bearer " + TOKEN)
            .body("{" +
                    "\"bookId\": 1," +
                    "\"customerName\": \"John Doe\"}" )
            .when()
            .post("/orders")
            .then()
            .statusCode(201)
            .body("orderId", notNullValue());
    }
}
