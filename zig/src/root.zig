const std = @import("std");
const LANG = "+-<>[],.!";
fn inLang(char: u8) bool {
    for (LANG) |c| {
        if (c == char) {
            return true;
        }
    }
    return false;
}

pub fn run(allocator: std.mem.Allocator, contents: []u8, writer: std.fs.File.Writer) !void {
    const l = filter(contents);
    const src = contents[0..l];

    var jl = std.AutoHashMap(usize, usize).init(allocator);
    try makeJumpList(allocator, src, &jl);
    defer jl.deinit();

    var i: usize = 0;
    var ptr: usize = 0;
    var mem = try std.ArrayList(u8).initCapacity(allocator, 128);
    defer mem.deinit();
    try mem.append(0);

    var output = try std.ArrayList(u8).initCapacity(allocator, 128);
    defer output.deinit();

    while (i < src.len) : (i += 1) {
        const code = src[i];
        switch (code) {
            '+' => mem.items[ptr] += 1,
            '-' => mem.items[ptr] -= 1,
            '>' => {
                ptr += 1;
                if (ptr + 1 > mem.items.len) {
                    try mem.append(0);
                }
            },
            '<' => {
                ptr -= 1;
                if (ptr < 0) {
                    unreachable;
                }
            },
            '.' => try output.append(mem.items[ptr]),
            '!' => break,
            '[' => {
                if (mem.items[ptr] == 0) {
                    i = jl.get(i).?;
                }
            },
            ']' => {
                if (mem.items[ptr] != 0) {
                    i = jl.get(i).?;
                }
            },
            else => unreachable,
        }
    }
    try writer.print("{s}\n", .{output.items});
}

fn filter(src: []u8) usize {
    var ptr: usize = 0;

    for (src) |c| {
        if (inLang(c)) {
            src[ptr] = c;
            ptr += 1;
        }
    }
    return ptr;
}

fn makeJumpList(allocator: std.mem.Allocator, src: []const u8, jl: *std.AutoHashMap(usize, usize)) !void {
    var stack = std.ArrayList(usize).init(allocator);
    defer stack.deinit();
    for (src, 0..) |c, i| {
        if (c == '[') {
            try stack.append(i);
        } else if (c == ']') {
            const j = stack.pop().?;
            try jl.put(i, j);
            try jl.put(j, i);
        }
    }
}
