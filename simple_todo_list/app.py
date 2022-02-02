from flask import Flask, render_template, request, redirect
from datetime import datetime

app=Flask(__name__)
list1=[]


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        task_content = request.form.get('content')
        dd=datetime.utcnow()
        list1.append([task_content,dd])
        return redirect('/')
    else:
        return render_template('index.html', tasks=list1)


@app.route('/delete/<int:id>')
def delete(id):
    list1.pop(id)
    return redirect('/')


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):

    if request.method == 'POST':
        list1[id]=[request.form['content'],datetime.utcnow()]
        return redirect('/')
    else:
        return render_template('update.html', task=list1[id], id=id)


if __name__ == "__main__":
    app.run(debug=True)