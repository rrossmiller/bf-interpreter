package app;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

public class Run {
    private static char[] LANG = { '+', '-', '<', '>', '[', ']', ',', '.', '!' };
    private static boolean[] inLangTable = new boolean[256];
    static {
        for (char c : LANG) {
            inLangTable[c] = true;
        }
    }

    private String src;
    private int[] jl;

    public Run(String src) {
        this.src = src;
        this.jl = new int[src.length()];
        Arrays.fill(jl, -1);

    }

    public void run() {
        this.filter();
        this.makeJL();

        int i = 0;
        int ptr = 0;
        int[] mem = new int[3000];
        StringBuilder output = new StringBuilder();
        while (i < src.length()) {
            var c = src.charAt(i);
            switch (c) {
                case '+':
                    mem[ptr]++;
                    break;
                case '-':
                    mem[ptr]--;
                    break;
                case '>':
                    ptr++;
                    break;
                case '<':
                    ptr--;
                    break;
                case '.':
                    output.append((char) mem[ptr]);
                    break;
                case '!':
                    i = src.length();
                    break;
                case '[':
                    if (mem[ptr] == 0) {
                        i = this.jl[i];
                    }
                    break;
                case ']':
                    if (mem[ptr] != 0) {
                        i = this.jl[i];
                    }
                    break;
            }
            i++;
        }
        System.out.println(output.toString());
    }

    private void filter() {
        StringBuilder filtered = new StringBuilder();
        for (int i = 0; i < src.length(); i++) {
            char c = src.charAt(i);
            if (c < 256 && inLangTable[c]) {
                filtered.append(c);
            }
        }
        this.src = filtered.toString();
    }

    private void makeJL() {
        var stack = new int[this.src.length()];
        int top = -1;

        for (int i = 0; i < this.src.length(); i++) {
            char c = this.src.charAt(i);
            if (c == '[') {
                stack[++top] = i;
            } else if (c == ']') {
                var j = stack[top--];
                this.jl[i] = j;
                this.jl[j] = i;
            }
        }
    }

}
