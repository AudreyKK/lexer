import lexer
from lexer import Lexer
from parse_table import NT_list, parse_table
from lexer import Token

myfile = open("RHS.txt")


# grammarTxt = myfile.read()
# print grammarTxt


def get_Productions(location):  # location is the number code retrieved from parse_table
    '''From RHS.txt based on input of location (integer) and
    outputs the productions in array format'''
    myfile.seek(0)
    for line in myfile:
        location = str(location)
        if location + ':' == line[0:(len(location) + 1)]:
            stack_stuff = line.split('::=')
            safe_stack = line.split('::=')
            stack_stuff[-1] = stack_stuff[-1].strip()
            productions = stack_stuff[1].split(' ')
            if safe_stack[1].strip(' ') == '\n':
                productions = ['E']
            line = 0
            return productions

class SymbolTable(object):

    def __init__(self, size):
        self.table = {}
        self.size = size
        self.remaining_capacity = size - 1
        for i in range(size):
            self.table[i] = 'none'

    def search(self, key):
        return self.table[key]

    def insert(self, symbol):
        if self.remaining_capacity > 0:
            self.table[symbol] = self.table.pop(self.remaining_capacity)
            self.remaining_capacity -= 1


    def dumpTable(self):
        print self.table

class SymbolTableEntry(object):


        def __init__(self):
            self.name = None
            self.address = None
            self.type = None
            self.upperBound = None
            self.lowerBound = None
            self.numParam = None
            self.paramInfo = None
            self.result = None
            self.local = False # the entry is default assumed global unless otherwise stated
            return

        def isVariable(self):
            return False

        def isProcedure(self):
            return False

        def isFunction(self):
            return False

        def isFunctionResult(self):
            return False

        def isParameter(self):
            return False

        def isArray(self):
            return False

        def isReserved(self):
            return False

class ArrayEntry(SymbolTableEntry):


    def __init__(self, name): #, address, type, upperBound, lowerBound):
        self.name = name # name
        self.address = None # address
        self.type = None # type
        self.upperBound = None # upperBound
        self.lowerBound = None # lowerBound
        self.local = False

    def isArray(self):
        return True
        
    def displayEntry(self):
        print 'name: %r, address: %r, type: %r, upperBound: %r, lowerBound: %r' % (self.name, self.address, self.type, self.upperBound, self.lowerBound)

class ConstantEntry(SymbolTableEntry):

    def __init__(self, name):
        self.name = name
        self.type = None
        self.local = False

    def isConstant(self):
        return True
        
    def displayEntry(self):
        print 'name: %r, type: %r' % (self.name, self.type)

class FunctionEntry(SymbolTableEntry):

    def __init__(self, name):
    
        self.name = name
        self.numParam = None
        self.paramInfo = None
        self.result = None
        self.local = False

    def isFunction(self):
        return True
        
    def displayEntry(self):
        print 'name: %r, numParam: %r, paramInfo: %r, result: %r' % (self.name, self.numParam, self.paramInfo, self.result)

class ProcedureEntry(SymbolTableEntry):

    def __init__(self, name):
        self.name = name
        self.numParam= None
        self.paramInfo = None
        self.local = False

    def isProcedure(self):
        return True
        
    def displayEntry(self):
        print 'name: %r, numParam: %r, paramInfo: %r' % (self.name, self.numParam, self.paramInfo)

class VariableEntry(SymbolTableEntry):

    def __init__(self, name): #, address, type):
        self.name = name
        self.address = None
        self.type = None
        self.local = False

    def isVariable(self):
        return True
        
    def displayEntry(self):
        print 'name: %r, address: %r, type: %r' % (self.name, self.address, self.type)

class IODeviceEntry(SymbolTableEntry):

    def __init__(self, name):
        self.name = name.upper() #lexer is standardized to uppercase
        self.local = False

    def isIODevice(self):
        return True
    
    def displayEntry(self):
        print 'name: %r' % self.name

class SymbolError(SymbolTableEntry):

    def __init__(self):
        print 'error'
        

class Quadruples(object):
    
    def __init__(self):
        self.Quadruple = []
        self.nextQuad = 0
        self.dummy_quad = [None] * 4
        self.Quadruple.append(self.dummy_quad)
        self.nextQuad += 1 
        return
        
    def getField(self, quadIndex, index):
        return self.Quadruple[quadIndex][index]
    
    def setField(self, quadIndex, index, field):
        self.Quadruple[quadIndex][index] = field
        return
    
    def getNextQuad(self):
        return self.nextQuad
        
    def incrementNextQuad(self):
        self.nextQuad += 1
        return
    
    def getQuad(self, index):
        return self.Quadruple[index]
    
    def addQuad(self):
        newQuad = [None] * 4
        self.Quadruple.append(newQuad)
        self.incrementNextQuad
        return
        
    
        
    def printCode(self):
        
        quadLabel = 1
        separator = None
        
        print'CODE:'
        
        for i in range(len(self.Quadruple)):
            quad = self.Quadruple[i]
            if quad[0] != None:
                print '%r: %s,' % (quadLabel, quad[0]),
            
            if quad[1] != None:
                print '%s,' % quad[1],
            
            if quad[2] != None:
                print '%s,' % quad[2],
            
            if quad[3] != None:
                print '%s \n' % quad[3]
            
            quadLabel += 1

