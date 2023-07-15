import sys
from parameters2 import registers2

def get_registers_A(inst):
    return registers2[inst[7:10]],registers2[inst[10:13]],registers2[inst[13:16]]

def get_registers_B(inst):
    return registers2[inst[6:9]],inst[9:16].zfill(16)

def get_registers_B_modified(inst):
    return registers2[inst[5:8]],inst[8:16].zfill(16)

def get_registers_C(inst):
    return registers2[inst[10:13]],registers2[inst[13:16]]

def get_registers_D(inst):
    return registers2[inst[6:9]],binary_decimal(inst[9:16])

def get_address_E(inst):
    return binary_decimal(inst[9:16])

def float_to_binary(number):
    if number == 0:
        return "0"
    if number < 0:
        r_values["FLAGS"]=flag_overflow
        return "0"*16
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
        r_values["FLAGS"]=flag_overflow
        return "0"*16
    split = binary.split(".")
    mantissa = split[1]
    if len(mantissa) > 8:
        r_values["FLAGS"]=flag_overflow
        return "0"*16
    final_mantissa = mantissa.ljust(5,"0")
    bias_exp = exp + 3
    bin_exp = bin(bias_exp)[2:]
    final_exp = bin_exp.zfill(3)
    return(final_exp + final_mantissa)

def rep_to_decimal(rep):
    exp = rep[:3]
    mantissa = rep[3:]
    int_exp = (int(exp, 2)) - 3
    mantissa_value = 0.0
    for i in range(len(mantissa)):
        mantissa_value = mantissa_value + float(mantissa[i])*((2)**(-(i+1)))
    return((1+mantissa_value)*(2**(int_exp)))  

def float_to_rep(number):
    binary_representation = float_to_binary(number)
    if binary_representation=="0"*16:
        return binary_representation
    standard_form, exponent = binary_to_rep(binary_representation)
    final_ans = truncate(standard_form, exponent)
    return final_ans    

def decimal_binary(n):  
    x=bin(n).replace("0b","")
    return x.zfill(16)

def binary_decimal(n):    
    x=int(n,2)
    return x

def decimal_binary_pc(k):
    y=bin(k).replace("0b","")  
    return y.zfill(7)

#Type A instructions

def add_op(inst,pc):
    out=""
    count=decimal_binary_pc(pc)
    destination,source_1,source_2=get_registers_A(inst)
    d_source_1=binary_decimal(r_values[source_1])
    d_source_2=binary_decimal(r_values[source_2])
    final=d_source_1+d_source_2
    if not (final >= 0 and final<=((2**16)-1)):
        final=0
        r_values["FLAGS"]=flag_overflow
    r_values[destination]=decimal_binary(final)
    out = count+" "*7
    for y in r_values.values():
        out+=" "
        out+=y  
    return out

def sub_op(inst,pc):
    out=""
    count=decimal_binary_pc(pc)
    destination,source_1,source_2=get_registers_A(inst)
    d_source_1=binary_decimal(r_values[source_1])
    d_source_2=binary_decimal(r_values[source_2])
    final=d_source_1-d_source_2
    if not (final >= 0 and final<=((2**16)-1)):
        final=0
        r_values["FLAGS"]=flag_overflow
    r_values[destination]=decimal_binary(final)
    out = count+" "*7
    for y in r_values.values():
        out+=" "
        out+=y  
    return out

def mul_op(inst,pc):
    out=""
    count=decimal_binary_pc(pc)
    destination,source_1,source_2=get_registers_A(inst)
    d_source_1=binary_decimal(r_values[source_1])
    d_source_2=binary_decimal(r_values[source_2])
    final=d_source_1*d_source_2
    if not (final >= 0 and final<=((2**16)-1)):
        final=0
        r_values["FLAGS"]=flag_overflow
    r_values[destination]=decimal_binary(final)
    out = count+" "*7
    for y in r_values.values():
        out+=" "
        out+=y  
    return out

