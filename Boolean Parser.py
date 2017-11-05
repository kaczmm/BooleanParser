# Boolean Parser
# Matthew Kaczmarek

# Program can be run as python2 or python3
from __future__ import print_function

# Tokens (defined using regular expressions)
# VAR = \$[0-9a-zA-Z]*
# BOOL = True | False
# OP = and | or
# NOT = not
# LP = \(
# RP = \)
# EQ = \=

# Tokens
EOF = 0
VAR = 1
BOOL = 2
OP = 3
NOT = 4
LP = 5
RP = 6
EQ = 7
ERR = 8

# Grammar
# prog-> LP expr1 RP tail2 | {VAR,BOOL} tail1 | NOT expr | epsilon
# tail1-> {EQ,OP} expr | epsilon
# tail2-> OP expr | epsilon
# expr-> LP expr1 RP tail2 | {VAR,BOOL} tail2 | NOT expr
# expr1-> LP expr1 RP tail2 | {VAR,BOOL} tail1 | NOT expr

import sys
debug = True

def show(indent,name,s,spp):
    if debug:
        print(indent+name+'("',end='')
        j = len(s)
        for i in range(spp,j):
            print(s[i],sep='',end='')
        print('")',end='\n')
        return
    else:
        return
#end show

def EatWhiteSpace(s,spp):
    j = len(s)
    if spp >= j:
        return spp

    while s[spp] == ' ' or s[spp] == '\n':
        spp=spp+1
        if spp >= j:
            break
    return spp
#end EatWhiteSpace

# function Parse ---------------------------------------------
def Parse(s,indent):
    show(indent,'Parse',s,0)

    spp = 0;
    indent1 = indent+' '
    res,spp = prog(s,spp,indent1)
    if debug:
        print(indent+"back to Parse from prog")
    if not res:
        return False

    token = LookAhead(s,spp)
    if token != EOF:
        return False
    else:
        return True
#end Parse

# prog-> LP expr1 RP tail2 | {VAR,BOOL} tail1 | NOT expr | epsilon
def prog(s,spp,indent):
    show(indent,'prog',s,spp)
    indent1 = indent+' '
    spp1 = spp #save position

    token = LookAhead(s,spp)
    if token == LP:
        token,spp = NextToken(s,spp)
        res,spp = expr1(s,spp,indent1)
        if debug:
            print(indent+'back to prog from expr1')
        if not res:
            return False,spp
        token = LookAhead(s,spp)
        if token != RP:
            return False,spp
        token = NextToken(s,spp)
        res,spp = tail2(s,spp,indent1)
        if debug:
            print(indent+'back to prog from tail2')
        if res:
            return True,spp
        else:
            return False,spp
    elif token == VAR or token == BOOL:
        token,spp = NextToken(s,spp)
        res,spp = tail1(s,spp,indent1)
        if debug:
            print(indent+'back to prog from tail1')
        if res:
            return True,spp
        else:
            return False,spp
    elif token == NOT:
        token,spp = NextToken(s,spp)
        res,spp = expr(s,spp,indent1)
        if debug:
            print(indent+'back to prog from expr')
        if res:
            return True,spp
        else:
            return False,spp
    else:
        return True,spp # epsilon
#end prog

# tail1-> {EQ,OP} expr | epsilon
def tail1(s,spp,indent):
    show(indent,'tail1',s,spp)
    indent1 = indent+' '
    spp1 = spp #save position

    token = LookAhead(s,spp)
    if token == EQ or token == OP:
        token,spp = NextToken(s,spp)
        res,spp = expr(s,spp,indent1)
        if debug:
            print(indent+'back to tail1 from expr')
        if res:
            return True,spp
        else:
            return False,spp
    else:
        return True,spp # epsilon
#end tail1