#### Semantic Actions ####

class SemanticActions(object):

    def __init__(self):
        return

    semStack = []
    quadruple = Quadruple()
    
    def peek():
        return semStack[-1]
    
    #### declarations of global and constant symbol tables #######
    
    globalSymbolTable = SymbolTable(100)
    localSymbolTable = SymbolTable(100)
    constantSymbolTable = SymbolTable(100)
    
    globalSymbolTable.insert(ProcedureEntry('READ', 0, 'none'))
    globalSymbolTable.insert(ProcedureEntry('MAIN', 0, 'none'))
    globalSymbolTable.insert(ProcedureEntry('WRITE', 0, 'none'))

    insertFlag = True # insert/search
    globalFlag = True # global/local
    arrayFlag = False # array/simple
    global_Store = 0
    global_Mem = 0
    local_Mem = 0
        
    
    
    def gen(self, tviCode=None, id1=None, id2=None, id3=None):
        
        if tviCode != None:
            operator = tviCode
            quadruple.setField((quadruple.getNextQuad() - 1), 0, operator)
        else:
            print 'error, no TVI instruction given'
        if id1 != None:
            if self.local:
                op1 = '%%%r' % id1.address
                quadruple.setField((quadruple.getNextQuad() - 1), 1, op1)
            else:
                op1 = '_%r' % id1.address
                quadruple.setField((quadruple.getNextQuad() - 1), 1, op1)
        if id2 != None:
            if self.local:
                op2 = '%%%r' % id2.address
                quadruple.setField((quadruple.getNextQuad() - 1), 2, op2)
            else:
                op2 = '_%r' % id2.address
                quadruple.setField((quadruple.getNextQuad() - 1), 2, op2)
        if id3 != None:
            if self.local:
                op3 = '%%%r' % id3.address
                quadruple.setField((quadruple.getNextQuad() - 1), 3, op3)
            else:
                op3 = '_%r' % id3.address
                quadruple.setField((quadruple.getNextQuad() - 1), 3, op3)
        
        quadruple.addQuad()
            
        

    def execute(self, action, token):
    
        if action == '#13':
            self.semStack.append(token)
        elif action == '#9':
            # pop the IDs output
            id1 = self.semStack[-1]
            del(self.semStack[-1])
            # input
            id2 = self.semStack[-1]
            del(self.semStack[-1])
            # program name
            id3 = self.semStack[-1]
            del(self.semStack[-1])

            globalSymbolTable.insert(IODeviceEntry(id1.type)) # name param takes a string not a token
            globalSymbolTable.insert(IODeviceEntry(id2.type))
            globalSymbolTable.insert(ProcedureEntry(id3.type, 0, 'none'))
            
            gen('call', 'main', 0)
            ge('exit')
            
        elif action == '#7':
            self.semStack.append(token) # should be an integer id
        elif action == '#6':
            self.arrayFlag = True
        elif action == '#4': # should be a <type>
            self.semStack.append(token)
        elif action == '#3':
            
            type = semStack.pop().type
            if self.arrayFlag:
                upperBound = int(semStack.pop().value)
                lowerBound = int(semStack.pop().value)
                memorySize = (upperBound - lowerBound) + 1

                while ( semStack.peek() == 'identifier'):
                        tok = semStack.pop()
                        id = ArrayEntry(tok.value)
                        id.type = type
                        id.upperBound = upperBound
                        id.lowerBound = lowerBound   
                        
                        if self.globalFlag:
                            id.address = global_Mem 
                            globalSymbolTable.insert(id)
                            global_Mem += memorySize
                        else:
                            id.address = local_Mem
                            # id.local = True
                            localSymbolTable.insert(id)
                            local_Mem += memorySize
                
            else: # simple variable
                while(semStack.peek() == 'identifier'):
                    tok = semStack.peek()
                    id = VariableEntry(tok.value)
                    id.type = type
                    
                    if self.globalFlag:
                        id.address = global_Mem
                        globalSymbolTable.insert(id)
                        global_Mem += 1
                    else:
                        id.address = local_Mem
                        # id.local = True
                        localSymbolTable.insert(id)
                        local_Mem += 1
            
            arrayFlag = False
                        
                    


        elif action =='#2':
            self.insertFlag = False
        elif action == '#1':
            self.insertFlag = True


        return
                
        
    


######## Parse Stack #######

class ParseStack(object):

    def __init__(self):
        self.items = ['ENDOFFILE', '<Goal>']

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def is_NT(self):  # determines if item on stack is a non-terminal
        string = self.items[-1]
        return string[0] == '<'

    def isAction(self):
        string = self.items[-1]
        return string[0] == '#'

    def dumpStack(self):
        print 'Stack ::==> %r ' % self.items[::-1]
        return



