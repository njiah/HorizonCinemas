import tkinter as tk
from tkinter import ttk, TclError, Text


class Staff:
    def __init__(self, firstName, lastName, staffID):
        self.firstName = firstName
        self.lastName = lastName
        self.staffID = staffID
    
    def setFirstName(self, firstName):
        self.firstName = firstName
    
    def setLastName(self, lastName):
        self.lastName = lastName


class AdminStaff(Staff):
    def __init__(self, firstName, lastName, adminID):
        super().__init__(firstName, lastName)
        self.adminID = adminID
    
class ManagingStaff(AdminStaff):
    def __init__(self, firstName, lastName, managerID):
        super().__init__(firstName, lastName)
        self.managerID = managerID


class Movie:
    def __init__(self, name, genre):
        self.name = name
        self.genre = genre
        self.showTime = Show
    
    def getShowTimes(self):
        return self.showTime

class Show:
    def __init__(self):
        self.movie = Movie
        self.screen = Screen

    def getMovieName(self):
        return self.movie
    
    def setScreen(self, screen):
        self.screen = screen
    
    def getScreen(self):
        return self.screen


class Screen:
    def __init__(self):
        self.seats = Seat 

    def getSeats(self):
        return self.seats

class Seat:
    def __init__(self, seatNumber, seatType, availabilty = 'Y'):
        self.seatNumber = seatNumber
        self.seatType = seatType
        self.availabilty = availabilty
    
    def getSeatNumber(self):
        return self.seatNumber

    def reserveSeat(self):
        self.availabilty = 'N'

class Cinema:
    def __init__(self):
        self.location = City 
        self.screens = Screen
        self.movies = Movie
    
    def getMovies(self):
        return self.movies
    
    def getScreens(self):
        return self.screens

class City:
    def __init__(self, cityName):
        self.cityName = cityName
        self.cinemas = Cinema
    
    def getCityName(self):
        return self.cityName
    
    def getCinemas(self):
        return self.cinemas

class Booking:
    def __init__(self, bookingID):
        self.bookingID = bookingID 
        self.movieName = Movie
        self.seatNumbers = Seat
        self.showTime = Show
    
    def getBookingID(self):
        return self.bookingID
    
    def getMovieName(self):
        return self.movieName
    
    def getSeatNumbers(self):
        return self.seatNumbers
    
    def getShowTime(self):
        return self.showTime

class HorizonCinemaSystem:
    def __init__(self):
        self.cities = City
    
    def getCities(self):
        return self.cities
        

#GUI
def create_main_window():
    window = tk.Tk()
    window.title('Horizon Cinemas')

    try:
        window.attributes(" - toolwindow ", True)
    except TclError:
        print(' - toolwindow NOT supported on your platform')

    window.mainloop()

if __name__= "__main__":
    create_main_window()