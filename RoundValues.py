import sys
import os
num=float(sys.argv[1])
err=float(sys.argv[2])
for i in range(len(str(err))+1):
	if err-10**i<-.0000000000001:
		if err-10**i<-.0000000000001:
			if i!=0:
				if str(err)[0]=='1':
					print int(round(num,-i+2)),int(round(err,-i+2))
					sys.exit()
				print int(round(num,-i+1)),int(round(err,-i+1))
				sys.exit()
		
			else:
				for i in range(len(str(err+3))):
						if 10**-i-err<(.000000000001):
							if round(err,i)!=1*10**-i:
								print round(num,i),round(err,i)
								sys.exit()
							else:
								print round(num,i+1),round(err,i+1)
								sys.exit()
sys.exit()