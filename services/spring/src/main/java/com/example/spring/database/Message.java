package com.example.spring.database;


import jakarta.persistence.*;

@Entity
public class Message {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private String val;

    public Message() {}

    public Message(String value) {
        this.val = value;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getValue() {
        return val;
    }

    public void setValue(String value) {
        this.val = value;
    }
}
