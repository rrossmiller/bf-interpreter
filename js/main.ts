// import { parseArgs } from "jsr:@std/cli/parse-args";
import { run } from "./lib.ts";

if (import.meta.main) {
  console.log("Deno");
  const fp = Deno.args[0];
  const src = (await Deno.readTextFile(fp)).split("");
  const start = performance.now();
  run(src);
  let elapsed = performance.now() - start;

  if (elapsed < 0.01) {
    elapsed = elapsed * 1000;
    console.log(`elapsed: ${elapsed.toFixed(4)} µs`);
  } else {
    console.log(`elapsed: ${elapsed.toFixed(4)} ms`);
  }
}
