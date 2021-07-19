

def lic():
    f = open("icfg.txt",'r')
    data = f.readlines()
    data = data[1:]
    f.close()
    imc = list()

    for line in data:
        gay = line.split('|')
        imc.append({"op":gay[0],"ar1":gay[1],"ar2":gay[2],"res":gay[3]})

    loop_var=dict()
    loop_ivar=""
    loop_invar=dict()
    imc_var=list()
    ifFalse=False
    next_lable=""
    flag=1
    nxt_flag=1
    line=""
    for i in range(0,len(imc)):
        line=imc[i]
        #print(line)
        if line["res"] == next_lable: #moving the loop invariant code outside the loop body to following the loop
            imc_var.append(line)
            nxt_flag=0
            print(loop_invar)
            for invariant_code in loop_invar:
                imc_var.append(loop_invar[invariant_code])
            #loop_invar.clear()


        if line["op"]=="Label" and line["res"]!="l0":
            next_line=imc[i+1]
            loop_ivar=next_line["ar1"]
            next_lable = line["res"].split('l')
            next_lable="l"+str((int(next_lable[1])+1))
            
            


        if line["op"]=="ifFalse": #body of loop starts
            ifFalse=True
            
            continue

        elif line["op"]=="goto": #body of loop ends
            ifFalse=False
            
            

        #true means it is not loop invariant and hence need to be retained as it is
        if ifFalse == True:
            if line["res"] not in loop_var:
            
                
                    #intialisation of a variable with the loop variance int b:=i
                try:
                    
                    print("in try",line)

                    if(line["res"]=='' and (line["op"]=="Param" or line["ar1"]=="printf")): #printf is loop variant 
                    	loop_var[line["op"]]="True"
                   
                    #elif line["ar1"]!="" and line["ar2"]!="" and (line["res"] == line["ar1"] or line["res"] == line["ar2"]): #c+=1
                     #   loop_var[line["res"]]= True

                    
                    elif (line["ar1"]!="" and loop_var[line["ar1"]] == True) and (line["ar2"]!="" and loop_var[line["ar2"]] == True): #all var is true
                            loop_var[line["res"]] = True 
                            
                    elif (line["ar1"]!="" and loop_var[line["ar1"]] == True) and (line["ar2"]==""):
                            loop_var[line["res"]] = True
                            
                    elif (loop_var[line["ar1"]] == True) or (loop_var[line["ar2"]] == True):
                            print(line,"try lastelif")
                            loop_var[line["res"]]= True
                            if line["ar1"]!="" and loop_var[line["ar1"]] == False:
                                loop_var[line["ar1"]]=True
                                #loop_invar[line["ar1"]]=line
                            if line["ar2"]!="" and loop_var[line["ar2"]] == False:
                                loop_var[line["ar2"]]=True
                                #loop_invar[line["ar2"]]=line
                            #loop_invar[line["res"]]=line
                            flag=0
                    
                except:
                    '''
                    line_spilt1=line["ar1"].split("#") 
                    line_spilt2=line["ar2"].split("#")
                    if loop_ivar.count(line_spilt1[0])==1 or loop_ivar.count(line_spilt2[0])==1:
                        loop_var[line["res"]] = True
                        print(line,line_spilt1,line_spilt2)
                        
                
                    else:
                        loop_var[line["res"]]= False
                        loop_invar[line["res"]]=line
                        flag=0
                    
                    '''             
                    print(line,"inexcept")
                    
                    if line["ar1"]==loop_ivar or line["res"]==loop_ivar:#or line["ar2"]==loop_ivar or line["res"]==loop_ivar:#loop_ivar.count(line_spilt1[0])==1  or loop_ivar.count(line_spilt2[0])==1:
                        loop_var[line["res"]] = True
                        #print(line,line_spilt1,line_spilt2)
                    else:
                    	loop_var[line["res"]]= False
                    	loop_invar[line["res"]]=line
                    	flag=0
                    
                    
                    
                    

        if flag==1 and nxt_flag==1:
            imc_var.append(line)
                                
        else:
            
            if nxt_flag==0: #label following the forloop
                nxt_flag=1
            if flag==0: #loop invariant code
                flag=1

    # for line in imc_var:
    #     print(line,end="\n")
        
    # print("\n\n")

    print(loop_var)
    for q in imc_var:
            if q["op"]=="Param" :
                print(q["op"],"=",q["ar1"])

            elif q["op"]=="Lable" or q["op"]=="goto":
                print(q["op"],"=",q["res"])

            elif  q["op"]=="call":
                print(q["ar1"],q["op"],q["ar2"])

            elif q["op"] != "=":
                print(q["res"],"=",q["ar1"],q["op"],q["ar2"])
            
            else:
                print(q["res"],q["op"],q["ar1"])

    f=open("code_motion.txt",'w')
    line=""
    for q in imc_var:
            if q["op"]=="Param" :
                line=q["op"]+" = "+q["ar1"]+"\n"
            
            elif q["op"]=="ifFalse" :
                line=q["op"]+" "+q["res"]+" = "+q["ar1"]+"\n"

            elif q["op"]=="Lable" or q["op"]=="goto":
                line=q["op"]+" = "+q["res"]+"\n"

            elif  q["op"]=="call":
                line=q["ar1"]+" "+q["op"]+" "+q["ar2"]+"\n"

            elif q["op"] != "=":
                line=q["res"]+" = "+q["ar1"]+" "+q["op"]+" "+q["ar2"]+"\n"
            
            else:
                line=q["res"]+" "+q["op"]+" "+q["ar1"]+"\n"
            f.write(line)
    f.close()
        
                
if __name__=="__main__":
    lic()
