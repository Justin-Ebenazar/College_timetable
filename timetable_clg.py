from flask import Flask, request, render_template, jsonify , redirect
import random

staff_name = eval(open("data.txt","r").read())

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',sn = staff_name)

staff_tt = {}
class_dict = {}
class_tt = {}

for i in staff_name:
    temp = []
    for j in range(6):
        temp.append([None for k in range(8)])
    staff_tt[i] = temp

def rnd_choose(sub_list):
    return random.choice(sub_list)

def allot(staff,day,hrs,sub,clas):
    global class_dict,class_tt,staff_tt
    staff_tt[staff][day][hrs] = sub[0]
    class_tt[clas][day][hrs] = sub[0]
    try:
        class_dict[clas][class_dict[clas].index(sub)] = [sub[0],sub[1],str(int(sub[2])-1)]
    except:
        print(class_dict[clas])

def tt_for_one(clas_tt,clas_name):
    for day in range(6): # clas_tt [[os,anita,8],[fds,akila,8],...]
        hrs = 0 
        while hrs < 8:
            subject = rnd_choose(class_dict[clas_name]) #[os,anita,8]
            if (staff_tt[subject[1]][day][hrs] != None) or (int(subject[-1]) <= 0): #subject[1] = anita / [[None,...][None,...],...]
                hrs += 1
            else:
                if (subject[-1] != '3' and subject[-1] != '2'):
                    if(subject[-1] == '1'):
                        if(subject[0] == 'sprt'):
                            if (hrs == 7):
                                allot(subject[1],day,hrs,subject,clas_name)
                                hrs += 1
                            else:
                                hrs += 1
                        elif (subject[0] == 'lib'):
                            if (hrs != 0):
                                allot(subject[1],day,hrs,subject,clas_name)
                                hrs += 1
                            else:
                                hrs += 1
                        else:
                            allot(subject[1],day,hrs,subject,clas_name)
                            hrs+=1
                    else:
                        if (class_tt[clas_name][day].count(subject[0]) < 2):
                            allot(subject[1],day,hrs,subject,clas_name)
                            hrs += 1
                        else:
                            hrs += 1
                elif (subject[-1] == '3'):
                    try:
                        if(subject[0][-3:] == 'lab'):
                            if (hrs == 2 or hrs == 5):
                                for j in range(3):
                                    allot(subject[1],day,hrs,[subject[0],subject[1],str(int(subject[2])-j)],clas_name)
                                    hrs += 1
                    except:
                        allot(subject[1],day,hrs,subject,clas_name)
                        hrs += 1
                elif (subject[-1] == '2'):
                    try:
                        if(subject[0][-3:] == 'lab'):
                            if (hrs == 2 or hrs == 5 or hrs == 3 or hrs == 6):
                                for j in range(2):
                                    allot(subject[1],day,hrs,[subject[0],subject[1],str(int(subject[2])-j)],clas_name)
                                    hrs += 1
                    except:
                        allot(subject[1],day,hrs,subject,clas_name)
                        hrs += 1
                else:
                    hrs += 1
                            
                    
                        
                    
                
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
    loop = 1
    while loop<10000:
        cont = 0
        for i in class_dict:
            tt_for_one(class_dict[i],i)
            if sum(sublist.count(None) for sublist in class_tt[i]) == 0:
                cont += 1
        if cont < len(class_dict):
            loop += 1
        else:
            loop = 0
    print(loop)
        
                 
        


    return render_template("timetable.html", classtt = class_tt, stafftt = staff_tt)
if __name__ == '__main__':
    app.run(debug=True)
