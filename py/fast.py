import argparse
import os
import time


LANG = "+-<>.,[]!"


def load_file(p: str):
    with open(p) as f:
        src = f.read()

    return src


def get_jump_table(src):
    jump_table = [-1 for _ in range(len(src))]
    stack = []
    for i, c in enumerate(src):
        match c:
            case "[":
                stack.append(i)
            case "]":
                j = stack.pop()
                jump_table[i] = j
                jump_table[j] = i

    if len(stack) > 0:
        return None
    return jump_table


def run(src: list[str], jmp_table: dict):
    i = 0
    ptr = 0
    mem = [0]
    output = ""
    while i < len(src):
        code = src[i]
        match code:
            case ">":
                ptr += 1
                if ptr + 1 > len(mem):
                    mem.append(0)
            case "<":
                ptr -= 1
                if ptr < 0:
                    raise IndexError("Pointer moved to negative index")
            case "+":
                mem[ptr] += 1
            case "-":
                mem[ptr] -= 1
                if mem[ptr] < 0:
                    raise IndexError(f"Memory cannot be < 0")
            case ".":
                output += chr(mem[ptr])
            # case OpCode.INPUT:
            #     mem[ptr] = ord(input("Input a single character: ")[0])
            case "!":
                break
            case "[":
                # jump to next ]
                if mem[ptr] == 0:
                    i = jmp_table[i]
            case "]":
                # jump back to [
                if mem[ptr] != 0:
                    i = jmp_table[i]
        i += 1

    return output


if __name__ == "__main__":
    print("python (faster)")
    parser = argparse.ArgumentParser()
    parser.add_argument("path", default="fib.bf", type=str, nargs="?")
    parser.add_argument("--debug", "-d", action="store_true")

    args = parser.parse_args()
    path = args.path
    if not os.path.exists(path):
        print(f'"{path}" does not exist')
        exit(1)

    src = load_file(path)
    debug_src = ""
    if args.debug:
        with open(path) as f:
            debug_src = f.read()
        debug_src = list(filter(lambda x: x in LANG, debug_src))

    n = 1000
    elapsed = 0
    for i in range(n):
        start = time.perf_counter()
        filtered_src = list(filter(lambda x: x in LANG, src))
        jmp = get_jump_table(filtered_src)
        if not jmp:
            print("Invalid program. Unbalanced brackets.")
            exit(1)
        output = run(filtered_src, jmp)
        elapsed += time.perf_counter() - start

    elapsed /= n
    print(output)
    print(f"elapsed: {(elapsed) * 1000 * 1000:.3f}µs")
