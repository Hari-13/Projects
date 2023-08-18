from tkinter import *
from Voronoi import Voronoi




def main():
    #visualisation
    points = [(100,200),(50,250), (200,280) , (20,400),(300,60), (250,250), (400,400)]
    vp = Voronoi(points)
    vp.process()
    lines = vp.get_output()
    print(lines)
    root = Tk()
    C = Canvas(root, bg ="white")

    for p in points:
        C.create_oval(p[0], p[1], p[0], p[1], width=0, fill="red")
    for l in lines:
        C.create_line(l[0],l[1],l[2],l[3],fill="black")

    C.pack(fill="both", expand = True)
    mainloop()

if __name__ == '__main__':
    main()