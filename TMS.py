import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QLineEdit, QTextEdit
from PyQt5.QtGui import QFont
class TimeManagementSystem():
    def __init__(self):
        self.tasks={}
        
class Task():
    def __init__(self,title,description,time):
        self.title=title
        self.description=description
        self.time=time

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
        
        self.create_new_task_button=QPushButton("Create",self)
        self.create_new_task_button.move(850,310)
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
        self.create_new_task_button.show()
        
              

def task_creator():
    global TMS, window
    TMS.tasks[window.new_task_title_textbox.text()]=Task(window.new_task_title_textbox.text(),window.new_task_description_textbox.toPlainText(),window.new_task_time_textbox.text())
    window.new_task_title_textbox.hide()
    window.new_task_description_textbox.hide()
    window.new_task_time_textbox.hide()    
    window.create_new_task_button.hide()
    window.new_task_button.show()


if __name__=="__main__":
    TMS=TimeManagementSystem()
    app=QApplication(sys.argv)
    window=Window()
    sys.exit(app.exec())