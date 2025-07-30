package app;

import java.nio.file.Files;
import java.nio.file.Paths;

public class App {
    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            System.out.println("usage: ./run.sh <path to file>");
            return;
        }
        System.out.println("java");
        var src = Files.readString(Paths.get(args[0]));

        var runner = new Run(src);
        var start = System.nanoTime();
        runner.run();
        var elapsed = (double) System.nanoTime() - start;
        System.out.println(String.format("elapsed: %.4f µs", elapsed / 1000));
    }

    // // list of chars is slow
    // private static List<Character> readFile(String fp) throws IOException {
    // var src = Files.readString(Paths.get(fp));
    // List<Character> chars = src.chars()
    // .mapToObj(c -> (char) c)
    // .collect(Collectors.toList());
    //
    // return chars;
    // }
}
