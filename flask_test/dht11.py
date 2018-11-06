import RPi.GPIO as GPIO
import time
import sqlite3

channel=37
dht_data=[]


GPIO.setmode(GPIO.BOARD)

def get_data(channel):
    j=0
    data=[]
    time.sleep(1)
    GPIO.setup(channel,GPIO.OUT)
    GPIO.output(channel,0)
    time.sleep(0.02)
    GPIO.output(channel,1)
    GPIO.setup(channel,GPIO.IN)
    while GPIO.input(channel)==0:
        continue
    while GPIO.input(channel)==1:
        continue
    while j<40:
        k=0
        while GPIO.input(channel)==0:
            continue
        while GPIO.input(channel)==1:
            k+=1
            if k>100:
                break
        if k<8:
            data.append(0)
        else:
            data.append(1)
        j+=1
    print(data)
    hum_int_b=data[0:8]
    hum_dec_b=data[8:16]
    tem_int_b=data[16:24]
    tem_dec_b=data[24:32]
    parity_b=data[32:40]
    hum_int=0
    hum_dec=0
    tem_int=0
    tem_dec=0
    parity=0
    for i in range(8):
        hum_int=hum_int*2+hum_int_b[i]
        hum_dec=hum_dec*2+hum_dec_b[i]
        tem_int=tem_int*2+tem_int_b[i]
        tem_dec=tem_dec*2+tem_dec_b[i]
        parity=parity*2+parity_b[i]
    tmp=hum_int+hum_dec+tem_int+tem_dec
    if parity==tmp:
        return 1,hum_int,hum_dec,tem_int,tem_dec
    else:
        return 0,hum_int,hum_dec,tem_int,tem_dec
    
try:
    flag=0
    while flag==0:
        time.sleep(5)
        flag,hum_int,hum_dec,tem_int,tem_dec=get_data(channel)
        # print("wrong")    
    hum=(str(hum_int)+'.'+str(hum_dec))
    tem=(str(tem_int)+'.'+str(tem_dec))
    print('humidity:'+str(hum_int)+'.'+str(hum_dec)+'\ntemperature:'+str(tem_int)+'.'+str(tem_dec))
    
    conn=sqlite3.connect('data.db')
    curs=conn.cursor()
    exestr="INSERT INTO data VALUES (datetime('now','localtime'),"+tem+","+hum+");"
    curs.execute(exestr)
    exestr="DELETE FROM data WHERE julianday('now')-julianday(datetime)>2"
    curs.execute(exestr)
    conn.commit()
    conn.close()
    print("success!")
except KeyboardInterrupt:
    pass
GPIO.cleanup()

