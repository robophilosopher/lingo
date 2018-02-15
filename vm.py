#TODO: store constants in const, not store
# the Buffer type represents an array of chars
# Buffer types should never
# For single chars, you don't want to generate a whole string
# Just use the char type
# Data in the constant pool and store are of type B for buffer
# The byte code variables are now specified like this s:s'1 which mean string type in store index 1
# get can be applied to store or const pool
# set can only be applied to ?
# We can declare arrays like this Let xs = [| 1, "a", "foo" |] where the bars help demarcate arrays
# Let xs = array(4)
# They will be heterogenous
# Arrays will always be stored in store
# They will take the a: type

# Temporary Pool
# t'1 | a:s'1

# Constant Pool
# c'1 | B: foo

# Storage Pool
# s'1 | A: 3
# s'2 | i: 1
# s'3 | c: a
# s'4 | s:c'1

# Imagine a nested array
# Let xs = [| [|1|], "a", "foo" |]
# s'1 | A:1
# s'2 | i:1
# s'3 | A:3
# s'4 | a:s'1
# ...

# We also have a record type
# Let xs = {| a: 1, b: 2 |}
# where the index is aliased, so xs.a == xs[1]
# s'1 | R:2; a,b
# s'2 | i:1
# s'3 | i:2

import pdb

class ProgramObject():
    def __init__(self):
        self._code = []
        self._const = []
        self._label_index = {}
        self._labeled_instruction_index = {}
        self._ip = 0

    def code(self, ins, label=0):
        self._code.append(ins)
        self._ip += 1

        if label != 0:
            self._labeled_instruction_index[ins] = label

    def const(self, val):
        self._const.append(val)

    def deciLbl(self, label):
        self._label_index[label] = self._ip

    def ilbl(self, label):
        return label

    def end(self):
        i = 0

        labeled_lines = self._labeled_instruction_index.keys()
        for ins in self._code:
            if ins in labeled_lines:
                label = self._labeled_instruction_index[ins]
                jump_to = self._label_index[label] - i
                self._code[i] = ins + ' {0}'.format(str(jump_to))
            i += 1

class VM():

    def run(po):
        # use ip as an instruction pointer
        ip = 0
        # use tmp to store variables
        tmp = {}
        # code stores bytecode instructions
        code = []
        # store is for globals and constants
        store = {}

        code.append(po.code)
        constant_index = 1

        # load constants
        for c in po._const:
            store['c{0}'.format(constant_index)] = c
            constant_index += 1

        # eval
        while(True):
            try:
                ins = po._code[ip].split(" ")
            except:
                break

            ip += 1
            op = ins[0]

            if op == 'set':
                tmp[ins[1]] = ins[2]

            if op == 'iadd':
                tmp[ins[1]] = int(tmp[ins[2]]) + int(tmp[ins[3]])

            if op == 'isub':
                tmp[ins[1]] = int(tmp[ins[2]]) - int(tmp[ins[3]])

            if op == 'bru':
                if tmp[ins[1]] == '0':
                    # move the ip by the distance to the jump point
                    ip = ip + (ip - int(ins[2]))

            if op == 'cload':
                tmp[ins[1]] = store[ins[2]]

            if op == 'print':
                # result is for testing purposes
                print(tmp[ins[1]])

po = ProgramObject()
po.code("set t1 1")
po.code("set t2 2")
po.code("iadd t3 t1 t2")
po.code("print t3")
assert(VM.run(po)) == 3

po = ProgramObject()
po.code("set t1 2")
po.code("set t3 3")
po.code("isub t4 t3 t1")
po.code("set t5 1")
po.code("isub t2 t4 t5")
po.code("print t2")
assert(VM.run(po)) == 0

po = ProgramObject()
po.code("set t1 2")
po.code("set t3 3")
po.code("set t4 1")
po.code("isub t5 t1 t4")
po.code("isub t2 t3 t5")
po.code("print t2")
assert(VM.run(po)) == 2

po = ProgramObject()
po.const('hello world')
po.code('cload t1 c1')
po.code('print t1')
assert(VM.run(po)) == 'hello world'

po = ProgramObject()
po.const('bar')
po.const('baz')
po.code('cload t1 c1')
po.code('set t2 1')
po.code('cload t3 c2')
po.code('print t3')
po.code('set t2 2')
po.code('print t1')
po.code('print t2')
VM.run(po)



po = ProgramObject()
po.code("set t1 0")
po.code("set t2 42")
po.code("bru t1", po.ilbl('else'))
po.code("print t1")
po.deciLbl("else")
po.code("print t2")
po.end()
VM.run(po)
