package main

import (
	"fmt"
	"log"
	"net/http"
)

func index(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, S2D service Demo ! - v4.0")
}

func main() {
	http.HandleFunc("/", index)
	log.Fatal(http.ListenAndServe(":80", nil))
}
