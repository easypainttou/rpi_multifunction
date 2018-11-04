from flask import Flask,render_template,request
import random
app=Flask(__name__)

@app.route('/')
def index():
	return render_template('dashboard.html')

@app.route('/print',methods=['POST'])
def printtext():
	if request.method=='POST':
		print(request.form['message'])
		return '你打了'+request.form['message']

@app.route('/chart',methods=['POST'])
def chart():
	if request.method=='POST':
		data=[]
		print(request.form['message'])
		for i in range(4):
			data.append(random.randint(20,70))
		print('{time:[1,2,3,4],data:'+str(data)+'}')
		return '{time:[1,2,3,4],data:'+str(data)+'}'
		
if __name__=='__main__':
	app.run(debug=True)
