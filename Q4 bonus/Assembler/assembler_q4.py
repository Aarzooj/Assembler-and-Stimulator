#assembler

'''Group members:
1. Aarzoo (2022008)
2. Anish Jain (2022077)
3. Anushka Srivastava (2022086)
4. Divyasha Priyadarshini (2022180)'''

import sys
from parameters import opcode,registers,type

def float_to_binary(number):
    if number == 0:
        return "0"  
    if number < 0:
        print("Invalid immediate value. (Negative number)")
        sys.exit()
    binary = ""
    fraction = number - int(number)
    integer_part = abs(int(number))
    while integer_part > 0:
        binary = str(integer_part % 2) + binary
        integer_part //= 2
    binary += "."
    max_digits = 16  
    while fraction > 0 and len(binary) <= max_digits:
        fraction *= 2
        bit = int(fraction)
        binary += str(bit)
        fraction -= bit
    return binary

def binary_to_rep(binary):
    str_binary = str(binary)
    split = str_binary.split(".")
    i = 0
    while split[0] != "1":
        if split[0] == "":
            i = i - 1
            if split[1][0] == "0":
                split[1] = split[1][1:]
            else:
                split[0] = "1"
                split[1] = split[1][1:]
        else:
            i = len(split[0]) - 1
            split[1] = split[0][1:] + split[1]
            split[0] = "1"    
    return(split[0] + "." + split[1], i)

def truncate(binary, exp):
    if exp < -3 or exp > 4:
        print("Error : Exponent out of range")
        sys.exit()
    split = binary.split(".")
    mantissa = split[1]
    if len(mantissa) > 8:
        print("Error : Mantissa out of range")
        sys.exit()
    final_mantissa = mantissa.ljust(5,"0")
    bias_exp = exp + 3
    bin_exp = bin(bias_exp)[2:]
    final_exp = bin_exp.zfill(3)
    return(final_exp + final_mantissa)

def float_to_rep(number):
    binary_representation = float_to_binary(number)
    standard_form, exponent = binary_to_rep(binary_representation)
    final_ans = truncate(standard_form, exponent)
    return final_ans

#Type A
def add(reg1, reg2, reg3):
        return(opcode["add"] + "00" + registers[reg1] + registers[reg2] + registers[reg3])

def sub(reg1, reg2, reg3):
        return(opcode["sub"] + "00" + registers[reg1] + registers[reg2] + registers[reg3])

def mul(reg1, reg2, reg3):
        return(opcode["mul"] + "00" + registers[reg1] + registers[reg2] + registers[reg3])

def xor(reg1, reg2, reg3):
        return(opcode["xor"] + "00" + registers[reg1] + registers[reg2] + registers[reg3])

def orr(reg1, reg2, reg3):
        return(opcode["or"] + "00" + registers[reg1] + registers[reg2] + registers[reg3])

def andd(reg1, reg2, reg3):
        return(opcode["and"] + "00" + registers[reg1] + registers[reg2] + registers[reg3])

def addf(reg1, reg2, reg3):
        return(opcode["addf"] + "00" + registers[reg1] + registers[reg2] + registers[reg3])

def subf(reg1, reg2, reg3):
        return(opcode["addf"] + "00" + registers[reg1] + registers[reg2] + registers[reg3])

#Type B 
def mov_addr(reg1,num):
        binary=bin(int(num))[2:]
        if len(binary)<7:
                binary="0"*(7-len(binary))+binary
        return (opcode["mov$"]+"0"+registers[reg1]+binary)

def rshift(reg1,num):
        binary=bin(int(num))[2:]
        if len(binary)<7:
                binary="0"*(7-len(binary))+binary
        return (opcode["rs"]+"0"+registers[reg1]+binary)

def lshift(reg1,num):
        binary=bin(int(num))[2:]
        if len(binary)<7:
                binary="0"*(7-len(binary))+binary
        return (opcode["ls"]+"0"+registers[reg1]+binary)

#Modified Type B
def movf(reg1, num):
        std_rep = float_to_rep(num)
        return (opcode["movf"] + registers[reg1] + std_rep)

