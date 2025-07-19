race:
    @clear
    cd go; go build; ./bfi ../hello.bf
    @echo
    cd rust; cargo build --release &>/dev/null;target/release/bfi ../hello.bf
