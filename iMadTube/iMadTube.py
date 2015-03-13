# coding:utf-8
# V 1
# by Imad-kh
import json,urllib2,urllib,webbrowser,os,tkFont,subprocess,datetime,cStringIO
import tkMessageBox
import re,time
from Tkinter import *
import ttk,D,threading
from PIL import Image,ImageTk
import icon_

pattern = "v=([^\s&]+)"
placeholder = "Enter the Video Link HERE !!!"
qualities ={5 : 'Low Quality, 240p, FLV, 400x240',
    17 : 'Low Quality, 144p, 3GP, 176×144',
    18 : 'Medium Quality, 360p, MP4, 480x360',
    22 : 'High Quality, 720p, MP4, 1280x720',
    34 : 'Medium Quality, 360p, FLV, 640x360',
    35 : 'Standard Definition, 480p, FLV, 854x480',
    36 : 'Low Quality, 240p, 3GP, 320×240',
    37 : 'Full High Quality, 1080p, MP4, 1920x1080',
    38 : 'Original Definition, MP4, 4096x3072',
    43 : 'Medium Quality, 360p, WebM, 640x360',
    44 : 'Standard Definition, 480p, WebM, 854x480',
    45 : 'High Quality, 720p, WebM, 1280x720',
    46 : 'Full High Quality, 1080p, WebM, 1280x720',
    82 : 'Medium Quality 3D, 360p, MP4, 640x360',
    84 : 'High Quality 3D, 720p, MP4, 1280x720',
    100 : 'Medium Quality 3D, 360p, WebM, 640x360',
    102 : 'High Quality 3D, 720p, WebM, 1280x720' }