#Type C
def mov(reg1, reg2):
        return(opcode["mov"] + "00000" + registers[reg1] + registers[reg2])

def div(reg1, reg2):
        return(opcode["div"] + "00000" + registers[reg1] + registers[reg2])

def nott(reg1, reg2):
        return(opcode["not"] + "00000" + registers[reg1] + registers[reg2])

def cmp(reg1, reg2):
        return(opcode["cmp"] + "00000" + registers[reg1] + registers[reg2])

#Type D
def ld(reg1, addr):
    return(opcode["ld"] + "0" + registers[reg1] + addr)

def st(reg1, addr):
    return(opcode["st"] + "0" + registers[reg1] + addr)

#Type E
def jmp(mem_addr):
        return(opcode["jmp"] + "0000" + mem_addr)

def jlt(mem_addr):
        return(opcode["jlt"] + "0000" + mem_addr)

def jgt(mem_addr):
        return(opcode["jgt"] + "0000" + mem_addr)

def je(mem_addr):
        return(opcode["je"] + "0000" + mem_addr)

#Type F
def hlt():
    return(opcode["hlt"] + "00000000000")

#Bonus functions

def swap(reg1, reg2):
    return(opcode["swap"] + "00000" + registers[reg1] + registers[reg2])

def rr(reg1,num):
        binary=bin(int(num))[2:].zfill(7)
        return (opcode["rr"]+"0"+registers[reg1]+binary)

def rl(reg1,num):
        binary=bin(int(num))[2:].zfill(7)
        return (opcode["rl"]+"0"+registers[reg1]+binary)

def rev(reg1,reg2):
        return (opcode["rev"]+"00000"+registers[reg1]+registers[reg2])

def nand(reg1, reg2, reg3):
        return(opcode["nand"] + "00" + registers[reg1] + registers[reg2] + registers[reg3])

       

instructions=["add","sub","addf","subf","mov","movf","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt","swap","rr","rl","rev","nand"]
reg=["R0","R1","R2","R3","R4","R5","R6","FLAGS","r0","r1","r2","r3","r4","r5","r6","flags"]

variables_a=[]
variables_u=[]
label_a=[]
label_u=[]

def checkerror():
        f0=syntax_error()
        if f0==1:
               sys.exit()
        f1 = error_handling1(instructions,reg)
        f6=error_handling6()
        if f6==0:
                f2 = error_handling2(variables_a,variables_u)
                f3 = error_handling3(label_a,label_u)
        else:
               f2=0
               f3=0
        f4 = error_handling4()
        f5 = error_handling5()
        f7=error_handling7()
        f8=errorhandling8(0)
        f9=errorhandling9()
        if any([f1,f2,f3,f4,f5,f6,f7,f8,f9]) == 1:
                sys.exit()
        else:
                return

#checking for correct syntax used
def syntax_error():
       f=0
       for i in lines:
              if i.split()[0]=="var":
                     if len(i.split())!=2:
                            f=1
                            line_no=lines.index(i)+1
                            print(f"Invalid syntax used to define variable in line {line_no}\n")
              else:
                     if ":" in i:
                            instruct=i.split(":")
                            if len(instruct[1])==0 or instruct[1].isspace()==1:
                                   f=1
                                   line_no=lines.index(i)+1
                                   print(f"Invalid syntax used in line {line_no}\n")
                            else:
                                   f=checksyntax(i)
                     else:
                            f=checksyntax(i)
              if f==1:
                     break
       return f

