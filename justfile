race:
    @clear
    @cd py; python3 main.py ../hello.bf
    @echo
    @cd go; go build; ./bfi ../hello.bf
    @echo
    @cd rust; cargo build --release &>/dev/null;target/release/bfi ../hello.bf
    @echo
    @cd zig; zig build --release=fast && zig-out/bin/bfi ../hello.bf
