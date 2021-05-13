import sys
import re
#kullanılmamamı gereken sözcükler
keywords = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'sifir', 'bir', 'iki', 'uc', 'dort', 'bes', 'alti', 'yedi', 'sekiz', 'dokuz', 'dogru', 'yanlis', '+', '-', '*', 'arti', 'eksi', 'carpi', 've', 'veya', '(', ')', 'ac-parantez', 'kapa-parantez', 'AnaDegiskenler', 'YeniDegiskenler', 'Sonuc', 'degeri', 'olsun', 'nokta'}
#tanımlanmış değerler
used = []
#tanımlanmış değerlerin type ı
types_used = {}
#işlem olmadan atanabilen değerler
possibilities = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'sifir', 'bir', 'iki', 'uc', 'dort', 'bes', 'alti', 'yedi', 'sekiz', 'dokuz', 'dogru', 'yanlis']
possibilities_num =  ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'sifir', 'bir', 'iki', 'uc', 'dort', 'bes', 'alti', 'yedi', 'sekiz', 'dokuz']
possibilities_log =  ['dogru', 'yanlis']
#rakamların yazı hali
nums_string = ['sifir', 'bir', 'iki', 'uc', 'dort', 'bes', 'alti', 'yedi', 'sekiz', 'dokuz']
f = open("calc.in", "r")
res = open("calc.out", "w")
line_list = list()
for i in f.readlines():
    i = i.strip()
    if not i == '':
        line_list.append(i.strip())

#aşağıdaki if bloğunda her üç bölümün bulunmasına bakıyoruz. eğer yoksa programı kapatıyoruz.
if not (line_list[0] == "AnaDegiskenler" and line_list.count("YeniDegiskenler") == 1 and line_list.count("Sonuc") == 1):
    res.write("Dont Let Me Down")
    res.close()
    f.close()
    sys.exit()
    
#burda her üç bölümü bir listeye atadık. sonradan burda işlemler yapacağız.
init_list = [i for i in line_list[line_list.index("AnaDegiskenler") + 1:line_list.index("YeniDegiskenler")] if not i =='']
mid_list = [j for j in line_list[line_list.index("YeniDegiskenler") + 1:line_list.index("Sonuc")] if not j == '']
fin_list = [k for k in line_list[line_list.index("Sonuc") + 1:] if not k == '']
#Sonuc tek satır olmalı
if len(fin_list) > 1:
    res.write("Dont Let Me Down")
    res.close()
    f.close()
    sys.exit()

#for döngüsüyle init_listte dolaşıp kuralları inceleyeceğiz.
for single_statement in init_list:
    
    single_statement = single_statement.split()
    first = single_statement[0]
    if first.isalnum() == False or len(first) > 10 or first in used or first in keywords:
        res.write("Dont Let Me Down")
        res.close()
        f.close()
        sys.exit()

    if not (single_statement[1] == "degeri" and single_statement[-1] == "olsun"):
        res.write("Dont Let Me Down")
        res.close()
        f.close()
        sys.exit()
    single_statement_value = ' '.join(single_statement[2 : -1])
    if not (single_statement_value in possibilities or re.findall(r"^[0-9]\.?[0-9]$", single_statement_value) == [single_statement_value] or (len(single_statement_value.split()) == 3 and single_statement_value.split()[1] == 'nokta' and single_statement_value.split()[0] in nums_string and single_statement_value.split()[-1] in nums_string)):
        res.write("Dont Let Me Down")
        res.close()
        f.close()
        sys.exit()
    used.append(first)
    if single_statement_value == "dogru" or single_statement_value == "yanlis":
        types_used[first] = "boolean"
    else:
        types_used[first] = "float"

binlop = ["ve", "veya"]
binaop = ['+', '-', '*', 'arti', 'eksi', 'carpi']
open_par = ['(', 'ac-parantez']
clos_par = [')', 'kapa-parantez']

