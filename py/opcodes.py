# >	Increment the data pointer by one (to point to the next cell to the right).
# <	Decrement the data pointer by one (to point to the next cell to the left).
# +	Increment the byte at the data pointer by one.
# -	Decrement the byte at the data pointer by one.
# .	Output the byte at the data pointer.
# ,	Accept one byte of input, storing its value in the byte at the data pointer.
# [	If the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command.
# ]	If the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command.
from enum import Enum, auto


class OpCode(Enum):
    INCR = auto()
    DECR = auto()
    INCR_PTR = auto()
    DECR_PTR = auto()

    LOOP_START = auto()
    LOOP_END = auto()
    OUTPUT = auto()
    INPUT = auto()
    EXIT = auto()


OPCODES_MAP = {
    ">": OpCode.INCR_PTR,  # Increment the data pointer by one (to point to the next cell to the right).
    "<": OpCode.DECR_PTR,  # Decrement the data pointer by one (to point to the next cell to the left).
    "+": OpCode.INCR,  # Increment the byte at the data pointer by one.
    "-": OpCode.DECR,  # Decrement the byte at the data pointer by one.
    ".": OpCode.OUTPUT,  # Output the byte at the data pointer.
    ",": OpCode.INPUT,  # Accept one byte of input, storing its value in the byte at the data pointer.
    "[": OpCode.LOOP_START,  # If the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command.
    "]": OpCode.LOOP_END,  # If the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command.[a]
    "!": OpCode.EXIT,
}