def checksyntax(line):
       f=0
       if ":" in line:
              i=line.split(":")[1].strip()
       else:
              i=line.strip()
       if i.split()[0] not in type:
              return 0
       if type[i.split()[0]]=="A":
              if len(i.split())!=4:
                     f=1
                     line_no=lines.index(line)+1
                     print(f"Invalid syntax used in line {line_no}\n")
       elif type[i.split()[0]]=="B":
              if len(i.split())!=3 or "$" not in i.split()[2]:
                     f=1
                     line_no=lines.index(line)+1
                     print(f"Invalid syntax used in line {line_no}\n")
       elif type[i.split()[0]]=="C":
              if len(i.split())!=3:
                     f=1
                     line_no=lines.index(line)+1
                     print(f"Invalid syntax used in line {line_no}\n")
       elif type[i.split()[0]]=="D":
              if len(i.split())!=3:
                     f=1
                     line_no=lines.index(line)+1
                     print(f"Invalid syntax used in line {line_no}\n")
       elif type[i.split()[0]]=="E":
              if len(i.split())!=2:
                     f=1
                     line_no=lines.index(line)+1
                     print(f"Invalid syntax used in line {line_no}\n")
       elif type[i.split()[0]]=="F":
              if len(i.split())!=1:
                     f=1
                     line_no=lines.index(line)+1
                     print(f"Invalid syntax used in line {line_no}\n")
       else:
              return 0
       return f

#Typos in instruction name or register name
def error_handling1(instructions,reg):
        f=0
        for i in lines:    
                if i.split()[0]!="var":
                        if ":" in i:
                                instruct=i.split(":")[1].split()[0]
                                if instruct not in instructions:
                                        f=1
                                        line_no=lines.index(i)+1
                                        print(f"Syntax error: Invalid instruction used in line {line_no}\n")               
                        else:
                                instruct=i.split()[0]
                                if instruct not in instructions:
                                        f=1
                                        line_no=lines.index(i)+1
                                        print(f"Syntax error: Invalid instruction used in line {line_no}\n")
                if i.split()[0]!="var":
                        reg_inst=[]
                        if ":" in i:
                               instruct=i.split(":")[1].split()
                        else:
                                instruct=i.split()
                        if (instruct[0]=="add" or instruct[0]=="sub" or instruct[0]=="mul" or instruct[0]=="xor" or instruct[0]=="or" or  instruct[0]=="and" or instruct[0]=="addf" or instruct[0]=="subf" or instruct[0]=="nand"):
                                reg_inst.extend([instruct[1],instruct[2],instruct[3]])
                                for j in reg_inst:
                                        if j not in reg:
                                                f=1
                                                line_no=lines.index(i)+1
                                                print(f"Syntax error: Invalid register used in line {line_no}\n") 
                        elif(instruct[0]=="ld" or instruct[0]=="st" or instruct[0]=="rs"or instruct[0]=="ls" or instruct[0]=="rr" or instruct[0]=="rl"):
                                reg_inst.append(instruct[1])
                                for j in reg_inst:
                                        if j not in reg:
                                                f=1
                                                line_no=lines.index(i)+1
                                                print(f"Syntax error: Invalid register used in line {line_no}\n")
                        elif(instruct[0]=="div" or instruct[0]=="not" or instruct[0]=="cmp" or instruct[0]=="swap" or instruct[0]=="rev"):
                                reg_inst.extend([instruct[1],instruct[2]])
                                for j in reg_inst:
                                        if j not in reg:
                                                f=1
                                                line_no=lines.index(i)+1
                                                print(f"Syntax error: Invalid register used in line {line_no}\n")
                        elif (instruct[0]=="mov" or instruct[0]=="movf"):
                                if "$" in instruct[2]:  
                                        reg_inst.append(instruct[1])
                                        for j in reg_inst:
                                                if j not in reg:
                                                        f=1
                                                        line_no=lines.index(i)+1
                                                        print(f"Syntax error: Invalid register in line {line_no}\n")
                                else:
                                        reg_inst.extend([instruct[1],instruct[2]])
                                        for j in reg_inst:
                                                if j not in reg:
                                                        f=1
                                                        line_no=lines.index(i)+1
                                                        print(f"Syntax error: Invalid register in line {line_no}\n") 
        return f

