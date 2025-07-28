const std = @import("std");
const LANG = "+-<>[],.!";
const IN_LANG_TABLE = blk: {
    var table = [_]bool{false} ** 256;
    for (LANG) |c| table[c] = true;
    break :blk table;
};
fn inLang(char: u8) bool {
    return IN_LANG_TABLE[char];
}

pub fn run(allocator: std.mem.Allocator, contents: []u8, writer: std.fs.File.Writer) !void {
    const src = filter(contents);
    var jl = try allocator.alloc(usize, src.len);
    defer allocator.free(jl);
    try makeJumpList(allocator, src, &jl);

    var i: usize = 0;
    var ptr: usize = 0;
    var mem: [3000]u8 = [_]u8{0} ** 3000;

    var output: [512]u8 = undefined;
    var output_len: usize = 0;

    while (i < src.len) : (i += 1) {
        const code = src[i];
        switch (code) {
            '+' => mem[ptr] += 1,
            '-' => mem[ptr] -= 1,
            '>' => {
                ptr += 1;
                if (ptr + 1 > mem.len) {
                    unreachable; //todo throw error
                }
            },
            '<' => {
                if (ptr == 0) {
                    unreachable; //todo throw error
                }
                ptr -= 1;
            },
            '.' => {
                output[output_len] = mem[ptr];
                output_len += 1;
            },
            '!' => break,
            '[' => {
                if (mem[ptr] == 0) {
                    i = jl[i];
                }
            },
            ']' => {
                if (mem[ptr] != 0) {
                    i = jl[i];
                }
            },
            else => unreachable,
        }
    }
    try writer.print("{s}\n", .{output[0..output_len]});
}

fn filter(src: []u8) []u8 {
    var ptr: usize = 0;

    for (src) |c| {
        if (inLang(c)) {
            src[ptr] = c;
            ptr += 1;
        }
    }
    return src[0..ptr];
}

fn makeJumpList(allocator: std.mem.Allocator, src: []const u8, jl: *[]usize) !void {
    var stack = std.ArrayList(usize).init(allocator);
    defer stack.deinit();
    for (src, 0..) |c, i| {
        if (c == '[') {
            try stack.append(i);
        } else if (c == ']') {
            const j = stack.pop().?;
            jl.*[i] = j;
            jl.*[j] = i;
        }
    }
}
