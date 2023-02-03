import sys
import re
from graphviz import Graph
import math
import random

filename = input("Enter file name: ")
log = open("log.txt","w")
sets = ["variables:","constants:","predicates:","equality:", "connectives:", "quantifiers:","formula:"] 
tempSets = sets
variables = []
constants = []
predicates = []
equality = []
connectives = []
quantifiers = []
formula = []
token_stream = []
formula_string = ""

predicate_pattern = r'[A-Za-z0-9_]*[\[][0-9]+[\]]$'
equality_pattern = r'^[\=A-Za-z0-9_\\]+$'
cons_var_pattern = r'^[A-Za-z0-9_]*$'
conn_quan_patter = r'^[A-Za-z0-9_\\]+$'

#Rules for grammer initialised and few values declared
rules = {
    "FORM":[
        "(TERM EQ TERM)",
        "PRED",
        "NEG FORM",
        "(FORM CONN FORM)",
        "QUANT VAR FORM"
    ],

    "PRED":[

    ],

    "TERM":[
        "VAR",
        "CONS"
    ],

    "QUANT":[

    ],

    "CONN":[

    ],

    "EQ":[

    ],

    "NEG":[

    ],

    "CONS":[

    ],

    "VAR": [

    ]
}

#Creates graph
dot = Graph(format='png')

#Checks to see if input file is a valid file or not
try:
    inputfile = open(filename,"r")
except:
    print("ERROR: Could not open input file!")
    logfile(f"ERROR: {filename} could not be opened!")
    sys.exit()

#Used to log error messages
def logfile(message):
    log.write(message + "\n")

#Checks to see if same values are in both list
def listCompare(listA, listB):
    same = False
  
    #Iterate in the 1st list 
    for i in listA: 
        #Iterate in the 2nd list 
        for j in listB: 
            #If there is a match
            if i == j: 
                same = True
                return same  

""" The validate file method will go through each set and make sure there are no invalid sets. This is done by checking if each element in the set matches a pattern that was set.
The validate file will also check for duplicate values within sets and makes sure that predicates have been written out corerctly.
"""

