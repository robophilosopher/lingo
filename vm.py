#TODO: store constants in const, not store
# the Buffer type represents an array of chars
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
                tmp[ins[1]] = ins[3]

            if op == 'iadd':
                tmp[ins[1]] = int(tmp[ins[2]]) + int(tmp[ins[3]])

            if op == 'isub':
                tmp[ins[1]] = int(tmp[ins[2]]) - int(tmp[ins[3]])

            if op == 'bru':
                if tmp[ins[1]] == '0':
                    # move the ip by the distance to the jump point
                    # TODO: why are you off by 2?
                    ip = ip + int(ins[2]) - 2

            if op == 'br':
                # move the ip by the distance to the jump point
                ip = ip + int(ins[1])

            if op == 'cload':
                tmp[ins[1]] = store[ins[2]]

            if op == 'arr':
                # example array code: arr s'1 a:c'6
                list = []
                _, length = ins[2].split(':')
                for i in range(0, int(length)):
                    list.append(0)

                store[ins[1]] = list

            if op == 'put':
                # this code is used to insert into an array
                array = store[ins[1]]
                _, index = ins[2].split(':')
                val_type, val = ins[3].split(':')
                
                # TODO: need some type handling based on val_type
                array[int(index)] = val

            if op == 'get':
                # this code gets from an array and sets to a temp
                # get t'1 s'1 i:1
                array = store[ins[2]]
                _, index = ins[3].split(':')
                tmp[ins[1]] = array[int(index)]

            if op == 'print':
                print(tmp[ins[1]])

# print 3
po = ProgramObject()
po.code("set t'1 i: 1")
po.code("set t'2 i: 2")
po.code("iadd t'3 t'1 t'2")
po.code("print t'3")
VM.run(po)

# print 42 when t'1 is 1
# otherwise, print 24
po = ProgramObject()
po.code("set t'1 i: 0")
po.code("set t'2 i: 42")
po.code("set t'3 i: 24")
po.code("bru t'1", po.ilbl("end"))
po.code("print t'2")
po.code("br", po.ilbl("end"))
po.code("print t'3")
po.deciLbl("end")
po.end()
VM.run(po)

# print 44 from array
po = ProgramObject()
po.code("arr s'1 i:1")
po.code("put s'1 i:0 i:44")
po.code("get t'1 s'1 i:0")
po.code("print t'1")
VM.run(po)