def xor_op(inst,pc):
    out=""
    count=decimal_binary_pc(pc)
    destination,source_1,source_2=get_registers_A(inst)
    d_source_1=binary_decimal(r_values[source_1])
    d_source_2=binary_decimal(r_values[source_2])
    final=d_source_1^d_source_2
    r_values[destination]=decimal_binary(final)
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out+=" "
        out+=y  
    return out

def or_op(inst,pc):
    out=""
    count=decimal_binary_pc(pc)
    destination,source_1,source_2=get_registers_A(inst)
    d_source_1=binary_decimal(r_values[source_1])
    d_source_2=binary_decimal(r_values[source_2])
    final=d_source_1|d_source_2
    r_values[destination]=decimal_binary(final)
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out+=" "
        out+=y  
    return out

def and_op(inst,pc):
    out=""
    count=decimal_binary_pc(pc)
    destination,source_1,source_2=get_registers_A(inst)
    d_source_1=binary_decimal(r_values[source_1])
    d_source_2=binary_decimal(r_values[source_2])
    final=d_source_1&d_source_2
    r_values[destination]=decimal_binary(final)
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out+=" "
        out+=y  
    return out

def addf_op(inst,pc):
    out=""
    count=decimal_binary_pc(pc)
    destination,source_1,source_2=get_registers_A(inst)
    d_source_1=rep_to_decimal(r_values[source_1])
    d_source_2=rep_to_decimal(r_values[source_2])
    final=d_source_1+d_source_2
    r_values[destination]=float_to_rep(final)
    out = count+" "*7
    for y in r_values.values():
        out+=" "
        out+=y  
    return out

def subf_op(inst,pc):
    out=""
    count=decimal_binary_pc(pc)
    destination,source_1,source_2=get_registers_A(inst)
    d_source_1=rep_to_decimal(r_values[source_1])
    d_source_2=rep_to_decimal(r_values[source_2])
    final=d_source_1-d_source_2
    r_values[destination]=float_to_rep(final)
    out = count+" "*7
    for y in r_values.values():
        out+=" "
        out+=y  
    return out

# Type B instructions

def mov_imm_op(inst, pc):
    out = ""
    count = decimal_binary_pc(pc)
    destination,immediate_value=get_registers_B(inst)
    r_values[destination] = immediate_value
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out

def ls_op(inst, pc):
    out = ""
    count = decimal_binary_pc(pc)
    destination, shift_amount = get_registers_B(inst)
    shift_amount=binary_decimal(shift_amount)
    value = r_values[destination]
    shifted_value = value[shift_amount:] + "0" * shift_amount
    r_values[destination] = shifted_value
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out

def rs_op(inst, pc):
    out = ""
    count = decimal_binary_pc(pc)
    destination, shift_amount = get_registers_B(inst)
    shift_amount=binary_decimal(shift_amount)
    value = r_values[destination]
    shifted_value = "0" * shift_amount + value[:-shift_amount]
    r_values[destination] = shifted_value
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out

def movf_op(inst,pc):
    out = ""
    count = decimal_binary_pc(pc)
    destination,immediate_value=get_registers_B_modified(inst)
    r_values[destination] = immediate_value
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out


# Type C instruction

def mov_reg_op(inst, pc):
    out = ""
    count = decimal_binary_pc(pc)
    destination,source=get_registers_C(inst)
    r_values[destination] = r_values[source]
    r_values[source]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out

