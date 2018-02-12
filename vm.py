import pdb

class ProgramObject():
    def __init__(self):
        self._code = []
        self._const = []

    def code(self, ins):
        self._code.append(ins)

    def const(self, val):
        self._const.append(val)

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

            if op == 'cload':
                tmp[ins[1]] = store[ins[2]]

            if op == 'print':
                # result is for testing purposes
                result = tmp[ins[1]]

                print(result)
                return result

# TODO: get these tests out of here and break out the classes into separate files
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