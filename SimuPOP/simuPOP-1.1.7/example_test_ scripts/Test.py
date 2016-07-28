import os, re
for f in os.listdir('.'):
   if re.match('001_MN_DX', f):
       print f