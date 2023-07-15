# Designing New Instructions (BONUS)

The following instructions have been created and added in the functioning of Assembler and Simulator:

|  Opcode  | Instruction | Semantics | Syntax | Type |
| :------: | :---------: | :------: | :------: | :------:|
|  10101   | Swap | Swaps the value stored in two registers i.e. reg1,reg2=reg2,reg1 | swap reg1 reg2|    C      |
|11011   |  Rotate Left  |   Rotates the value of the binary representation by specified bits towards left i.e. the value shifts towards left and the value at front goes to back       |      rl reg1 $Imm    |      B    |
| 10111   |  Rotate Right |  Rotates the value of the binary representation by specified bits towards right i.e. the value shifts towrds right and the value at back goes to front      |     rr reg1 $Imm     |     B     |
| 10110    |    Reverse         |     Reverses the value of the binary in reg1 and stores it in reg2   |     rev reg1 reg2     |     C     |
| 11110   |     Nand        |    Performs the nand operation of binary values stored in reg1 and reg2 and stores it in reg3      |     nand reg3 reg1 reg2     |     A     |