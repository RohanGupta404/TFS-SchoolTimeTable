import mysql.connector
import socket
import random


def call_database(name_database):
    global mydb
    mydb = mysql.connector.connect(
        username="doadmin",
        password="aiyherpvx760tdng",
        host="db-mysql-blr1-16639-do-user-7263481-0.a.db.ondigitalocean.com",
        port="25060",
        database=name_database)
    global mycursor
    global cursor2
    global cursor3
    global cursor4
    mycursor = mydb.cursor()
    cursor2 = mydb.cursor()
    cursor3 = mydb.cursor()
    cursor4 = mydb.cursor()


def school_id_create1(school_id, school_pa, school_periods_day, school_lower_grade, school_upper_grade):
    call_database("anything")

    mycursor.execute("SELECT * FROM school_id_record")
    for i in mycursor:
        if school_id == i[0]:
            print("no")

    school_account = (school_id, school_pa)
    school_data = (school_id, school_periods_day, school_lower_grade, school_upper_grade)

    query = "INSERT INTO school_id_record VALUES(%s, %s)"
    mycursor.execute(query, school_account)

    query = "INSERT INTO school_general_record VALUES(%s, %s, %s, %s)"
    mycursor.execute(query, school_data)

    mycursor.execute("CREATE DATABASE " + school_id)
    call_database(school_id)

    mycursor.execute("CREATE TABLE teacher_id_record(teacher_id VARCHAR(256) PRIMARY KEY, teacher_pa VARCHAR(256))")
    mycursor.execute(
        "CREATE TABLE teacher_general_record(teacher_id VARCHAR(256) PRIMARY KEY, teacher_subject VARCHAR(256), teacher_type VARCHAR(256), class1 int, class2 int, sections_assigned int)")
    mycursor.execute(
        "CREATE TABLE sections_and_classes(the_grade int, section varchar(256), subject1 varchar(256), subject2 varchar(256), subject3 varchar(256), subject4 varchar(256), subject5 varchar(256), subject6 varchar(256), subject7 varchar(256), subject8 varchar(256), subject9 varchar(256), subject10 varchar(256), class_name VARCHAR(256) PRIMARY KEY)")
    mycursor.execute(
        "CREATE TABLE teachers_in_section(the_grade int, section varchar(256), subject1 varchar(256), subject2 varchar(256), subject3 varchar(256), subject4 varchar(256), subject5 varchar(256), subject6 varchar(256), subject7 varchar(256), subject8 varchar(256), subject9 varchar(256), subject10 varchar(256), class_name VARCHAR(256) PRIMARY KEY)")

    mydb.commit()


