import random

LONG_MIN=-122.327361
LONG_MAX=-122.312425
LONG_RANGE=LONG_MAX - LONG_MIN

LAT_MAX=47.625556
LAT_MIN=47.618333
LAT_RANGE=LAT_MAX - LAT_MIN

V_long=-122.32083
H_lat=47.6196889


f=open('uid.csv','r')
lines=f.readlines()
f.close()

f_stat=open('static.csv','w')
CLIENT_HOME='./client_data/'
lines1=lines[0:50]
lines2=lines[50:]

def randomSign():
	return (-1)**random.randint(1, 10)

def jiggle():
	return randomSign()*random.random()*0.00001

def generate_v():
	x=V_long+jiggle()
	y=LAT_RANGE*random.random()+LAT_MIN+jiggle()
	return [x,y]

def generate_h():
	x=LONG_RANGE*random.random()+LONG_MIN+jiggle()
	y=H_lat+jiggle()
	return [x,y]

def generate_0():
	lx=LONG_MIN
	ly=LAT_MIN
	rx=V_long-LONG_MIN
	ry=H_lat-LAT_MIN
	x=rx*random.random()+lx+jiggle()
	y=ry*random.random()+ly+jiggle()
	return [x,y]

def generate_1():
	lx=V_long
	ly=LAT_MIN
	rx=LONG_MAX-V_long
	ry=H_lat-LAT_MIN
	x=rx*random.random()+lx+jiggle()
	y=ry*random.random()+ly+jiggle()
	return [x,y]

def generate_2():
	lx=V_long
	ly=H_lat
	rx=LONG_MAX-V_long
	ry=LAT_MAX-H_lat
	x=rx*random.random()+lx+jiggle()
	y=ry*random.random()+ly+jiggle()
	return [x,y]

def generate_3():
	lx=LONG_MIN
	ly=H_lat
	rx=V_long-LONG_MIN
	ry=LAT_MAX-H_lat
	x=rx*random.random()+lx+jiggle()
	y=ry*random.random()+ly+jiggle()
	return [x,y]

def generate_loc(d):
	if d==0:
		return generate_0()
	elif d==1:
		return generate_1()
	elif d==2:
		return generate_2()
	else:
		return generate_3()	


def roll(d):
	key=random.random()
	if d==0:
		if key<0.4:
			return 0
		else:
			return 1
	elif d==1:
		if key<0.3:
			return 1
		elif key<0.5:
			return 3
		else:
			return 2
	elif d==2:
		if key<0.4:
			return 2
		else:
			return 3
	else:
		if key<0.7:
			return 3
		else:
			return 0


for line in lines1:
	uid=str(line.strip())
	if random.random()>0.55:
		loc=generate_h()
		msg=uid+','+str(loc[0])+','+str(loc[1])
		f_stat.writelines(msg+'\n')
	else:
		loc=generate_v()
		msg=uid+','+str(loc[0])+','+str(loc[1])
		f_stat.writelines(msg+'\n')	
f_stat.close()


for line in lines2:
	uid=str(line.strip())
	filename=CLIENT_HOME+str(uid)+'.csv'
	f_tmp=open(filename,'w')

	landmark=[]
	dice=0
	for i in range(5):
		dice=roll(dice)
		landmark.append(generate_loc(dice))

	record=[]
	record.append(landmark[0])
	for i in range(len(landmark)-1):
		loc1=landmark[i]
		loc2=landmark[i+1]
		deltax=(loc1[0]-loc2[0])/10.0
		deltay=(loc1[1]-loc2[1])/10.0
		x=loc1[0]
		y=loc1[1]
		for i in range(10):
			x+=deltax
			y+=deltay
			record.append([x,y])
	for loc in record:
		msg=uid+','+str(loc[0])+','+str(loc[1])
		f_tmp.writelines(msg+'\n')	
	f_tmp.close()



