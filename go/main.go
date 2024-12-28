package main

import (
	"fmt"
	"io"
	"os"
	"strings"
)

const lang = "+-<>[],."

func main() {
	fname := os.Args[1]
	src := readFile(fname)
	step := true
	step = false
	r := Runner{step: step}
	r.run(src)
	fmt.Println()
	// t := []int{1, 2, 3, 4}
	// //pop
	// a := t[len(t)-1]
	// t = t[:len(t)-1]
	// fmt.Println(a, t)
	// //push
	// t = append(t, 1)
	// fmt.Println(t)
	// //pop
	// a = t[len(t)-1]
	// t = t[:len(t)-1]
	// fmt.Println(a, t)
}

func readFile(fp string) []rune {
	if _, err := os.Stat(fp); err != nil {
		fmt.Println("file doesn't exist")
		os.Exit(1)
	}

	file, err := os.Open(fp)
	if err != nil {
		panic(err)
	}
	b, err := io.ReadAll(file)
	if err != nil {
		panic(err)
	}
	src := []rune{}
	for _, s := range string(b) {
		if strings.ContainsRune(lang, s) {
			src = append(src, rune(s))
		}
	}
	return src
}
