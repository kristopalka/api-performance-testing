package com.example.spring.dto;

public class FibonacciDTO {
    private int number;
    private int value;

    public FibonacciDTO() {}

    public FibonacciDTO(int number, int value) {
        this.number = number;
        this.value = value;
    }

    public int getNumber() {
        return number;
    }

    public void setNumber(int number) {
        this.number = number;
    }

    public int getValue() {
        return value;
    }

    public void setValue(int value) {
        this.value = value;
    }
}