for statement in mid_list:
    
    statement = statement.split()
    first_elem = statement[0]
    if first_elem.isalnum() == False or len(first) > 10 or first_elem in used or first_elem in keywords:
        
        res.write("Dont Let Me Down")
        res.close()
        f.close()
        sys.exit()
    
    if not (statement[1] == "degeri" and statement[-1] == "olsun"):
        
        res.write("Dont Let Me Down")
        res.close()
        f.close()
        sys.exit()
    
    expression = statement[2 : -1]
    
    for k in expression:
        if not(k in possibilities + open_par + clos_par + binaop + binlop + used+ ["nokta"]+ [str(i)+"."+str(j) for i in range(10) for j in range(10)]) :
            
            res.write("Dont Let Me Down")
            res.close()
            f.close()
            sys.exit()
    
    type_expression = ""
    if len(expression) == 1:
        
        expression_str = expression[0]
        if not(expression_str in used or expression_str in possibilities or re.findall(r"^[0-9]\.?[0-9]$", expression_str) == [expression_str]):
            
            res.write("Dont Let Me Down")
            res.close()
            f.close()
            sys.exit()
        if expression_str in used:
            if types_used[expression_str] == "boolean":
                type_expression = "boolean"
            else:
                type_expression = "float" 
        else:
            if expression_str in possibilities_log:
                type_expression = "boolean"
            else:
                type_expression = "float"
    
    else:
        
        expression_str = ' '.join(expression)
        expression_str = expression_str.replace('kapa-parantez', ')')
        expression_str = expression_str.replace('ac-parantez', '(')
        if not(expression_str.count("(") == expression_str.count(")")):
            
            res.write("Dont Let Me Down")
            res.close()
            f.close()
            sys.exit()
        logs = []
        nums = []
        for i,j in types_used.items():
            if j == "boolean":
                logs.append(i)
            elif j == "float":
                nums.append(i)
        possibilities_logg  = logs + possibilities_log
        possibilities_numm = nums + possibilities_num + ["nokta"] + [str(i)+"."+str(j) for i in range(10) for j in range(10)]
        all_possibilities_log = open_par + clos_par + binlop + possibilities_logg
        all_possibilities_bin = open_par + clos_par + binaop + possibilities_numm 
        if len([i for i in expression if i in all_possibilities_bin]) == len(expression):
            #arithmetic operation
            
            #binaopdan sonra binaop gelirse hata verecek.
            if expression[0] == "nokta" or expression[-1] == "nokta":
            
                res.write("Dont Let Me Down")
                res.close()
                f.close()
                sys.exit()
            for l in range(len(expression) - 1):
                if expression[l] == "nokta":
                    if not(expression[l - 1] in nums_string and expression[l + 1] in nums_string):
                        
                        res.write("Dont Let Me Down")
                        res.close()
                        f.close()
                        sys.exit()
            
            new_possibilities_numm = possibilities_numm.copy()
            new_expression = []
            
            for n in range(len(expression) - 1):
                if expression[n + 1] == "nokta" or expression[n - 1] == "nokta":
                    continue
                if expression[n] == "nokta":
                    new_possibilities_numm.append(expression[n - 1] + " " + expression[n] + " " + expression[n + 1])
                    new_expression.append(expression[n - 1] + " " + expression[n] + " " + expression[n + 1])
                elif re.findall(r"^[0-9]\.?[0-9]$", expression[n]) == [expression[n]]:
                    new_possibilities_numm.append(expression[n])
                    new_expression.append(expression[n])
                else:
                    new_expression.append(expression[n])
            if expression[-2] != "nokta":
                new_expression.append(expression[-1])
            
            for i in range(len(new_expression)):
                if i == 0: 
                    if new_expression[i] in binaop or new_expression[i] in clos_par:
                        
                        res.write("Dont Let Me Down")
                        res.close()
                        f.close()
                        sys.exit()
                elif i == len(new_expression) - 1:
                    if new_expression[i] in binaop or new_expression[i] in open_par:
                        
                        res.write("Dont Let Me Down")
                        res.close()
                        f.close()
                        sys.exit() 
                else:
                    #####all_possibilities_bin = open_par + clos_par + binaop + new_possibilities_numm######
                    if new_expression[i] in binaop:
                        if new_expression[i + 1] in binaop or new_expression[i + 1] in clos_par or new_expression[i - 1] in open_par or new_expression[i - 1] in binaop: 
                            
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit()
                    elif new_expression[i] in clos_par:
                        if new_expression[i - 1] in open_par or new_expression[i + 1] in open_par or new_expression[i + 1] in new_possibilities_numm:
                            
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit()
                    elif new_expression[i] in open_par:
                        if new_expression[i + 1] in clos_par or new_expression[i - 1] in new_possibilities_numm:
                            
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit()
                    elif new_expression[i] in new_possibilities_numm:
                        if new_expression[i - 1] in new_possibilities_numm or new_expression[i + 1] in new_possibilities_numm:
                            
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit()

            type_expression =   "float"

        elif len([j for j in expression if j in all_possibilities_log]) == len(expression):
            #logical operation
            
            #binlootan sonra binlop gelirse hata verecek.
            for q in range(len(expression)):
                if q == 0: 
                    if expression[q] in binlop or expression[q] in clos_par:
                        
                        res.write("Dont Let Me Down")
                        res.close()
                        f.close()
                        sys.exit()
                elif q == len(expression) - 1:
                    if expression[q] in binlop or expression[q] in open_par:
                        
                        res.write("Dont Let Me Down")
                        res.close()
                        f.close()
                        sys.exit()                 
                else:
                    
                    if expression[q] in binlop:
                        if expression[q + 1] in binlop or expression[q - 1] in binlop  or expression[q - 1] in open_par or expression[q + 1] in clos_par:  
                            
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit() 
                    elif expression[q] in clos_par:
                        if expression[q + 1] in open_par or expression[q + 1] in possibilities_logg or expression[q - 1] in open_par :
                            
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit() 
                    elif expression[q] in open_par:
                        if expression[q + 1] in clos_par or expression[q - 1] in possibilities_logg:
                            
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit()
                    elif expression[q] in possibilities_logg:
                        if expression[q - 1] in possibilities_logg or expression[q + 1] in possibilities_logg:
                            
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit()                                       
            type_expression = "boolean"
        else:
            res.write("Dont Let Me Down")
            res.close()
            f.close()
            sys.exit()
    used.append(first_elem)
    if type_expression == "float":
        types_used[first_elem] = "float"
    else:
        types_used[first_elem] = "boolean"