class PDownloader():
    def __init__(self):
        self.downloads_windows_error={}
        
        self.root = Tk()
        self.root.title("iMadTube (download any youtube video !)")
        self.root.resizable(width=FALSE, height=FALSE)
        file = cStringIO.StringIO(icon_.icon_bas64.decode('base64'))
        img = Image.open(file)
        self.tk_image = ImageTk.PhotoImage(img)
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.tk_image)
        #self.root.iconbitmap(tk_image)
        #lab = Label(tk, text='Window with transparent icon.')
        self.mf = ttk.Frame(self.root, padding="12 12 12 12")
        self.mf.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mf.columnconfigure(0, weight=1)
        self.mf.rowconfigure(0, weight=1)
        self.url=""
        self.resF = ttk.Frame(self.root, padding="12 12 12 12",width=60,height=10)
        self.resF.grid(column=0, row=1, sticky=(N, W, E, S))
        ff = tkFont.Font(family='Helvetica',size=10, weight='bold')
        ##self.progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.msg_tst = StringVar()
        self.radioVar = StringVar()
        
        
        self.pattern = StringVar()
        self.status = StringVar()
        self.title = StringVar()
        #self.status.set("success ! ");
        #self.chkbx = StringVar()
        self.pattern.set(placeholder)
        self.pattern.set("https://www.youtube.com/watch?v=450p7goxZqg")
        
        
        self.patt_Etr = ttk.Entry(self.mf, width=50 ,textvariable=self.pattern)
        self.button_go = ttk.Button(self.mf, width=10,text="Start" ,command = self.getUrls)
        self.Label_status = ttk.Label(self.resF, width=60,textvariable=self.status,font=ff)
        self.Label_title = ttk.Label(self.resF, width=60,textvariable=self.title,font=ff)
        self.Label_img = ttk.Label(self.resF, width=60,borderwidth=1)
        self.downloadIt = ttk.Button(self.resF, width=70,text="Download Now !",command = self.Download)
        #self.checkB_force = ttk.Checkbutton(self.mf, width=8,variable=self.chkbx,text="Forced")

        self.patt_Etr.bind("<FocusIn>", self.pkname)
        
        self.patt_Etr.grid(column=0, row=0, columnspan=9)
        
        self.button_go.grid(column=12, row=0, columnspan=2)
        self.Label_status.grid(column=0, row=100, columnspan=13)
        self.Label_title.grid(column=0, row=1, columnspan=13)
        self.Label_img.grid(column=0, row=0, columnspan=13)
        self.downloadIt.grid(column=0, row=99, columnspan=13)
        self.downloadIt.state(statespec=('active', 'disabled'))

    def run(self):
        self.tkloop()
        mainloop()
    def tkloop(self):
        try:
            #print self.downloads_windows_error
            if self.downloads_windows_error and len(self.downloads_windows_error) >0:
                for t,d in self.downloads_windows_error.items():
                    if d and d.error:
                        tkMessageBox.showerror(d.filename.get(),"%s"%d.error,parent=t)
                        del self.downloads_windows_error[t]
                        del d
                        t.destroy()
                    elif d and d.status and d.status == 1 :
                        tkMessageBox.showinfo(d.filename.get(),"Download Completed !!",parent=t)
                        del self.downloads_windows_error[t]
                        del d
                        t.destroy()
                    elif d and d.status and d.status == -1 :
                        tkMessageBox.showinfo(d.filename.get(),"Download Canceled !!",parent=t)
                        del self.downloads_windows_error[t]
                        del d
                        t.destroy()
        except Exception,e:
            self.log(e)
        self.root.after(100, self.tkloop)
    def getUrls(self):
        if not self.pattern.get()=="":
            try:
                id = re.findall(pattern,self.pattern.get())[0]
            except Exception,e:
                tkMessageBox.showinfo("Error","Invalide url ,please check it!",parent=self.root)
                return -1
            
            try:
                urls = D.getURLS(id)
                if isinstance(urls,unicode) :
                    tkMessageBox.showinfo("Error",urls.split("<")[0].replace("+"," "),parent=self.root)
                    return 0
            except KeyError:
                tkMessageBox.showinfo("Error","Can't download this video, pls try with another video !",parent=self.root)
                self.pattern.set(placeholder)
                return 0
            self.loadImg(urls[0]["iurlmq"])

            self.urls_units = []
            title = urls[0]["title"]
            ##print title

            #title_short = title[:50]
            row_var = 3
            print self.title
                
            self.title.set(title.replace("+"," "))
            
            for url in urls[1] :
                #print url
                #title_short = title_short.replace("+"," ")
                quality = qualities[int(url["itag"])]
                self.urls_units.append(ttk.Radiobutton(self.resF, width=60,variable=self.radioVar,value=url['url'],text=quality,command=self.select).grid(column=0, row=row_var, columnspan=13))
                #self.urls_units 
                row_var+=1
            #self.Label_msg = ttk.Label(self.mf, width=60,textvariable=self.msg,font=ff)
            #print urls
    def select(self):
        self.url_to_download = str(self.radioVar.get())
        if self.url_to_download!="" :
            self.downloadIt.state(statespec=('active', '!disabled'))
    def Download(self):
        self.create_window()
    def pkname(self,v):
        if self.pattern.get()==placeholder:
            self.pattern.set("")
    
    def create_window(self):
        #self.counter += 1
        #print "aa"
        try:
            itag = re.findall("itag=([0-9]+)&",self.url_to_download)[0]
            ext = qualities[int(itag)].split(", ")[2].lower().replace(" ","")
            title = "%s.%s"%(self.title.get(),ext)
            t = Toplevel()
            t.wm_title(title)
            t.protocol('WM_DELETE_WINDOW', lambda: self.OnDownloadClose(t,d))
            t.tk.call('wm', 'iconphoto', t._w, self.tk_image)
            filename = StringVar()

            speed_downloaded_total = StringVar()

            lbl_filename = ttk.Label(t, width=60,textvariable=filename)
            lbl_filename_lb =                ttk.Label(t, width=15,text = "File Name  :")
            lbl_url =                        ttk.Label(t, width=15,text = "URL        :")
            lbl_speed_downloaded_total_lbl = ttk.Label(t, width=15,text = "speed      :")
            ent_url = ttk.Entry(t, width=60)
            ent_url.insert(INSERT, self.url_to_download)
            lbl_speed_downloaded_total = ttk.Label(t,textvariable=speed_downloaded_total)
            progress = ttk.Progressbar(t, orient="horizontal", length=500, mode="determinate")
                        
            d = D.Downloader(title,self.url_to_download,progress)##
            d.set_txt_vars(speed_downloaded_total,filename)##
            self.downloads_windows_error[t]=d
            
            btn_cancel = ttk.Button(t, width=10,text="cancel" ,command = d.cancel)
            btn_pause_play = ttk.Button(t, width=10,text="pause/play" ,command = d.pause_play)
            btn_play_vid = ttk.Button(t, width=10,text="Play Video" , command= lambda: self.play_vid(filename))
            
            ## command= lambda: action(someNumber)
            progress.grid(column=0, row=5, columnspan=10)
            btn_pause_play.grid(column=3, row=6, columnspan=2)
            btn_cancel.grid(column=5, row=6, columnspan=2)
            ##os.system("start "+filename)
            btn_play_vid.grid(column=4, row=6, columnspan=2)
            
            lbl_filename_lb.grid(column=0, row=2,columnspan=2)
            lbl_url.grid(column=0, row=4,columnspan=2)
            lbl_speed_downloaded_total_lbl.grid(column=0, row=3,columnspan=2)
            lbl_filename.grid(column=2, row=2,columnspan=6)
            ent_url.grid(column=2, row=4, columnspan=6)
            lbl_speed_downloaded_total.grid(column=2, row=3, columnspan=6)
            #print title
            ##d.startDownload()
            ##progress["value"]=10
            th = threading.Thread(target=d.startDownload)
            th.daemon = True
            th.start()
            
        except Exception,e:
            self.log(e)
            tkMessageBox.showinfo("Error while Downloading","%s"%e)
        #l.pack(side="top", fill="both", expand=True, padx=100, pady=100)
    def play_vid(self,filename):
        #try:
        current_path = os.getcwd()
        file = u"""\"%s\%s\""""%(current_path,filename.get())
        os.startfile(file)
        #except Exception,e:
        #    print e
        #    print file
    def OnDownloadClose(self,t,d):
        d.cancel()
        #t.destroy()
    def loadImg(self,url_img):
        try:
            file = cStringIO.StringIO(urllib.urlopen(url_img).read())
            img = Image.open(file)
            tk_image = ImageTk.PhotoImage(img)
            self.Label_img["image"]=tk_image
            #self.Label_img.configure(image = tk_image)
            self.Label_img.image = tk_image
        except Exception,e:
            print e
    def log(self,msg):
        print msg
        try:
            with open("log","a") as f:
                msg_ = "%s %s"%(datetime.datetime.today().strftime('[%Y-%m-%d %H:%M:%S]'),msg)
                f.write(msg_)
                f.write("\n")
            print msg
        except Exception,e:
            print e
    def __del__(self):
        print "here"
pd = PDownloader()

pd.run()