#Misuse of labels as variables or vice-versa
def error_handling6():
        f=0
        for i in lines: 
                if checksyntax(i)==1:
                        sys.exit()      
                if i.split()[0]=="var":
                        variables_a.append(i.split()[1])
                elif i.split()[0]=="ld" or i.split()[0]=="st":
                        variables_u.append([i,i.split()[2]])
                for i in lines:
                        if ":" in i:
                                label_u.append(i.split(":")[0])
                for i in lines: 
                        if i.split()[0]=="jmp" or i.split()[0]=="jlt" or i.split()[0]=="jgt" or i.split()[0]=="je":
                                label_a.append([i,i.split()[1]])
        var_u=[i[1] for i in variables_u]
        label_used=[i[1] for i in label_a]
        if list(set(var_u).intersection(label_u))!=[]:
               f=1
               ele=list(set(var_u).intersection(label_u))
               print(f"Error: Misuse of label {ele} as a variable\n")
        if list(set(label_used).intersection(variables_a))!=[]:
               f=1
               ele=list(set(label_used).intersection(variables_a))
               print(f"Error: Misuse of variable {ele} as label\n")
        return f

#Use of undefined variables
def error_handling2(variables_a,variables_u):
        f=0
        for j in variables_u:
            if j[1] not in variables_a:
                f=1
                line_no=lines.index(j[0])+1
                print(f"Syntax error: Use of undefined variable {j[1]} in line {line_no}\n") 
        return f

#Use of undefined labels   
def error_handling3(label_a,label_u):
        f=0
        for j in label_a:
            if j[1] not in label_u:
                f=1
                line_no=lines.index(j[0])+1
                print(f"Syntax error: Use of undefined label {j[1]} in line {line_no}\n")
        return f

#Illegal use of FLAGS register
def error_handling4():
    f=0
    for i in lines:
        regs = []        
        if ":" in i:
            instruct = i.split(":")[1].split()
        else:
            instruct = i.split()
                    
        if instruct[0] == "add" or instruct[0] == "sub" or instruct[0] == "mul" or instruct[0] == "xor" or instruct[0] == "or" or instruct[0] == "and" or instruct[0]=="addf" or instruct[0]=="subf" or instruct[0]=="nand":
            regs.append(instruct[1])
            regs.append(instruct[2])
            regs.append(instruct[3])
            
        elif instruct[0] == "mov" or instruct[0] == "rs" or instruct[0] == "ls" or instruct[0]=="movf" or (instruct[0] in ["rr","rl"]):
            regs.append(instruct[1])
                
        elif instruct[0] == "div" or instruct[0] == "not" or instruct[0] == "cmp" or (instruct[0] in ["swap","rev"]):
            regs.append(instruct[1])
            regs.append(instruct[2])
            
        elif instruct[0] == "ld" or instruct[0] == "st":
            regs.append(instruct[1])
            
        if "FLAGS" in regs:
            f=1
            line_no=lines.index(i) + 1
            print(f"Syntax error: Illegal use of FLAGS register in line {line_no}\n")
    return f

#Illegal Immediate values (more than 7 bits)
def error_handling5():
        imm_values=[str(i) for i in range(128)]
        f = 0
        for i in lines:
                if ":" in i:
                        instruct = i.split(":")[1].split()
                else:
                        instruct = i.split()             
                if instruct[0] == "mov" or instruct[0] == "rs" or instruct[0] == "ls" or instruct[0] == "rr" or instruct[0] == "rl":                     
                        if instruct[2][0] == "$":                      
                                imm_value = instruct[2][1:]                      
                                if imm_value not in imm_values:                               
                                        f = 1
                                        line_no=lines.index(i) + 1
                                        print(f"Syntax error: Illegal immediate value in line {line_no}\n")       
        return f

#Variables not declared at the beginning
def error_handling7():
        l=[]
        f=0
        count=0
        for j in lines:
               l.append(j)
        var_b=[]
        for i in l:
               if i.split()[0]=="var":
                      var_b.append(l.index(i))
        for k in var_b:
                if k>=len(var_b):
                      count+=1
                      ele=l[k].split()[1]
                      print(f"Variable: {ele} not declared at the beginning\n")
        if count!=0:
               f=1
        return f

#Missing hlt instruction
def errorhandling8(t):
        f=1
        for i in lines:
                if ":" in i:
                       if "hlt" in i.split(":")[1].split():
                            f=0
                else:
                     if "hlt" in i.split():
                            f=0
        if f==1 and t==0:
               print("Syntax error: Missing halt instruction\n")
        return f 

