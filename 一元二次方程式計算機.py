#imports and inputs
import math
a = float(input("a: "))
b = float(input("b: "))
c = float(input("c: "))

def is_prime(value):
    """
    Check if the value is prime
    """

    #Check if the value can be divide by lower numbers or not
    for i in range(2, value):
        if value % i == 0: 
            return False      
    return True


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


def check_valid(a,b,c):
    """
    1. Check the discriminant is valid or not
    2. return check is float or integer
    3. calculate the discriminant and return it
    """

    check = (b*b) - (4*a*c)  #Calculate the discriminant

    if check > 0:  #If there's 2 solutions
        valid = 2

    elif check == 0:  #If there's 1 solutions
        valid = 1
        
    elif check < 0:  #If there's no solutions
        print("N/A, No ans") #Output

        exit() #End the script, because there's no need to keep it


    num_type = is_float(math.sqrt(check))  #Check if the value is float or integer


    return valid, num_type, check


def short_divid(x):
    """
    short divide a number 
    return with a dictionary

    return form:
    {(prime number: value), (second prime number: value)}

    e.g. input 50
    returns {(2: 1), (5: 2)}
    """

    #setup values
    ans = dict()
    v = int(x) + 1
    

    #Check all the value inside "x + 1" can be divide by "x" or not 
    for i in range(2, v):
        n = 1
        while x % i == 0 and is_prime(i):  #Reapet the same value till "x" cant be divide by it
            ans.update({i: n})  #Update the value to the dictionary

            x = x / i  #create new "x" after divided by "i (The value right now)" 
            n += 1  #counter of the value
            

    return ans
        

def reduct_sqrt(x):
    """
    reduct a squareroot of a number

    return form:
    coefficient, new constant inside of squareroot

    e.g. input 20
    return 2, 5
    as known as 2√5

    """

    #setup values
    coeff = 1
    new_x = 1
    sd = short_divid(x)
    for a, b in sd.items():

        while b >= 2: #Calculate for the coefficient of the squareroot
            coeff = coeff * a
            b = b-2
            sd.update({a: b})

    for (a, b) in sd.items(): #Calculate for the new constant inside of the squarerot
        if b > 0:
            new_x = new_x*(a*b)
        else:
            continue

    return coeff, new_x


def reduct_ans(a, b, c):
    """
    Reduct the anwser (b, coeff, 2a)
    """

    larger = abs(a) if abs(a) > abs(b) else abs(b)
    larger = abs(int(larger)) if larger > abs(c) else abs(int(c))  #Find the largest number

    for i in range(2, larger):
        while a % i == 0 and b % i == 0 and c % i == 0:  #Reduct the numbers
            a = a / i
            b = b / i
            c = c / i

    return a, b, c



valid, num_type, check = check_valid(a,b,c)  #call check_valid() function


if valid == 2:
    #2 answers, normal root
    sqrt_check = math.sqrt(check) #Calculate squareroot of the "discriminant" 

    if num_type: #If the discriminant is float
        coeff, new_x = reduct_sqrt(check)  #reducting squareroot
        b, coeff, a = reduct_ans(b, coeff, a*2)  #reducting anwser

        if coeff > 1 : #If the squareroot of the discriminant can be split out
            if a == 1: #Check if the "a" is needed or not
                ans = (str(int(-b)) + " ± " + str(int(coeff)) + "sqrt(" + str(new_x) + ")")

            else:
                ans = ("(" + str(int(-b)) + " ± " + str(int(coeff)) + "sqrt(" + str(new_x) + "))/" + str(int((a))))

        else: #If the squareroot of the discriminant can not be split out
            ans = ("(" + str(int(-b)) + " ± sqrt(" + str(int(new_x)) + "))/" + str(int((a))))

    else: #If the discriminant is constant
        ans = ("(" + str(int(-b)) + " ± " + str(int(sqrt_check)) + ")/" + str(int((2*a))))
        

if valid == 1:
    #1 anwser, repeated root, double root
    if is_float(-b/(2*a)): #If the final anwser is float
        ans = ("(" + str(int(-b)) + ")/" + str(int(2*a)))
    else: #If the final anwser is constant
        ans = (int(-b/(2*a)))
    
    #No anwser's script already ended


#Output anwser
print("x = " + str(ans))
