const std = @import("std");
const run = @import("run.zig");

pub fn main() !void {
    var arg_iter = std.process.args();
    _ = arg_iter.skip(); // skip prg arg

    // open the file
    const fname = arg_iter.next() orelse "";
    var f = try std.fs.cwd().openFile(fname, .{});
    defer f.close();

    const runner = run.Runner.init(f);
    try runner.run();
}
