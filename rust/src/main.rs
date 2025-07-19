use core::panic;
use std::{self, fs, io::Read, path, time};

mod run;
fn main() -> Result<(), run::BfiError> {
    println!("rust");
    let mut args = std::env::args();
    if args.len() < 2 {}
    let file_path = if let Some(a) = args.nth(1) {
        a
    } else {
        println!("usage:\n  bfi <file_path>");
        std::process::exit(1)
    };
    let file_path = path::Path::new(&file_path);
    let src = read_file(file_path);

    let start = time::Instant::now();
    run::run(src)?;
    println!("elapsed: {:?}", time::Instant::now().duration_since(start));
    Ok(())
}

fn read_file(fp: &std::path::Path) -> String {
    let mut file = match fs::File::open(fp) {
        Err(e) => panic!("couldn't open: {} {}", fp.display(), e),
        Ok(f) => f,
    };

    let mut rtn = String::new();
    match file.read_to_string(&mut rtn) {
        Err(why) => panic!("couldn't read {}: {}", fp.display(), why),
        Ok(_) => {}
    };

    rtn
}
