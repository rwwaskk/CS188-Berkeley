strings=['HELLO','WORLD','PYTHON','IS','VERY','COOL']
greaterThanFive=[x for x in strings if len(x)>=5]
lowerCase=map(lambda x:x.lower(),greaterThanFive)
print lowerCase