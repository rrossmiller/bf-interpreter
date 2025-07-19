use std::{collections::HashMap, thread::sleep, time};
use thiserror::Error;

const LANG: &str = "+-<>[],.!";
const ESC: &str = "\x1b";
const WAIT_TIME: time::Duration = time::Duration::from_millis(10);

#[derive(Error, Debug)]
pub enum BfiError {
    #[error("Custom error: {0}")]
    InvalidProgram(String),

    #[error("Custom error: {0}")]
    RuntimeErr(String),
}
// fn get_jump_table(src: &Vec<u8>) -> Result<HashMap<usize, usize>, BfiError> {
// let mut jump_table = HashMap::new();
fn get_jump_table(src: &Vec<u8>) -> Result<Vec<Option<usize>>, BfiError> {
    let mut jump_table = vec![None; src.len()];

    let mut stack: Vec<usize> = Vec::new();
    for (i, c) in src.iter().enumerate() {
        match c {
            b'[' => stack.push(i),
            b']' => {
                if let Some(tkn) = stack.pop() {
                    // jump_table.insert(i, tkn);
                    // jump_table.insert(tkn, i);
                    jump_table[i] = Some(tkn);
                    jump_table[tkn] = Some(i);
                } else {
                    return Err(BfiError::InvalidProgram(
                        "Invalid program. Unmatched brackets".to_string(),
                    ));
                }
            }
            _ => {}
        }
    }
    if stack.len() > 0 {
        return Err(BfiError::InvalidProgram(
            "Invalid program. Unmatched brackets".to_string(),
        ));
    }
    Ok(jump_table)
}

fn debug_print(src: &Vec<u8>, idx: usize) {
    let mut out = String::from("[");
    for (i, c) in src.iter().enumerate() {
        if i == idx {
            out.push_str(ESC);
            out.push_str("[91m");
            // out.push('"');
            out.push(*c as char);
            // out.push('"');
            out.push_str(ESC);
            out.push_str("[0m");
        } else {
            out.push(*c as char);
        }
        out.push_str(", ");
    }
    out = String::from(&out[..out.len() - 2]);
    out.push(']');

    println!("{}", out);
}

fn call_debug_print(
    src: &Vec<u8>,
    idx: usize,
    ptr: usize,
    mem: &Vec<u8>,
    out: &String,
    clear: bool,
) {
    debug_print(src, idx);
    println!("{ptr}");
    println!("mem: {:?}", mem);
    println!("{}", out);
    sleep(WAIT_TIME);
    if clear {
    print!("\x1b[2J");
        print!("\x1b[H")
    }
}

pub fn run(src: String) -> Result<(), BfiError> {
    let chars: Vec<u8> = src.bytes().filter(|b| LANG.contains(*b as char)).collect();

    let jmp = get_jump_table(&chars)?;
    let mut i: usize = 0;
    let mut ptr = 0;
    let mut mem: Vec<u8> = Vec::from([0; 32]);
    let mut output = String::with_capacity(100);

    while i < chars.len() {
        let c = chars[i as usize];
        #[cfg(feature = "debug-mode")]
        call_debug_print(&chars, i, ptr, &mem, &output, true);
        match c {
            // '+' => mem[ptr] += 1,
            b'+' => unsafe {
                *mem.get_unchecked_mut(ptr) += 1;
            },
            // '-' => mem[ptr] -= 1,
            b'-' => unsafe {
                *mem.get_unchecked_mut(ptr) -= 1;
            },
            b'>' => {
                ptr += 1;
                if ptr + 1 > mem.len() {
                    mem.push(0);
                }
            }
            b'<' => {
                if ptr == 0 {
                    return Err(BfiError::RuntimeErr(
                        "Pointer moved to a negative index".to_string(),
                    ));
                }
                ptr -= 1;
            }
            b'.' => {
                // output.push(mem[ptr] as char);
                unsafe {
                    output.push(*mem.get_unchecked(ptr) as char);
                }
                #[cfg(feature = "debug-mode")]
                call_debug_print(&chars, i, ptr, &mem, &output, true);
            }
            b'!' => break,
            b'[' => {
                // jump to next ]
                // if mem[ptr] == 0 {
                //     // i = *jmp.get(&i).unwrap();
                //     i = jmp[&i];
                // }
                unsafe {
                    if *mem.get_unchecked(ptr) == 0 {
                        // i = jmp[&i];
                        i = jmp[i].unwrap();
                    }
                }
            }
            b']' => {
                // jump back to [
                // if mem[ptr] != 0 {
                //     i = *jmp.get(&i).unwrap();
                // }
                unsafe {
                    if *mem.get_unchecked(ptr) != 0 {
                        i = jmp[i].unwrap();
                    }
                }
            }
            _ => unreachable!(),
        }
        i += 1;
    }

    #[cfg(feature = "debug-mode")]
    call_debug_print(&chars, i, ptr, &mem, &output, false);
    println!("{}", output);
    Ok(())
}
