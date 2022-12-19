r = ["00" for _ in range(16)]
add = ["00" for _ in range(256)]

def writememorytotext():
    memoryfile = open("memory.txt","w")
    x = 00
    while True:
        address = hex(x).upper() if x > 15 else hex(x).replace("0x","0x0").upper()
        memoryfile.write(f"{address}           {add[x]}{add[x+1]}\n")
        x += 2
        if x >= 256:
            memoryfile.close()
            break

def writeregistrytotext():
    registryfile = open("registry.txt","w")
    x = 00
    while True:
        address = hex(x).upper() if x > 15 else hex(x).replace("0x","0x0").upper()
        registryfile.write(f"{address}           {r[x]}\n")
        x += 1
        if x >= 16:
            registryfile.close()
            break

def writeinstructionstomemory():
    instructionsfile = open("instructions.txt")
    instructions = instructionsfile.read()
    instructionsfile.close()

    #Remove Comments
    l = instructions.split("\n")
    x = 0
    c = []
    for i in l:
        i = i.replace("     "," ") #Tab to Space
        if i == "" or i[0] =="#" or i[0] == "/":
            c.append(i)
        elif i.count(" ") != 1:
            l[x] = f"{i.split()[0]} {i.split()[1]}"
        x+=1  
    for j in c:
        l.remove(j)
    del c,j,i,x
    #Insert to Memory 
    for i in l:
        ins = i.split()
        if len(ins[1]) == 2:
            address = int(ins[0], base=16)
            add[address] = ins[1]
        if len(ins[1]) == 4:
            address = int(ins[0], base=16)
            add[address] = ins[1][0] + ins[1][1]
            add[address + 1] = ins[1][2] + ins[1][3]
    del i,address,ins,instructions,instructionsfile,l

counter = 00
con = True

def executeinstruction(code):
    opcode = code[0]

    if opcode == "0":
        return ["CON"]

    elif opcode == "1":
        #Load From Memory    
        address = int(code[2], base=16) * 16 + int(code[3], base=16)
        radd = int(code[1], base=16)
        r[radd] = add[address]

    elif opcode == "2":
        #Load Value
        value = code[2]+ code[3]
        radd = int(code[1], base=16)
        r[radd] = value

    elif opcode == "3":
        #Store or Display
        if code[2] == "0" and code[3] == "0":
            #Display
            outputfile = open("output.txt","a")
            radd = int(code[1], base=16)
            outputfile.write(f"{bytes.fromhex(r[radd])}\n")
            outputfile.close()
            return ["CON"]
        #Store
        address = int(code[2], base=16) * 16 + int(code[3], base=16)
        radd = int(code[1], base=16)
        add[address] = r[radd]
    
    elif opcode == "4":
        #Copy contents
        orad = int(code[2], base=16)
        nrad = int(code[3], base=16)
        r[nrad] = r[orad]
    
    elif opcode == "5":
        #Add (twos complement)
        s = int(code[2], base=16) 
        t = int(code[3], base=16)
        s = int(r[s],base=16)
        t = int(r[t],base=16)
        radd = int(code[1], base=16)
        r[radd] = hex(s + t).replace("0x","").upper() if len(hex(s + t).replace("0x","").upper()) > 1 else f"0{hex(s + t).replace('0x','').upper()}"

    elif opcode == "6":
        #Add (floating point)
        s = int(code[2], base=16) 
        t = int(code[3], base=16)
        s = int(r[s],base=16)
        t = int(r[t],base=16)
        radd = int(code[1], base=16)
        r[radd] = hex(s + t).replace("0x","").upper() if len(hex(s + t).replace("0x","").upper()) > 1 else f"0{hex(s + t).replace('0x','').upper()}"
    
    elif opcode == "7":
        #OR
        s = int(code[2], base=16) 
        t = int(code[3], base=16)
        s = int(r[s],base=16)
        t = int(r[t],base=16)
        radd = int(code[1], base=16)
        result = s | t
        result = hex(result).replace("0x","").upper() if len(hex(result).replace("0x","").upper()) > 1 else f"0{hex(result).replace('0x','').upper()}"
        r[radd] =result 

    elif opcode == "8":
        #AND
        s = int(code[2], base=16) 
        t = int(code[3], base=16)
        s = int(r[s],base=16)
        t = int(r[t],base=16)
        radd = int(code[1], base=16)
        result = s & t
        result = hex(result).replace("0x","").upper() if len(hex(result).replace("0x","").upper()) > 1 else f"0{hex(result).replace('0x','').upper()}"
        r[radd] = result

    elif opcode == "9":
        #XOR
        s = int(code[2], base=16) 
        t = int(code[3], base=16)
        s = int(r[s],base=16)
        t = int(r[t],base=16)
        radd = int(code[1], base=16)
        result = s ^ t
        result = hex(result).replace("0x","").upper() if len(hex(result).replace("0x","").upper()) > 1 else f"0{hex(result).replace('0x','').upper()}"
        r[radd] = result

    elif opcode == "A":
        #ROTATE 
        t = int(code[3], base=16)
        radd = int(code[1], base=16)
        num = int(r[radd],base=16)
        num = num >> t
        num = hex(num).replace("0x","").upper() if len(hex(num).replace("0x","").upper()) > 1 else f"0{hex(num).replace('0x','').upper()}"
        r[radd] = num 

    elif opcode == "B":
        #Jump
        address = int(code[2], base=16) * 16 + int(code[3], base=16)
        radd = int(code[1], base=16)
        if r[0] == r[radd]:
            return ["JMP",address]

    elif opcode == "C":
        if code[1] == code[2] == code[3] == "0":
            #Terminate
            return ["TER"]
            
    elif code[2] == code[3] == "0":
        return ["CON"]
    else:
        print("ERROR EXECUTING INSTRUCTION")
        exit(-3)
    return ["CON"]

print("Starting Up")
print("Adding Instructions")
writeinstructionstomemory()
print("Instructions Added")

print("Starting to Execute")
while counter < 256:
    ocounter = counter
    ret = executeinstruction(add[counter] + add[counter + 1])
    if ret[0] == "TER": con = False
    if ret[0] == "JMP": counter = ret[1]
    if not con: break
    counter = counter + 2 if ocounter == counter else counter
print("Execute Finished")

print("Writing Memory to File")
writememorytotext()
print("Done")
print("Writing Registry to File")
writeregistrytotext()
print("Done")
print("Finished")