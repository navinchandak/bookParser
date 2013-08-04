def lineread (f):
  s=''
  while True:
    c=f.read(1)
    if not c:
      break
    if (c==":"or c=="_" or c =='"' or c=="?" or c=="!" or c=="-" or (c=='\n' and s[-1:]=='\n') or (c=="." and  s[-2:] != "Mr" and s[-3:]!= "Mrs")):
      if (c=='.' or c=='?'):
        return {'num':1,'string':s}  
      else:
        return {'num':0,'string':s}
    else:
      s+=c
      
      
      
      


      
