#import python, tkinter, mysql library
import sys
import tkinter as tk
from tkinter import *
import mysql.connector
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import shutil
import datetime
import time
import re
import webbrowser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import sv_ttk as st
from tkcalendar import DateEntry




#connect to database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
 database="auto360",
)

#create table users query
users_table = '''
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  driving_license VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL  DEFAULT 'user',
    staff_available VARCHAR(255) NOT NULL  DEFAULT 'Not Available'
)
'''

#create table vehicles query
vehicles_table = '''
CREATE TABLE IF NOT EXISTS vehicles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  vehicle_name VARCHAR(255) NOT NULL,
  vehicle_model VARCHAR(255) NOT NULL,
  vehicle_number VARCHAR(255) NOT NULL,
  vehicle_type VARCHAR(255) NOT NULL,
  vehicle_image LONGBLOB,
  FOREIGN KEY (user_id) REFERENCES users(id)
)
'''

#create table vehicle_maintenance appoinment query
vehicle_maintenance_appoinment_table = '''
CREATE TABLE IF NOT EXISTS appoinment (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  vehicle_id INT NOT NULL,
  appoinment_date DATE NOT NULL,
  appoinment_time TIME NOT NULL,
  appoinment_type VARCHAR(255) NOT NULL,
  appoinment_description TEXT NOT NULL,
  appoinment_status VARCHAR(255) DEFAULT 'Created',
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
)
'''

#create table appoinment_results query
appoinment_results_table = '''
CREATE TABLE IF NOT EXISTS appoinment_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appoinment_id INT NOT NULL,
    staff_id INT NOT NULL,
    appoinment_result TEXT NOT NULL,
    appoinment_status VARCHAR(255) DEFAULT 'Pending',
    FOREIGN KEY (appoinment_id) REFERENCES appoinment(id),
    FOREIGN KEY (staff_id) REFERENCES users(id)
)
'''


#execute all queries
mycursor = mydb.cursor()
mycursor.execute(users_table)
mycursor.execute(vehicles_table)
mycursor.execute(vehicle_maintenance_appoinment_table)
mycursor.execute(appoinment_results_table)



#class auto360 
class auto360:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto360")
        self.root.geometry("950x700")
        self.style = ttk.Style(self.root)
        self.style.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        self.style.configure('TNotebook', tabposition='n',)


        self.login_screen()

    #login_screen
    def login_screen(self):

        for i in self.root.winfo_children():
            i.destroy()



        #welcome to auto360 label
        self.welcome_label = Label(self.root, text="Welcome to Auto360", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.welcome_label.place(x=0, y=0, relwidth=1)

        #login frame
        self.login_frame = Frame(self.root, bg="white")
        self.login_frame.place(x=250, y=100, width=500, height=500)

        #login title
        self.login_title = Label(self.login_frame, text="Login", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.login_title.place(x=0, y=50, relwidth=1)

        #username label
        self.username_label = Label(self.login_frame, text="Username", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.username_label.place(x=100, y=100)

        #username entry
        self.username_entry = Entry(self.login_frame, font=("times new roman", 15), bg="lightgray")
        self.username_entry.place(x=100, y=130)

        #password label
        self.password_label = Label(self.login_frame, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.password_label.place(x=100, y=180)

        #password entry
        self.password_entry = Entry(self.login_frame, font=("times new roman", 15), bg="lightgray", show="*")
        self.password_entry.place(x=100, y=210)

        #login button
        self.login_button = Button(self.login_frame, text="Login", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.login)
        self.login_button.place(x=100, y=260)

        #register button
        self.register_button = Button(self.login_frame, text="Register", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.register_screen)
        self.register_button.place(x=250, y=260)


    #register screen by clearing all the children first
    def register_screen(self):
        for i in self.root.winfo_children():
            i.destroy()

        #welcome to auto360 label
        self.welcome_label = Label(self.root, text="Welcome to Auto360", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.welcome_label.place(x=0, y=0, relwidth=1)

        #register frame
        self.register_frame = Frame(self.root, bg="white")
        self.register_frame.place(x=250, y=50, width=500, height=600)

        #register title
        self.register_title = Label(self.register_frame, text="Register", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.register_title.place(x=0, y=50, relwidth=1)

        #username label
        self.username_label = Label(self.register_frame, text="Username", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.username_label.place(x=100, y=100)

        #username entry
        self.username_entry = Entry(self.register_frame, font=("times new roman", 15), bg="lightgray")
        self.username_entry.place(x=100, y=130)

        #email label
        self.email_label = Label(self.register_frame, text="Email", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.email_label.place(x=100, y=180)

        #email entry
        self.email_entry = Entry(self.register_frame, font=("times new roman", 15), bg="lightgray")
        self.email_entry.place(x=100, y=210)

        #password label
        self.password_label = Label(self.register_frame, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.password_label.place(x=100, y=260)

        #password entry
        self.password_entry = Entry(self.register_frame, font=("times new roman", 15), bg="lightgray", show="*")
        self.password_entry.place(x=100, y=290)

        #driving license label
        self.driving_license_label = Label(self.register_frame, text="Driving License", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.driving_license_label.place(x=100, y=340)

        #driving license entry
        self.driving_license_entry = Entry(self.register_frame, font=("times new roman", 15), bg="lightgray")
        self.driving_license_entry.place(x=100, y=370)

        #phone number label
        self.phone_number_label = Label(self.register_frame, text="Phone Number", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.phone_number_label.place(x=100, y=420)

        #phone number entry
        self.phone_number_entry = Entry(self.register_frame, font=("times new roman", 15), bg="lightgray")
        self.phone_number_entry.place(x=100, y=450)

        #register button
        self.register_button = Button(self.register_frame, text="Register", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.register)
        self.register_button.place(x=100, y=500)

        #back to login screen
        self.login_button = Button(self.register_frame, text="Login", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.login_screen)
        self.login_button.place(x=250, y=500)




    #dashboard screen with notebook(Auto360,My Appointment, Book Apponitment, My Vehicles, My profile)
    def dashboard_screen(self):
        for i in self.root.winfo_children():
            i.destroy()

        #welcome to auto360 label
        self.welcome_label = Label(self.root, text="Welcome to Auto360", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.welcome_label.place(x=0, y=0, relwidth=1)

        #dashboard frame
        self.dashboard_frame = Frame(self.root, bg="white")
        self.dashboard_frame.place(x=0, y=50, relwidth=1, height=600)

        #notebook
        self.notebook = ttk.Notebook(self.dashboard_frame)
        self.notebook.place(x=0, y=0, relwidth=1, relheight=1)

        #Auto360 tab
        self.auto360_tab = Frame(self.notebook, bg="white")
        self.notebook.add(self.auto360_tab, text="Auto360")

        #My Appointment tab
        self.my_appointment_tab = Frame(self.notebook, bg="white")
        self.notebook.add(self.my_appointment_tab, text="My Appointments")

        #Book Apponitment tab
        self.book_appointment_tab = Frame(self.notebook, bg="white")
        self.notebook.add(self.book_appointment_tab, text="Book Apponitment")

        #My Vehicles tab
        self.my_vehicles_tab = Frame(self.notebook, bg="white")
        self.notebook.add(self.my_vehicles_tab, text="My Vehicles")

        #My Profile tab
        self.my_profile_tab = Frame(self.notebook, bg="white")
        self.notebook.add(self.my_profile_tab, text="My Profile")

        #frame inside book appointment tab
        self.book_appointment_frame = Frame(self.book_appointment_tab, bg="white")
        self.book_appointment_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        #book appointment heading "Book an Appointment for Vehicle Inspection"
        self.book_appointment_heading = Label(self.book_appointment_frame, text="Book an Appointment for Vehicle Inspection", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.book_appointment_heading.place(x=5, y=5, relwidth=1)

        #vehicle name label
        self.vehicle_name_label = Label(self.book_appointment_frame, text="Vehicle Name", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_name_label.place(x=100, y=50)

        #vehicle details combobox
        self.vehicle_name_combobox = ttk.Combobox(self.book_appointment_frame, font=("times new roman", 15), state="readonly")
        self.vehicle_name_combobox.place(x=100, y=80,width=200)

        #get all user vehicle names
        mycursor.execute("SELECT * FROM vehicles WHERE user_id=%s", (self.user_id,))
        vehicles = mycursor.fetchall()
        vehicle_names = []

        for vehicle in vehicles:
            vehicle_names.append(vehicle[2])
        self.vehicle_name_combobox['values'] = vehicle_names

        #vehicle model label
        self.vehicle_model_label = Label(self.book_appointment_frame, text="Vehicle Model", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_model_label.place(x=100, y=130)

        #vehicle model entry
        self.vehicle_model_entry = Entry(self.book_appointment_frame, font=("times new roman", 15), bg="lightgray")
        self.vehicle_model_entry.place(x=100, y=160,width=200)

        #vehicle number label
        self.vehicle_number_label = Label(self.book_appointment_frame, text="Vehicle Number", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_number_label.place(x=100, y=210)

        #vehicle number entry
        self.vehicle_number_entry = Entry(self.book_appointment_frame, font=("times new roman", 15), bg="lightgray")
        self.vehicle_number_entry.place(x=100, y=240,width=200)



        #inspection type label
        self.inspection_type_label = Label(self.book_appointment_frame, text="Inspection Type", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.inspection_type_label.place(x=100, y=290)

        #inspection type combobox
        self.inspection_type_combobox = ttk.Combobox(self.book_appointment_frame, font=("times new roman", 15), state="readonly")
        self.inspection_type_combobox['values'] = ("General Inspection", "Oil Change", "Brake Inspection", "Tire Rotation", "Battery Check", "Air Filter Replacement", "Coolant Flush", "Transmission Flush", "Engine Tune-up", "Wheel Alignment", "Exhaust System Inspection", "Fuel Filter Replacement", "Timing Belt Replacement", "Spark Plug Replacement", "Suspension Inspection", "Steering Inspection", "Air Conditioning Inspection", "Electrical System Inspection", "Exhaust System Inspection", "Fuel System Inspection", "Transmission Inspection", "Engine Inspection", "Cooling System Inspection", "Brake System Inspection", "Steering System Inspection", "Suspension System Inspection", "Drivetrain Inspection", "Emission System Inspection", "Safety Inspection", "Pre-purchase Inspection", "Other")
        self.inspection_type_combobox.place(x=100, y=320,width=200)

        #inspection description label
        self.inspection_description_label = Label(self.book_appointment_frame, text="Inspection Description", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.inspection_description_label.place(x=400, y=50)

        #inspection description entry
        self.inspection_description_entry = Text(self.book_appointment_frame, font=("times new roman", 15), bg="lightgray", height=5)
        self.inspection_description_entry.place(x=400, y=80, relwidth=0.5)

        #appoinment date label
        self.appoinment_date_label = Label(self.book_appointment_frame, text="Appoinment Date", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.appoinment_date_label.place(x=100, y=370)

        #appoinment date entry
        self.appoinment_date_entry = DateEntry(self.book_appointment_frame, font=("times new roman", 15), bg="lightgray")
        self.appoinment_date_entry.place(x=100, y=400,width=200)

        #appoinment time label
        self.appoinment_time_label = Label(self.book_appointment_frame, text="Appoinment Time", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.appoinment_time_label.place(x=100, y=450)

        #appoinment time comboxbox ( availability of time)
        self.appoinment_time_combobox = ttk.Combobox(self.book_appointment_frame, font=("times new roman", 15), state="readonly")
        self.appoinment_time_combobox['values'] = ("9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM")
        self.appoinment_time_combobox.place(x=100, y=480,width=200)

        #book appointment button
        self.book_appointment_button = Button(self.book_appointment_frame, text="Book Appointment", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.book_appointment)
        self.book_appointment_button.place(x=400, y=210)


        #frame inside vehicle tab for title and button
        self.vehicle_frame = Frame(self.my_vehicles_tab, bg="white")
        self.vehicle_frame.place(x=0, y=0, relwidth=1, relheight=1)

        #my vehicles heading "My Vehicles"
        self.my_vehicles_heading = Label(self.vehicle_frame, text="My Vehicles", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.my_vehicles_heading.place(x=5, y=5, relwidth=1)

        #add vehicle details fill event
        self.vehicle_name_combobox.bind("<<ComboboxSelected>>", self.vehicle_model_number)


        #frame inside my appointment tab for treeview
        self.my_vehicles_frame = Frame(self.my_vehicles_tab, bg="white")
        self.my_vehicles_frame.place(x=100, y=50,width=800, height=400)



        #treeview of vehicles
        self.my_appointment_tree = ttk.Treeview(self.my_vehicles_frame, columns=("Vehicle id","Vehicle Name", "Vehicle Model", "Vehicle Number"))
        self.my_appointment_tree.heading("Vehicle id", text="Vehicle id")
        self.my_appointment_tree.heading("Vehicle Name", text="Vehicle Name")
        self.my_appointment_tree.heading("Vehicle Model", text="Vehicle Model")
        self.my_appointment_tree.heading("Vehicle Number", text="Vehicle Number")

        self.my_appointment_tree['show'] = 'headings'

        self.my_appointment_tree.column("Vehicle id", width=100)
        self.my_appointment_tree.column("Vehicle Name", width=100)
        self.my_appointment_tree.column("Vehicle Model", width=100)
        self.my_appointment_tree.column("Vehicle Number", width=100)
        
        self.my_appointment_tree.pack(fill=BOTH, expand=1)


        #fill the treeview
        mycursor.execute("SELECT * FROM vehicles WHERE user_id=%s", (self.user_id,))
        vehicles = mycursor.fetchall()
        for vehicle in vehicles:
            vehicle_id = vehicle[0]
            vehicle_name = vehicle[2]
            vehicle_model = vehicle[3]
            vehicle_number = vehicle[4]

            self.my_appointment_tree.insert("", "end", values=(vehicle_id, vehicle_name, vehicle_model, vehicle_number))

        #configure the treeview column
        self.my_appointment_tree.column("#1", anchor="center")
        self.my_appointment_tree.column("#2", anchor="center")
        self.my_appointment_tree.column("#3", anchor="center")
        self.my_appointment_tree.column("#4", anchor="center")

    #add vehicle button
        self.add_vehicle_button = Button(self.vehicle_frame, text="Add Vehicle", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.add_vehicle)
        self.add_vehicle_button.place(x=100, y=500)

        #update vehicle button
        self.update_vehicle_button = Button(self.vehicle_frame, text="Update Vehicle", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.update_vehicle)
        self.update_vehicle_button.place(x=250, y=500)

        #delete vehicle button
        self.delete_vehicle_button = Button(self.vehicle_frame, text="Delete Vehicle", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.delete_vehicle)
        self.delete_vehicle_button.place(x=450, y=500)


        #my appointments tab title frame
        self.my_appointment_title_frame = Frame(self.my_appointment_tab, bg="white")
        self.my_appointment_title_frame.place(x=0, y=0, relwidth=1, height=50)

        #my appointments heading "My Appointments"
        self.my_appointment_heading = Label(self.my_appointment_title_frame, text="My Appointments", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.my_appointment_heading.place(x=5, y=5, relwidth=1)

        #frame inside my appointment tab for treeview
        self.my_appointment_frame = Frame(self.my_appointment_tab, bg="white")
        self.my_appointment_frame.place(x=100, y=50,width=800, height=400)

        #treeview of appointments
        self.my_appointment_tree = ttk.Treeview(self.my_appointment_frame, columns=("Appoinment id","Vehicle Name", "Appoinment Date", "Appoinment Time", "Appoinment Type", "Appoinment Status"))
        self.my_appointment_tree.heading("Appoinment id", text="Appoinment id")

        self.my_appointment_tree.heading("Vehicle Name", text="Vehicle Name")
        self.my_appointment_tree.heading("Appoinment Date", text="Appoinment Date")
        self.my_appointment_tree.heading("Appoinment Time", text="Appoinment Time")
        self.my_appointment_tree.heading("Appoinment Type", text="Appoinment Type")
        self.my_appointment_tree.heading("Appoinment Status", text="Appoinment Status")

        self.my_appointment_tree['show'] = 'headings'

        self.my_appointment_tree.column("Appoinment id", width=100)
        self.my_appointment_tree.column("Vehicle Name", width=100)
        self.my_appointment_tree.column("Appoinment Date", width=100)
        self.my_appointment_tree.column("Appoinment Time", width=100)
        self.my_appointment_tree.column("Appoinment Type", width=100)
        self.my_appointment_tree.column("Appoinment Status", width=100)
        
        self.my_appointment_tree.pack(fill=BOTH, expand=1)
        
        #fill the treeview
        mycursor.execute("SELECT * FROM appoinment WHERE user_id=%s", (self.user_id,))
        appoinments = mycursor.fetchall()
        for appoinment in appoinments:
            appoinment_id = appoinment[0]
            vehicle_id = appoinment[2]
            appoinment_date = appoinment[3]
            appoinment_time = appoinment[4]
            appoinment_type = appoinment[5]
            appoinment_status = appoinment[7]

            mycursor.execute("SELECT * FROM vehicles WHERE id=%s", (vehicle_id,))
            vehicle = mycursor.fetchone()
            vehicle_name = vehicle[2]

            self.my_appointment_tree.insert("", "end", values=(appoinment_id, vehicle_name, appoinment_date, appoinment_time, appoinment_type, appoinment_status))

        #configure the treeview column
        self.my_appointment_tree.column("#1", anchor="center")
        self.my_appointment_tree.column("#2", anchor="center")
        self.my_appointment_tree.column("#3", anchor="center")
        self.my_appointment_tree.column("#4", anchor="center")
        self.my_appointment_tree.column("#5", anchor="center")
        self.my_appointment_tree.column("#6", anchor="center")

        #create appoinment
        self.create_appointment_button = Button(self.my_appointment_tab, text="Create Appointment", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.book_appointment_page)
        self.create_appointment_button.place(x=100, y=500)

        #update appoinment
        self.update_appointment_button = Button(self.my_appointment_tab, text="Update Appointment", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.update_appointment)
        self.update_appointment_button.place(x=300, y=500)

        #delete appoinment
        self.delete_appointment_button = Button(self.my_appointment_tab, text="Delete Appointment", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.delete_appointment)
        self.delete_appointment_button.place(x=500, y=500)


        #My Profile tab title frame
        self.my_profile_title_frame = Frame(self.my_profile_tab, bg="white")
        self.my_profile_title_frame.place(x=0, y=0, relwidth=1, height=50)

        #my profile heading "My Profile"
        self.my_profile_heading = Label(self.my_profile_title_frame, text="My Profile", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.my_profile_heading.place(x=5, y=5, relwidth=1)

        #frame inside my profile tab for user details
        self.my_profile_frame = Frame(self.my_profile_tab, bg="white")
        self.my_profile_frame.place(x=100, y=50,width=800, height=400)

        #username label
        self.username_label = Label(self.my_profile_frame, text="Username", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.username_label.place(x=100, y=50)

        #username entry side by side
        self.username_entry = Entry(self.my_profile_frame, font=("times new roman", 15), bg="lightgray")
        self.username_entry.place(x=300, y=50)

        #fill in the username entry
        self.username_entry.insert(0, self.username)

        #email label
        self.email_label = Label(self.my_profile_frame, text="Email", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.email_label.place(x=100, y=100)

        #email entry side by side
        self.email_entry = Entry(self.my_profile_frame, font=("times new roman", 15), bg="lightgray")
        self.email_entry.place(x=300, y=100)

        #fill in the email entry
        self.email_entry.insert(0, self.email)

        #driving license label
        self.driving_license_label = Label(self.my_profile_frame, text="Driving License", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.driving_license_label.place(x=100, y=150)

        #driving license entry side by side
        self.driving_license_entry = Entry(self.my_profile_frame, font=("times new roman", 15), bg="lightgray")
        self.driving_license_entry.place(x=300, y=150)

        #fill in the driving license entry
        self.driving_license_entry.insert(0, self.driving_license)
        
        #phone number label
        self.phone_number_label = Label(self.my_profile_frame, text="Phone Number", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.phone_number_label.place(x=100, y=200)

        #phone number entry side by side
        self.phone_number_entry = Entry(self.my_profile_frame, font=("times new roman", 15), bg="lightgray")
        self.phone_number_entry.place(x=300, y=200)

        #fill in the phone number entry
        self.phone_number_entry.insert(0, self.phone_number)

        #update profile button
        self.update_profile_button = Button(self.my_profile_frame, text="Update Profile", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.update_profile)
        self.update_profile_button.place(x=100, y=250)

        #logout button
        self.logout_button = Button(self.my_profile_frame, text="Logout", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.logout)
        self.logout_button.place(x=300, y=250)




    #staff dashboard
    def staff_dashboard(self):
        for i in self.root.winfo_children():
            i.destroy()

        #welcome to auto360 label
        self.welcome_label = Label(self.root, text="Welcome to Auto360", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.welcome_label.place(x=0, y=0, relwidth=1)

        #dashboard frame
        self.dashboard_frame = Frame(self.root, bg="white")
        self.dashboard_frame.place(x=0, y=50, relwidth=1, height=600)

        #staff login heading "Staff Login"
        self.staff_login_heading = Label(self.dashboard_frame, text="Staff Login", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.staff_login_heading.place(x=5, y=5, relwidth=1)

        #staff availability combobox right corner
        self.staff_available_combobox = ttk.Combobox(self.dashboard_frame, font=("times new roman", 15), state="readonly")
        self.staff_available_combobox['values'] = ("Available", "Not Available")
        self.staff_available_combobox.place(x=700, y=5,width=200)

        #staff available label right corner
        self.staff_available_label = Label(self.dashboard_frame, text="Staff Availability", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.staff_available_label.place(x=500, y=5)

        #notebook frame
        self.notebook = ttk.Notebook(self.dashboard_frame)
        self.notebook.place(x=0, y=50, relwidth=1, relheight=1)

        #current apporinment tab
        self.current_appoinment_tab = Frame(self.notebook, bg="white")
        self.notebook.add(self.current_appoinment_tab, text="Current Appoinment")

        #previous appoinment tab
        self.previous_appoinment_tab = Frame(self.notebook, bg="white")
        self.notebook.add(self.previous_appoinment_tab, text="Previous Appoinment")

        #my profile tab
        self.my_profile_tab = Frame(self.notebook, bg="white")
        self.notebook.add(self.my_profile_tab, text="My Profile")

        #frame inside current appoinment tab for treeview




    #logout
    def logout(self):
        self.login_screen()



    #update_profile
    def update_profile(self):
        #get detials from entries
        username = self.username_entry.get()
        email = self.email_entry.get()
        driving_license = self.driving_license_entry.get()
        phone_number = self.phone_number_entry.get()

        #update users table
        mycursor.execute("UPDATE users SET username=%s, email=%s, driving_license=%s, phone_number=%s WHERE id=%s", (username, email, driving_license, phone_number, self.user_id))
        mydb.commit()

        #update username and email in the dashboard
        self.username = username
        self.email = email
        self.driving_license = driving_license
        self.phone_number = phone_number

        #open dashboard
        self.dashboard_screen()

        #my profile tab
        self.notebook.select(self.my_profile_tab)




    #book appointment page
    def book_appointment_page(self):
        self.dashboard_screen()

        #open book appointment tab
        self.notebook.select(self.book_appointment_tab)


    #create appoinment
    def create_appointment(self):
        self.dashboard_screen()

        #open book appointment tab
        self.notebook.select(self.book_appointment_tab)

    #update appoinment
    def update_appointment(self):
        #get appoinment details from selector
        self.current_appoinment_id = self.my_appointment_tree.item(self.my_appointment_tree.selection())['values'][0]
        vehicle_name = self.my_appointment_tree.item(self.my_appointment_tree.selection())['values'][1]
        appoinment_date = self.my_appointment_tree.item(self.my_appointment_tree.selection())['values'][2]
        appoinment_time = self.my_appointment_tree.item(self.my_appointment_tree.selection())['values'][3]
        appoinment_type = self.my_appointment_tree.item(self.my_appointment_tree.selection())['values'][4]
        appoinment_status = self.my_appointment_tree.item(self.my_appointment_tree.selection())['values'][5]

        #clear all children
        for i in self.root.winfo_children():
            i.destroy()

        #frame inside book appointment tab
        self.update_appointment_frame = Frame(self.root, bg="white")
        self.update_appointment_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        #update appointment heading "Update Appointment for Vehicle Inspection"
        self.update_appointment_heading = Label(self.update_appointment_frame, text="Update Appointment for Vehicle Inspection", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.update_appointment_heading.place(x=5, y=5, relwidth=1)

        #vehicle name label
        self.vehicle_name_label = Label(self.update_appointment_frame, text="Vehicle Name", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_name_label.place(x=100, y=50)

        #vehicle details combobox
        self.vehicle_name_combobox = ttk.Combobox(self.update_appointment_frame, font=("times new roman", 15), state="readonly")
        self.vehicle_name_combobox.place(x=100, y=80,width=200)


        #add event update button
        self.vehicle_name_combobox.bind("<<ComboboxSelected>>", self.vehicle_model_number)

        #get all user vehicle names
        mycursor.execute("SELECT * FROM vehicles WHERE user_id=%s", (self.user_id,))
        vehicles = mycursor.fetchall()
        vehicle_names = []

        for vehicle in vehicles:
            vehicle_names.append(vehicle[2])
        self.vehicle_name_combobox['values'] = vehicle_names

        #vehicle model label
        self.vehicle_model_label = Label(self.update_appointment_frame, text="Vehicle Model", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_model_label.place(x=100, y=130)

        #vehicle model entry
        self.vehicle_model_entry = Entry(self.update_appointment_frame, font=("times new roman", 15), bg="lightgray")
        self.vehicle_model_entry.place(x=100, y=160,width=200)

        #vehicle number label
        self.vehicle_number_label = Label(self.update_appointment_frame, text="Vehicle Number", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_number_label.place(x=100, y=210)

        #vehicle number entry
        self.vehicle_number_entry = Entry(self.update_appointment_frame, font=("times new roman", 15), bg="lightgray")
        self.vehicle_number_entry.place(x=100, y=240,width=200)



        #inspection type label
        self.inspection_type_label = Label(self.update_appointment_frame, text="Inspection Type", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.inspection_type_label.place(x=100, y=290)

        #inspection type combobox
        self.inspection_type_combobox = ttk.Combobox(self.update_appointment_frame, font=("times new roman", 15), state="readonly")
        self.inspection_type_combobox['values'] = ("General Inspection", "Oil Change", "Brake Inspection", "Tire Rotation", "Battery Check", "Air Filter Replacement", "Coolant Flush", "Transmission Flush", "Engine Tune-up", "Wheel Alignment", "Exhaust System Inspection", "Fuel Filter Replacement", "Timing Belt Replacement", "Spark Plug Replacement", "Suspension Inspection", "Steering Inspection", "Air Conditioning Inspection", "Electrical System Inspection", "Exhaust System Inspection", "Fuel System Inspection", "Transmission Inspection", "Engine Inspection", "Cooling System Inspection", "Brake System Inspection", "Steering System Inspection", "Suspension System Inspection", "Drivetrain Inspection", "Emission System Inspection", "Safety Inspection", "Pre-purchase Inspection", "Other")
        self.inspection_type_combobox.place(x=100, y=320,width=200)


        #fill in the inspection type combobox
        self.inspection_type_combobox.set(appoinment_type)

        #inspection description label
        self.inspection_description_label = Label(self.update_appointment_frame, text="Inspection Description", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.inspection_description_label.place(x=400, y=50)

        #inspection description entry
        self.inspection_description_entry = Text(self.update_appointment_frame, font=("times new roman", 15), bg="lightgray", height=5)
        self.inspection_description_entry.place(x=400, y=80, relwidth=0.5)

        #appoinment date label
        self.appoinment_date_label = Label(self.update_appointment_frame, text="Appoinment Date", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.appoinment_date_label.place(x=100, y=370)

        #appoinment date entry
        self.appoinment_date_entry = DateEntry(self.update_appointment_frame, font=("times new roman", 15), bg="lightgray")
        self.appoinment_date_entry.place(x=100, y=400,width=200)

        #fill in the appoinment date entry
        self.appoinment_date_entry.set_date(appoinment_date)

        #appoinment time label
        self.appoinment_time_label = Label(self.update_appointment_frame, text="Appoinment Time", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.appoinment_time_label.place(x=100, y=450)

        #appoinment time comboxbox ( availability of time)
        self.appoinment_time_combobox = ttk.Combobox(self.update_appointment_frame, font=("times new roman", 15), state="readonly")
        self.appoinment_time_combobox['values'] = ("9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM")
        self.appoinment_time_combobox.place(x=100, y=480,width=200)

        #fill in the appoinment time combobox
        self.appoinment_time_combobox.set(appoinment_time)

        #update appointment button
        self.update_appointment_button = Button(self.update_appointment_frame, text="Update Appointment", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.update_appointment_db)
        self.update_appointment_button.place(x=400, y=210)


    #delete appointment
    def delete_appointment(self):
        appoinment_id = self.current_appoinment_id
        mycursor.execute("DELETE FROM appoinment WHERE id=%s", (appoinment_id,))
        mydb.commit()
        messagebox.showinfo("Success", "Appointment deleted successfully")
        self.dashboard_screen()

    #update appointment in database
    def update_appointment_db(self):
        appoinment_id = self.current_appoinment_id
        vehicle_name = self.vehicle_name_combobox.get()
        appoinment_date = self.appoinment_date_entry.get()
        appoinment_time = self.appoinment_time_combobox.get()
        appoinment_type = self.inspection_type_combobox.get()
        appoinment_description = self.inspection_description_entry.get(1.0, "end")

        #convert timestamp to time
        appoinment_time = datetime.datetime.strptime(appoinment_time, "%I:%M %p").time()


        if vehicle_name == "" or appoinment_date == "" or appoinment_time == "" or appoinment_type == "":
            messagebox.showerror("Error", "All fields are required")
            return

        mycursor.execute("SELECT * FROM vehicles WHERE user_id=%s AND vehicle_name=%s", (self.user_id, vehicle_name))
        vehicle = mycursor.fetchone()
        vehicle_id = vehicle[0]

        mycursor.execute("UPDATE appoinment SET vehicle_id=%s, appoinment_date=%s, appoinment_time=%s, appoinment_type=%s, appoinment_description=%s WHERE id=%s", (vehicle_id, appoinment_date, appoinment_time, appoinment_type, appoinment_description, appoinment_id))

        mydb.commit()
        messagebox.showinfo("Success", "Appointment updated successfully")
        self.dashboard_screen()


    #
    #vehicle model number and vehicle number label auto full with combobox
    def vehicle_model_number(self, event):
        vehicle_name = self.vehicle_name_combobox.get()
        mycursor.execute("SELECT * FROM vehicles WHERE user_id=%s AND vehicle_name=%s", (self.user_id, vehicle_name))
        vehicle = mycursor.fetchone()
        self.vehicle_id = vehicle[0]
        self.vehicle_model_entry.delete(0, "end")
        self.vehicle_model_entry.insert(0, vehicle[3])
        self.vehicle_number_entry.delete(0, "end")
        self.vehicle_number_entry.insert(0, vehicle[4])    


    #delete vehicle
    def delete_vehicle(self):
        vehicle_id = self.my_appointment_tree.item(self.my_appointment_tree.selection())['values'][0]
        mycursor.execute("DELETE FROM vehicles WHERE id=%s", (vehicle_id,))
        mydb.commit()
        messagebox.showinfo("Success", "Vehicle deleted successfully")
        self.dashboard_screen()
            

    #add vehicle
    def add_vehicle(self):
        for i in self.root.winfo_children():
            i.destroy()

        #welcome to auto360 label
        self.welcome_label = Label(self.root, text="Welcome to Auto360", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.welcome_label.place(x=0, y=0, relwidth=1)

        #add vehicle frame
        self.add_vehicle_frame = Frame(self.root, bg="white")
        self.add_vehicle_frame.place(x=250, y=100, width=500, height=500)

        #add vehicle title
        self.add_vehicle_title = Label(self.add_vehicle_frame, text="Add Vehicle", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.add_vehicle_title.place(x=0, y=50, relwidth=1)

        #vehicle name label
        self.vehicle_name_label = Label(self.add_vehicle_frame, text="Vehicle Name", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_name_label.place(x=100, y=100)

        #vehicle name entry
        self.vehicle_name_entry = Entry(self.add_vehicle_frame, font=("times new roman", 15), bg="lightgray")
        self.vehicle_name_entry.place(x=100, y=130)

        #vehicle model label
        self.vehicle_model_label = Label(self.add_vehicle_frame, text="Vehicle Model", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_model_label.place(x=100, y=180)

        #vehicle model entry
        self.vehicle_model_entry = Entry(self.add_vehicle_frame, font=("times new roman", 15), bg="lightgray")
        self.vehicle_model_entry.place(x=100, y=210)

        #vehicle number label
        self.vehicle_number_label = Label(self.add_vehicle_frame, text="Vehicle Number", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_number_label.place(x=100, y=260)

        #vehicle number entry
        self.vehicle_number_entry = Entry(self.add_vehicle_frame, font=("times new roman", 15), bg="lightgray")
        self.vehicle_number_entry.place(x=100, y=290)

        #vehicle type label
        self.vehicle_type_label = Label(self.add_vehicle_frame, text="Vehicle Type", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_type_label.place(x=100, y=340)

        #vehicle type combobox
        self.vehicle_type_combobox = ttk.Combobox(self.add_vehicle_frame, font=("times new roman", 15), state="readonly")
        self.vehicle_type_combobox['values'] = ("Car", "Bike", "Truck", "Bus", "SUV", "Van", "Other")

        self.vehicle_type_combobox.place(x=100, y=370,width=200)

        #add vehicle
        self.add_vehicle_button = Button(self.add_vehicle_frame, text="Add Vehicle", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.add_vehicle_db)
        self.add_vehicle_button.place(x=100, y=420)

        #back to dashboard
        self.dashboard_button = Button(self.add_vehicle_frame, text="Dashboard", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.dashboard_screen)
        self.dashboard_button.place(x=250, y=420)



    #add vehicle to database
    def add_vehicle_db(self):
        vehicle_name = self.vehicle_name_entry.get()
        vehicle_model = self.vehicle_model_entry.get()
        vehicle_number = self.vehicle_number_entry.get()
        vehicle_type = self.vehicle_type_combobox.get()

        if vehicle_name == "" or vehicle_model == "" or vehicle_number == "" or vehicle_type == "":
            messagebox.showerror("Error", "All fields are required")
            return

        mycursor.execute("INSERT INTO vehicles (user_id, vehicle_name, vehicle_model, vehicle_number, vehicle_type) VALUES (%s, %s, %s, %s, %s)", (self.user_id, vehicle_name, vehicle_model, vehicle_number, vehicle_type))
        mydb.commit()
        messagebox.showinfo("Success", "Vehicle added successfully")
        self.dashboard_screen()


    #update vehicle
    def update_vehicle(self):
        
        #get vehicle details from selector
        vehicle_id = self.my_appointment_tree.item(self.my_appointment_tree.selection())['values'][0]
        vehicle_name = self.my_appointment_tree.item(self.my_appointment_tree.selection())['values'][1]
        vehicle_model = self.my_appointment_tree.item(self.my_appointment_tree.selection())['values'][2]
        vehicle_number = self.my_appointment_tree.item(self.my_appointment_tree.selection())['values'][3]

        #clear all children
        for i in self.root.winfo_children():
            i.destroy()

        #welcome to auto360 label
        self.welcome_label = Label(self.root, text="Welcome to Auto360", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.welcome_label.place(x=0, y=0, relwidth=1)

        #update vehicle frame
        self.update_vehicle_frame = Frame(self.root, bg="white")
        self.update_vehicle_frame.place(x=250, y=100, width=500, height=500)

        #update vehicle title
        self.update_vehicle_title = Label(self.update_vehicle_frame, text="Update Vehicle", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.update_vehicle_title.place(x=0, y=50, relwidth=1)

        #vehicle name label
        self.vehicle_name_label = Label(self.update_vehicle_frame, text="Vehicle Name", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_name_label.place(x=100, y=100)

        #vehicle name Entry
        self.vehicle_name_entry = Entry(self.update_vehicle_frame, font=("times new roman", 15), bg="lightgray")
        self.vehicle_name_entry.place(x=100, y=130)

        #vehicle model label
        self.vehicle_model_label = Label(self.update_vehicle_frame, text="Vehicle Model", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_model_label.place(x=100, y=180)


        #vehicle model entry
        self.vehicle_model_entry = Entry(self.update_vehicle_frame, font=("times new roman", 15), bg="lightgray")
        self.vehicle_model_entry.place(x=100, y=210)

        #vehicle number label
        self.vehicle_number_label = Label(self.update_vehicle_frame, text="Vehicle Number", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_number_label.place(x=100, y=260)

        #vehicle number entry
        self.vehicle_number_entry = Entry(self.update_vehicle_frame, font=("times new roman", 15), bg="lightgray")
        self.vehicle_number_entry.place(x=100, y=290)

        #vehicle type label
        self.vehicle_type_label = Label(self.update_vehicle_frame, text="Vehicle Type", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.vehicle_type_label.place(x=100, y=340)

        #vehicle type combobox
        self.vehicle_type_combobox = ttk.Combobox(self.update_vehicle_frame, font=("times new roman", 15), state="readonly")
        self.vehicle_type_combobox['values'] = ("Car", "Bike", "Truck", "Bus", "SUV", "Van", "Other")

        self.vehicle_type_combobox.place(x=100, y=370,width=200)


        #fill the entries with the selected vehicle details
        self.vehicle_name_entry.insert(0, vehicle_name)
        self.vehicle_model_entry.insert(0, vehicle_model)
        self.vehicle_number_entry.insert(0, vehicle_number)
        
        #update vehicle button
        self.update_vehicle_button = Button(self.update_vehicle_frame, text="Update Vehicle", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.update_vehicle_db)
        self.update_vehicle_button.place(x=100, y=420)

        #back to dashboard
        self.dashboard_button = Button(self.update_vehicle_frame, text="Dashboard", font=("times new roman", 15, "bold"), bg="blue", fg="white", command=self.dashboard_screen)
        self.dashboard_button.place(x=250, y=420)

    #update vehicle to database
    def update_vehicle_db(self):
        vehicle_name = self.vehicle_name_entry.get()
        vehicle_model = self.vehicle_model_entry.get()
        vehicle_number = self.vehicle_number_entry.get()
        vehicle_type = self.vehicle_type_combobox.get()

        if vehicle_name == "" or vehicle_model == "" or vehicle_number == "" or vehicle_type == "":
            messagebox.showerror("Error", "All fields are required")
            return

        mycursor.execute("UPDATE vehicles SET vehicle_name=%s, vehicle_model=%s, vehicle_number=%s, vehicle_type=%s WHERE user_id=%s", (vehicle_name, vehicle_model, vehicle_number, vehicle_type, self.user_id))
        mydb.commit()
        messagebox.showinfo("Success", "Vehicle updated successfully")
        self.dashboard_screen()
        


    #book appointment
    def book_appointment(self):
        vehicle_name = self.vehicle_name_combobox.get()
        vehicle_model = self.vehicle_model_entry.get()
        vehicle_number = self.vehicle_number_entry.get()
        inspection_type = self.inspection_type_combobox.get()
        inspection_description = self.inspection_description_entry.get(1.0,'end')
        appoinment_date = self.appoinment_date_entry.get()
        appoinment_time = self.appoinment_time_combobox.get()

        print(len(inspection_description),inspection_type)

        #if inspection_type is Other then description is required
        if inspection_type == "Other" and len(inspection_description) == 1:
            messagebox.showerror("Error", "Inspection description is required")
            return
        
        #if description is none set to None then it will be empty
        if inspection_description == "":
            inspection_description = None

        #convert timestring to time format is in
        appoinment_time = datetime.datetime.strptime(appoinment_time, "%I:%M %p").time()

        if vehicle_name == "" or vehicle_model == "" or vehicle_number == "" or inspection_type == "" or inspection_description == "" or appoinment_date == "" or appoinment_time == "":
            messagebox.showerror("Error", "All fields are required")
            return

        mycursor.execute("INSERT INTO appoinment (user_id, vehicle_id, appoinment_date, appoinment_time, appoinment_type, appoinment_description) VALUES (%s, %s, %s, %s, %s, %s)", (self.user_id,self.vehicle_id,appoinment_date, appoinment_time, inspection_type, inspection_description))
        mydb.commit()
        messagebox.showinfo("Success", "Appointment booked successfully")

        #back to main
        self.dashboard_screen()

        #open my appoinment tab
        self.notebook.select(1)



    #login button
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "All fields are required")
            return
        
        #seperate from @ auto360.com then redirect to staff dashboard
        if username == "admin" and password == "admin":
            self.admin_dashboard()
            return
    
        
        mycursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = mycursor.fetchone()






        if user == None:
            messagebox.showerror("Error", "Invalid username or password")
        else:
            self.username = user[1]
            self.email = user[2]
            self.driving_license = user[4]
            self.phone_number = user[5]
            messagebox.showinfo("Success", "Login successful")
            self.user_id = user[0]
            self.type=user[6]
            if self.type == "staff":
                self.staff_dashboard()
            self.dashboard_screen()


    #register
    def register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        driving_license = self.driving_license_entry.get()
        phone_number = self.phone_number_entry.get()

        if username == "" or email == "" or password == "" or driving_license == "" or phone_number == "":
            messagebox.showerror("Error", "All fields are required")
            return

        mycursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = mycursor.fetchone()
        if user != None:
            messagebox.showerror("Error", "Username already exists")
            return

        mycursor.execute("INSERT INTO users (username, email, password, driving_license, phone_number) VALUES (%s, %s, %s, %s, %s)", (username, email, password, driving_license, phone_number))
        mydb.commit()
        messagebox.showinfo("Success", "Register successful")
        #restart project
        self.login_screen()

    
        
    





#starter code
if __name__ == "__main__":
    root = tk.Tk()
    obj = auto360(root)
    root.mainloop()
