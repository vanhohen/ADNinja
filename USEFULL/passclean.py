#Basicly cleans a gives wordlist according to Active Directory requirements


from string import punctuation
import sys

#https://stackoverflow.com/a/28056873
special_chars = set(punctuation)
upper_chars = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"}
lower_chars = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}
Numbers = {"1","2","3","4","5","6","7","8","9","0"}


#returns true if found
def check(passwd,list):
    found = False
    for search in list:
        if search in passwd:
            found = True
            break
    return found

def read_file(path):
    with open(path,"r") as plist:
        lines = plist.readlines()
    return lines

if __name__ == "__main__":
    wlist = read_file(sys.argv[1])
    
    for line in wlist:
        
        result = 0
        result += check(line,upper_chars)
        result += check(line,lower_chars)
        result += check(line,Numbers)
        result += check(line,special_chars)
        
        #accoring to microsof it should pass at least 3 check
        #https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/password-must-meet-complexity-requirements#reference
        #you can change it 4 if you want all requirements meet, maybe add password length also?
        if result < 3:
            pass
        else:
            print (line)