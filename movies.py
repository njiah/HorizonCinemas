from db_connect import *
import tkinter as tk
from tkinter import *

conn = getConn()
cur = getCursor()

class MovieModel:
    def __init__(self, moviename, genre, description, pg, rating):
        self.__moviename = moviename
        self.__genre = genre
        self.__description = description
        self.__pg = pg
        self.__rating = rating

    def getMovieName(self):
        return self.__moviename

    def getGenre(self):
        return self.__genre

    def getDescription(self):
        return self.__description

    def getPG(self):
        return self.__pg

    def getRating(self):
        return self.__rating

    #def getMovie(self, moviename, )


class MovieView(tk.Frame):
    def __init__(self, container, movieName, genre, rating, pg, description):
        super().__init__(container)

        self.container = container
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.border = tk.Frame(self, background="black")
        self.border.grid(row=0, column=0, padx=1, pady=1)
        self.frame = tk.Frame(self.border)
        self.frame.grid(padx=1, pady=1)

        self.movieName = movieName
        self.genre = genre
        self.rating = rating
        self.pg = pg
        self.description = description

        self.movie_name_label = Label(self.frame, text=str(self.movieName), font=("bold"))
        self.movie_name_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.rating_label = Label(self.frame, text="IMDb Rating: 8.5, Action, Drama, 2022, PG-13, 2h 10m")
        self.rating_label.grid(row=1, sticky=tk.W, column=0, padx=5, pady=5)

        #self.description_label = ttk.Label(self.frame, text="After more than thirty years of service as one of the Navy's top aviators, Pete Mitchell is where he belongs,\n pushing the envelope as a courageous test pilot and dodging the advancement\n in rank that would ground him.")
        self.description_label = Label(self.frame, text=self.description )
        self.description_label.grid(row=2, sticky=tk.W, column=0, padx=5, pady=5)

        self.cast_label = Label(self.frame, text="Cast: Tom Cruise, Jennifer Conelly, Miles Teller")
        self.cast_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        self.showings_label = Label(self.frame, text="Showings: ", font=("bold"))
        self.showings_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.show_frame = Frame(self.frame, borderwidth=1)
        self.show_frame.grid(row=5, column=0, padx=10, pady=10)
        for i in range(3):
            

            self.shows = Label(self.show_frame, text=f"Show {i+1}", background="black", relief=tk.RAISED)
            self.shows.grid(row=6, column=i, padx=5, pady=5)

            self.showtime = Label(self.show_frame, text=f"{10+(2*i)}:00 [60 seats available]")
            self.showtime.grid(row=7, column=i, padx=5, pady=5)

    def setController(self, controller):
        self.controller = controller

class movieController:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view

    #def getMovie(self)

'''
class movieApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('List of Movies showing')
        #self.geometry("1000x800")
        #self.resizable(0,0)
        self.config(bg='#F25252')
        border = tk.Frame(self)
        border.pack()
        
        frame = tk.Text(border)
        frame.grid(row=0, column=0)
        v = tk.Scrollbar(border, orient='vertical')
        v.grid(row=0, column=1)
        #v = tk.Scrollbar(frame, orient='vertical')
        #v.bind()
        frame.config(yscrollcommand=v.set)
        v.config(command=frame.yview)

        # create a model
        cur.execute('SELECT * FROM Movie')
        movies = cur.fetchall()
        i=0
        for movie in movies:
            
            movieName = movie[1]
            genre = movie[2]
            rating = movie[3]
            PG = movie[4]
            description = movie[5]
            model = MovieModel(moviename=movieName, genre=genre, rating=rating, pg=PG, description=description)
            view = MovieView(border, movieName=movieName, genre=genre, rating=rating, pg=PG, description=description)
            view.grid(row=i, column=0, padx=10, pady=10)
            frame.insert(tk.END, view)
            i=i+1
        # create a view and place it on the root window
        #view = MovieView(self)
        #view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = movieController(model, view)
        #view.config(yscrollcommand=h.set)
        #h.config(command=view.yview)

        # set the controller to view
        view.setController(controller)


if __name__ == '__main__':
    app = movieApp()
    app.mainloop()  

        

'''