#hlt not being used as the last instruction
def errorhandling9():
        if errorhandling8(1)==1:
               return
        f=1
        for i in range(len(lines)):
               if "hlt" in lines[i].split():
                      if i==len(lines)-1:
                             f=0
        if f==1:
               print("Syntax error: hlt not being used as the last instruction\n")
        return f

lines = []

while True:
    line = sys.stdin.readline().strip()
    if not line:
        break
    lines.append(line)

checkerror()
k=0
memory={}
var={}
for i in lines:
        if i.split()[0]!="var":
                pointer=bin(k)[2:]
                if len(pointer)<7:
                        pointer="0"*(7-len(pointer))+pointer
                memory[pointer]=i
                k+=1
        else:
                var[i.split()[1]]=None
for i in var:
        var_bin=bin(k)[2:]
        if len(var_bin)<7:
                var_bin="0"*(7-len(var_bin))+var_bin
        var[i]=var_bin
        k+=1

output=[]

for i in memory:
        if ":" in memory[i]:
                instruct=memory[i].split(":")[1].split()
        else:
                instruct=memory[i].split()
        if instruct[0]=="add":
                output.append(add(instruct[1],instruct[2],instruct[3]))
        elif instruct[0]=="sub":
                output.append(sub(instruct[1],instruct[2],instruct[3]))
        elif instruct[0]=="mul":
                output.append(mul(instruct[1],instruct[2],instruct[3]))
        elif instruct[0]=="addf":
                output.append(addf(instruct[1],instruct[2],instruct[3]))
        elif instruct[0]=="subf":
                output.append(subf(instruct[1],instruct[2],instruct[3]))
        elif instruct[0]=="xor":
                output.append(xor(instruct[1],instruct[2],instruct[3]))
        elif instruct[0]=="or":
                output.append(orr(instruct[1],instruct[2],instruct[3]))
        elif instruct[0]=="and":
                output.append(andd(instruct[1],instruct[2],instruct[3]))
        elif instruct[0]=="nand":
                output.append(nand(instruct[1],instruct[2],instruct[3]))
        elif instruct[0]=="mov":
                if "$" in instruct[2]:
                        output.append(mov_addr(instruct[1],instruct[2][1:]))
                else:
                        output.append(mov(instruct[1],instruct[2]))
        elif instruct[0]=="movf":
                output.append(movf(instruct[1],float(instruct[2][1:])))
        elif instruct[0]=="rs":
                output.append(rshift(instruct[1],instruct[2][1:]))
        elif instruct[0]=="ls":
                output.append(lshift(instruct[1],instruct[2][1:]))
        elif instruct[0]=="div":
                output.append(div(instruct[1],instruct[2]))
        elif instruct[0]=="not":
                output.append(nott(instruct[1],instruct[2]))
        elif instruct[0]=="cmp":
                output.append(cmp(instruct[1],instruct[2]))
        elif instruct[0]=="rev":
                output.append(rev(instruct[1],instruct[2]))
        elif instruct[0]=="ld":
                output.append(ld(instruct[1],var[instruct[2]]))
        elif instruct[0]=="st":
                output.append(st(instruct[1],var[instruct[2]]))
        elif instruct[0] == "swap":
               output.append(swap(instruct[1],instruct[2]))
        elif instruct[0] == "rr":
               output.append(rr(instruct[1],instruct[2][1:]))
        elif instruct[0] == "rl":
               output.append(rl(instruct[1],instruct[2][1:]))
        elif instruct[0] in ["jmp","jlt","jgt","je"]:
                label=instruct[1]
                for j in memory:
                        if memory[j].split(":")[0]==label:
                                address=j
                                break
                if instruct[0]=="jmp":
                        output.append(jmp(address))
                elif instruct[0]=="jlt":
                        output.append(jlt(address))
                elif instruct[0]=="jgt":
                        output.append(jgt(address))
                elif instruct[0]=="je":
                        output.append(je(address))
        elif "hlt" in memory[i]:
                output.append(hlt())
       
for i in output:
        print(i)