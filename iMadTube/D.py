import urllib2,urllib,json,sys,time,os,sys
import tkMessageBox
from Tkinter import TclError

url_base = "http://www.youtube.com/get_video_info?video_id="
url_base = "http://www.youtube.com/get_video_info?el=vevo&el=embedded&video_id="

def urlParserParameters(str,isu = 0):
    param = str.split("&")
    parameters ={}
    for p in param:
        pp = p.split("=")
        if isu == 1:
            parameters[pp[0]] = urllib.unquote(pp[1]).decode('utf8') if len(pp)==2 else ""
            continue
        parameters[pp[0]] = pp[1] if len(pp)==2 else ""
    return parameters
    
def getURLS(id):
    stream_info = urllib2.urlopen(url_base+id).read()
    
    parameters = urlParserParameters(stream_info)
    if parameters["status"]=="fail" :
        return urllib.unquote(parameters["reason"]).decode('utf8')
    #formats =urllib.unquote(parameters["url_encoded_fmt_stream_map"]).decode('utf8').split(",")
    formats = urllib.unquote(parameters["url_encoded_fmt_stream_map"]).decode('utf8').split(",")
    #print urlParserParameters(urllib.unquote(formats[0]).decode('utf8').split(",")[0])
    #quit()
    resultat = []
    resultat.append({})
    resultat.append([])
    resultat[0]["title"]="%s"%urllib.unquote(parameters["title"]).decode('utf8')
    resultat[0]["iurlmq"]="%s"%urllib.unquote(parameters["iurlmq"]).decode('utf8')
    i=0
    for frm in formats :
        resultat[1].append({})
        frms = urlParserParameters(frm)
        for k,v in frms.items():
            resultat[1][i][k]="%s"%urllib.unquote(v).decode('utf8')

        i+=1
    return resultat
class Downloader():
    def __init__(self,file,url,progressB):
        self.file_location_orig=file
        self.file_location=file
        self.url = str(url)
        self.CHUNK = 5 * 1024
        self.process= 0
        self.progressB = progressB
        self.to_cancel=0
        self.to_pause =0
        self.file_name_count=1
        self.filename=None
        self.speed_dd_total=None
        self.error= None
        self.status=None
    def set_txt_vars(self,speed_dd_total,filename):
        self.speed_dd_total = speed_dd_total
        self.filename=filename
    def check_existence(self):
        if os.path.isfile(self.file_location) :
            self.file_location="%s_%s.%s"%(self.file_location_orig.replace(".%s"%self.file_location_orig.split(".")[-1],""),self.file_name_count,self.file_location_orig.split(".")[-1])
            self.file_name_count= self.file_name_count +1
            self.check_existence()
        else:
            self.filename.set(self.file_location)
    def cancel(self):
        self.to_cancel=1
        print "canceled"
    def pause_play(self):
        self.to_pause = 0 if self.to_pause == 1 else 1
        print "paused/played"
    def startDownload(self):
        try:
            self.check_existence()
            #self.process=0
            req = urllib2.urlopen(self.url)
            #self.progressB["mode"]="indeterminate"
            try:
                length = req.headers["Content-Length"]
            except:
                length = -1
                self.progressB["mode"]="indeterminate"
                
            start_time = time.time()
            #print "%s:%s:%s:%s"%(dt_now1.hour,dt_now1.minute,dt_now1.second,dt_now1.microsecond)
            with open(self.file_location, 'wb') as fp:
              while True:
                if not self.filename : print "brrrrrrrrrrrrrrrrrrrrrr"
                if self.to_cancel==1 : break
                if self.to_pause==1 : 
                    time.sleep(1)
                    continue
                chunk = req.read(self.CHUNK)
                if not chunk: break
                fp.write(chunk)
                self.process += self.CHUNK
                try:
                    if length>0:
                        self.progressB["value"] = (float(self.process)/float(length))*100
                    else :
                        self.progressB["value"] = int(self.process)
                    if self.speed_dd_total :
                        self.speed_dd_total.set("total = %.2f Mo  || downloaded = %.2f Mo   ( %.2f %%)"%(float(length)/1000000,float(self.process)/1000000,float(self.process)/float(length)*100))
                except TclError:
                    break
            print"%s bytes--- %s seconds ---" % (length,time.time() - start_time)
            #print "length bytes  =>  %s:%s:%s"%(length,dt_total.minute if dt_total.minute else 0,dt_total.second if dt_total.second else 0,dt_total.microsecond)
            if self.to_cancel==0:self.status = 1
            else:self.status = -1
        except Exception,e :
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #tkMessageBox.showinfo("Error while Downloading","%s"%e)
            print(e, fname, exc_tb.tb_lineno)
            self.error = str(e)
            print self.url
            #raise (e, fname, exc_tb.tb_lineno)
        
            
#print resultat
#def getUrls(formats_str)