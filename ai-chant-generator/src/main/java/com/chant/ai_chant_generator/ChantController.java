
package com.chant.ai_chant_generator;

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ChantController {

    @GetMapping("/chant")
    public String generateChant(
            @RequestParam(defaultValue = "study") String topic)
            throws Exception {

        String encodedTopic =
                URLEncoder.encode(topic, StandardCharsets.UTF_8);

        URI uri = URI.create(
                "http://localhost:5000/?topic=" + encodedTopic);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(uri)
                .GET()
                .build();

        HttpClient client = HttpClient.newHttpClient();

        HttpResponse<String> response = client.send(
                request,
                HttpResponse.BodyHandlers.ofString());

        return response.body();
    }
}