def validateFile():
    prevLine = "??"
    count = 0
    #Gets every line of file
    Lines = [line.split() for line in inputfile]
    count_quantifiers = 0
    count_connectives = 0
    count_equality = 0
    error_check = False

    for line in Lines: 
        if line[0] in sets:
            tempSets.remove(line[0])
            count+=1

        #Next few statements just add the symbols or formula to its respective set
        if prevLine[0] == "formula:" or prevLine[0] not in sets:
            for b in range(1,len(line)):
                formula.append(line[b])

        if line[0] == "formula:":
            for a in range(1,len(line)):
                formula.append(line[a])

        elif line[0] == "variables:" or line[0] == "constants:" or line[0] == "predicates:": 
            check = None

            for i in range(1,len(line)):
                if line[0] == "variables:":
                    variables.append(line[i])
                if line[0] == "constants:":
                    constants.append(line[i])
                if line[0] == "predicates:":
                    predicates.append(line[i])
                    found = "?"
                    try:
                        check = re.match(predicate_pattern, line[i])
                        if check != None:
                            found = str(re.search(r'\[([0-9]+)\]{1}', line[i]).group(1))
                    except:
                        error_check = True
                        print("SYNTAX ERROR: Predicates have not been defined correctly!")
                        logfile("SYNTAX ERROR: " + line[i] + " has been defined incorrectly, format should be predicate[arity], where arity is a positive integer greater than 0!")
                        sys.exit(0)

                    if found == "":
                        error_check = True
                        print("SYNTAX ERROR: Predicates have no arity!")
                        logfile("SYNTAX ERROR: " + line[i] + " has invalid arity!")
                        sys.exit(0)

                    elif found == "0":
                        error_check = True
                        print("SYNTAX ERROR: Predicates must have arity greater than 0!")
                        logfile("SYNTAX ERROR: " + line[i] + " has invalid arity. Must use arity greater than 0!") 
                        sys.exit(0)
                else:
                    check = re.match("^[A-Za-z0-9_]*$", line[i])

                if check == None:
                    error_check = True
                    print("SYNTAX ERROR: Invalid syntax used!")
                    logfile("SYNTAX ERROR: " + line[0][:-1] + " set" + ", " + line[i] + " has invalid syntax!")
                    sys.exit(0)

        elif line[0] == "quantifiers:" or line[0] == "connectives:":
            for j in range(1,len(line)):
                if line[0] == "quantifiers:":
                    count_quantifiers+=1
                    quantifiers.append(line[j])
                if line[0] == "connectives:":
                    count_connectives+=1
                    connectives.append(line[j])
                if re.match(conn_quan_patter, line[j]) == None:
                    error_check = True
                    print("SYNTAX ERROR: Invalid syntax used!")
                    logfile("SYNTAX ERROR: " + line[0][:-1] + " set" + ", " + line[j] + " has invalid syntax. Should only contain letters, numbers or backslashes.")
                    sys.exit(0)

        elif line[0] == "equality:":
            for k in range(1,len(line)):
                count_equality+=1
                equality.append(line[k])
            if re.match(equality_pattern, line[k]) == None:
                error_check = True
                print("SYNTAX ERROR: Invalid syntax used!")
                logfile("SYNTAX ERROR: " + line[0][:-1] + " set" + ", " + line[j] + " has invalid syntax. Should only contain letters, numbers, backslashes or equals(=.)")
                sys.exit(0)
            
        prevLine = line

    #Makes sure to see if there are seven sets in file.
    if count < 7:
        showMissing = [x[:-1] for x in tempSets]
        error_check = True
        print("ERROR: Missing sets in input file!")
        logfile("ERROR: " + ', '.join(showMissing) + " sets missing in input file!")
        sys.exit(0)
        
    if count_connectives != 5:
        error_check = True
        print("ERROR: Expected 5 connectives but recieved " + str(count_connectives))
        logfile("ERROR: Expected 5 connectives but recieved " + str(count_connectives))
        sys.exit(0)
    if count_quantifiers != 2:
        error_check = True
        print("ERROR: Expected 2 quantifiers but recieved " + str(count_quantifiers))
        logfile("ERROR: Expected 2 quantifiers but recieved " + str(count_quantifiers))
        sys.exit(0)
    if count_equality != 1:
        error_check = True
        print("ERROR: Expected 1 equality but recieved " + str(count_equality))
        logfile("ERROR: Expected 2 equality but recieved " + str(count_equality))
        sys.exit(0)

    tempPredicates = [sub[ :-3] for sub in predicates]
    if listCompare(tempPredicates,constants) ==  True:
        error_check = True
        print("ERROR: Same symbol found in both predicates and constants!")
        logfile("ERROR: Same symbol found in both predicates and constants!")
        sys.exit(0)
    if listCompare(tempPredicates,variables) ==  True:
        error_check = True
        print("ERROR: Same symbol found in both predicates and variables!")
        logfile("ERROR: Same symbol found in both predicates and variables!")
        sys.exit(0)
    if listCompare(variables,constants) ==  True:
        error_check = True
        print("ERROR: Same symbol found in both variables and constants!")
        logfile("ERROR: Same symbol found in both variables and constants!")
        sys.exit(0)

    if error_check == False:
        print("Input file is valid!")
        logfile("Input file is valid!")

