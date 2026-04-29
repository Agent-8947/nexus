# RISC-V Assembler Cheat Sheet

A thorough reference to 32-bit RISC-V instructions, registers, and fundamental concepts. This guide is intended for software developers working with the RISC-V assembly language and includes grouped instructions by purpose, common pseudoinstructions, and usage examples.
## Table of Contents

1. [Arithmetic Instructions](#arithmetic-instructions)
2. [Bitwise Logic Instructions](#bitwise-logic-instructions)
3. [Shift Instructions](#shift-instructions)
4. [Load Immediate Instructions](#load-immediate-instructions)
5. [Load and Store Instructions](#load-and-store-instructions)
6. [Jump and Function Instructions](#jump-and-function-instructions)
7. [Branch Instructions](#branch-instructions)
8. [Set Instructions](#set-instructions)
9. [Counter Instructions](#counter-instructions)
10. [Miscellaneous Instructions](#miscellaneous-instructions)
11. [Instruction Terminology](#instruction-terminology)
12. [RV32 ABI Registers](#rv32-abi-registers)
13. [RISC-V Concepts](#risc-v-concepts)
14. [Usage Examples](#usage-examples)

---

## Arithmetic Instructions

Arithmetic operations perform basic mathematical computations.

| **Instruction** | **Description**         | **Usage**           | **Result**                          | **Guide**    |
|-----------------|-------------------------|---------------------|-------------------------------------|--------------|
| `add`           | Add                     | `add rd, rs1, rs2`  | `rd = rs1 + rs2`                    | Arithmetic    |
| `addi`          | Add Immediate            | `addi rd, rs1, imm` | `rd = rs1 + imm`                    | Arithmetic    |
| `neg`           | Negate (pseudoinstruction)| `neg rd, rs2`       | `rd = -rs2`                          | Arithmetic    |
| `sub`           | Subtract                | `sub rd, rs1, rs2`  | `rd = rs1 - rs2`                    | Arithmetic    |
| `mul`           | Multiply                | `mul rd, rs1, rs2`  | `rd = (rs1 * rs2)[31:0]`            | Multiply      |
| `mulh`          | Multiply High           | `mulh rd, rs1, rs2` | `rd = (rs1 * rs2)[63:32]`           | Multiply      |
| `mulhu`         | Multiply High Unsigned  | `mulhu rd, rs1, rs2`| `rd = (rs1 * rs2)[63:32]`           | Multiply      |
| `mulhsu`        | Multiply High Signed Unsigned | `mulhsu rd, rs1, rs2` | `rd = (rs1 * rs2)[63:32]`      | Multiply      |
| `div`           | Divide                  | `div rd, rs1, rs2`  | `rd = rs1 / rs2`                    | Divide        |
| `rem`           | Remainder               | `rem rd, rs1, rs2`  | `rd = rs1 % rs2`                    | Divide        |

**Notes:**
- Use `addi` for subtracting with an immediate value: `addi rd, rs1, -imm`
- Multiply and divide instructions require the **M** extension.

### Example:
```assembly
addi t0, t1, 10      # t0 = t1 + 10
sub t2, t0, t1       # t2 = t0 - t1
mul t3, t2, t1       # t3 = t2 * t1
```

---

## Bitwise Logic Instructions

Perform logical operations on binary data.

| **Instruction** | **Description**       | **Usage**           | **Result**                          | **Guide**    |
|-----------------|-----------------------|---------------------|-------------------------------------|--------------|
| `and`           | Logical AND           | `and rd, rs1, rs2`  | `rd = rs1 & rs2`                    | Logical      |
| `andi`          | AND Immediate          | `andi rd, rs1, imm` | `rd = rs1 & imm`                    | Logical      |
| `not`           | Logical NOT (pseudoinstruction) | `not rd, rs1`       | `rd = ~rs1`                          | Logical      |
| `or`            | Logical OR            | `or rd, rs1, rs2`   | `rd = rs1 | rs2`                    | Logical      |
| `ori`           | OR Immediate           | `ori rd, rs1, imm`  | `rd = rs1 | imm`                    | Logical      |
| `xor`           | Logical XOR           | `xor rd, rs1, rs2`  | `rd = rs1 ^ rs2`                    | Logical      |
| `xori`          | XOR Immediate          | `xori rd, rs1, imm` | `rd = rs1 ^ imm`                    | Logical      |

### Example:
```assembly
and t0, t1, t2       # t0 = t1 & t2
ori t3, t0, 0xFF     # t3 = t0 | 0xFF
not t4, t3           # t4 = ~t3
```

---

## Shift Instructions

Handle bitwise shifting operations.

| **Instruction** | **Description**               | **Usage**                | **Result**                          | **Guide**    |
|-----------------|-------------------------------|--------------------------|-------------------------------------|--------------|
| `sll`           | Shift Left Logical            | `sll rd, rs1, rs2`       | `rd = rs1 << rs2`                   | Shift        |
| `slli`          | Shift Left Logical Immediate   | `slli rd, rs1, imm`      | `rd = rs1 << imm`                   | Shift        |
| `srl`           | Shift Right Logical           | `srl rd, rs1, rs2`       | `rd = rs1 >> rs2`                   | Shift        |
| `srli`          | Shift Right Logical Immediate  | `srli rd, rs1, imm`      | `rd = rs1 >> imm`                   | Shift        |
| `sra`           | Shift Right Arithmetic        | `sra rd, rs1, rs2`       | `rd = rs1 >>> rs2`                  | Shift        |
| `srai`          | Shift Right Arithmetic Immediate | `srai rd, rs1, imm` | `rd = rs1 >>> imm`                   | Shift        |

### Example:
```assembly
slli t0, t1, 2       # t0 = t1 << 2
srli t2, t0, 1       # t2 = t0 >> 1
sra t3, t2, t1       # t3 = t2 >>> t1
```

---

## Load Immediate Instructions

Load immediate values into registers.

| **Instruction** | **Description**              | **Usage**           | **Result**                          | **Guide**    |
|-----------------|------------------------------|---------------------|-------------------------------------|--------------|
| `li`            | Load Immediate (pseudoinstruction) | `li rd, imm`        | `rd = imm`                          | Arithmetic    |
| `lui`           | Load Upper Immediate         | `lui rd, imm`       | `rd = imm << 12`                    | Arithmetic    |
| `auipc`         | Add Upper Immediate to PC    | `auipc rd, imm`     | `rd = pc + (imm << 12)`             | Branch        |

### Example:
```assembly
li t0, 100           # t0 = 100
lui t1, 0x1F         # t1 = 0x1F000
auipc t2, 0x10       # t2 = pc + 0x10000
```

---

## Load and Store Instructions

Manage data movement between registers and memory.

| **Instruction** | **Description**             | **Usage**                | **Result**                                 | **Guide**    |
|-----------------|-----------------------------|--------------------------|--------------------------------------------|--------------|
| `lw`            | Load Word                   | `lw rd, imm(rs1)`        | `rd = mem[rs1 + imm]`                      | Load         |
| `lh`            | Load Half                   | `lh rd, imm(rs1)`        | `rd = mem[rs1 + imm][0:15]`                | Load         |
| `lhu`           | Load Half Unsigned          | `lhu rd, imm(rs1)`       | `rd = mem[rs1 + imm][0:15]`                | Load         |
| `lb`            | Load Byte                   | `lb rd, imm(rs1)`        | `rd = mem[rs1 + imm][0:7]`                 | Load         |
| `lbu`           | Load Byte Unsigned          | `lbu rd, imm(rs1)`       | `rd = mem[rs1 + imm][0:7]`                 | Load         |
| `la`            | Load Symbol Address (pseudoinstruction) | `la rd, symbol`      | `rd = &symbol`                             | Load         |
| `sw`            | Store Word                  | `sw rs2, imm(rs1)`       | `mem[rs1 + imm] = rs2`                     | Store        |
| `sh`            | Store Half                  | `sh rs2, imm(rs1)`       | `mem[rs1 + imm][0:15] = rs2`               | Store        |
| `sb`            | Store Byte                  | `sb rs2, imm(rs1)`       | `mem[rs1 + imm][0:7] = rs2`                | Store        |

### Example:
```assembly
lw t0, 0(sp)         # t0 = mem[sp + 0]
sw t1, 4(sp)         # mem[sp + 4] = t1
la t2, data_label    # t2 = address of data_label
```

---

## Jump and Function Instructions

Control the flow of the program through jumps and function calls.

| **Instruction** | **Description**                                | **Usage**                   | **Result**                                  | **Guide**    |
|-----------------|------------------------------------------------|-----------------------------|---------------------------------------------|--------------|
| `j`             | Jump (pseudoinstruction)                        | `j imm`                     | `pc += imm`                                 | Jump         |
| `jal`           | Jump and Link                                    | `jal rd, imm`               | `rd = pc + 4; pc += imm`                    | Jump         |
| `jalr`          | Jump and Link Register                           | `jalr rd, rs1, imm`         | `rd = pc + 4; pc = rs1 + imm`               | Jump         |
| `call`          | Call Function (pseudoinstruction)                | `call symbol`               | `ra = pc + 4; pc = &symbol`                  | Function     |
| `ret`           | Return from Function (pseudoinstruction)         | `ret`                       | `pc = ra`                                   | Function     |

**Notes:**
- Labels can be used in place of immediate values for jump instructions.

### Example:
```assembly
jal ra, function_label    # Jump to function_label and store return address in ra
call main                 # Call the main function
ret                       # Return from the current function
```

---

## Branch Instructions

Conditional branching based on comparisons.

| **Instruction** | **Description**             | **Usage**                   | **Result**                                    | **Guide**    |
|-----------------|-----------------------------|-----------------------------|-----------------------------------------------|--------------|
| `beq`           | Branch Equal                | `beq rs1, rs2, imm`         | `if(rs1 == rs2) pc += imm`                   | Branch       |
| `beqz`          | Branch Equal Zero (pseudoinstruction) | `beqz rs1, imm`       | `if(rs1 == 0) pc += imm`                     | Branch       |
| `bne`           | Branch Not Equal            | `bne rs1, rs2, imm`         | `if(rs1 ≠ rs2) pc += imm`                    | Branch       |
| `bnez`          | Branch Not Equal Zero (pseudoinstruction) | `bnez rs1, imm`     | `if(rs1 ≠ 0) pc += imm`                     | Branch       |
| `blt`           | Branch Less Than            | `blt rs1, rs2, imm`         | `if(rs1 < rs2) pc += imm`                    | Branch       |
| `bltu`          | Branch Less Than Unsigned   | `bltu rs1, rs2, imm`        | `if(rs1 < rs2) pc += imm`                    | Branch       |
| `bltz`          | Branch Less Than Zero (pseudoinstruction) | `bltz rs1, imm`       | `if(rs1 < 0) pc += imm`                      | Branch       |
| `bgt`           | Branch Greater Than (pseudoinstruction) | `bgt rs1, rs2, imm`   | `if(rs1 > rs2) pc += imm`                    | Branch       |
| `bgtu`          | Branch Greater Than Unsigned (pseudoinstruction) | `bgtu rs1, rs2, imm` | `if(rs1 > rs2) pc += imm`            | Branch       |
| `bgtz`          | Branch Greater Than Zero (pseudoinstruction) | `bgtz rs1, imm`       | `if(rs1 > 0) pc += imm`                      | Branch       |
| `ble`           | Branch Less or Equal (pseudoinstruction) | `ble rs1, rs2, imm`   | `if(rs1 ≤ rs2) pc += imm`                    | Branch       |
| `bleu`          | Branch Less or Equal Unsigned (pseudoinstruction) | `bleu rs1, rs2, imm` | `if(rs1 ≤ rs2) pc += imm`                | Branch       |
| `blez`          | Branch Less or Equal Zero (pseudoinstruction) | `blez rs1, imm`       | `if(rs1 ≤ 0) pc += imm`                      | Branch       |
| `bge`           | Branch Greater or Equal     | `bge rs1, rs2, imm`         | `if(rs1 ≥ rs2) pc += imm`                    | Branch       |
| `bgeu`          | Branch Greater or Equal Unsigned | `bgeu rs1, rs2, imm` | `if(rs1 ≥ rs2) pc += imm`                  | Branch       |
| `bgez`          | Branch Greater or Equal Zero (pseudoinstruction) | `bgez rs1, imm`   | `if(rs1 ≥ 0) pc += imm`                      | Branch       |

**Notes:**
- Labels can be used in place of immediate values for branch instructions.

### Example:
```assembly
beq t0, t1, equal_label    # If t0 == t1, jump to equal_label
bnez t2, not_zero_label    # If t2 != 0, jump to not_zero_label
blt t3, t4, less_than_label # If t3 < t4, jump to less_than_label
```

---

## Set Instructions

Set register values based on comparisons.

| **Instruction** | **Description**             | **Usage**                   | **Result**                                    | **Guide**    |
|-----------------|-----------------------------|-----------------------------|-----------------------------------------------|--------------|
| `slt`           | Set Less Than               | `slt rd, rs1, rs2`          | `rd = (rs1 < rs2)`                            | Set          |
| `slti`          | Set Less Than Immediate      | `slti rd, rs1, imm`         | `rd = (rs1 < imm)`                            | Set          |
| `sltu`          | Set Less Than Unsigned      | `sltu rd, rs1, rs2`         | `rd = (rs1 < rs2)`                            | Set          |
| `sltiu`         | Set Less Than Immediate Unsigned | `sltiu rd, rs1, imm`    | `rd = (rs1 < imm)`                            | Set          |
| `seqz`          | Set Equal Zero (pseudoinstruction) | `seqz rd, rs1`          | `rd = (rs1 == 0)`                             | Set          |
| `snez`          | Set Not Equal Zero (pseudoinstruction) | `snez rd, rs1`        | `rd = (rs1 ≠ 0)`                             | Set          |
| `sltz`          | Set Less Than Zero (pseudoinstruction) | `sltz rd, rs1`        | `rd = (rs1 < 0)`                              | Set          |
| `sgtz`          | Set Greater Than Zero (pseudoinstruction) | `sgtz rd, rs1`      | `rd = (rs1 > 0)`                              | Set          |

### Example:
```assembly
slt t0, t1, t2        # t0 = (t1 < t2)
slti t3, t0, 5        # t3 = (t0 < 5)
seqz t4, t3           # t4 = (t3 == 0)
```

---

## Counter Instructions

Access CPU cycle and instruction counters. *Note: These instructions require the Zicntr and Zicsr extensions and are not yet available in all implementations.*

| **Instruction** | **Description**                 | **Usage**                    | **Result**                                       | **Guide**    |
|-----------------|---------------------------------|------------------------------|--------------------------------------------------|--------------|
| `rdcycle`       | CPU Cycle Count (pseudoinstruction) | `rdcycle rd`              | `rd = csr_cycle[31:0]`                            | Not Available |
| `rdcycleh`      | CPU Cycle Count High (pseudoinstruction) | `rdcycleh rd`            | `rd = csr_cycle[63:32]`                           | Not Available |
| `rdtime`        | Current Time (pseudoinstruction)     | `rdtime rd`               | `rd = csr_time[31:0]`                             | Not Available |
| `rdtimeh`       | Current Time High (pseudoinstruction) | `rdtimeh rd`             | `rd = csr_time[63:32]`                            | Not Available |
| `rdinstret`     | CPU Instructions Retired (pseudoinstruction) | `rdinstret rd`      | `rd = csr_instret[31:0]`                          | Not Available |
| `rdinstreth`    | CPU Instructions Retired High (pseudoinstruction) | `rdinstreth rd`    | `rd = csr_instret[63:32]`                         | Not Available |

---

## Miscellaneous Instructions

Additional instructions for various purposes.

| **Instruction** | **Description**                          | **Usage**                   | **Result**                                    | **Guide**    |
|-----------------|------------------------------------------|-----------------------------|-----------------------------------------------|--------------|
| `ebreak`        | Environment Break (Debugger Call)        | `ebreak`                    | -                                             | Not Available |
| `ecall`         | Environment Call (OS Function)           | `ecall`                     | -                                             | Not Available |
| `fence`         | I/O Ordering                             | `fence`                     | -                                             | Not Available |
| `mv`            | Copy Register (pseudoinstruction)        | `mv rd, rs1`                | `rd = rs1`                                   | Arithmetic    |
| `nop`           | No Operation (pseudoinstruction)         | `nop`                       | -                                             | Arithmetic    |

**Notes:**
- The `fence` instruction requires the **Zifencei** extension.

### Example:
```assembly
mv t0, t1            # t0 = t1
nop                  # No operation
ecall                # Environment call
```

---

## Instruction Terminology

Understanding the terminology used in RISC-V assembly instructions.

| **Term**  | **Description**                                    |
|-----------|----------------------------------------------------|
| `imm`     | Immediate value (normally sign-extended)            |
| `mem`     | Memory                                             |
| `(p)`     | Pseudoinstruction                                   |
| `pc`      | Program counter                                     |
| `pc+4`    | Next instruction on RV32                            |
| `ra`      | Return address register (x1)                       |
| `rd`      | Destination register                                 |
| `rs1`     | First source register                                |
| `rs2`     | Second source register                               |
| `symbol`  | Symbol (may be a label in assembly)                  |

---

## RV32 ABI Registers

Overview of the ABI (Application Binary Interface) registers for RV32.

| **ABI Name** | **Register** | **Description**                | **Preserved** |
|--------------|--------------|--------------------------------|---------------|
| `zero`       | `x0`         | Always 0 (zero)                 | N/A           |
| `ra`         | `x1`         | Return address                  | No            |
| `sp`         | `x2`         | Stack pointer                   | Yes           |
| `gp`         | `x3`         | Global pointer*                 | N/A           |
| `tp`         | `x4`         | Thread pointer*                 | N/A           |
| `t0`         | `x5`         | Temporary                        | No            |
| `t1`         | `x6`         | Temporary                        | No            |
| `t2`         | `x7`         | Temporary                        | No            |
| `fp (s0)`    | `x8`         | Frame pointer†                   | Yes           |
| `s1`         | `x9`         | Saved register                    | Yes           |
| `a0`         | `x10`        | Function argument‡                | No            |
| `a1`         | `x11`        | Function argument‡                | No            |
| `a2`         | `x12`        | Function argument                  | No            |
| `a3`         | `x13`        | Function argument                  | No            |
| `a4`         | `x14`        | Function argument                  | No            |
| `a5`         | `x15`        | Function argument                  | No            |
| `a6`         | `x16`        | Function argument                  | No            |
| `a7`         | `x17`        | Function argument                  | No            |
| `s2`         | `x18`        | Saved register                    | Yes           |
| `s3`         | `x19`        | Saved register                    | Yes           |
| `s4`         | `x20`        | Saved register                    | Yes           |
| `s5`         | `x21`        | Saved register                    | Yes           |
| `s6`         | `x22`        | Saved register                    | Yes           |
| `s7`         | `x23`        | Saved register                    | Yes           |
| `s8`         | `x24`        | Saved register                    | Yes           |
| `s9`         | `x25`        | Saved register                    | Yes           |
| `s10`        | `x26`        | Saved register                    | Yes           |
| `s11`        | `x27`        | Saved register                    | Yes           |
| `t3`         | `x28`        | Temporary                        | No            |
| `t4`         | `x29`        | Temporary                        | No            |
| `t5`         | `x30`        | Temporary                        | No            |
| `t6`         | `x31`        | Temporary                        | No            |

**Notes:**
- \* Let the compiler/linker use the global `gp` and thread `tp` pointers; ignore them in your own code.
- † The frame pointer `fp` supports local variables but can be used as a regular saved register.
- ‡ Argument registers `a0` and `a1` also handle the function return value.

---

## RISC-V Concepts

Key concepts to understand when working with RISC-V assembly:

- **Extensions:** RISC-V is modular, allowing for different extensions (e.g., M for Multiply/Divide, A for Atomic, etc.) to add functionality.
- **Base Instruction Set:** This cheat sheet focuses on the base integer instruction set (RV32I).
- **Pseudoinstructions:** These are simplified instructions that are translated into one or more actual RISC-V instructions by the assembler.

---

## Usage Examples

Below are examples demonstrating how to use various RISC-V instructions in assembly code.

### Example 1: Simple Arithmetic Operations

```assembly
.section .text
.globl main

main:
    li t0, 10          # Load immediate 10 into t0
    li t1, 20          # Load immediate 20 into t1
    add t2, t0, t1     # t2 = t0 + t1 (30)
    sub t3, t1, t0     # t3 = t1 - t0 (10)
    mul t4, t2, t3     # t4 = t2 * t3 (300)
    ecall              # Exit program
```

### Example 2: Branching Based on Comparison

```assembly
.section .text
.globl main

main:
    li t0, 5           # t0 = 5
    li t1, 10          # t1 = 10
    blt t0, t1, less_than_label  # If t0 < t1, jump to less_than_label
    j end_label        # Else, jump to end_label

less_than_label:
    li a0, 1           # Set a0 to 1 (indicating true)
    j end_label

end_label:
    li a0, 0           # Set a0 to 0 (indicating false)
    ecall              # Exit program
```

### Example 3: Function Call and Return

```assembly
.section .text
.globl main

main:
    jal ra, function_label  # Jump to function_label and save return address
    li a0, 0               # Set return value to 0
    ecall                  # Exit program

function_label:
    addi sp, sp, -16       # Allocate stack space
    sw ra, 12(sp)          # Save return address
    li t0, 42              # Perform some operations
    lw ra, 12(sp)          # Restore return address
    addi sp, sp, 16        # Deallocate stack space
    jalr ra, 0(ra)         # Return to caller
```

---

## Additional Resources

- [Project F RISC-V Assembler Guide](#)
- [RISC-V Specification](https://riscv.org/technical/specifications/)

---

*This cheat sheet covers the base integer instruction set (RV32I) and some standard extensions. Make sure to consult the official RISC-V documentation for comprehensive information and updates.*
