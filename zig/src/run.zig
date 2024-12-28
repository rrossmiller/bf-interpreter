const std = @import("std");

pub const Runner = struct {
    i: u8,
    loopI: u8,
    cursor: u8,
    // state : [256]byte,
    state: [12]u8,
    reader: std.fs.File.Reader,
    out: []u8,
    step: bool,

    pub fn init(f: std.fs.File) Runner {
        var rtn = std.mem.zeroes(Runner);
        rtn.reader = f.reader();
        return rtn;
    }

    pub fn run(r: Runner) !void {
        r.reader.readAllAlloc();
    }

};
