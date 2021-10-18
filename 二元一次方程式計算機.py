def is_float(num):
    """
    Check the value is float or integer
    """

    num = float(num)  #Change the value to float (Make sure all integer's last digit will be 0)
    str_num = str(num)  #Change the value to string (To check the value)

    if str_num[-1] == "0": # Check the last digit of the value, if the value's last digit was 0 then it will be integer
        return False

    else: 
        return True

keep = "1"
while keep == "1":
    #first function inputs
    print("first function: (ax + by + c = 0)")
    a = float(input("a: "))
    b = float(input("b: "))
    c = float(input("c: "))
    #second function inputs
    print("second function: (ax + by + c = 0)")
    a2 = float(input("a: "))
    b2 = float(input("b: "))
    c2 = float(input("c: "))

    #about first function
    a1 = a/b
    c1 = c/b

    a1 = a1*b2
    b1 = b2
    c1 = c1*b2

    #minus 2 functions together
    new_a = a2 - a1
    new_c = c2 - c1

    if new_a == 0: #check if theres infinity anwser
        print("infinity Ans")

    else:    
        x = -new_c / new_a  #calculate x
        y = -(a*x+c)/b

        if is_float(x):
            y = str(-(a*x+c)/b)

        elif is_float(-(a*x+c)/b):
            y = str(-(a*x+c)) + "/" + str(int(b)) #calculate y if its float
        else:
            y = -(a*x+c)/b #calculate y if it's interger

        if is_float(x):
            x = str(-new_c) + "/" + str(-new_a) #check if x is float 

        print("x:", x) #print x
        print("y:", y) #print y
    keep = input("keep? (1 = keep, other = no): ") #check if user need this again