# tail2-> OP expr | epsilon
def tail2(s,spp,indent):
    show(indent,'tail2',s,spp)
    indent1 = indent+' '
    spp1 = spp #save position

    token = LookAhead(s,spp)
    if token == OP:
        token,spp = NextToken(s,spp)
        res,spp = expr(s,spp,indent1)
        if debug:
            print(indent+'back to tail2 from expr')
        if res:
            return True,spp
        else:
            return False,spp
    else:
        return True,spp # epsilon
#end tail2

# expr-> LP expr1 RP tail2 | {VAR,BOOL} tail2 | NOT expr
def expr(s,spp,indent):
    show(indent,'expr',s,spp)
    indent1 = indent+' '
    spp1 = spp #save position

    token = LookAhead(s,spp)
    if token == LP:
        token,spp = NextToken(s,spp)
        res,spp = expr1(s,spp,indent1)
        if debug:
            print(indent+'back to expr from expr1')
        if not res:
            return False,spp
        token = LookAhead(s,spp)
        if token != RP:
            return False,spp
        token = NextToken(s,spp)
        res,spp = tail2(s,spp,indent1)
        if debug:
            print(indent+'back to expr from tail2')
        if res:
            return True,spp
        else:
            return False,spp
    elif token == VAR or token == BOOL:
        token,spp = NextToken(s,spp)
        res,spp = tail2(s,spp,indent1)
        if debug:
            print(indent+'back to expr from tail2')
        if res:
            return True,spp
        else:
            return False,spp
    elif token == NOT:
        token,spp = NextToken(s,spp)
        res,spp = expr(s,spp,indent1)
        if debug:
            print(indent+'back to expr from expr')
        if res:
            return True,spp
        else:
            return False,spp
    else:
        return False,spp # no epsilon
#end expr

# expr1-> LP expr1 RP tail2 | {VAR,BOOL} tail1 | NOT expr
def expr1(s,spp,indent):
    show(indent,'expr1',s,spp)
    indent1 = indent+' '
    spp1 = spp #save position

    token = LookAhead(s,spp)
    if token == LP:
        token,spp = NextToken(s,spp)
        res,spp = expr1(s,spp,indent1)
        if debug:
            print(indent+'back to expr1 from expr1')
        if not res:
            return False,spp
        token = LookAhead(s,spp)
        if token != RP:
            return False,spp
        token = NextToken(s,spp)
        res,spp = tail2(s,spp,indent1)
        if debug:
            print(indent+'back to expr1 from tail2')
        if res:
            return True,spp
        else:
            return False,spp
    elif token == VAR or token == BOOL:
        token,spp = NextToken(s,spp)
        res,spp = tail1(s,spp,indent1)
        if debug:
            print(indent+'back to expr1 from tail1')
        if res:
            return True,spp
        else:
            return False,spp
    elif token == NOT:
        token,spp = NextToken(s,spp)
        res,spp = expr(s,spp,indent1)
        if debug:
            print(indent+'back to expr1 from expr')
        if res:
            return True,spp
        else:
            return False,spp
    else:
        return False,spp # no epsilon
#end expr1

# scanner ##############################

# LookAhead function
def LookAhead(s,spp):
    j = len(s)
    i = EatWhiteSpace(s,spp)
    
    if i >= j:
        return EOF

    #print('LookAhead sees: ' + s[i])

    if s[i] == '=':
        return EQ
    elif s[i] == 'T' or s[i] == 'F':
        return BOOL
    elif s[i] == 'a':
        if i+1 >= j:
            return EOF
        if s[i+1] != 'n':
            return ERR
        if i+2 >= j:
            return EOF
        if s[i+2] != 'd':
            return ERR
        return OP
    elif s[i] == 'o':
        if i+1 >= j:
            return EOF
        if s[i+1] != 'r':
            return ERR
        return OP
    elif s[i] == 'n':
        if i+1 >= j:
            return EOF
        if s[i+1] != 'o':
            return ERR
        if i+2 >= j:
            return EOF
        if s[i+2] != 't':
            return ERR
        return NOT
    elif s[i] == '(':
        return LP
    elif s[i] == ')':
        return RP
    elif s[i] == '$':
        return VAR
    else:
        return ERR
