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

