import os
import sys

from tqdm import tqdm


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


def rm_extra_chars(src):
    lang = "+-<>.,[]"
    return list(filter(lambda x: x in lang, src))


def print_src(src, idx):
    out = "["
    for i, s in enumerate(src):
        if i == idx:
            out += bcolors.FAIL + f'"{s}", ' + bcolors.ENDC
        else:
            out += f"'{s}', "
    # remove trailing space and ,
    out = out[:-2]
    out += " ]"
    print(out)


def run(s: str, step=False):
    src = rm_extra_chars(s)
    t = tqdm(total=len(s))

    # data = [0 for _ in range(512)]
    # data = [0 for _ in range(30)]
    data = [0 for _ in range(1_000_000)]
    idx = 0
    i = 0
    loop = []
    # for i in range(len(src)):
    out = ""
    while i < len(src):
        t.reset(total=len(s))
        t.update(i)
        t.display()
        c = src[i]

        if step:
            print_src(src, i)
            print(i, c)
            print(idx, data[idx])
            print(data)
            print(loop)
            print()
            # input("continue...")
            print("\033[2J")
            print("\033[H")

        match c:
            case "+":
                data[idx] += 1
            case "-":
                data[idx] -= 1
            case "<":
                idx = idx - 1 if idx > 0 else len(src) - 1
            case ">":
                idx = idx + 1 if idx < len(src) - 1 else 0
            case ".":
                # print(f"{data[idx]}")
                out += chr(data[idx])
            case ",":
                inp = input("> ")
                data[idx] = int(inp)
            case "[":
                # If the byte at the data pointer is zero,
                # then instead of moving the instruction pointer forward to the next command,
                # jump it forward to the command after the matching ] command.
                if data[idx] == 0:
                    i = src.index("]", i)
                    continue
                else:
                    loop.append(i)
            case "]":
                # If the byte at the data pointer is nonzero,
                # then instead of moving the instruction pointer forward to the next command,
                # jump it back to the command after the matching [ command.
                if data[idx] > 0:
                    i = loop[-1]
                    continue
                else:
                    loop.pop()
        i += 1
    print(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit(1)
    elif not os.path.exists(sys.argv[1]):
        print(sys.argv[1], "does not exist")
        exit(1)

    with open(sys.argv[1]) as f:
        src = f.read()

    print("\033[2J")
    print("\033[H")
    print("*********")
    # run(src, step=True)
    run(src)
