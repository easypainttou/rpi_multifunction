from flask import Flask,render_template,request
import random
import sqlite3
import RPi.GPIO as GPIO
import os

led=11

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))
 
# Return RAM information (unit=kb) in a list                                       
# Index 0: total RAM                                                               
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])
 
# Return % of CPU used by user as a character string                                
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))
 
# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                         
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])
 
 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led,GPIO.OUT)

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/print',methods=['POST'])
def printtext():
    if request.method=='POST':
        msg=request.form['message']
        if msg=='r on':
            GPIO.output(led,1)
        elif msg=='r off':
            GPIO.output(led,0)
        print(msg)
        return '你打了'+msg

@app.route('/chart',methods=['POST'])
def chart():
    if request.method=='POST':	
        msg=request.form['message']
		#for i in range(4):
		#	data.append(random.randint(20,70))
        conn=sqlite3.connect('data.db')
        curs=conn.cursor()
        exestr='SELECT * FROM data'
        all_data=curs.execute(exestr)
        time=[]
        data1=[]
        data2=[]
        for i in all_data:
            time.append(i[0])
            data1.append(i[1])
            data2.append(i[2])
        conn.close()
        res={}
        res['time']=time
        if msg=='tem':
            res['data']=data1
        elif msg=='hum':
            res['data']=data2
        return str(res)
@app.route('/info',methods=['POST'])
def info():
    if request.method=='POST':
        # CPU informatiom
        CPU_temp = getCPUtemperature()
        CPU_usage = getCPUuse()
 
        # RAM information
        # Output is in kb, here I convert it in Mb for readability
        RAM_stats = getRAMinfo()
        RAM_total = round(int(RAM_stats[0]) / 1000,1)
        RAM_used = round(int(RAM_stats[1]) / 1000,1)
        RAM_free = round(int(RAM_stats[2]) / 1000,1)
         
        # Disk information
        DISK_stats = getDiskSpace()
        DISK_total = DISK_stats[0]
        DISK_used = DISK_stats[1]
        DISK_perc = DISK_stats[3]
        res={}
        res['CPU_temp']=CPU_temp
        res['CPU_usage']=CPU_usage
        res['RAM_total']=RAM_total
        res['RAM_used']=RAM_used
        res['RAM_free']=RAM_free
        res['DISK_total']=DISK_total
        res['DISK_used']=DISK_used
        res['DISK_perc']=DISK_perc
        print(res)
        return str(res)

if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0")