def school_id_create2(school_id, section_name, grade, subject1, subject2, subject3, subject4, subject5, subject6,
                      subject7, subject8, subject9, subject10):
    call_database(school_id)
    mycursor.execute(
        f"INSERT INTO teachers_in_section VALUES(%s, %s, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', %s)",
        (grade, section_name, str(grade)+section_name))
    values_for_table = (
    grade, section_name, subject1, subject2, subject3, subject4, subject5, subject6, subject7, subject8, subject9,
    subject10, str(grade)+section_name)
    mycursor.execute("INSERT INTO sections_and_classes VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                     values_for_table)

    mydb.commit()


def school_id_check(school_id, school_pa):
    call_database("anything")
    school_account = (school_id, school_pa)

    mycursor.execute("SELECT * FROM school_id_record")

    id_school_check = False
    for i in mycursor:
        if school_account == i:
            id_school_check = True
            break

    if id_school_check == True:
        # TODO redirect to the teacher's login tab
        return True
    else:
        # TODO give them 2 more tries, then ask them to fuck off
        return False


def teacher_id_check(school_id, teacher_id, teacher_pa):
    call_database(school_id)
    teacher_account = (teacher_id, teacher_pa)

    mycursor.execute("SELECT * FROM teacher_id_record")

    id_teacher_check = False
    for i in mycursor:
        if teacher_account == i:
            id_teacher_check = True
            break

    if id_teacher_check == True:
        # TODO redirect the user to there account(home page)
        return True
    else:
        # TODO just give 2 more trys then ask them to fuck off
        return False


def teacher_id_create(school_id, teacher_id, teacher_pa, teacher_subject, teacher_type, teacher_class1, teacher_class2):
    call_database(school_id)

    teacher_account = (teacher_id, teacher_pa)
    teacher_data = (teacher_id, teacher_subject, teacher_type, teacher_class1, teacher_class2, 0)

    query = "INSERT INTO teacher_id_record VALUES(%s, %s)"
    mycursor.execute(query, teacher_account)

    # TODO also insert the teacher ip address, initialy set it to null
    query = "INSERT INTO teacher_general_record VALUES(%s, %s, %s, %s, %s, %s)"
    mycursor.execute(query, teacher_data)

    mydb.commit()


def list_to_tuple(list):
    return tuple(list)


def teacher_assign(school_id):
    call_database(school_id)
    conn = mysql.connector.connect(
        username="doadmin",
        password="aiyherpvx760tdng",
        host="db-mysql-blr1-16639-do-user-7263481-0.a.db.ondigitalocean.com",
        port="25060",
        database=school_id)
    mycursor = conn.cursor(buffered=True, dictionary=True)
    cursor2 = conn.cursor(buffered=True, dictionary=True)
    mycursor.execute("TRUNCATE TABLE teachers_in_section")

    mycursor.execute("SELECT * FROM sections_and_classes")
    for i in mycursor:
        Class = i['the_grade']
        Section = i['section']
        teachers = [Class, Section]
        for k in range(1, 11):
            if i[f"subject{k}"] != "NULL" and i[f"subject{k}"] != "null":
                subject = i[f"subject{k}"]
                cursor2.execute(
                    "SELECT teacher_id, sections_assigned FROM teacher_general_record WHERE class1 = %s and teacher_subject = %s and sections_assigned < 8 or class2 = %s and teacher_subject = %s and sections_assigned < 8",
                    (Class, subject, Class, subject))
                for j in cursor2:
                    Teacher = j["teacher_id"]
                    cursor4.execute("SET SQL_SAFE_UPDATES = 0")
                    cursor4.execute(
                        "UPDATE teacher_general_record SET sections_assigned = sections_assigned + 1 WHERE teacher_id = %s",
                        (Teacher,))
                teachers.append(Teacher)
            else:
                teachers.append("NULL")
        teachers.append(str(Class)+Section)
        cursor3.execute("INSERT INTO teachers_in_section VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        list_to_tuple(teachers))
    mydb.commit()


def create_tables_for_classes(school_id):
    call_database("anything")
    cursor3.execute(f"SELECT school_periods_day FROM school_general_record WHERE school_id = '{school_id}'")
    for j in cursor3:
        school_periods_day = int(j[0])
    call_database(school_id)
    conn = mysql.connector.connect(
        username="doadmin",
        password="aiyherpvx760tdng",
        host="db-mysql-blr1-16639-do-user-7263481-0.a.db.ondigitalocean.com",
        port="25060",
        database=school_id)
    cursor2 = conn.cursor(buffered=True, dictionary=True)
    mycursor.execute("SELECT the_grade, section FROM sections_and_classes")
    for i in mycursor:
        Class = str(i[0])
        Section = i[1]
        class_name = Class + Section
        cursor2.execute(
            f"CREATE TABLE {class_name} (period int PRIMARY KEY, monday varchar(256), tuesday varchar(256), wednesday varchar(256), thursday varchar(256), friday varchar(256))")
    conn.commit()

    mycursor.execute("SELECT teacher_id FROM teacher_id_record")
    for i in mycursor:
        cursor2 = conn.cursor(buffered=True, dictionary=True)
        cursor2.execute(
            f"CREATE TABLE {i[0]}(period int PRIMARY KEY, monday varchar(256), tuesday varchar(256), wednesday varchar(256), thursday varchar(256), friday varchar(256))")
        conn.commit()
        cursor2 = conn.cursor(buffered=True, dictionary=True)
        for j in range(school_periods_day):
            period = j + 1
            cursor2.execute(f"INSERT INTO {i[0]} VALUES({period}, 'NULL', 'NULL', 'NULL', 'NULL', 'NULL')")
            conn.commit()
    conn.commit()
    mydb.commit()


def create_time_table(school_id):
    # check the number of periods in the day
    call_database("anything")
    mycursor.execute(f"SELECT school_periods_day FROM school_general_record WHERE school_id = '{school_id}'")
    for i in mycursor:
        school_periods_day = int(i[0])

    # All the database calling stuff
    call_database(school_id)
    mycursor.execute("SELECT teacher_id FROM teacher_id_record")

    conn = mysql.connector.connect(
        username="doadmin",
        password="aiyherpvx760tdng",
        host="db-mysql-blr1-16639-do-user-7263481-0.a.db.ondigitalocean.com",
        port="25060",
        database=school_id)
    cursor2 = conn.cursor(buffered=True, dictionary=True)
    cursor3 = conn.cursor(buffered=True)
    cursor4 = conn.cursor(buffered=True)
    cursor5 = conn.cursor(buffered=True)
    cursor6 = conn.cursor(buffered=True)
    cursor7 = conn.cursor(buffered=True)
    cursor8 = conn.cursor(buffered=True)
    cursor9 = conn.cursor(buffered=True)

    # generate a fresh table for the classes setting each to be null
    for i in mycursor:
        cursor2 = conn.cursor(buffered=True, dictionary=True)
        cursor2.execute(f"UPDATE {i[0]} SET monday = 'NULL'")
        cursor2.execute(f"UPDATE {i[0]} SET tuesday = 'NULL'")
        cursor2.execute(f"UPDATE {i[0]} SET wednesday = 'NULL'")
        cursor2.execute(f"UPDATE {i[0]} SET thursday = 'NULL'")
        cursor2.execute(f"UPDATE {i[0]} SET friday = 'NULL'")
        conn.commit()
    conn.commit()
    mydb.commit()

    # generates the time table
    mycursor.execute(f"SELECT * FROM teachers_in_section")
    for i in mycursor:
        # decide the class
        Class = str(i[0])
        Section = i[1]
        class_name = Class + Section
        cursor7.execute(f"DELETE FROM {class_name}")

        # check the teachers that teach the class
        teachers_teaching = [i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10]]
        for j in range(0, len(teachers_teaching)):
            if teachers_teaching[j] == "NULL":
                teachers_teaching = teachers_teaching[0:j]
                break

        # returns the day
        def val_day(k):
            if k == 0:
                return 'monday'
            elif k == 1:
                return 'tuesday'
            elif k == 2:
                return 'wednesday'
            elif k == 3:
                return 'thursday'
            elif k == 4:
                return 'friday'

        list_to_insert = []
        periods_in_week = school_periods_day * 5
        # loop runs 5 times for the 5 days of the week
        for k in range(5):
            a_list = []
            # see which teachers have the perticular period free
            for l in range(0, school_periods_day):
                teachers_ = []
                for teacher_id in range(0, len(teachers_teaching)):
                    day = val_day(k)
                    cursor6.execute(f"SELECT {day} FROM {teachers_teaching[teacher_id]} WHERE period = '{l + 1}'")
                    for z in cursor6:
                        teachers_.append(z)

                # chose a random teacher based on who has the free period
                while True:
                    value_adding = random.choice(teachers_teaching[0:len(teachers_teaching)])
                    while True:
                        value_adding = random.choice(teachers_teaching[0:len(teachers_teaching)])
                        ind = teachers_teaching.index(value_adding)
                        if teachers_[ind][0] != 'NULL':
                            value_adding = random.choice(teachers_teaching[0:len(teachers_teaching)])
                        else:
                            break
                    # checking how many periods does the selected teacher teaches the class for
                    cursor8.execute(f"SELECT monday, tuesday, wednesday, thursday, friday FROM {value_adding}")
                    periods_teaching = 0
                    for n in cursor8:
                        for n2 in n:
                            if n2 == class_name:
                                periods_teaching += 1

                    # Decide weather the teacher has sufficient periods in the class
                    if periods_teaching > (periods_in_week / len(teachers_teaching)):
                        value_adding = random.choice(teachers_teaching[0:len(teachers_teaching)])
                        while True:
                            value_adding = random.choice(teachers_teaching[0:len(teachers_teaching)])
                            ind = teachers_teaching.index(value_adding)
                            if teachers_[ind][0] != 'NULL':
                                value_adding = random.choice(teachers_teaching[0:len(teachers_teaching)])
                            else:
                                break
                        # checking how many periods does the selected teacher teaches the class for
                        cursor8.execute(f"SELECT monday, tuesday, wednesday, thursday, friday FROM {value_adding}")
                        periods_teaching = 0
                        for n in cursor8:
                            for n2 in n:
                                if n2 == class_name:
                                    periods_teaching += 1
                    else:
                        break

                # update the teachers table based on the teacher selected
                cursor4.execute("SET SQL_SAFE_UPDATES = 0")
                cursor4.execute(f"UPDATE {value_adding} SET {day} = '{class_name}' WHERE period = '{l + 1}'")
                conn.commit()

                a_list.append(value_adding)
            list_to_insert.append(a_list)
        # update the class time table based on collected data
        period_count = 1
        for z in range(len(list_to_insert[0])):
            actual_list = []
            for y in list_to_insert:
                for x in range(z, z + 1):
                    actual_list.append(y[x])

            query = f"INSERT INTO {class_name} VALUES ({period_count}, '{actual_list[0]}', '{actual_list[1]}', '{actual_list[2]}', '{actual_list[3]}', '{actual_list[4]}')"
            cursor7.execute(query)
            period_count += 1
    mydb.commit()
    conn.commit()

    mydb.commit()


def table_droper(school_id):
    call_database(school_id)
    mycursor.execute("SHOW TABLES")

    conn = mysql.connector.connect(
        username="doadmin",
        password="aiyherpvx760tdng",
        host="db-mysql-blr1-16639-do-user-7263481-0.a.db.ondigitalocean.com",
        port="25060",
        database=school_id)
    cursor2 = conn.cursor(buffered=True, dictionary=True)
    cursor3 = conn.cursor(buffered=True, dictionary=True)
    cursor4 = conn.cursor(buffered=True, dictionary=True)

    for i in mycursor:
        table_name = i[0]
        if table_name != "sections_and_classes" and table_name != "teacher_general_record" and table_name != "teacher_id_record" and table_name != "teachers_in_section":
            cursor2.execute(f"DROP TABLE {table_name}")
    cursor3.execute("UPDATE teacher_general_record SET sections_assigned = 0 WHERE sections_assigned > 0")
    cursor4.execute("TRUNCATE TABLE teachers_in_section")


def chatSend(send_message, school_id, teacher_id):
    call_database(school_id)
    mycursor.execute("TRUNCATE TABLE chat")
    mycursor.execute(f"INSERT INTO chat VALUES('{teacher_id}', '{send_message}')")
    mydb.commit()
