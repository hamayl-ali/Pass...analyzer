import random
import string
import math
import hashlib
import requests

#i have added the breach for confirming that your entered password is really safe to use and is not compromised...

def breach(password):
    hash1=hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    
    prefix= hash1[:5]
    sufix= hash1[5:]

    url=f"https://api.pwnedpasswords.com/range/{prefix}"
    #i used some try catch here just to make sure about the network requests
    try:
        response=requests.get(url,timeout=5)
    except requests.exceptions.RequestException as e:
        return f"Network error: {e}"
    #here i checked just API response validation 

    if response.status_code !=200:
        return f"error this api is not reachable"
    #this is the part where im checking the response line by line spliting each sufix...
    for line in response.text.splitlines():
        sufix1,count=line.split(":")
        if sufix1==sufix:
            return f"the password is breached {count} times"
    return f"password is not found in breach very well"




#lets first add an entropy in project ;)
def is_entropy(password):
    lowers = string.ascii_lowercase
    uppers = string.ascii_uppercase
    digit = string.digits
    symbols = string.punctuation
#simple way to check on  the requirments of a simple password
    T = 0
    if any(i in lowers for i in password):
        T += len(lowers)
    if any(i in uppers for i in password):
        T += len(uppers)
    if any(i in digit for i in password):
        T += len(digit)
    if any(i in symbols for i in password):
        T += len(symbols)
    
    # here we should get the entropy 
    L = len(password)
    if T > 0:
        entropy = L * math.log2(T)#the formula of entropy is x*math.log2(y) here "L" is the lenght of the password and "T" is the size of charecters used which is 94 in this case
    else:
        entropy = 0
    
    return round(entropy, 2)

#method to check the strnght 
def password_strength_checker(password):

    if not password:
        return "password cannot be empty mate"#checking ...user should not enter empty password
    
    if len(password) < 8:
        return "Weak password: must be at least 8 characters long"
    if not any(char.isdigit() for char in password):
        return "Weak password: must contain at least 1 digit"
    if not any(char.isupper() for char in password):
        return "Weak password: must contain at least 1 uppercase letter"
    if not any(char.islower() for char in password):
        return "Weak password: must contain at least 1 lowercase letter"
    if not any(char in string.punctuation for char in password):
        return "Weak password: must contain at least 1 special character"
    
    #getting the checks of entroy here for better understanding
    check = is_entropy(password)
    if check < 30:
        strength = f"Very weak entropy man... {check} bits"
    elif check < 38:
        strength = f" Weak entropy boy ... {check} bits"
    elif check < 59:
        strength = f" Okay entropy ... {check} bits"
    elif check < 70:
        strength = f" Strong entropy nice ... {check} bits"
    elif check < 90:
        strength = f"Very good entropy (perfect)... {check} bits"
    else:
        strength = f"super strong password ... a jangli password"


    #having the resuts of breach and entropy here
    breach_result = breach(password)
    return f"{strength}\n{breach_result}"


    
    

# i can suggest you a simple password too....
def generate_password(length=12):
    s1 = string.ascii_lowercase
    s2 = string.ascii_uppercase
    s3 = string.digits
    s4 = string.punctuation

    all_chars = list(s1 + s2 + s3 + s4)
    random.shuffle(all_chars)

    password = "".join(random.choice(all_chars) for _ in range(length))
    return password


#  main function...
def password_tool():
    print("Hola amigo... welcome to the Password Tool 🔐")
    print("Type 'exit' to quit anytime.")

    while True:
        password = input("\nEnter a password to check (or type 'generate' to get a suggestion): ")

        if password.lower() == "exit":
            print("Thanks for using my tool! Goodbye 👋")
            break

        if password.lower() == "generate":
            try:
                length = int(input("Enter password length: "))
            except ValueError:
                print("Please enter a valid number")
                continue

            new_pass = generate_password(length)
            print("Suggested strong password:", new_pass)
            continue

        # Otherwise: analyze password
        result = password_strength_checker(password)
        print(result)

#runnnnnnnnnnnnnnnnnnnnnnnn
if __name__ == "__main__":
    password_tool()
