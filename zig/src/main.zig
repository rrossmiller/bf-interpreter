const std = @import("std");
const run = @import("root.zig");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("zig\n", .{});

    var allocator: std.mem.Allocator = undefined;
    if (true) {
        allocator = std.heap.c_allocator;
    } else {
        var gpa = std.heap.GeneralPurposeAllocator(.{}){};
        allocator = gpa.allocator();
        defer {
            const c = gpa.deinit();
            switch (c) {
                .ok => {},
                .leak => std.debug.print("leaked\n", .{}),
            }
        }
    }

    var args = try std.process.argsWithAllocator(allocator);
    _ = args.skip();
    const path = if (args.next()) |p| p else {
        std.debug.print("Usage: ./bfi <path>\n", .{});
        return;
    };
    args.deinit();

    const src = try readFile(allocator, path);
    defer allocator.free(src);
    var timer = try std.time.Timer.start();
    try run.run(allocator, src, stdout);
    const elapsed_ns = timer.read();
    try stdout.print("elapsed: {d} µs\n", .{elapsed_ns / 1000});
}

fn readFile(allocator: std.mem.Allocator, path: []const u8) ![]u8 {
    const f = try std.fs.cwd().openFile(path, .{});
    defer f.close();
    const r = f.reader();
    const s = try f.stat();
    const b = r.readAllAlloc(allocator, s.size);
    return b;
}
