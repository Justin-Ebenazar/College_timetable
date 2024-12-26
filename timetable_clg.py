from flask import Flask, request, render_template, jsonify , redirect
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

staff_tt = {}
for i in ['tangam','anita','edwin','arul','bhuvana','moni','kavita','santi','akila','simi']:
    temp = []
    for j in range(6):
        temp.append([None for k in range(8)])
    staff_tt[i] = temp
class_dict = {}
class_tt = {}

def rnd_choose(sub_list):
    return random.choice(sub_list)

def tt_for_one(clas_tt,clas_name):
    for i in range(len(clas_tt)):
        for j in range(8):
            subject = rnd_choose(class_dict[clas_name])
            if staff_tt[subject[1]][i][j] != None:
                pass
            else:
                staff_tt[subject[1]][i][j] = subject[0]
                class_tt[clas_name][i][j] = subject[0]

@app.route('/submit', methods=['POST'])
def submit():
    global class_dict
    class_data = request.form['classData']
    class_dict = eval(class_data)

    # TO CREATE AN EMPTY TT FOR CLASS
    for i in class_dict:
        temp = []
        for j in range(6):
            temp.append([None for k in range(8)])
        class_tt[i] = temp
    
    for i in class_dict:
        tt_for_one(class_dict[i],i)

    for i in class_tt:
        for j in class_tt[i]:
            for k in range(8):
                print(j[k],end=" | ")
            print()
        print("\n")
    

    return render_template("timetable.html", classtt = class_tt)
if __name__ == '__main__':
    app.run(debug=True)
