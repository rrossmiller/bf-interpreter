package main

import (
	"fmt"
	"strings"
	"time"
)

func run(src []rune, debug bool) error {
	jumpTable, err := getJumpTable(src)
	if err != nil {
		return err
	}

	i := 0
	ptr := 0
	mem := []int{0}
	var output strings.Builder

Loop:
	for i < len(src) {
		code := src[i]
		if debug {
			callDebug(src, i, ptr, mem, output)
			// time.Sleep(50 * time.Millisecond)
			time.Sleep(1 * time.Millisecond)
			fmt.Print("\033[2J")
			fmt.Print("\033[H")
		}

		switch code {
		case '+':
			mem[ptr]++
		case '-':
			mem[ptr]--
		case '>':
			ptr++
			if ptr+1 > len(mem) {
				mem = append(mem, 0)
			}
		case '<':
			ptr--
			if ptr < 0 {
				return fmt.Errorf("Pointer moved to negative index")

			}
		case '.':
			output.WriteRune(rune(mem[ptr]))
		case '!':
			break Loop
		case '[':
			// jump to next ]
			if mem[ptr] == 0 {
				i = jumpTable[i]
			}
		case ']':
			// jump back to [
			if mem[ptr] != 0 {
				i = jumpTable[i]
			}

		}
		i++
	}
	if debug {
		callDebug(src, i, ptr, mem, output)
	} else {
		fmt.Println(output.String())
	}
	return nil
}

type token struct {
	idx int
	r   rune
}

func getJumpTable(src []rune) (map[int]int, error) {
	stack := []token{}
	jumpTable := map[int]int{}
	for i, c := range src {
		switch c {
		case '[':
			stack = append(stack, token{i, c})
		case ']':
			tkn := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			if tkn.r != '[' {
				return nil, fmt.Errorf("Invalid program. Unmatched brackets")
			}
			jumpTable[i] = tkn.idx
			jumpTable[tkn.idx] = i

		}
	}
	if len(stack) > 0 {
		return nil, fmt.Errorf("Invalid program. Unmatched brackets")

	}

	return jumpTable, nil
}

func debugPrint(src []rune, idx int) {
	var sb strings.Builder
	sb.WriteString("[")
	for i, s := range src {
		if i == idx {
			// output.WriteString(FAIL)
			sb.WriteString("\033[91m")
			sb.WriteRune('"')
			sb.WriteRune(s)
			sb.WriteRune('"')
			sb.WriteString("\033[0m")
			// output.WriteString(ENDC)

		} else {
			sb.WriteRune(s)
		}
		sb.WriteString(", ")
	}

	//  remove trailing space and ,
	output := sb.String()
	output = output[:len(output)-2]
	output += " ]"
	fmt.Println(output)
}

func callDebug(debug []rune, i, ptr int, mem []int, output strings.Builder) {
	debugPrint(debug, i)
	fmt.Println("ptr=", ptr)
	fmt.Printf("mem: %v\n", mem)
	fmt.Printf("output:\n%v\n", output.String())

}
