# Assembler
The [Simple-Assembler](https://en.wikipedia.org/wiki/Assembly_language) is the first part of the project assigned under the Computer Organisation (CSE112) course. It consists of 2 files:

## parameters.py 
The file consists of all the parameters being used. It consists of 3 dictionaries:

- registers: which consists of registers (which are not case-sensitive) names and their addresses.

- opcode: which consists of instructions and their opcodes.

- type: which includes instructions and their type.

## assembler.py
The file contains the main code which includes:

- Functions for the binary encoding of the types A to F.

- Functions for checking the errors which consists of any kind of syntax errors and all the error handling cases mentioned in the comments of the file.

- Finally the code in the `main` section which reads the input from `stdin` and converts it into machine code according to types, opcodes and instructions in `parameters.py` file and displays it in `stdout`.

### Running the file
To run the file, clone the repository in the device and navigate to the automatedTesting folder after making all run files executable.

To run the Assembler, run the following command on Linux:
```
./run --no-sim
```

# Simulator
The [Simple-Simulator](https://en.wikipedia.org/wiki/Trace-based_simulation) is the second part of the project assigned under the Computer Organisation (CSE112) course. It consists of 2 files:

## parameters2.py 
The file consists of all the parameters being used. It consists of 2 dictionaries:

- registers2: which consists of registers (which are not case-sensitive) names and their addresses as keys.

- opcode2: which consists of instructions and their opcodes as keys.

## simulator.py
The file contains the main code which includes:

- Functions for extracting the registers and immediate value according to the syntax of the instruction for that opcode.

- Functions calculation purposes according to the instructions.

- A list to store the memory being used in the entire code.

- Finally the code in the `main` section which reads the input from `stdin` and generates the trace and the memory used and displays it in `stdout`.

### Running the file
To run the file, clone the repository in the device and navigate to the automatedTesting folder after making all run files executable.

To run the Simulator, run the following command on Linux:
```
./run --no-asm
```

## Running both
To run both Assembler and Simulator, run the following command on Linux:
```
./run
```

# Floating point
Following have been added to Assembler and Simulator to handle floating point numbers:

- Functions for conversions of binary to decimal and vice versa.

- Functions to implement addf, subf and movf.