for new_statement in fin_list:
    
    expression = new_statement.split()

    for k in expression:
        if not(k in possibilities + open_par + clos_par + binaop + binlop + used+ ["nokta"] + [str(i)+"."+str(j) for i in range(10) for j in range(10)]) :
        
            res.write("Dont Let Me Down")
            res.close()
            f.close()
            sys.exit()
    type_expression = ""
    if len(expression) == 1:
        expression_str = expression[0]
        if not(expression_str in used or expression_str in possibilities or re.findall(r"^[0-9]\.?[0-9]$", expression_str) == [expression_str]):
            
            res.write("Dont Let Me Down")
            res.close()
            f.close()
            sys.exit()
        if expression_str in used:
            if types_used[expression_str] == "boolean":
                type_expression = "boolean"
            else:
                type_expression = "float" 
        else:
            if expression_str in possibilities_log:
                type_expression = "boolean"
            else:
                type_expression = "float"
    
    else:
        expression_str = ' '.join(expression)
        expression_str = expression_str.replace('kapa-parantez', ')')
        expression_str = expression_str.replace('ac-parantez', '(')
        if not(expression_str.count("(") == expression_str.count(")")):
    
            res.write("Dont Let Me Down")
            res.close()
            f.close()
            sys.exit()
        logs = []
        nums = []
        for i,j in types_used.items():
            if j == "boolean":
                logs.append(i)
            elif j == "float":
                nums.append(i)
        possibilities_logg  = logs + possibilities_log
        possibilities_numm = nums + possibilities_num + ["nokta"] + [str(i)+"."+str(j) for i in range(10) for j in range(10)]
        all_possibilities_log = open_par + clos_par + binlop + possibilities_logg
        all_possibilities_bin = open_par + clos_par + binaop + possibilities_numm 
        if len([i for i in expression if i in all_possibilities_bin]) == len(expression):
            #arithmetic operation
            #binaopdan sonra binaop gelirse hata verecek.
            if expression[0] == "nokta" or expression[-1] == "nokta":
                
                res.write("Dont Let Me Down")
                res.close()
                f.close()
                sys.exit()
            for l in range(len(expression) - 1):
                if expression[l] == "nokta":
                    if not(expression[l - 1] in nums_string and expression[l + 1] in nums_string):
                        
                        res.write("Dont Let Me Down")
                        res.close()
                        f.close()
                        sys.exit()
            new_possibilities_numm = possibilities_numm.copy()
            new_expression = []
            for n in range(len(expression) - 1):
                if expression[n + 1] == "nokta" or expression[n - 1] == "nokta":
                    continue
                if expression[n] == "nokta":
                    new_possibilities_numm.append(expression[n - 1] + " " + expression[n] + " " + expression[n + 1])
                    new_expression.append(expression[n - 1] + " " + expression[n] + " " + expression[n + 1])
                elif re.findall(r"^[0-9]\.?[0-9]$", expression[n]) == [expression[n]]:
                    new_possibilities_numm.append(expression[n])
                    new_expression.append(expression[n])
                else:
                    new_expression.append(expression[n])
            if expression[-2] != "nokta":
                new_expression.append(expression[-1])
            
            for i in range(len(new_expression)):
                if i == 0: 
                    if new_expression[i] in binaop or new_expression[i] in clos_par:
                        
                        res.write("Dont Let Me Down")
                        res.close()
                        f.close()
                        sys.exit()
                elif i == len(new_expression) - 1:
                    if new_expression[i] in binaop or new_expression[i] in open_par:
                        
                        res.write("Dont Let Me Down")
                        res.close()
                        f.close()
                        sys.exit() 
                else:
                    #####all_possibilities_bin = open_par + clos_par + binaop + new_possibilities_numm######
                    if new_expression[i] in binaop:
                        if new_expression[i + 1] in binaop or new_expression[i + 1] in clos_par or new_expression[i - 1] in open_par or new_expression[i - 1] in binaop: 
                            
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit()
                    elif new_expression[i] in clos_par:
                        if new_expression[i - 1] in open_par or new_expression[i + 1] in open_par or new_expression[i + 1] in new_possibilities_numm:
                            
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit()
                    elif new_expression[i] in open_par:
                        if new_expression[i + 1] in clos_par or new_expression[i - 1] in new_possibilities_numm:
                            
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit()
                    elif new_expression[i] in new_possibilities_numm:
                        if new_expression[i - 1] in new_possibilities_numm or new_expression[i + 1] in new_possibilities_numm:
                            
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit()

        

        elif len([j for j in expression if j in all_possibilities_log]) == len(expression):
            #logical operation
            
            #binlootan sonra binlop gelirse hata verecek.
            for q in range(len(expression)):
                if q == 0: 
                    if expression[q] in binlop or expression[q] in clos_par:
                        res.write("Dont Let Me Down")
                        res.close()
                        f.close()
                        sys.exit()
                elif q == len(expression) - 1:
                    if expression[q] in binlop or expression[q] in open_par:
                        res.write("Dont Let Me Down")
                        res.close()
                        f.close()
                        sys.exit()                 
                else:
                    if expression[q] in binlop:
                        if expression[q + 1] in binlop or expression[q - 1] in binlop  or expression[q - 1] in open_par or expression[q + 1] in clos_par:  
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit() 
                    elif expression[q] in clos_par:
                        if expression[q + 1] in open_par or expression[q + 1] in possibilities_logg or expression[q - 1] in open_par :
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit() 
                    elif expression[q] in open_par:
                        if expression[q + 1] in clos_par or expression[q - 1] in possibilities_logg:
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit()
                    elif expression[q] in possibilities_logg:
                        if expression[q - 1] in possibilities_logg or expression[q + 1] in possibilities_logg:
                            res.write("Dont Let Me Down")
                            res.close()
                            f.close()
                            sys.exit()                            
            
        else:
            res.write("Dont Let Me Down")
            res.close()
            f.close()
            sys.exit()
    

        
res.write("Here Comes the Sun")
res.close()
f.close()