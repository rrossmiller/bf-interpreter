import argparse
import os
import time

from opcodes import OPCODES_MAP, OpCode

LANG = "+-<>.,[]!"


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def debug_print(src, idx):
    output = "["
    for i, s in enumerate(src):
        if i == idx:
            output += bcolors.FAIL + f'"{s}"' + bcolors.ENDC
        else:
            output += f"'{s}'"
        output += ", "

    # remove trailing space and ,
    output = output[:-2]
    output += " ]"
    print(output)


def call_debug(debug, i, ptr, mem, output):
    debug_print(debug, i)
    print(f"{ptr= }")
    print(mem)
    print(f"output:\n{output}")


def load_file(p: str):
    with open(p) as f:
        src = f.read()

    return src


def get_jump_table(src):
    jump_table = {}
    stack = []
    for i, c in enumerate(src):
        match c:
            case OpCode.LOOP_START:
                stack.append((i, c))
            case OpCode.LOOP_END:
                prev_i, prev = stack.pop()
                if prev != OpCode.LOOP_START:
                    return None
                jump_table[i] = prev_i
                jump_table[prev_i] = i

    if len(stack) > 0:
        return None
    return jump_table


def run(src: list[OpCode], jmp_table: dict, debug=""):
    i = 0

    ptr = 0
    mem = [0]
    output = ""
    while i < len(src):
        code = src[i]
        if debug:
            call_debug(debug, i, ptr, mem, output)
            # input()
            time.sleep(0.02)
            print("\033[2J")
            print("\033[H")
        match code:
            case OpCode.INCR_PTR:
                ptr += 1
                if ptr + 1 > len(mem):
                    mem.append(0)
            case OpCode.DECR_PTR:
                ptr -= 1
                if ptr < 0:
                    if debug:
                        call_debug(debug, i, ptr, mem, output)
                    raise IndexError("Pointer moved to negative index")
            case OpCode.INCR:
                mem[ptr] += 1
            case OpCode.DECR:
                mem[ptr] -= 1
                if mem[ptr] < 0:
                    if debug:
                        call_debug(debug, i, ptr, mem, output)
                    raise IndexError(f"Memory cannot be < 0")
            case OpCode.OUTPUT:
                output += chr(mem[ptr])
            case OpCode.INPUT:
                mem[ptr] = ord(input("Input a single character: ")[0])
            case OpCode.EXIT:
                call_debug(debug, i, ptr, mem, output)
                exit()
            case OpCode.LOOP_START:
                # jump to next ]
                if mem[ptr] == 0:
                    i = jmp_table[i]
            case OpCode.LOOP_END:
                # jump back to [
                if mem[ptr] != 0:
                    i = jmp_table[i]
        i += 1

    if debug:
        call_debug(debug, i, ptr, mem, output)
    # else:
    # print(output)
    return output


if __name__ == "__main__":
    print("python")
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
    for _ in range(n):
        start = time.perf_counter()
        filtered_src = [OPCODES_MAP[c] for c in filter(lambda x: x in LANG, src)]
        jmp = get_jump_table(filtered_src)
        if not jmp:
            print("Invalid program. Unbalanced brackets.")
            exit(1)
        output = run(filtered_src, jmp, debug_src)
        elapsed += time.perf_counter() - start

    print(output)
    print(f"elapsed: {elapsed / n * 1000 * 1000:.3f}µs")
