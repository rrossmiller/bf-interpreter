package main

import (
	"flag"
	"fmt"
	"io"
	"os"
	"strings"
	"time"
)

const lang = "+-<>[],.!"

func main() {
	debug := false
	fmt.Println("go")
	flag.BoolVar(&debug, "d", false, "debug")
	flag.Parse()
	args := flag.Args()

	if len(args) != 1 {
		fmt.Println("You must supply a file path")
		flag.Usage()
		return
	}
	fname := args[0]
	src := readFile(fname)

	start := time.Now()
	err := run(src, debug)
	if err != nil {
		panic(err)
	}
	fmt.Printf("elapsed: %v\n", time.Since(start))

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
