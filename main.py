import backFunc
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
import subprocess
import mysql.connector
from threading import Thread
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout


class HomeScreen(Screen):
    pass


class SchoolIdCreate(Screen):
    pass


class SchoolIdCreate2(Screen):
    pass


class SchoolIdCreate3(Screen):
    pass


class TeacherIdCheck(Screen):
    pass


class TeacherIdCreate(Screen):
    pass


class IndexScreen(Screen):
    pass


class DisplayTimeTable(Screen):
    pass


# class for functions
class ImageButton(ButtonBehavior, Image):
    pass


GUI = Builder.load_file('main.kv')


class MainApp(App):
    def build(self):
        return GUI

    def change_screen(self, screen_name):
        global screen_manager
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name

    def check_school_id(self):
        MainApp.change_screen(self, 'HomeScreen')
        school_id = self.root.ids['HomeScreen'].ids["school_id"].text
        school_pa = self.root.ids['HomeScreen'].ids["school_pa"].text
        school_check = backFunc.school_id_check(school_id, school_pa)
        if school_check == True:
            MainApp.change_screen(self, "TeacherIdCheck")
        else:
            self.root.ids['HomeScreen'].ids["school_id"].text = ""
            self.root.ids['HomeScreen'].ids["school_pa"].text = ""

    def lower_grade(self, grade_recived_lower):
        global school_lower_grade
        school_lower_grade = grade_recived_lower
        print(school_lower_grade)

    def upper_grade(self, grade_recived_upper):
        global school_upper_grade
        school_upper_grade = grade_recived_upper
        print(school_upper_grade)

    def School_id_create(self):
        school_id = self.root.ids['SchoolIdCreate'].ids["school_id"].text
        school_pa = self.root.ids['SchoolIdCreate'].ids["school_pa"].text
        if self.root.ids['SchoolIdCreate'].ids["school_periods_day"].text in "1234567890":
            school_periods_day = self.root.ids['SchoolIdCreate'].ids["school_periods_day"].text
            try:
                backFunc.school_id_create1(school_id, school_pa, school_periods_day, school_lower_grade, school_upper_grade)
                MainApp.School_id_create2(self)
            except NameError:
                self.root.ids['SchoolIdCreate'].ids["submit"].text = "Form Incomplete"
            except:
                self.root.ids['SchoolIdCreate'].ids["school_id"].text = ""
                self.root.ids['SchoolIdCreate'].ids["school_id"].hint_text = "This id is taken, please try another one"
        else:
            self.root.ids['SchoolIdCreate'].ids["school_periods_day"].text = ""
            self.root.ids['SchoolIdCreate'].ids["school_periods_day"].hint_text = "Enter a Numeric Value"

    def School_id_create2(self):
        MainApp.change_screen(self, "SchoolIdCreate2")
        global grades_school
        grades_school = []
        for i in range(int(school_lower_grade), int(school_upper_grade) + 1):
            grades_school.append(i)
        MainApp.count = 0
        MainApp.School_id_create3(self)

    count = 0

    # rotate through each grade in the school asking for the number of sections
    def School_id_create3(self):
        if MainApp.count < len(grades_school):
            grade = grades_school[MainApp.count]
            print(grade)
            self.root.ids['SchoolIdCreate2'].ids["label_message"].text = f"How many sections does grade {grade} has"
            MainApp.change_screen(self, "SchoolIdCreate2")
            global sections_in_class
            sections_in_class = self.root.ids['SchoolIdCreate2'].ids["number_sections"].text
            MainApp.count += 1
            MainApp.count2 = 0
        else:
            if sections_in_class in "1234567890":
                MainApp.check_school_id(self)
            else:
                self.root.ids['SchoolIdCreate2'].ids["number_sections"].text = ""
                self.root.ids['SchoolIdCreate2'].ids["number_sections"].hint_text = "Enter a Numeric Value"

    count2 = 0

    def sub1(self, subject):
        global subject1
        subject1 = subject

    def sub2(self, subject):
        global subject2
        subject2 = subject

    def sub3(self, subject):
        global subject3
        subject3 = subject

    def sub4(self, subject):
        global subject4
        subject4 = subject

    def sub5(self, subject):
        global subject5
        subject5 = subject

    def sub6(self, subject):
        global subject6
        subject6 = subject

    def sub7(self, subject):
        global subject7
        subject7 = subject

    def sub8(self, subject):
        global subject8
        subject8 = subject

    def sub9(self, subject):
        global subject9
        subject9 = subject

    def sub10(self, subject):
        global subject10
        subject10 = subject

    def School_id_create4(self):
        if self.root.ids['SchoolIdCreate2'].ids["number_sections"].text in "1234567890":
            if MainApp.count2 < int(self.root.ids['SchoolIdCreate2'].ids["number_sections"].text):
                self.root.ids['SchoolIdCreate3'].ids["grade_name"].text = str(
                    MainApp.count + school_lower_grade - 1) + chr(
                    MainApp.count2 + 65)
                MainApp.change_screen(self, "SchoolIdCreate3")
            else:
                MainApp.School_id_create3(self)
        else:
            self.root.ids['SchoolIdCreate2'].ids["number_sections"].text = ""
            self.root.ids['SchoolIdCreate2'].ids["number_sections"].hint_text = "Enter a Numeric Value"

    def subject_assigning(self):
        school_id = self.root.ids['SchoolIdCreate'].ids["school_id"].text
        try:
            subject_list = (subject1, subject2, subject3, subject4, subject5, subject6, subject7, subject8, subject9, subject10)
            backFunc.school_id_create2(school_id, chr(MainApp.count2 + 65), str(MainApp.count + school_lower_grade - 1), subject1, subject2, subject3, subject4, subject5, subject6, subject7, subject8, subject9, subject10)
            MainApp.count2 += 1
            MainApp.School_id_create4(self)
        except NameError:
            self.root.ids['SchoolIdCreate3'].ids["submit"].text = "Form Incomplete"

    def check_teacher_id(self):
        school_id = self.root.ids['HomeScreen'].ids["school_id"].text
        teacher_id = self.root.ids['TeacherIdCheck'].ids['teacher_id'].text
        teacher_pa = self.root.ids['TeacherIdCheck'].ids['teacher_pa'].text
        teacher_check = backFunc.teacher_id_check(school_id, teacher_id, teacher_pa)
        if teacher_check == True:
            self.root.ids['IndexScreen'].ids['username'].text = self.root.ids['TeacherIdCheck'].ids['teacher_id'].text
            MainApp.change_screen(self, "IndexScreen")
        else:
            self.root.ids['TeacherIdCheck'].ids["teacher_id"].text = ""
            self.root.ids['TeacherIdCheck'].ids["teacher_pa"].text = ""

    def subject_of_teacher(self, subject_recived):
        global subject_teacher
        subject_teacher = subject_recived
        print(subject_teacher)

    def type_of_teacher(self, type_recived):
        global type_teacher
        type_teacher = type_recived
        print(type_teacher)

    def grade_of_teacher(self, grade_recived):
        global grade_teacher
        grade_teacher = grade_recived
        print(grade_teacher)

    def grade_of_teacher2(self, grade_recived2):
        global grade_teacher2
        grade_teacher2 = grade_recived2
        print(grade_teacher2)

    def teacher_id_create(self):
        school_id = self.root.ids['HomeScreen'].ids["school_id"].text
        teacher_id = self.root.ids['TeacherIdCreate'].ids["teacher_id"].text
        teacher_pa = self.root.ids['TeacherIdCreate'].ids["teacher_pa"].text
        try:
            backFunc.teacher_id_create(school_id, teacher_id, teacher_pa, subject_teacher, type_teacher, grade_teacher,
                                       grade_teacher2)
            self.root.ids['TeacherIdCreate'].ids["teacher_id"].text = ""
            self.root.ids['TeacherIdCreate'].ids["teacher_pa"].text = ""
            MainApp.check_teacher_id(self)
            MainApp.change_screen(self, "TeacherIdCheck")
        except NameError:
            self.root.ids['TeacherIdCreate'].ids["submit"].text = "Form Incomplete"
        except:
            teacher_id = self.root.ids['TeacherIdCreate'].ids["teacher_id"].text = ""
            teacher_id = self.root.ids['TeacherIdCreate'].ids[
                "teacher_id"].hint_text = "This id is taken, please try another one"

    def index_create_time_table(self):
        school_id = self.root.ids['HomeScreen'].ids["school_id"].text
        teacher_id = self.root.ids['TeacherIdCheck'].ids['teacher_id'].text
        mydb = mysql.connector.connect(username="doadmin",password="aiyherpvx760tdng",host="db-mysql-blr1-16639-do-user-7263481-0.a.db.ondigitalocean.com",port="25060",database=school_id)
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT teacher_type FROM teacher_general_record WHERE teacher_id = '{teacher_id}'")
        for i in mycursor:
            teacher_type = i[0]
        if teacher_type == "teacher":
            self.root.ids["IndexScreen"].ids["create_button"].text = "You don\'t have the write to create a time table"
        else:
            try:
                backFunc.table_droper(school_id)
                backFunc.teacher_assign(school_id)
                backFunc.create_tables_for_classes(school_id)
                backFunc.create_time_table(school_id)
            except:
                self.root.ids["IndexScreen"].ids["create_button"].text = "insufficient teachers"

    def index_update_time_table(self):
        school_id = self.root.ids['HomeScreen'].ids["school_id"].text
        teacher_id = self.root.ids['TeacherIdCheck'].ids['teacher_id'].text
        mydb = mysql.connector.connect(username="doadmin",password="aiyherpvx760tdng",host="db-mysql-blr1-16639-do-user-7263481-0.a.db.ondigitalocean.com",port="25060",database=school_id)
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT teacher_type FROM teacher_general_record WHERE teacher_id = '{teacher_id}'")
        for i in mycursor:
            teacher_type = i[0]
        if teacher_type == "teacher":
            self.root.ids["IndexScreen"].ids[
                "update_button"].text = "You don\'t have the write to update the time table"
        else:
            try:
                backFunc.create_time_table(school_id)
            except:
                self.root.ids["IndexScreen"].ids["update_button"].text = "First click the create time table button"

    def display_time_table(self):
        school_id = self.root.ids['HomeScreen'].ids["school_id"].text
        teacher_id = self.root.ids['TeacherIdCheck'].ids["teacher_id"].text

        mydb = mysql.connector.connect(
            username="doadmin",
            password="aiyherpvx760tdng",
            host="db-mysql-blr1-16639-do-user-7263481-0.a.db.ondigitalocean.com",
            port="25060",
            database=school_id)
        mycursor = mydb.cursor()

        mycursor.execute(f"SELECT * FROM {teacher_id}")
        for i in mycursor:
            day = str(i[0])
            self.root.ids['DisplayTimeTable'].ids[f"p{day}"].text = f"Period {str(i[0])}"
            self.root.ids['DisplayTimeTable'].ids[f"p{day}"].color = 0, 0, 0, 1
            self.root.ids['DisplayTimeTable'].ids[f"mon{day}"].text = i[1]
            self.root.ids['DisplayTimeTable'].ids[f"mon{day}"].color = 0, 0, 0, 1
            self.root.ids['DisplayTimeTable'].ids[f"tue{day}"].text = i[2]
            self.root.ids['DisplayTimeTable'].ids[f"tue{day}"].color = 0, 0, 0, 1
            self.root.ids['DisplayTimeTable'].ids[f"wen{day}"].text = i[3]
            self.root.ids['DisplayTimeTable'].ids[f"wen{day}"].color = 0, 0, 0, 1
            self.root.ids['DisplayTimeTable'].ids[f"thr{day}"].text = i[4]
            self.root.ids['DisplayTimeTable'].ids[f"thr{day}"].color = 0, 0, 0, 1
            self.root.ids['DisplayTimeTable'].ids[f"fri{day}"].text = i[5]
            self.root.ids['DisplayTimeTable'].ids[f"fri{day}"].color = 0, 0, 0, 1

        MainApp.change_screen(self, "DisplayTimeTable")


MainApp().run()

# find a place for this thing
# while True:
#   Thread(target = MainApp().chatRecive("Left")).start()
