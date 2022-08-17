import os
import re
from tkinter import *
import threading as th
from tkinter import ttk
from io import BytesIO
from pytube import YouTube
from PIL import Image,ImageTk
from urllib.request import urlopen
from pytube.cli import on_progress
from tkinter.ttk import Progressbar
from tkinter import filedialog as fd
from tkinter import messagebox as msg


class main:
    WIDTH = 500
    HEIGHT = 550
    THEAMS = "night"
    COLORS = [
        '#171f26',
        '#1d262f',
        '#202932',
        '#121a23',
        '#191a21',
        '#353535',
        '#03e9f4',
        '#009025',
        '#faf9f6'
    ]
    img_obj = {}
    gui_obj = {}
    data_obj = {}

    def __init__(self,window):
        os.system("clear")
        self.window = window
        self.window.title("Video / Audio Downloader ( Created By NightDevil PT)")
        self.window.config(bg=self.COLORS[0])
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}+50+50")

        night2 = Image.open('icons/night.png')
        night1 = night2.resize((25,25),Image.ANTIALIAS)
        self.img_obj['night'] = ImageTk.PhotoImage(night1)

        light2 = Image.open('icons/light.png')
        light1 = light2.resize((25,25),Image.ANTIALIAS)
        self.img_obj['light'] = ImageTk.PhotoImage(light1)

        ####====== Theams Text Label
        self.gui_obj['theam2.l'] = Label(self.window,text="Developed By : NightDevilPT",fg="white",bg=self.COLORS[0],font=("arial",14,"bold"))
        self.gui_obj['theam2.l'].place(x=10,y=12)

        ####====== Theams Text Label
        self.gui_obj['theam.l'] = Label(self.window,text="Night Mode:",fg="white",bg=self.COLORS[0],font=("arial",14,"bold"))
        self.gui_obj['theam.l'].place(x=330,y=12)

        ####====== Theams Text Button
        self.gui_obj['theam.btn'] = Button(self.window,image=self.img_obj['night'],bg=self.COLORS[0],command=CENTER)
        self.gui_obj['theam.btn'].config(highlightbackground=self.COLORS[0],highlightcolor=self.COLORS[0],bd=0,relief=FLAT,activebackground=self.COLORS[0])
        self.gui_obj['theam.btn'].image = self.img_obj['night']
        self.gui_obj['theam.btn'].config(command=self.Theams_Change)
        self.gui_obj['theam.btn'].place(x=450,y=10,width=30,height=30)

        self.gui_obj['frame1'] = Frame(self.window,height=2,width=500,bg="#03e9f4")
        self.gui_obj['frame1'].place(x=0,y=50)

        ####====== Title Frame and Label
        self.gui_obj['title.l'] = Label(self.window,text="Video / Audio Downloader",fg="white",bg=self.COLORS[0],font=("arial",25,"bold"))
        self.gui_obj['title.l'].place(x=45,y=80)

        self.gui_obj['title.f1'] = Frame(self.window,height=2,width=410,bg="#03e9f4")
        self.gui_obj['title.f1'].place(x=45,y=125)

        self.gui_obj['title.f2'] = Frame(self.window,height=2,width=410,bg="#03e9f4")
        self.gui_obj['title.f2'].place(x=45,y=130)

        ####====== URL Label
        self.gui_obj['link.l'] = Label(self.window,text="Link :",fg="white",bg=self.COLORS[0],font=("arial",15,"bold"))
        self.gui_obj['link.l'].place(x=10,y=150)

        ####====== URL Entry Box
        self.data_obj['link'] = StringVar()
        self.data_obj['link'].set("")

        self.gui_obj['link.e'] = Entry(self.window,textvariable=self.data_obj['link'],fg="black",font=("arial",14,"bold"))
        self.gui_obj['link.e'].config(highlightbackground="white",highlightcolor="white",bd=0,relief=FLAT)
        self.gui_obj['link.e'].place(x=80,y=150,height=30,width=320)

        ####====== Fetch Button
        self.gui_obj['fetch.btn'] = Button(self.window,text="Fetch",bg="#009025",activebackground="#009025",highlightbackground="#009025",highlightcolor="#009025")
        self.gui_obj['fetch.btn'].config(fg="white",font=("arial",15,"bold"),relief=FLAT,bd=0,activeforeground="white")
        self.gui_obj['fetch.btn'].config(command=lambda:th.Thread(target=self.Fetch_Video).start())
        self.gui_obj['fetch.btn'].place(x=410,y=150,height=30)

        ####====== Thumbnail Label
        self.gui_obj['thumbnail'] = Label(self.window,bg="grey")
        self.gui_obj['thumbnail'].place(x=20,y=200,width=16*12,height=9*12)

        ####====== Video Author Label
        self.gui_obj['author.l1'] = Label(self.window,anchor=W,text="Author :",fg="white",bg=self.COLORS[0],font=("arial",12,"bold"),wraplength=460)
        self.gui_obj['author.l1'].place(x=16*12+30,y=200,width=70)

        self.data_obj['author'] = StringVar()
        self.data_obj['author'].set(None)

        self.gui_obj['author.l2'] = Label(self.window,anchor=NW,textvariable=self.data_obj['author'],fg="white",bg=self.COLORS[0],font=("arial",12,"bold"),wraplength=460)
        self.gui_obj['author.l2'].place(x=16*12+100,y=200,width=200)

        ####====== Video Title Label
        self.gui_obj['video_title.l1'] = Label(self.window,anchor=W,text="Title :",fg="white",bg=self.COLORS[0],font=("arial",12,"bold"),wraplength=460)
        self.gui_obj['video_title.l1'].place(x=16*12+30,y=230,width=50)

        self.data_obj['title'] = StringVar()
        self.data_obj['title'].set(None)

        self.gui_obj['video_title.l2'] = Label(self.window,anchor=NW,textvariable=self.data_obj['title'],fg="white",bg=self.COLORS[0],font=("arial",12,"bold"),wraplength=220)
        self.gui_obj['video_title.l2'].place(x=16*12+80,y=230,width=220,height=60)

        ####====== Views Label
        self.gui_obj['view.l1'] = Label(self.window,anchor=W,text="Total Views :",fg="white",bg=self.COLORS[0],font=("arial",12,"bold"),wraplength=460)
        self.gui_obj['view.l1'].place(x=10,y=320,width=100)

        self.data_obj['view'] = StringVar()
        self.data_obj['view'].set(0)

        self.gui_obj['view.l2'] = Label(self.window,anchor=NW,textvariable=self.data_obj['view'],fg="white",bg=self.COLORS[0],font=("arial",12,"bold"),wraplength=460)
        self.gui_obj['view.l2'].place(x=115,y=320)

        ####====== Views Label
        self.gui_obj['duration.l1'] = Label(self.window,anchor=W,text="Duration :",fg="white",bg=self.COLORS[0],font=("arial",12,"bold"),wraplength=460)
        self.gui_obj['duration.l1'].place(x=300,y=320,width=80)

        self.data_obj['duration'] = StringVar()
        self.data_obj['duration'].set("00:00")

        self.gui_obj['duration.l2'] = Label(self.window,anchor=NW,textvariable=self.data_obj['duration'],fg="white",bg=self.COLORS[0],font=("arial",12,"bold"),wraplength=460)
        self.gui_obj['duration.l2'].place(x=380,y=320)
        
        self.gui_obj['frame2'] = Frame(self.window,height=2,width=500,bg="#03e9f4")
        self.gui_obj['frame2'].place(x=0,y=360)

        ####======== Progress Bar
        self.data_obj['info'] = StringVar()
        self.data_obj['info'].set("0%")
        self.gui_obj['progress'] = ttk.Progressbar(self.window,orient=HORIZONTAL,length=400,mode='indeterminate')
        
        self.gui_obj['info.l'] = Label(self.window,anchor=CENTER,textvariable=self.data_obj['info'],fg="white",bg=self.COLORS[0],font=("arial",12,"bold"))
        
    ####===========[ Theams Changing Function ]===========####
    def Theams_Change(self):
        LIGHT = self.COLORS[8]
        NIGHT = self.COLORS[0]
        lst = ['info.l','res.l','theam.btn','theam.l','theam2.l','title.l','link.l','video_title.l1','video_title.l2','author.l1','author.l2','duration.l1','duration.l2','view.l1','view.l2','option.l']

        if self.THEAMS == "night":
            self.window.config(bg="#FAF9F6")
            self.THEAMS = "light"
            self.gui_obj['theam.btn'].config(image=self.img_obj['light'])
            self.gui_obj['theam.btn'].image = self.img_obj['light']
            self.gui_obj['theam.l'].config(text="Light Mode :")
            self.gui_obj['frame1'].config(bg="black")
            self.gui_obj['frame2'].config(bg="black")
            self.gui_obj['title.f1'].config(bg="black")
            self.gui_obj['title.f2'].config(bg="black")
            self.gui_obj['link.e'].config(highlightbackground="black",highlightcolor="black")
            
        else:
            self.window.config(bg=self.COLORS[0])
            self.THEAMS = "night"
            self.gui_obj['theam.btn'].config(image=self.img_obj['night'])
            self.gui_obj['theam.btn'].image = self.img_obj['night']
            self.gui_obj['theam.l'].config(text="Night Mode :")
            self.gui_obj['frame1'].config(bg="#03e9f4")
            self.gui_obj['frame2'].config(bg="#03e9f4")
            self.gui_obj['title.f1'].config(bg="#03e9f4")
            self.gui_obj['title.f2'].config(bg="#03e9f4")
            self.gui_obj['link.e'].config(highlightbackground="white",highlightcolor="white")
        
        for i in lst:
            try:
                if self.THEAMS=="night":
                    self.gui_obj[i].config(fg=LIGHT,highlightbackground=NIGHT,highlightcolor=NIGHT,activebackground=NIGHT,bg=NIGHT)
                else:
                    self.gui_obj[i].config(fg="black",highlightbackground=LIGHT,highlightcolor=LIGHT,activebackground=LIGHT,bg=LIGHT)
            except:
                pass

    ####===========[ Fetching / Searching Video Function ]===========####
    def Fetch_Video(self):
        os.system("clear")
        self.gui_obj['info.l'].place_forget()

        if self.data_obj['link'].get()=="":
            return
        
        # chuck_size= 1024
        self.gui_obj['progress'].place(x=self.WIDTH/2-200,y=self.HEIGHT-70)
        self.gui_obj['progress'].start(10)

        if self.THEAMS=="light":
            self.gui_obj['info.l'].config(fg="black")
        else:
            self.gui_obj['info.l'].config(fg="white")

        try:
            #####======= [ Fetching Video From Youtube ]
            self.yt = YouTube(self.data_obj['link'].get())
            self.data_obj['title'].set(self.yt.title)
            self.data_obj['author'].set(self.yt.author)
            self.data_obj['view'].set(self.yt.views)

            ###===== Converting URL Image Link to Image
            url_thumbnail = urlopen(self.yt.thumbnail_url).read()
            im = Image.open(BytesIO(url_thumbnail))
            resize = im.resize((16*12,9*12),Image.BOX)
            thumbnail = ImageTk.PhotoImage(resize)

            self.gui_obj['thumbnail'].config(image=thumbnail)
            self.gui_obj['thumbnail'].image=thumbnail

            ####========[ Converting Total Seconds In (Hour:Minute:Second) ]
            length = self.yt.length
            time = ""
            if length>60 and length<3600:
                minute = length//60
                second = length%60
                if minute<10:
                    minute = "0"+str(minute)
                if second<10:
                    second = "0"+str(second)
            
                time = f"{minute}:{second}"
            elif length>=3600:
                hour = (length//60)//60
                minute = (length//60)%60
                second = length%60
                if minute<10:
                    minute = "0"+str(minute)
                if second<10:
                    second = "0"+str(second)
                if hour<10:
                    hour = "0"+str(hour)

                time = f"{hour}:{minute}:{second}"
            elif length<60:
                time = length
            
            self.data_obj['duration'].set(time)

            self.gui_obj['progress'].place_forget()

            self.Video_Audio_Options()

        except Exception as e:
            self.gui_obj['progress'].place_forget()
            self.gui_obj['info.l'].place(x=0,y=self.HEIGHT-30,width=500,height=30)
            self.gui_obj['info.l'].config(fg="red")
            self.data_obj['info'].set(e)

    ####===========[ Showiing Options After Fetching Function ]===========####
    def Video_Audio_Options(self):
        os.system("clear")
        self.gui_obj['info.l'].place_forget()

        def Fetch_Options(event=None):
            lst = ['res.l','res.e','download.btn']
            for i in lst:
                try:
                    self.gui_obj[i].destroy()
                except:
                    pass
            
            if self.data_obj['option'].get()=="Video":
                self.gui_obj['progress'].place(x=self.WIDTH/2-200,y=self.HEIGHT-70)
                self.gui_obj['progress'].start(10)
                
                resolution = ['']
                for i in self.yt.streams.filter(progressive=True,file_extension="mp4"):
                    resolution.append(f"{i.resolution} ({(i.filesize//1024)//1024}MB)")
                
                self.gui_obj['res.l'] = Label(self.window,anchor=W,text="Resolution :",fg="white",bg=self.COLORS[0],font=("arial",14,"bold"),wraplength=460)
                
                if self.THEAMS=="night":
                    self.gui_obj['res.l'].config(bg=self.COLORS[0],fg="white")
                elif self.THEAMS=="light":
                    self.gui_obj['res.l'].config(bg=self.COLORS[8],fg="black")

                self.gui_obj['res.l'].place(x=210,y=380,width=110)

                self.data_obj['res'] = StringVar()
                self.data_obj['res'].set(resolution[1])
                self.gui_obj['res.e'] = ttk.OptionMenu(self.window,self.data_obj['res'],*resolution)
                self.gui_obj['res.e'].place(x=330,y=380,width=150,height=30)

                ####====== Download Button
                self.gui_obj['download.btn'] = Button(self.window,text="Download Video",bg="#009025",activebackground="#009025",highlightbackground="#009025",highlightcolor="#009025")
                self.gui_obj['download.btn'].config(fg="white",font=("arial",15,"bold"),relief=FLAT,bd=0,activeforeground="white")
                self.gui_obj['download.btn'].config(command=lambda:th.Thread(target=self.Download_Video).start())
                self.gui_obj['download.btn'].place(x=50,y=430,height=30,width=400)

                self.gui_obj['progress'].place_forget()

            elif self.data_obj['option'].get()=="Audio":
                self.gui_obj['progress'].place(x=self.WIDTH/2-200,y=self.HEIGHT-40)
                self.gui_obj['progress'].start(10)
                
                quality = ['']
                for i in self.yt.streams.filter(only_audio=True):
                    quality.append(f"{i.abr} ({(i.filesize//1024)//1024}MB)")
                
                self.gui_obj['res.l'] = Label(self.window,anchor=W,text="Audio Quality :",fg="white",bg=self.COLORS[0],font=("arial",14,"bold"),wraplength=460)
                
                if self.THEAMS=="night":
                    self.gui_obj['res.l'].config(bg=self.COLORS[0],fg="white")
                elif self.THEAMS=="light":
                    self.gui_obj['res.l'].config(bg=self.COLORS[8],fg="black")
                
                self.gui_obj['res.l'].place(x=200,y=380,width=130)

                self.data_obj['res'] = StringVar()
                self.data_obj['res'].set(quality[1])
                self.gui_obj['res.e'] = ttk.OptionMenu(self.window,self.data_obj['res'],*quality)
                self.gui_obj['res.e'].place(x=340,y=380,width=140,height=30)

                ####====== Download Button
                self.gui_obj['download.btn'] = Button(self.window,text="Download Video",bg="#009025",activebackground="#009025",highlightbackground="#009025",highlightcolor="#009025")
                self.gui_obj['download.btn'].config(fg="white",font=("arial",15,"bold"),relief=FLAT,bd=0,activeforeground="white")
                self.gui_obj['download.btn'].config(command=lambda:th.Thread(target=self.Download_Video).start())
                self.gui_obj['download.btn'].place(x=50,y=430,height=30,width=400)

                self.gui_obj['progress'].place_forget()

        self.gui_obj['option.l'] = Label(self.window,anchor=W,text="Select :",fg="white",bg=self.COLORS[0],font=("arial",14,"bold"),wraplength=460)
        
        if self.THEAMS=="night":
            self.gui_obj['option.l'].config(bg=self.COLORS[0])
        elif self.THEAMS=="light":
            self.gui_obj['option.l'].config(bg=self.COLORS[8])
        
        self.gui_obj['option.l'].place(x=10,y=380,width=70)

        options = ['','Audio','Video']
        self.data_obj['option'] = StringVar()
        self.data_obj['option'].set(options[1])

        self.gui_obj['option.e'] = ttk.OptionMenu(self.window,self.data_obj['option'],*options,command=lambda event=None:th.Thread(target=Fetch_Options).start())
        self.gui_obj['option.e'].place(x=90,y=380,width=100,height=30)

        Fetch_Options()

    ####===========[ Showiing Downloading Progress Function ]===========####
    def on_progress(self,stream,chuck,bytes_remaining):
        total = stream.filesize
        bytes_downloaded = total - bytes_remaining
        percentage = bytes_downloaded / total * 100
        
        self.gui_obj['progress']['value'] += int(percentage) - self.gui_obj['progress']['value']
        self.data_obj['info'].set(f"{int(percentage)}%")

        if self.gui_obj['progress']['value'] == 100:
            msg.showerror("Downloaded File","File is Sucessfully Downloaded...")
            self.gui_obj['progress'].place_forget()
            self.gui_obj['info.l'].place_forget()

    ####===========[ Downloading Video Function ]===========####
    def Download_Video(self):
        os.system("clear")
        self.gui_obj['info.l'].place_forget()
        path = fd.askdirectory()
        
        if len(path)==0:
            return
        
        self.gui_obj['progress'].config(mode='determinate')
        self.gui_obj['progress'].stop()
        self.gui_obj['progress'].place(x=self.WIDTH/2-200,y=self.HEIGHT-70)
        self.gui_obj['info.l'].place(x=0,y=self.HEIGHT-30,width=500,height=30)

        if self.THEAMS=="light":
            self.gui_obj['info.l'].config(fg="black")
        else:
            self.gui_obj['info.l'].config(fg="white")    

        try:
            quality = self.data_obj['res'].get().split(" ")[0]
            print(quality)
            if self.data_obj['option'].get()=="Video":
                self.yt.register_on_progress_callback(self.on_progress)
                self.yt.streams.filter(res=quality).first().download(f"{path}")

            elif self.data_obj['option'].get()=="Audio":
                self.yt.register_on_progress_callback(self.on_progress)
                self.yt.streams.filter(abr=quality).first().download(f"{path}")
                
        except Exception as e:
            self.gui_obj['progress'].place_forget()

# https://youtu.be/KTkuTqltHZs
# https://youtu.be/5fbm5GP_0Ds
# https://youtu.be/5qo4-D4Mn3E
# https://youtu.be/2nNOmXTH54c
# https://youtu.be/xgcLwtGlgLU

window = Tk()
window.resizable(0,0)
main(window)
window.mainloop()