import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QLineEdit, QTextEdit
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt
import time, json
class TimeManagementSystem():
    def __init__(self):
        self.tasks={}


class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.resize(1000,500)
        
        self.new_task_button=QPushButton("New task",self)
        self.new_task_button.move(850,200)
        self.new_task_button.setToolTip("Create your new task xd")
        self.new_task_button.clicked.connect(self.new_task)
        
        self.new_task_title_textbox=QLineEdit(self)
        self.new_task_title_textbox.hide()
        self.new_task_title_textbox.move(850,150)
        self.new_task_title_textbox.setFixedWidth(100)    
        
        self.new_task_description_textbox=QTextEdit(self)
        self.new_task_description_textbox.hide()
        self.new_task_description_textbox.move(850,180)
        self.new_task_description_textbox.setFixedHeight(100)
        self.new_task_description_textbox.setFixedWidth(100)
        
        self.new_task_time_textbox=QLineEdit(self)
        self.new_task_time_textbox.hide()
        self.new_task_time_textbox.move(850,290)
        self.new_task_time_textbox.setFixedWidth(100)    
        
        self.new_task_color_textbox=QLineEdit(self)
        self.new_task_color_textbox.hide()
        self.new_task_color_textbox.move(850,320)
        self.new_task_color_textbox.setFixedWidth(100)           
        
        self.create_new_task_button=QPushButton("Create",self)
        self.create_new_task_button.move(865,350)
        self.create_new_task_button.clicked.connect(task_creator)
        self.create_new_task_button.hide()
        
        self.show()  
        
    def new_task(self):
        self.new_task_button.hide()
        self.new_task_title_textbox.show()
        self.new_task_title_textbox.setText("Title")
        self.new_task_description_textbox.show()
        self.new_task_description_textbox.setText("Description")
        self.new_task_time_textbox.show()
        self.new_task_time_textbox.setText("Time")
        self.new_task_color_textbox.show()
        self.new_task_color_textbox.setText("Color")
        self.create_new_task_button.show()
        
              
    def paintEvent(self,event):
        q=QPainter()
        q.setPen(Qt.red)   
        q.begin(self)
        self.plot_drawing(q)
        self.task_drawing(q)
        q.end()
        self.update()
        
    def plot_drawing(self,q):
        q.drawLine(425,225,425,275)
        q.drawLine(50,250,800,250) 
        #timeshift=375+(-12*60+time.localtime()[3]*60+time.localtime()[4])*375/12/60
        #q.drawLine(50+timeshift,235,50+timeshift,265)
            
    
    def task_drawing(self,q):
        global TMS
        timeshift=time.localtime()[4]/60
        for i in TMS.tasks.items():
            lasttime=0
            for j in i[1]["Time"]["Time"]:
                if i[1]["Time"]["Repeats"]=="Inf":
                    repeat_count=9999
                else:
                    repeat_count=int(i[1]["Repeats"])
                dateshift=0
                for k in range(-1,min(repeat_count,2)):
                    date=time.mktime(time.strptime(i[1]["Time"]["Startdate"],"%d %m %Y"))+k*24*60*60
                    startbari=date+int(j.split('-')[0].split(':')[0])*60*60+int(j.split('-')[0].split(':')[1])*60+dateshift*24*3600
                    if startbari<lasttime:
                        dateshift+=1
                        startbari+=24*3600
                    lasttime=startbari
                    endbari=date+int(j.split('-')[1].split(':')[0])*60*60+int(j.split('-')[1].split(':')[1])*60+dateshift*24*3600
                    if endbari<lasttime:
                        dateshift+=1
                        endbari+=24*3600
                    lasttime=endbari    
                    x=425+(startbari-time.time())/60/60*750/24
                    width=(endbari-startbari)/60/60*750/24
                    if x+width>50 and x<800:
                        q.fillRect(x,240,width,20,self.color_determinant(i[1]["Color"]))
                
    def color_determinant(self,string):
        if string=="Red":
            return QColor(255,0,0)
        if string=="Green":
            return QColor(0,255,0)
        if string=="Blue":
            return QColor(0,0,255) 
        if string =="Pink":
            return QColor(255,84,167)
        
            
        
def task_creator():
    global TMS, window
    startdate=window.new_task_time_textbox.text().split(', ')[0]
    if int(startdate)>=time.localtime()[2]:
        startdate=startdate+time.strftime(" %m %Y",time.localtime())
    else:
        month=int(time.localtime()[1])+1
        if month>12:
            month=1
        startdate= startdate+' '+str(month)+time.strftime(" %Y",time.localtime())
    d={"Repeats":window.new_task_time_textbox.text().split(', ')[-1],
       "Startdate":startdate,
       "Time": window.new_task_time_textbox.text().split(', ')[1:-1]}
    TMS.tasks[window.new_task_title_textbox.text()]={"Description": window.new_task_description_textbox.toPlainText(),"Time": d,"Color":window.new_task_color_textbox.text()}
    window.new_task_title_textbox.hide()
    window.new_task_description_textbox.hide()
    window.new_task_time_textbox.hide()    
    window.create_new_task_button.hide()
    window.new_task_color_textbox.hide()
    window.new_task_button.show()

    with open("tasks.txt","w") as f:
        json.dump(TMS.tasks,f, indent=4)


if __name__=="__main__":
    TMS=TimeManagementSystem()
    try:
        with open("tasks.txt") as f:            
            TMS.tasks=json.load(f)
    except:
        pass
    app=QApplication(sys.argv)
    window=Window()
    sys.exit(app.exec_())