#This is where the grammer of a valid FO formula is made.
def grammer():
    grammerFile = open("grammer.txt","w")
    termin = ""
    nontermin = ""

    rules["NEG"].append(connectives[len(connectives)-1])
    termin += " " + connectives[len(connectives)-1]
    rules["EQ"].append(equality[0])
    termin += " " + equality[0]

    for i in range(0,len(connectives)-1):
        rules["CONN"].append(connectives[i])
        termin += " " + connectives[i]

    for j in quantifiers:
        rules["QUANT"].append(j)
        termin += " " + j
    for k in constants:
        rules["CONS"].append(k)
        termin += " " + k

    for l in variables:
        rules["VAR"].append(l)
        termin += " " + l

    morethancount = 0
    for m in predicates:
        tempHold = int(re.search(r"\[([A-Za-z0-9_]+)\]", m).group(1))
        termin +=  " " + m[:-3]
        predHold = m[:-3] + "("
        for a in range(0,tempHold):
            if a == tempHold-1:
                predHold = predHold + "Term)"
            else:
                predHold = predHold + "Term, "
                morethancount += 1

        rules["PRED"].append(predHold)

    padding = "          "
    for key in rules.keys():
        switch = 0
        tempStr = key + " ->"
        grammerFile.write(tempStr)
        for value in rules[key]:
            if switch == 0:
                pad = (len(padding) - len(tempStr)+1) * " "
                tempSt = pad + value + "\n"
                grammerFile.write(tempSt)
                switch = 1
            else:
                grammerFile.write(padding + "|" + value + "\n")
        grammerFile.write("\n")

    termin += " (" + " )"
    if morethancount > 0:
        termin += " " + ","

    grammerFile.write("TERMINALS:" + termin + "\n")

    for y in rules:
        nontermin += " " + y

    grammerFile.write("NON-TERMINALS:" + nontermin)
    grammerFile.close()
    


""" The lexer goes through each character in formula and joins the characters up. These characters are then split if the next character is either a key word or a space """
def lexer():
    global formula_string
    inputfile.seek(0)
    allData = inputfile.readlines()
    start = 0
    end = 0

    for l in range(0,len(allData)):
        if "formula:" in allData[l]:
            start = l
            end = l

    end = end + (len(allData) - 7) 

    for k in range(start,end+1):
        formula_string = formula_string + allData[k]

    formula_string = formula_string.replace("formula: ","")
    formula_string = formula_string + '\n'
    formula_string = formula_string.replace('\n', ' ')

    symbols = ['(', ')', '[', ']', ','] 
    KEYWORDS = symbols + connectives
    white_space = ' '
    lexeme = ''
    for i,char in enumerate(formula_string):
        if char != white_space:
            lexeme += char
        #Makes sure it doesn't go out of list index    
        if (i+1 < len(formula_string)):
            if formula_string[i+1] == white_space or formula_string[i+1] in KEYWORDS or lexeme in KEYWORDS:
                if lexeme != '':
                    tokeniser(lexeme, i - (len(lexeme)-1), i)
                    lexeme = ''

    #To tell parser that it has reached the end
    token_stream.append("$")

""" This is where each lexeme is assigned a token along with a variable and the location of that lexeme in the formula"""
def tokeniser(lexeme, start, end):

    if lexeme in quantifiers:
        token_stream.append("QUANTIFIER " + lexeme + " " + str(start) + " " + str(end))
    elif lexeme in connectives[:-1]:
        token_stream.append("CONNECTIVE " + lexeme + " " + str(start) + " " + str(end))
    elif lexeme in [w[:-3] for w in predicates]:
        token_stream.append("PREDICATE " + lexeme + " " + str(start) + " " + str(end))
    elif lexeme in equality:
        token_stream.append("EQUAL " + lexeme + " " + str(start) + " " + str(end))
    elif lexeme in variables:
        token_stream.append("TERM " + lexeme + " " + str(start) + " " + str(end))
    elif lexeme in constants:
        token_stream.append("TERM " + lexeme + " " + str(start) + " " + str(end))
    elif lexeme == connectives[-1]:
        token_stream.append("NEGATION " + lexeme + " " + str(start) + " " + str(end))
    elif lexeme == '(':
        token_stream.append("LEFTPARENTH " + lexeme + " " + str(start) + " " + str(end))
    elif lexeme == ')':
        token_stream.append("RIGHTPARENTH " + lexeme + " " + str(start) + " " + str(end))
    elif lexeme == ',':
        token_stream.append("COMMA " + lexeme + " " + str(start) + " " + str(end))
    else:
        print("ERROR: Invalid symbol found when tokenising")
        logfile("ERROR: Invalid symbol found: " + lexeme + " at start position: " + str(start) + " and end position: " + str(end) + " of formula")
        sys.exit(0)



