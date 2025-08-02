race:
    @clear
    @cd py; python3 main.py ../hello.bf
    @echo ---
    @cd py; python3 fast.py ../hello.bf
    @echo ---
    @cd go; go build; ./bfi ../hello.bf
    @echo ---
    @cd rust; cargo build --release &>/dev/null && target/release/bfi ../hello.bf
    @echo ---
    @cd zig; zig build --release=fast && zig-out/bin/bfi ../hello.bf
    @echo ---
    @cd js; deno run -q main ../hello.bf
    @echo ---
    @cd java; mvn package &>/dev/null && java -cp target/bfi-1.0-SNAPSHOT.jar app.App ../hello.bf
    @echo ---
    @cd lua; lua main.lua ../hello.bf