#end LookAhead

# NextToken function

# VAR = \$[0-9a-zA-Z]*
# BOOL = True | False
# OP = and | or
# NOT = not
# LP = \(
# RP = \)
# EQ = \=

def NextToken(s,spp):
    spp1 = spp
    spp = EatWhiteSpace(s,spp)
    #print('NextToken: s = ' + s)
    #print('spp = ',spp)
    j = len(s)
    if spp >= j:
        return ERR,spp1

    if spp >= j:
        return EOF,spp
    elif s[spp] == '=': # ~~~~~ EQ ~~~~~~~~~~~~~~~
        return EQ,spp+1
    elif s[spp] == 'T': # ~~~~~ TRUE ~~~~~~~~~~~~~~~
        spp = spp+1
        if spp >= j:
            return EOF,spp1
        if s[spp] != 'r':
            return ERR,spp
        spp = spp+1
        if spp >= j:
            return EOF,spp1
        if s[spp] != 'u':
            return ERR,spp
        spp = spp+1
        if spp >= j:
            return EOF,spp1
        if s[spp] != 'e':
            return ERR,spp
        return BOOL,spp+1
    elif s[spp] == 'F': # ~~~~~ FALSE ~~~~~~~~~~~~~~~
        spp = spp+1
        if spp >= j:
            return EOF,spp1
        if s[spp] != 'a':
            return ERR,spp
        spp = spp+1
        if spp >= j:
            return EOF,spp1
        if s[spp] != 'l':
            return ERR,spp
        spp = spp+1
        if spp >= j:
            return EOF,spp1
        if s[spp] != 's':
            return ERR,spp
        spp = spp+1
        if spp >= j:
            return EOF,spp1
        if s[spp] != 'e':
            return ERR,spp
        return BOOL,spp+1
    elif s[spp] == 'a': # ~~~~~ AND ~~~~~~~~~~~~~~~
        spp = spp+1
        if spp >= j:
            return EOF,spp1
        if s[spp] != 'n':
            return ERR,spp
        spp = spp+1
        if spp >= j:
            return EOF,spp1
        if s[spp] != 'd':
            return ERR,spp
        return OP,spp+1
    elif s[spp] == 'o': # ~~~~~ OR ~~~~~~~~~~~~~~~
        spp = spp+1
        if spp >= j:
            return EOF,spp1
        if s[spp] != 'r':
            return ERR,spp
        return OP,spp+1
    elif s[spp] == 'n': # ~~~~~ NOT ~~~~~~~~~~~~~~~
        spp = spp+1
        if spp >= j:
            return EOF,spp1
        if s[spp] != 'o':
            return ERR,spp
        spp = spp+1
        if spp >= j:
            return EOF,spp1
        if s[spp] != 't':
            return ERR,spp
        return NOT,spp+1
    elif s[spp] == '(': # ~~~~~ LP ~~~~~~~~~~~~~~~
        return LP,spp+1
    elif s[spp] == ')': # ~~~~~ RP ~~~~~~~~~~~~~~~
        return RP,spp+1
    elif s[spp] == '$': # ~~~~~ VAR ~~~~~~~~~~~~~~~
        spp = spp+1 # eat dollar sign
        while (ord(s[spp]) >= ord('0') and ord(s[spp]) <= ord('9')) or (ord(s[spp]) >= ord('a') and ord(s[spp]) <= ord('z')) or (ord(s[spp]) >= ord('A') and ord(s[spp]) <= ord('Z')):
            spp = spp+1
            if spp >= j:
                return EOF,spp
            if s[spp] == ' ':
                break
        return VAR,spp+1
    else: # ~~~~~ ERR ~~~~~~~~~~~~~~~
        return ERR,spp
#end NextToken

#Main Section
s = '$Banana123 = True and False'
show('','main',s,0)
indent = ' '
res = Parse(s,indent)
if res:
    print('parsing OK')
else:
    print('parse error')
#end main section