def divide_op(inst,pc):
    out = ""
    count = decimal_binary_pc(pc)
    reg3,reg4=get_registers_C(inst)
    value_1=binary_decimal(r_values[reg3])
    value_2=binary_decimal(r_values[reg4])
    if value_2==0:
        r_values["R0"]=decimal_binary(0)
        r_values["R1"]=decimal_binary(0)
        r_values["FLAGS"]=flag_overflow
    else:
        r_values["R0"]=decimal_binary(value_1//value_2)
        r_values["R1"]=decimal_binary(value_1%value_2)
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out

def not_op(inst,pc):
    out = ""
    count = decimal_binary_pc(pc)
    destination,source=get_registers_C(inst)
    d_source_1=r_values[source]
    final=d_source_1.replace("0", "_").replace("1", "0").replace("_", "1")
    r_values[destination]=final
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out

def cmp_op(inst,pc):
    out = ""
    count = decimal_binary_pc(pc)
    reg1,reg2=get_registers_C(inst)
    value_1=binary_decimal(r_values[reg1])
    value_2=binary_decimal(r_values[reg2])
    if value_1>value_2:
        r_values["FLAGS"]=flag_greater_than
    elif value_1<value_2:
        r_values["FLAGS"]=flag_less_than
    else:
        r_values["FLAGS"]=flag_equal
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out
    

# Type D instruction

def ld_op(inst, pc):
    out = ""
    count = decimal_binary_pc(pc)
    destination,memory_address=get_registers_D(inst)
    r_values[destination] = memory[memory_address]
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out

def st_op(inst, pc):
    out = ""
    count = decimal_binary_pc(pc)
    source,memory_address=get_registers_D(inst)
    memory[memory_address] = r_values[source]
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out

# Type E instruction

def jmp_op(inst,pc):
    out = ""
    count = decimal_binary_pc(pc)
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out

def jlt_op(inst,pc):
    out = ""
    count = decimal_binary_pc(pc)
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out[:-16]+"0"*16

def jgt_op(inst,pc):
    out = ""
    count = decimal_binary_pc(pc)
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out[:-16]+"0"*16

def je_op(inst,pc):
    out = ""
    count = decimal_binary_pc(pc)
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out[:-16]+"0"*16

# Type F instruction

def halt_op(inst,pc):
    out = ""
    count = decimal_binary_pc(pc)
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out[:-16]+"0"*16

#Bonus instructions

def swap_op(inst, pc):
    out = ""
    count = decimal_binary_pc(pc)
    source_1, source_2 = get_registers_C(inst)
    r_values[source_1], r_values[source_2] = r_values[source_2], r_values[source_1]
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out

def rr_op(inst,pc):
    out = ""
    count = decimal_binary_pc(pc)
    destination, rotate_amount = get_registers_B(inst)
    rotate_amount=binary_decimal(rotate_amount)
    value = r_values[destination]
    rotated_value = value[-rotate_amount:]+value[:-rotate_amount]
    r_values[destination] = rotated_value
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out

def rl_op(inst,pc):
    out = ""
    count = decimal_binary_pc(pc)
    destination, rotate_amount = get_registers_B(inst)
    rotate_amount=binary_decimal(rotate_amount)
    value = r_values[destination]
    rotated_value = value[rotate_amount:]+value[:rotate_amount]
    r_values[destination] = rotated_value
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out += " "
        out += y
    return out

def nand_op(inst,pc):
    out=""
    count = decimal_binary_pc(pc)
    destination,source_1,source_2=get_registers_A(inst)
    d_source_1=binary_decimal(r_values[source_1])
    d_source_2=binary_decimal(r_values[source_2])
    final=d_source_1&d_source_2
    final=decimal_binary(final)
    final2=final.replace("0", "_").replace("1", "0").replace("_", "1")
    r_values[destination]=final2
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out+=" "
        out+=y  
    return out

def rev_op(inst,pc):
    out=""
    count = decimal_binary_pc(pc)
    destination,source=get_registers_C(inst)
    r_values[destination] = r_values[source][::-1]
    r_values["FLAGS"]="0"*16
    out = count+" "*7
    for y in r_values.values():
        out+=" "
        out+=y  
    return out
# Main function

#input for testing
 
# f=open("stdin.txt","r")

lines = []

while True:
    line = sys.stdin.readline().strip()
    if not line:
        break
    lines.append(line)

r_values={
    "R0":"0"*16,
    "R1":"0"*16,
    "R2":"0"*16,
    "R3":"0"*16,
    "R4":"0"*16,
    "R5":"0"*16,
    "R6":"0"*16,
    "FLAGS":"0"*16
}

k=0
file_instructions={}
memory=["0"*16]*128
pointers=[]
for i in lines:
    pointer=bin(k)[2:].zfill(7)
    pointers.append(pointer)
    file_instructions[pointer]=i.rstrip("\n")
    memory[k]=file_instructions[pointer]
    k+=1

#Flag initialisation
flag_overflow="0"*12+"1000"
flag_less_than="0"*12+"0100"
flag_greater_than="0"*12+"0010"
flag_equal="0"*12+"0001"

i=0
inst=file_instructions[pointers[i]]
while True:
    op_code=inst[0:5]
    if op_code=="0"*5:
        final_result=add_op(inst,i)
    elif op_code=="00001":
        final_result=sub_op(inst,i)
    elif op_code=="00110":
        final_result=mul_op(inst,i)
    elif op_code=="01010":
        final_result=xor_op(inst,i)
    elif op_code=="01011":
        final_result=or_op(inst,i)
    elif op_code=="01100":
        final_result=and_op(inst,i)
    elif op_code=="00010":
        final_result=mov_imm_op(inst,i)
    elif op_code=="00100":
        final_result=ld_op(inst,i)
    elif op_code=="00101":
        final_result=st_op(inst,i)
    elif op_code=="01001":
        final_result=ls_op(inst,i)
    elif op_code=="01000":
        final_result=rs_op(inst,i)
    elif op_code=="00011":
        final_result=mov_reg_op(inst,i)
    elif op_code=="00111":
        final_result=divide_op(inst,i)
    elif op_code=="01101":
        final_result=not_op(inst,i)
    elif op_code=="01110":
        final_result=cmp_op(inst,i)
    elif op_code=="01111":
        final_result=jmp_op(inst,i)
    elif op_code=="11100":
        final_result=jlt_op(inst,i)
    elif op_code=="11101":
        final_result=jgt_op(inst,i)
    elif op_code=="11111":
        final_result=je_op(inst,i)
    elif op_code=="10000":
        final_result=addf_op(inst,i)
    elif op_code=="10001":
        final_result=subf_op(inst,i)
    elif op_code=="10010":
        final_result=movf_op(inst,i)
    elif op_code=="11011":
        final_result=rl_op(inst,i)
    elif op_code=="10111":
        final_result=rr_op(inst,i)
    elif op_code=="10101":
        final_result=swap_op(inst,i)
    elif op_code=="10110":
        final_result=rev_op(inst,i)
    elif op_code=="11110":
        final_result=nand_op(inst,i)
    
    elif op_code=="11010":
        final_result=halt_op(inst,i)
        print(final_result.strip())
        break
    print(final_result.strip())
    if op_code not in ["11100","11101","01111","11111"]:
        i+=1
        inst=file_instructions[pointers[i]]
    elif op_code == "01111":
        mem_address = get_address_E(inst)
        i = mem_address
        inst = file_instructions[pointers[i]]
    elif op_code == "11100":
        if r_values["FLAGS"] == flag_less_than:
            mem_address = get_address_E(inst)
            i = mem_address
            inst = file_instructions[pointers[i]]
            r_values["FLAGS"]="0"*16
        else:
            i+=1
            inst=file_instructions[pointers[i]]
    elif op_code == "11101":
        if r_values["FLAGS"] == flag_greater_than:
            mem_address = get_address_E(inst)
            i = mem_address
            inst = file_instructions[pointers[i]]
            r_values["FLAGS"]="0"*16
        else:
            i+=1
            inst=file_instructions[pointers[i]]
    elif op_code == "11111":
        if r_values["FLAGS"] == flag_equal:
            mem_address = get_address_E(inst)
            i = mem_address
            inst = file_instructions[pointers[i]]
            r_values["FLAGS"]="0"*16
        else:
            i+=1
            inst=file_instructions[pointers[i]]
for i in memory:
    print(i.strip())  