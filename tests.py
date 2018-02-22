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

# print 3
#po = ProgramObject()
#po.code("set t'1 i: 1")
#po.code("set t'2 i: 2")
#po.code("iadd t'3 t'1 t'2")
#po.code("print t'3")
#VM.run(po)

# print 42 when t'1 is 1
# otherwise, print 24
#po = ProgramObject()
#po.code("set t'1 i: 0")
#po.code("set t'2 i: 42")
#po.code("set t'3 i: 24")
#po.code("bru t'1", po.ilbl("end"))
#po.code("print t'2")
#po.code("br", po.ilbl("end"))
#po.code("print t'3")
#po.deciLbl("end")
#po.end()
#VM.run(po)

# print 44 from array
#po = ProgramObject()
#po.code("arr s'1 i:1")
#po.code("put s'1 i:0 i:44")
#po.code("get t'1 s'1 i:0")
#po.code("print t'1")
#VM.run(po)