class Parser(object):

    def __init__(self):
        return

    def parsely(self):

        lexer = Lexer()
        stack = ParseStack()
        semantics = SemanticActions()
        i = 1


        for token in lexer.GetNextToken():

            tok = token.type.lower()

            if stack.peek().lower() == tok:
                # two equivalent terminals we pop the stack and go to the next token
                print '>>- %r -<<' % i
                stack.dumpStack()
                i += 1
                print 'Popped %r with token %r -> * MATCH * {consumes token}\n' % (stack.peek(), tok.upper())

                stack.pop()


            elif stack.isAction():
                semantics.execute(stack.peek(), prev)
                print '>>- %r -<<' % i
                stack.dumpStack()
                i += 1
                print 'Popped [%r] with token %r -> # SEMANTIC ACTION # [%r] \n' % (stack.peek(), tok.upper(), stack.peek().strip('#'))

                stack.pop()

                if stack.isAction():
                    while stack.isAction():
                        semantics.execute(stack.peek(), prev)
                        print '>>- %r -<<' % i
                        stack.dumpStack()
                        i += 1
                        print 'Popped [%r] with token %r -> # SEMANTIC ACTION # [%r] \n' % (stack.peek(), tok.upper(), stack.peek().strip('#'))

                        stack.pop()

                if stack.peek().lower() == tok:
                    print '>>- %r -<<' % i
                    stack.dumpStack()
                    print 'Popped %r with token %r -> *MATCH* {consumes tokens} \n' % (stack.peek(), tok.upper())
                    i += 1
                    prev = token
                    stack.pop()

                elif not(stack.is_NT()):
                    print 'error'

                elif stack.is_NT():
                    while not(stack.peek()) == tok:
                        next = abs(parse_table[NT_list.index(stack.peek())][tok])

                        if next == 999:
                            print 'error'
                            return
                        else:
                            print '>>- %r -<<' % i
                            stack.dumpStack()
                            i += 1
                            print 'Popped %r with token %r ->' % (stack.peek(), tok)

                            prods = get_Productions(next)
                            print '$ PUSH $ [%r]%r ::= %r \n' % (next, stack.peek(), prods)
                            stack.pop()
                            for x in prods[::-1]:
                                stack.push(x)

                            if stack.peek() == 'E':
                                stack.pop()

                            if stack.isAction():
                                while stack.isAction():
                                    semantics.execute(stack.peek(), prev)
                                    print '>>- %r -<<' % i
                                    stack.dumpStack()
                                    i += 1
                                    print 'Popped [%r] with token %r -> # SEMANTIC ACTION # [%r] \n' % (stack.peek(), tok.upper(), stack.peek().strip('#'))

                                    stack.pop()

                            if stack.peek().lower() == tok:
                                print '>>- %r -<<' % i
                                stack.dumpStack()
                                print 'Popped %r with token %r -> * MATCH * {consume tokens} \n' % (stack.peek(), tok)
                                i += 1
                                prev = token #.type.lower()
                                stack.pop()
                                break
                            elif not (stack.is_NT):
                                # if top of stack is a terminal that doesn't match,return error
                                print 'error'
                                return

            elif not(stack.is_NT()):
                # two non equivalent terminals return an error message
                print 'error'
                return

            elif stack.is_NT():
                # if the stack is a non-terminal, it either produces a 999 error
                # or it continues to refresh the stack until the current token finds an
                # equivalent terminal and the parser can retrieve the next token

                while not (stack.peek()) == tok:
                    next = abs(parse_table[NT_list.index(stack.peek())][tok])


                    if next == 999:
                        print'error'
                        return
                    else:
                        print '>>- %r -<<' % i
                        stack.dumpStack()
                        i += 1
                        print 'Popped %r with token %r ->' % (stack.peek(), tok.upper())

                        prods = get_Productions(next)
                        print '$ PUSH $ [%r]%r ::= %r \n' % (next, stack.peek(), prods)
                        stack.pop()
                        for x in prods[::-1]:
                           # print x
                            stack.push(x)

                        if stack.peek() == 'E':
                            stack.pop()

                        if stack.isAction():
                            while stack.isAction():
                                semantics.execute(stack.peek(), prev)
                                print '>>- %r -<<' % i
                                stack.dumpStack()
                                i += 1
                                print 'Popped [%r] with token %r -> # SEMANTIC ACTION # [%r] \n' % (stack.peek(), tok.upper(), stack.peek().strip('#'))

                                stack.pop()

                        if stack.peek().lower() == tok:
                            print '>>- %r -<<' % i
                            stack.dumpStack()
                            print 'Popped %r with token %r -> * MATCH *  {consume tokens}\n' % (stack.peek(), tok.upper())
                            i += 1
                            prev = token
                            stack.pop()
                            break
                        elif not (stack.is_NT):
                            # if top of stack is a terminal that doesn't match,return error
                            print 'error'
                            return

        if stack.isEmpty:
            print '! ACCEPT !'

def main():
    parser = Parser()
    parser.parsely()


main()

# def run_parser:
