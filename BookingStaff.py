import tkinter.messagebox
from datetime import datetime, date
from functools import partial
from random import randrange
from tkinter import *
from PIL import Image, ImageTk

from Main import *
from db_connect import *
from movies import *

bookingConn = getConn()
bookingCur = getCursor()

#########################
## Booking Staff Pages ##   
#########################

#Booking Staff Main Page once logged in
class Booking_staff_main(tk.Frame):
    #Booking Staff main menu page. Allows user to update profile, see booking history, and search for films by date
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.__user = user
        self.defdate1 = StringVar()
        self.controller = None


        self.user_label = Label(self, text=f"Welcome! {self.__user}")
        self.user_label.grid(row=0, column=0, padx=5, pady=5)

        
        #Button for Updating Profile
        self.up = Button(self.master, font=("Helvetica", 16), text="Update Profile", bg="yellow", command=self.Update_Profile_window)
        self.up.grid(row=1, column=0, padx=5, pady=5)
        #Button for Booking History
        self.bh = Button(self.master, font=("Helvetica", 16), text="Booking History", bg="yellow", command=self.Booking_History_window)
        self.bh.grid(row=2, column=0, padx=5, pady=5)
        #Label for "Search for films by date:"
        self.search_label = Label(self.master, font=("Helvetica", 16), text='Search for films by date:')
        self.search_label.grid(row=3, column=0, padx=5, pady=5)

        # default value
        dates = ["Monday 01/12/22", "Tuesday 02/12/22", "Wednesday 03/12/22", "Thursday 04/12/22", "Friday 05/12/22", "Saturday 06/12/22", "Sunday 07/12/22" ]
        self.defdate1.set("Pick a date...") 
        self.datelist1 = OptionMenu(master, self.defdate1, *dates)
        self.datelist1.grid(row=4, column=0, padx=5, pady=5)
        self.datelist1.config(width=15)
        #Button for Searching films within specified date
        self.searching = Button(self.master, text="Search", command=self.search)
        self.searching.grid(row=5, column=0, padx=5, pady=5)

        #Button for Logging out
        self.logout_button = Button(self.master, font=("Helvetica", 12), text="Logout", fg="white", bg='black', command=self.logout)
        self.logout_button.grid(row=6, column=0, padx=5, pady=5)

    def set_controller(self, controller):
        self.controller = controller

    def search(self):
        if self.controller:
            self.controller.searchDate(self.__user, self.defdate1.get())

    def getMovies(self, username, date):
        user = username
        date = date
        self.newWindow = Toplevel(self.master)
        #view = MovieView(self.newWindow)
        bookingCur.execute('SELECT * FROM Movie')
        movies = bookingCur.fetchall()
        i=0
        for movie in movies:
            
            movieName = movie[1]
            genre = movie[2]
            rating = movie[3]
            PG = movie[4]
            description = movie[5]
            #model = MovieModel(moviename=movieName, genre=genre, rating=rating, pg=PG, description=description)
            view = MovieView(self.newWindow, movieName=movieName, genre=genre, rating=rating, pg=PG, description=description)
            view.grid(row=i, column=0, padx=10, pady=10)
            i=i+1
        self.master.withdraw()


    def sch(self):
        search_date = self.defdate1.get()
        c2.execute("""SELECT * FROM movies WHERE
                            date = ? ORDER BY time='1pm' DESC,
                                                time='2pm' DESC,
                                                time='3pm' DESC,
                                                time='4pm' DESC,
                                                time='5pm' DESC,
                                                time='6pm' DESC,
                                                time='7pm' DESC,
                                                time='8pm' DESC,
                                                time='9pm' DESC,
                                                time='10pm' DESC """, (search_date,))
        output = c2.fetchall()
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1450x720')
        self.app = SearchResults(self.newWindow, output, search_date)
        self.master.withdraw()

    def Update_Profile_window(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('400x400')
        self.app = Booking_staff_profile(self.newWindow)
        self.master.withdraw()

    def Booking_History_window(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1096x720')
        self.app = BookHist(self.newWindow)
        self.master.withdraw()

    def logout(self):
        msg = tkinter.messagebox.askyesno('Logout', 'Are you sure you want to log out?')
        if msg:
            self.newWindow = Toplevel(self.master)
            self.newWindow.geometry('350x350')
            self.app = MainPage(self.newWindow)
            self.master.withdraw()

    def show_error(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'        
        self.username_entry['foreground'] = 'red'
        self.password_entry['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)

class BookingController:
    def __init__(self, model):
        self.model = model 

    def searchDate(self, user, date):
        try:
            self.model.getMovies(user, date)
        except ValueError as error:
            self.model.show_error(error)



#Search Results page according to date selected on the booking staff home page
class SearchResults(Booking_staff_main):
    def __init__(self, master, output, search_date):
        self.search_date = search_date
        self.master = master
        self.output = output
        self.frame = Frame(self.master)
        self.label = Label(self.master)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0)
        self.date = Label(self.master, text='Date', font=("Helvetica", 13), width=8).grid(row=0, column=1, pady='1')
        self.time = Label(self.master, text='Time', font=("Helvetica", 13), width=6).grid(row=0, column=2, pady='1')
        self.title = Label(self.master, text='Title', font=("Helvetica", 13), width=15).grid(row=0, column=3, pady='1')
        self.description = Label(self.master, text='Description', font=("Helvetica", 13), width=30).grid(row=0, column=4, pady='1')
        self.city = Label(self.master, text='City', font=("Helvetica", 13), width=8).grid(row=0, column=5, pady='1')
        self.price = Label(self.master, text='Price', font=("Helvetica", 13), width=8).grid(row=0, column=6, pady='1')
        self.booked = Label(self.master, text='Booked', font=("Helvetica", 13), width=8).grid(row=0, column=7, pady='1')
        self.available = Label(self.master, text='Available', font=("Helvetica", 13), width=8).grid(row=0, column=8, pady='1')
        self.book = Label(self.master, text='Book ticket', font=("Helvetica", 13), width=12).grid(row=0, column=9, pady='1')
        widths = (15, 6, 20, 20, 8, 8, 8, 12)
        for i in self.output:
            for j in i:
                b = Label(self.master, text=j, font=("Helvetica", 11), width=widths[i.index(j)])
                b.grid(row=output.index(i) + 1, column=i.index(j) + 1, pady='1')
            # c2.execute('SELECT booked FROM movies WHERE rowid=?', (output.index(i) + 1,))
            # self.taken = c2.fetchone()[0]  # returns the number of available seats for that movie
            # c2.execute('SELECT date, time FROM movies WHERE date=? AND rowid=?',
            # (self.search_date, output.index(i) + 1,))
            # self.datetime = c2.fetchone()  # returns the date and time of the movie
            
            
            #The variable for bookings in database
            self.taken = i[6]
            #The variable
            self.datetime = (i[0], i[1])
            d = Button(self.master, text='Book', command=partial(self.boo, self.taken, self.datetime), font=("Helvetica", 9))
            d.grid(row=output.index(i) + 1, column=9, pady='1')
        self.back = Button(self.master, font=("Helvetica", 12), text="Back", bg="black", fg="white", command=self.back).grid(row=10, column=1, pady='1')
        self.log = Button(self.master, font=("Helvetica", 12), text="Logout", fg="white", bg='black', command=self.logout).grid(row=10, column=2, pady='1')

    def boo(self, gone, datetime7):
        msg = tkinter.messagebox.askyesno('Book', 'Do you want to confirm this booking?')
        if msg:
            self.gone = gone
            self.datetime = datetime7
            self.usr = username.split('_')
            c3.execute("SELECT * FROM bookings WHERE username = ? AND date = ? AND time = ?", (username, self.datetime[0], self.datetime[1]))
            alr = c3.fetchone()
            if alr:
                tkinter.messagebox.showinfo("---- ERROR ----", "You are already booked into this film", icon="warning")
            elif self.gone == 100:
                tkinter.messagebox.showinfo("---- ERROR ----", "Movie showing full", icon="warning")
            else:
                td_hour = datetime.today().hour - 12
                td_day = date.today().day
                td_month = date.today().month
                td_year = date.today().year
                new_time = int(self.datetime[1][:-2])
                temp_date = self.datetime[0].split()
                new_date = int(temp_date[1][:2])
                # print(new_time, new_date)
                if td_year < 2018:
                    tkinter.messagebox.showinfo("---- ERROR ----", "Date and time of showing has passed!", icon="warning")
                    
                else:
                    with conn2:
                        c2.execute("UPDATE movies SET booked = ?, available = ? WHERE date = ? AND time = ?", (self.gone + 1, 100 - (self.gone + 1), datetime7[0], datetime7[1]))
                    self.newWindow = Toplevel(self.master)
                    self.newWindow.geometry('1096x720')
                    self.app = Booked(self.newWindow, self.datetime)
                    self.master.withdraw()

    def back(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1096x720')
        self.app = Booking_staff_main(self.newWindow)
        self.master.withdraw()
#This page is used for updating booking staff profile
class Booking_staff_profile(Frame):
    #Allows the customer to update their profile
    def __init__(self, master, user):
        self.master = master
        self.__user = user
        self.frame = Frame(self.master)
        self.label = Label(self.master)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0)
        self.usr = username.split('_')
        c.execute('SELECT * FROM customers WHERE username = ?', (username,))

        self.title = Label(self.master, text="Please update your details below:", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady='3')
        self.output = c.fetchone()
        
        self.first = Label(self.master, text="First Name:", width='15').grid(row=1, column=0, pady='3')
        self.firstname = Entry(self.master, width='30')
        self.firstname.insert(END, self.output[0])
        self.firstname.grid(row=1, column=1, pady='3')

        self.last = Label(self.master, text="Last Name:", width='15').grid(row=2, column=0, pady='3')
        self.lastname = Entry(self.master, width='30')
        self.lastname.insert(END, self.output[1])
        self.lastname.grid(row=2, column=1, pady='3')

        self.email = Label(self.master, text="Email Address:", width='15').grid(row=3, column=0, pady='3')
        self.emailadd = Entry(self.master, width='30')
        self.emailadd.insert(END, self.output[2])
        self.emailadd.grid(row=3, column=1, pady='3')

        self.ag = Label(self.master, text="Age:", width='15').grid(row=4, column=0, pady='3')
        self.age = Entry(self.master, width='30')
        self.age.insert(END, self.output[3])
        self.age.grid(row=4, column=1, pady='3')

        self.ps1 = Label(self.master, text="Password:", width='15').grid(row=5, column=0, pady='3')
        self.firstpassword = Entry(self.master, width='30', show='*')
        self.firstpassword.insert(END, self.output[5])
        self.firstpassword.grid(row=5, column=1, pady='3')

        self.ps2 = Label(self.master, text="Confirm Password:", width='15').grid(row=6, column=0, pady='3')
        self.secondpassword = Entry(self.master, width='30', show='*')
        self.secondpassword.insert(END, self.output[5])
        self.secondpassword.grid(row=6, column=1, pady='3')
        
        #Button for updating details
        self.update = Button(self.master, text="Update Details", command=self.change).grid(row=7, columnspan=2, pady='3')
        #Button for "Back" which leads back to previous screen
        self.back = Button(self.master, font=("Helvetica", 12), text="Back", fg="white", bg='black', command=self.back).grid(row=8, column=0, pady='3')
        #Button for logging out of the system
        self.log = Button(self.master, font=("Helvetica", 12), text="Logout", fg="white", bg='black', command=self.logout).grid(row=8, column=1, pady='3')

    def change(self):
        msg = tkinter.messagebox.askyesno('Update Profile', 'Confirm changes?')
        if msg:
            new_first = self.firstname.get()
            new_last = self.lastname.get()
            new_email = self.emailadd.get()
            new_age = self.age.get()
            new_firstpassword = self.firstpassword.get()
            new_secondpassword = self.secondpassword.get()
            
            c.execute("""UPDATE customers SET first = ?, last = ?, email = ?, age = ?, password = ? WHERE username = ?""", (new_first, new_last, new_email, new_age, new_firstpassword, username))
            self.newWindow = Toplevel(self.master)
            self.newWindow.geometry('400x400')
            self.app = Booking_staff_main(self.newWindow)
            self.master.withdraw()
            tkinter.messagebox.showinfo("---- SUCCESSFUL ----", "Profile successfully updated.", icon="info")

    def back(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('400x400')
        self.app = Booking_staff_main(self.newWindow)
        self.master.withdraw()
''' 
    def managerback(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('400x400')
        self.app = ManagerMain(self.newWindow)
        self.master.withdraw()
'''
    

#The class where booking is done successfully
class Booked(Booking_staff_profile, SearchResults):
    def __init__(self, master, datetime1):
        self.datetime1 = datetime1
        self.master = master
        self.frame = Frame(self.master)
        self.label = Label(self.master)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0, pady='1')
        self.usr = username.split('_')   
        c.execute('SELECT * FROM customers WHERE username = ?', (username,))

        self.heading = Label(self.master, text='Booking successful! booking details are below:', width=45, font=("Helvetica", 16)).grid(row=0, columnspan=2, pady='5')

        self.output = c.fetchone()
        self.first = Label(self.master, text="First Name:", width=15).grid(row=1, column=0, pady='3')
        self.firstname = Label(self.master, text=self.output[0], width=30)
        self.firstname.grid(row=1, column=1, pady='3')

        self.last = Label(self.master, text="Last Name:", width=15).grid(row=2, column=0, pady='3')
        self.lastname = Label(self.master, text=self.output[1], width=30)
        self.lastname.grid(row=2, column=1, pady='3')

        self.email = Label(self.master, text="Email Address:", width=15).grid(row=3, column=0, pady='3')
        self.emailadd = Label(self.master, text=self.output[2], width=30)
        self.emailadd.grid(row=3, column=1, pady='3')

        self.ag = Label(self.master, text="Age:", width=15).grid(row=4, column=0, pady='3')
        self.age = Label(self.master, text=self.output[3], width=30)
        self.age.grid(row=4, column=1, pady='3')

        self.da = Label(self.master, text="Date:", width=15).grid(row=5, column=0, pady='3')
        self.date = Label(self.master, text=self.datetime1[0], width=30)
        self.date.grid(row=5, column=1, pady='3')

        self.ti = Label(self.master, text="Time:", width=15).grid(row=6, column=0, pady='3')
        self.time = Label(self.master, text=self.datetime1[1], width=30)
        self.time.grid(row=6, column=1, pady='3')


        c2.execute('''SELECT booked FROM movies WHERE date = ? AND time = ?''', (self.datetime1[0], self.datetime1[1]))

        numb = str(c2.fetchone()[0])
        if len(numb) == 1:
            numb = '0' + str(numb)
        numb0 = int(numb[0])
        numb1 = int(numb[1])
        list_of_rows = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')

        seat_row = list_of_rows[numb0]
        seat_number = str(seat_row) + str(numb1)

        self.se = Label(self.master, text="Seat Number:", width=15).grid(row=8, column=0, pady='1')
        self.seat = Label(self.master, text=seat_number, width=30)
        self.seat.grid(row=9, column=1, pady='1')
        
        
        #Button for going back
        self.back = Button(self.master, font=("Helvetica", 12), text="Back", fg="white", bg='black', command=self.back).grid(row=10, column=0, pady='1')
        #Button for logging out
        self.log = Button(self.master, font=("Helvetica", 12), text="Logout", fg="white", bg='black', command=self.logout).grid(row=10, column=1, pady='1')

        c.execute('SELECT first, last FROM customers WHERE username = ?', (username,))
        namess = c.fetchall()[0]
        with conn3:
            c3.execute('INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?)', (namess[0], namess[1], self.datetime1[0], self.datetime1[1], seat_number, username))
#This class is where the user could view booking history
class BookHist(Booked):
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        self.label = Label(self.master)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0)
        self.usr = username.split('_')

        self.date = Label(self.master, text='Date', font=("Helvetica", 16), width='15').grid(row=0, column=0)
        self.time = Label(self.master, text='Time', font=("Helvetica", 16), width='10').grid(row=0, column=1)
        self.title = Label(self.master, text='Title', font=("Helvetica", 16), width='33').grid(row=0, column=2)
        self.seatno = Label(self.master, text='Seat Number', font=("Helvetica", 16), width='15').grid(row=0, column=3)
        self.remove_booking = Label(self.master, text='Remove Booking', font=("Helvetica", 16), width='15').grid(row=0, column=4)


        c3.execute('''SELECT date, time, seatno FROM bookings WHERE
                    username = ? ORDER BY date='Monday 02/01/23' DESC,
                                                    date='Tuesday 03/01/23' DESC,
                                                    date='Wednesday 04/01/23' DESC,
                                                    date='Thursday 05/01/23' DESC,
                                                    time='1pm' DESC,
                                                    time='2pm' DESC,
                                                    time='3pm' DESC,
                                                    time='4pm' DESC,
                                                    time='5pm' DESC,
                                                    time='6pm' DESC,
                                                    time='7pm' DESC,
                                                    time='8pm' DESC,
                                                    time='9pm' DESC,
                                                    time='10pm' DESC''', (username,))
        tempresult = c3.fetchall()
        for i in tempresult:
            c2.execute('''SELECT title FROM movies WHERE date = ? AND time = ?''', (i[0], i[1]))
            history = c2.fetchone()

            b0 = Label(self.master, text=i[0], font=("Helvetica", 12), width='17')
            b0.grid(row=tempresult.index(i) + 1, column=0)

            b1 = Label(self.master, text=i[1], font=("Helvetica", 12), width='10')
            b1.grid(row=tempresult.index(i) + 1, column=1)

            b2 = Label(self.master, text=history[0], font=("Helvetica", 12), width='40')
            b2.grid(row=tempresult.index(i) + 1, column=2)

            b4 = Label(self.master, text=i[2], font=("Helvetica", 12), width='15')
            b4.grid(row=tempresult.index(i) + 1, column=3)

            b3 = Button(self.master, text='remove', font=("Helvetica", 12), width='15', command=partial(self.remove, i[0], i[1]))
            b3.grid(row=tempresult.index(i) + 1, column=4)

        #The button for going back
        self.back = Button(self.master, font=("Helvetica", 12), text="Back", fg="white", bg='black', command=self.back).grid(row=20, column=0)
        #The button for logging out
        self.log = Button(self.master, font=("Helvetica", 12), text="Logout", fg="white", bg='black', command=self.logout).grid(row=20, column=1)

    def remove(self, date1, time):
        msg = tkinter.messagebox.askyesno('Remove', 'Are you sure you want remove this booking?')
        if msg:
            td_hour = datetime.today().hour - 12
            td_day = date.today().day
            td_month = date.today().month
            td_year = date.today().year
            new_time = int(time[:-2])
            temp_date = date1.split()
            new_date = int(temp_date[1][:2])
            if td_year < 2018 or \
                    td_year == 2018 and td_month > 1 or \
                    td_year == 2018 and td_month == 1 and td_day > new_date or \
                    td_year == 2018 and td_month == 1 and td_day == new_date and td_hour >= new_time:
                tkinter.messagebox.showinfo("---- ERROR ----", "Date and time of showing has passed!", icon="warning")
            else:
                with conn3:
                    c3.execute('''DELETE FROM bookings WHERE username = ? AND date = ? AND time = ?''', (username, date1, time))
                c2.execute('''SELECT booked FROM movies WHERE date = ? AND time = ?''', (date1, time))
                tempgone = c2.fetchone()
                with conn2:
                    c2.execute('''UPDATE movies SET booked = ?, available = ? WHERE date = ? AND time = ?''', (tempgone[0] - 1, 100 - (tempgone[0] - 1), date1, time))
                tkinter.messagebox.showinfo("---- REMOVED ----", "Film removed from booking history.", icon="info")
                self.newWindow = Toplevel(self.master)
                self.newWindow.geometry('1096x720')
                self.app = BookHist(self.newWindow)
                self.master.withdraw()