class Parser:
    def parse(self, text):
        self.curr_indx = 0
        self.curr_tok = None
        self.curr_val = None
        self.next_tok = token_stream[self.curr_indx].split()[0]
        empty = ""
        self.lparenth_count = 0
        self.rparenth_count = 0
        self.switch = False
        self.scope = 0
        self.check = False
        self.count = 0
        self.rcount = 0
        self.termcount = 0
        self.stack = []
        self.next_form = 0
        self.negcount = 99999
        self.variablecount = 99999
        self.constantcount = 99999
        self.quantifiercount = 99999
        self.eqcount = 99999
        self.connectivecount = 99999
        self.termCheck = False
        
        return self.form(empty)

    #Advances current token, current value, current index and next token
    def _advance(self):
        self.curr_indx +=1
        self.curr_tok, self.next_tok, self.curr_val = self.next_tok, token_stream[self.curr_indx].split()[0], token_stream[self.curr_indx-1].split()[1]

    #Checks to see if the next toke type matches what we had expected
    def _accept(self, token_type):
        if self.curr_indx < len(token_stream) and self.next_tok == token_type:
            self._advance()
            return True
        else:
            return False

    #Creates errors for log file when parsing
    def _except(self, token_type):
        if not self._accept(token_type):
            logfile('Expected ' + token_type)

    #This is the FORM non-terminal. This recurses onto itself when certain conditions are met.
    def form(self, formula):

        #Creates the FORM nodes and their location
        if self.count == 0:
            formname = "FORM " + str(self.count)
            dot.node(formname, "FORM")
        elif self.curr_tok == "CONNECTIVE":
            formname = "FORM " + str(self.count)
            dot.node(formname, "FORM")
            dot.edge("FORM " + str(self.next_form), formname)
        elif self.curr_tok == "NEGATION":
            formname = "FORM " + str(self.count)
            dot.node(formname, "FORM")
            dot.edge("NEG " + str(self.count), formname)
        elif self.check == True:
            formname = "FORM " + str(self.count)
            dot.node(formname, "FORM")
            dot.edge("FORM " + str(self.count-1), formname)
            self.stack.append(self.count)
        else:
            formname = "FORM " + str(self.count)
            dot.node(formname, "FORM")
            dot.edge("FORM " + str(self.count-1), formname)

        self.count += 1

        self.check = False

        if self._accept("PREDICATE"):
            predname = "PRED " + str(self.count)
            dot.node(predname, "PRED")
            dot.edge("FORM " + str(self.count-1), predname)
            formula += self.Pred()
            if self.next_tok == "$" or self.switch == True:
                return formula
            else:
                self._except("END OF FORMULA AFTER PREDICATE")


        elif self._accept("NEGATION"):
            formula += self.Neg()
            self.switch = True
            negname = "NEG " + str(self.count)
            dot.node(negname, "NEG")
            dot.edge("FORM " + str(self.count-1),negname)
            formula = self.form(formula)
            self.switch = False
            

        elif self._accept("LEFTPARENTH"):
            formula += "("
            leftname = "( " + str(self.count)
            dot.node(leftname, "(")
            dot.edge("FORM " + str(self.count-1), leftname)
            self.scope += 1
            self.lparenth_count += 1
            if self._accept("TERM"):
                formula += self.Term()
                termname = "TERM " + str(self.count+self.termcount)
                dot.node(termname, "TERM")
                dot.edge("FORM " + str(self.count-1), termname)
                self.termcount +=1
                if self._accept("EQUAL"):
                    formula += self.Eq()
                    eqname = "EQ " + str(self.count)
                    dot.node(eqname, "EQ")
                    dot.edge("FORM " + str(self.count-1), eqname)
                    if self._accept("TERM"):
                        formula += self.Term()
                        termname = "TERM " + str(self.count+self.termcount)
                        dot.node(termname, "TERM")
                        dot.edge("FORM " + str(self.count-1), termname)
                        self.termcount+=1
                        if self._accept("RIGHTPARENTH"):
                            self.rparenth_count +=1
                            formula += ")"
                            self.scope -= 1
                            rightname = ") " + str(self.rcount)
                            dot.node(rightname, ")")
                            dot.edge("FORM " + str(self.count-1), rightname)
                            self.rcount += 1
                        else:
                            self._except("RIGHTPARENTH")
                    else:
                        self._except("TERM")
                else:
                    self._except("EQUAL")
            elif self.next_tok == "$":
                self._except("FORMULA")
            else:
                self.switch = True
                self.check = True
                formula = self.form(formula)
                if self._accept("CONNECTIVE"):
                    formula += self.Conn()
                    conname = "CONN " + str(self.count)
                    dot.node(conname, "CONN")
                    self.next_form = self.stack.pop()-1
                    tempCheck = self.next_form
                    dot.edge("FORM " + str(self.next_form), conname)
                    if self.next_tok == "$":
                        self._except("FORMULA")
                    else:
                        self.check = True
                        formula = self.form(formula)
                        if self.next_tok == "$":
                            return formula
                        elif self._accept("RIGHTPARENTH"):
                            self.rparenth_count += 1
                            self.scope -= 1
                            rightname = ") " + str(self.rcount)
                            dot.node(rightname, ")")
                            dot.edge("FORM " + str(tempCheck), rightname)
                            self.rcount += 1
                            formula += ")"
                        else:
                            self._except("PARENTHESIS")
                else:
                    self._except("CONNECTIVE")

        elif self._accept("QUANTIFIER"):
            formula += self.Quant()
            quantname = "QUANT " + str(self.count)
            dot.node(quantname, "QUANT")
            dot.edge("FORM " + str(self.count-1),quantname)
            if self._accept("TERM"):
                formula += self.Var()
                varname = "VAR " + str(self.count)
                dot.node(varname, "VAR")
                dot.edge("FORM " + str(self.count-1),varname)
                self.switch = True
                formula = self.form(formula)
                self.switch = False
            else:
                self._except("VARIABLE")
        else:
            self._except("LEFTPARANTH, NEG, QUANTIFIER or PREDICATE")
        
        return formula

    #Counts how many left and right parentheses there are
    def ParCount(self):
        left = 0
        right = 0
        for i in range(0,len(token_stream)):
            tokenCheck = token_stream[i].split()[0]
            if(tokenCheck == "LEFTPARENTH"):
                left += 1
            elif (tokenCheck == "RIGHTPARENTH"):
                right += 1

        if left != right:
            print("ERROR: Number of left parentheses and right parentheses do not match!")
            logfile("ERROR: Number of left parentheses and right parentheses do not match!")
            return False
        else:
            return True
    
    #From here on its the definitions of the non terminals. Each function creates a new node and attaches it onto correct parent node. It also parses through the formula while doing this.
    def Pred(self):
        predic =  self.curr_val

        if self._accept("LEFTPARENTH"):
            predic += "("
            var_count = 0
            comma_count = 0
            for k in rules:
                for v in rules[k]:
                    if predic in v:
                        pre = v
                        break
            randomlist=[]
            for i in range(30):
                r=random.randint(1,1000)
                if r not in randomlist: 
                    randomlist.append(r)

            arity = pre.count('Term')
            while self._accept("TERM") or self._accept("COMMA"):
                predic += self.curr_val
                if self.curr_tok == 'TERM' and (self.next_tok == "COMMA" or self.next_tok == "RIGHTPARENTH") and self.curr_val in variables:
                    term = "VARIABLE " + str(randomlist[var_count])
                    dot.node(term,self.curr_val)
                    dot.edge("PRED " + str(self.count),term)
                    var_count += 1
                    
                elif self.curr_tok == 'COMMA' and self.next_tok == "TERM":
                    termComma = "COMMA " + str(randomlist[-comma_count])
                    dot.node(termComma,self.curr_val)
                    dot.edge("PRED " + str(self.count),termComma)
                    comma_count += 1
                elif self.curr_tok == 'COMMA' and self.next_tok != "VARIABLE":
                    self._except("VARIABLE")
                else:
                    self._except("COMMA")

            if var_count == arity and (comma_count == math.ceil(var_count/2) or comma_count == 0):
                if self._accept("RIGHTPARENTH"):
                    predic += self.curr_val
                else:
                    self._except("RIGHTPARENTH")
            else:
                self._except("PREDICATE WITH ARITY " + str(arity))
        else:
            self._except("LEFTPARENTH")
        
        return predic

    def Term(self):
        if self.curr_tok == "TERM" and self.curr_val in variables:
            self.termCheck = True
            return self.Var()
        elif self.curr_tok == "TERM" and self.curr_val in constants:
            self.termCheck = True
            return self.Const()
        else:
            self._except("TERM")

    def Neg(self):
        if self.curr_val != connectives[-1]:
            self._except("NEGATION")
        else:
            tempN = self.curr_val
            backslashcount = tempN.count("\\")
            if backslashcount > 0:
                for i in range(backslashcount):
                    location = tempN.find("\\")
                    newN = tempN[:location] + "\\" + tempN[location:]
                    tempN = newN

            termNeg = "NEGATIVE " + str(self.negcount)
            dot.node(termNeg,tempN)
            dot.edge("NEG " + str(self.count),termNeg)
            self.negcount -=1
            return self.curr_val

    def Eq(self):
        if self.curr_val not in equality:
            self._except("EQUAL")
        else:
            tempE = self.curr_val
            backslashcount = tempE.count("\\")
            if backslashcount > 0:
                for i in range(backslashcount):
                    location = tempE.find("\\")
                    newE = tempE[:location] + "\\" + tempE[location:]
                    tempE = newE

            termEq = "EQUALITY " + str(self.eqcount)
            dot.node(termEq,tempE)
            dot.edge("EQ " + str(self.count),termEq)
            self.eqcount -=1
            return self.curr_val

    def Conn(self):
        if self.curr_val not in connectives[:-1]:
            self._except("CONNECTIVE")
        else:
            tempC = self.curr_val
            backslashcount = tempC.count("\\")
            if backslashcount > 0:
                for i in range(backslashcount):
                    location = tempC.find("\\")
                    newC = tempC[:location] + "\\" + tempC[location:]
                    tempC = newC

            termCon = "CONNECTIVE " + str(self.connectivecount)
            dot.node(termCon,tempC)
            dot.edge("CONN " + str(self.count),termCon)
            self.connectivecount -= 1
            return self.curr_val

    def Quant(self):
        if self.curr_val not in quantifiers:
            self._except("QUANTIFIER")
        else:
            termQuan = "QUANTIFIER " + str(self.quantifiercount)
            dot.node(termQuan,self.curr_val)
            dot.edge("QUANT " + str(self.count),termQuan)
            self.quantifiercount -=1
            return self.curr_val

    def Const(self):
        if self.curr_val not in constants:
            self._except("CONSTANT")
        elif self.termCheck == True:
            termCons = "CONSTANT " + str(self.constantcount)
            dot.node(termCons,self.curr_val)
            dot.edge("TERM " + str(self.count+self.termcount),termCons)
            self.constantcount -= 1
            self.termCheck = False
            return self.curr_val
        else:
            termCons = "CONSTANT " + str(self.constantcount)
            dot.node(termCons,self.curr_val)
            dot.edge("TERM " + str(self.count),termCons)
            self.constantcount -= 1
            self.termCheck = False
            return self.curr_val

    def Var(self):
        if self.curr_val not in variables:
            self._except("VARIABLE")
        elif(self.termCheck == True):
            termVar = "VARIABLE " + str(self.variablecount)
            dot.node(termVar,self.curr_val)
            dot.edge("TERM " + str(self.count+self.termcount),termVar)
            self.variablecount -=1
            self.termCheck = False
            return self.curr_val
        else:
            termVar = "VARIABLE " + str(self.variablecount)
            dot.node(termVar,self.curr_val)
            dot.edge("VAR " + str(self.count),termVar)
            self.variablecount -=1
            self.termCheck = False
            return self.curr_val

#Creates a parse tree image file, also displays the graph to the user when function called.
def parsetree():
    dot.render('abstract-syntax-tree', view=True)  

validateFile()
grammer()
lexer()
e = Parser()
parsed = e.parse(formula_string)

if e.ParCount() == True:
    parsetree()
    print("PARSED SUCCESSFULLY!")
    logfile("Formula is valid!")
else:
    print("PARSE FAILED!")
    logfile("Formula is not valid!")

log.close()
