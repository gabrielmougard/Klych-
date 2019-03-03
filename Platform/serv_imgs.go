package main

import (
	"fmt"
	"net/http"
	"os"
)

func main() {
	port := os.Args[1]
	directory := os.Args[2]
	fmt.Println(directory)
	http.Handle("/", http.FileServer(http.Dir("./build")))
	http.Handle("/photos/", http.StripPrefix("/photos/", http.FileServer(http.Dir(directory))))
	http.ListenAndServe(":"+port, nil)
}
