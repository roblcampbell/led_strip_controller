import sys

class A(object):
	myInt = 1
	myStr = "one"
	def printme(self):
		print "myInt %d, myStr %s" % (self.myInt, self.myStr)

class B(A):
	def printme(self):
		print "I am subclass"


print "hello"
a = A()
a.printme()
b = B()
b.printme()
print sys.path


