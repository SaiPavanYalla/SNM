import ipaddress
import re
import math
import pickle

NetAdd = {}
customer = []

try:
    f = open('store.pckl', 'rb')
    NetAdd,customer = pickle.load(f)
    f.close()
except:
    pass

while 1:
    print("1. Allocate Subnet to a new customer")
    print("2. Print allocated Subnets")
    print("3. Reset Subnet Allocation System")
    print("4. Exit")
    print()
    sel = int(input())
    if(sel==1):
        inpNetAdd = input("Enter the network address from Class B Pool: (e.g. :156.234.0.0)")
        print()
        if not re.match(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',inpNetAdd):
            print("Please enter a valid IP address")
            print()
        else:
            splInpNetAdd = inpNetAdd.split(".")
            #print(splInpNetAdd)
            #print()
            if (len(splInpNetAdd)==4):    
                if (int(splInpNetAdd[0])>127 and int(splInpNetAdd[0])<192):
                    if (int(splInpNetAdd[2])==0 and int(splInpNetAdd[3])==0):
                        #print(NetAdd)
                        #print()
                        nh=int(input("Number of hosts? (1-65536)"))
                        print()
                        if(nh > 0 and nh < 65537):
                            subnet=math.ceil(math.log(nh,2))
                            addSpace=2**subnet
                            #print(addSpace)
                            strnetadd=str(int(splInpNetAdd[0]))+'.'+str(int(splInpNetAdd[1]))
                            if not NetAdd:
                                print("======================================")
                                print("Allocated Subnet is: "+strnetadd+".0.0/"+str(32-subnet))
                                print("======================================")
                                customer.append(strnetadd+".0.0/"+str(32-subnet))
                                print()
                                NetAdd.update({strnetadd:[[addSpace,65536]]})
                                #print(NetAdd)
                                #print()
                            elif not strnetadd in NetAdd:
                                print("======================================")
                                print("Allocated Subnet is: "+strnetadd+".0.0/"+str(32-subnet))
                                print("======================================")
                                customer.append(strnetadd+".0.0/"+str(32-subnet))
                                print()
                                NetAdd.update({strnetadd:[[addSpace,65536]]})
                                #print(NetAdd)
                                #print()
                            else:
                                addSpaceList = NetAdd.get(strnetadd)
                                subIDnum=0
                                for i in range(len(addSpaceList)):
                                    if addSpaceList[i][1]-addSpaceList[i][0]==addSpace:
                                        subIDnum = addSpaceList[i][0]
                                        addSpaceList.remove(addSpaceList[i])
                                        break
                                    if addSpaceList[i][1]-addSpaceList[i][0]>addSpace:
                                        subIDnum=math.ceil(addSpaceList[i][0]/addSpace)*addSpace
                                        if(subIDnum==addSpaceList[i][0]):
                                            addSpaceList[i][0]=addSpaceList[i][0]+addSpace
                                        else:
                                            temp=addSpaceList[i][0]
                                            addSpaceList[i][0]=subIDnum+addSpace
                                            addSpaceList.insert(i,[temp,subIDnum])
                                        break
                                splhostip=str(ipaddress.ip_address(subIDnum)).split(".")
                                #print(NetAdd)
                                #print()
                                if subIDnum==0:
                                    print("There is no space in the selected Network address, Please try again with different Network address")
                                else:
                                    print("======================================")
                                    print("Allocated Subnet is: "+strnetadd+"."+splhostip[2]+"."+splhostip[3]+"/"+str(32-subnet))
                                    print("======================================")
                                    customer.append(strnetadd+"."+splhostip[2]+"."+splhostip[3]+"/"+str(32-subnet))
                                    print()
                        else:
                            print("Please enter a valid Number of hosts")
                            print()
                    else:
                        print("Please enter a valid class B Network address (e.g. :156.234.0.0)")
                        print()
                else:
                    print("Please enter a valid class B Network address (e.g. :156.234.0.0)")
                    print()
            else:
                print("Please enter a valid IP address")
                print()
    elif(sel==2):
        print("======================================")
        print("Subnets allocated to the customers:")
        for i in range(len(customer)):
            print("--------------------------------------")
            print("Customer "+str(i+1)+" - "+customer[i])
        print("======================================")
        print()
    elif(sel==3):
        f = open('store.pckl', 'wb')
        NetAdd = {}
        customer = []
        pickle.dump([NetAdd, customer],f)
        print("======================================")
        print("Successfully Reset Subnet Allocation System")
        print("======================================")
        f.close()
    elif(sel==4):
        f = open('store.pckl', 'wb')
        pickle.dump([NetAdd, customer],f)
        f.close()
        print("======================================")
        print("Thank you, Have a great day!!")
        print("======================================")
        print()
        break
    else:
        print("Please enter a valid selection")
        print()