package main

import (
	"database/sql"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/go-sql-driver/mysql"
	_ "github.com/go-sql-driver/mysql"
	"log"
	"math/rand"
	"net/http"
	"strconv"
	"time"
)

var db *sql.DB
var random *rand.Rand

type Message struct {
	Message string `json:"message" binding:"required"`
}

type Fibonacci struct {
	Number int `json:"number" binding:"required"`
	Value  int `json:"value" binding:"required"`
}

func connectDatabase() {
	cfg := mysql.Config{
		User:                 "user",
		Passwd:               "password",
		Net:                  "tcp",
		Addr:                 "mariadb:3306",
		DBName:               "database",
		AllowNativePasswords: true,
	}
	var err error
	db, err = sql.Open("mysql", cfg.FormatDSN())
	if err != nil {
		log.Fatal(err)
	}

	pingErr := db.Ping()
	if pingErr != nil {
		log.Fatal(pingErr)
	}
	fmt.Println("Database connected!")
}

func config() {
	r := gin.New()

	r.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Content-Type", "application/json")
		c.Next()
	})

	r.GET("/hello", getHello)
	r.GET("/fibonacci/:n", getFibonacci)
	r.GET("/database", getDatabase)

	err := r.Run(":8080")
	if err != nil {
		fmt.Println("Failed to start!")
		fmt.Println(err.Error())
	}
}

func main() {
	random = rand.New(rand.NewSource(time.Now().UnixNano()))
	gin.SetMode(gin.ReleaseMode)
	connectDatabase()
	config()
}

func getHello(c *gin.Context) {
	c.JSON(http.StatusOK, Message{Message: "Hello World!"})
}

func getFibonacci(c *gin.Context) {
	nStr := c.Param("n")
	n, err := strconv.Atoi(nStr)
	if err != nil || n < 0 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid parameter"})
		return
	}

	value := fibonacci(n)
	c.JSON(http.StatusOK, Fibonacci{Number: n, Value: value})
}

func fibonacci(n int) int {
	if n < 2 {
		return n
	}
	a, b := 0, 1
	for i := 2; i <= n; i++ {
		a, b = b, a+b
	}
	return b
}

func getDatabase(c *gin.Context) {
	id := random.Intn(25) + 1

	var message Message
	row := db.QueryRow("SELECT val FROM message WHERE id = ?", id)
	if err := row.Scan(&message.Message); err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Not found"})
		return
	}

	c.JSON(http.StatusOK, message)
	fmt.Println(message)

}
