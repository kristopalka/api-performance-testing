package com.example.spring;

import com.example.spring.database.Message;
import com.example.spring.database.MessageRepository;
import com.example.spring.dto.FibonacciDTO;
import com.example.spring.dto.MessageDTO;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.Random;

import static com.example.spring.FibonacciGenerator.calculateFibonacci;

@RestController
public class ApiController {
    private final MessageRepository repo;
    Random rand = new Random();

    public ApiController(MessageRepository repo) {
        this.repo = repo;
    }

    @GetMapping("/hello")
    public ResponseEntity<MessageDTO> getHello() {
        MessageDTO message = new MessageDTO("Hello World!");
        return ResponseEntity.ok(message);
    }

    @GetMapping("/fibonacci/{n}")
    public ResponseEntity<FibonacciDTO> getFibonacci(@PathVariable int n) {
        if (n < 0) {
            return ResponseEntity.badRequest().build();
        }
        int value = calculateFibonacci(n);
        FibonacciDTO fibonacci = new FibonacciDTO(n, value);
        return ResponseEntity.ok(fibonacci);
    }



    @GetMapping("/database")
    public ResponseEntity<MessageDTO> getDatabaseMessage() {
        int id = rand.nextInt(1, 26);
        Message message = repo.findById(id);

        if (message != null) {
            MessageDTO messageDTO = new MessageDTO(message.getValue());
            return ResponseEntity.ok(messageDTO);
        } else {
            return ResponseEntity.status(404).build();
        }
   }
}
