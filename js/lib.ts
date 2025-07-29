export const LANG = "+-<>[],.!";
const IN_LANG_ARR = function () {
  const a = Array(256).fill(false);
  LANG.split("").forEach((c) => {
    const i = c.charCodeAt(0);
    a[i] = true;
  });
  return a;
}();

export function run(src: string[]) {
  src = src.filter((c) => {
    return IN_LANG_ARR[c.charCodeAt(0)];
  });
  const jl = makeJumpList(src);

  let i: number = 0;
  let ptr: number = 0;
  const mem: number[] = Array(3000).fill(0);

  let output = "";

  while (i < src.length) {
    const code = src[i];
    switch (code) {
      case "+":
        mem[ptr]++;
        break;
      case "-":
        mem[ptr]--;
        break;
      case ">":
        ptr++;
        break;
      case "<":
        ptr--;
        break;
      case "[":
        if (mem[ptr] == 0) {
          i = jl[i];
        }
        break;
      case "]":
        if (mem[ptr] != 0) {
          i = jl[i];
        }
        break;
      case ".":
        output += String.fromCharCode(mem[ptr]);
        break;
      case "!":
        i = src.length;
        break;
    }
    i++;
  }
  console.log(output);
}

function makeJumpList(src: string[]) {
  const stack: number[] = [];
  const jl: number[] = Array(src.length);
  let j = undefined;
  src.forEach((c, i) => {
    switch (c) {
      case "[":
        stack.push(i);
        break;
      case "]":
        j = stack.pop()!;
        jl[i] = j;
        jl[j] = i;
        break;
    }
  });
  return jl;
}
