import tkinter as tk
from tkinter import ttk
import module as mod
import threading
from tkinter import filedialog
import time
from PIL import Image

win=tk.Tk()
win.geometry('512x400')

style=ttk.Style()
style.theme_use('default')
style.configure('blue.Horizontal.TProgressbar')

fnWasSet=False
times=0
filename ='./Novels.txt'
now_progressPercent=0
Img_howToUse = Image.open('NovelsGetter/howToUse.png')

def ChoosePath():
    print('选择路径')
    global fnWasSet,filename,fnWasSet
    filename = filedialog.askopenfilename()
    fnWasSet=True
    print(filename)


def GetTheNovels():
    global times,num_quantity,now_progressPercent
    num_begin_and_end = Ent_Number.get().split(' ')
    num_begin = int(num_begin_and_end[0])
    num_quantity = int(num_begin_and_end[1])-num_begin+1
    length_all = 1  
    for times in range(num_quantity):
        SourceUrl = Ent_url.get()+'/'+str(num_begin+times)+'.html'
        page = (num_begin+times)
        mod.GetSingleNovel(SourceUrl,times,filename,page)
        # length_all+=mod.GetNovelLength(SourceUrl)这用来统计字数，尚且用不着
        now_progressPercent=int((times+1)/num_quantity*100)
        with open(filename,mode='r',encoding='utf-8') as f:
            print('write in {} Done!\n{}%COMPLETED!\n已经写入{}个字符\n'.format(filename,str(now_progressPercent),int(len(f.read()))))

def UpdateProgressBar():
    global now_progressPercent
    Prg_Getting['value']=0
    while Prg_Getting['value']<100:
        # now_progressPercent=int((times)/num_quantity*100)
        Prg_Getting['value']+=(now_progressPercent-Prg_Getting['value'])/16
        # print('更新后，value={}'.format(Prg_Getting['value']))
        win.update_idletasks()
        time.sleep(0.01)
def GetStarted():
    print('Start!')
    
    Trd_GetNovels = threading.Thread(target=GetTheNovels)
    Trd_UpdateProgressBar = threading.Thread(target=UpdateProgressBar)
    print('线程创建完成')
    Trd_GetNovels.start()
    Trd_UpdateProgressBar.start()

    # Trd_GetNovels.join()
    # Trd_UpdateProgressBar.join()
    print('Done!')
    
def show_selection():
    """显示用户在下拉菜单中选择的值，但是多源网址爬取的功能不完善"""
    selection = variable.get()
    if selection == '落霞小说(www.luoxia263.com)':
        Source='https://www.luoxia263.com/'
    elif selection == '文学网(chaoxinxingjiyuan.chibaba.cn)':
        Source='https://xxxxx.chibaba.cn/'
    else:
        Source='nothing'

def changePrg():
    Prg_Getting.config(length=1000)
    Prg_Getting.place(x=32,y=400)
    win.geometry('1080x450')


variable = tk.StringVar(win)
choices = ["落霞小说(www.luoxia263.com)", "文学网(chaoxinxingjiyuan.chibaba.cn)"]
variable.trace("w", lambda name, index, mode, sv=variable: show_selection())


Lab_MainTitle = tk.Label(win,text='NovelsGetter-UI',font=('微软雅黑',20))
Lab_Description1 = tk.Label(win,text='在此键入小说编号范围\n (以空格分割)',font=('微软雅黑',13))
Ent_Number = tk.Entry(win,width=20,font=('微软雅黑',13))
Ent_Number.insert(0,'小说编号范围')
# Lab_Description2 = tk.Label(win,text='选择小说源',font=('微软雅黑',13))
# variable.set("请选择小说资源网站前缀")   # 多源网址爬取的功能不完善
Lab_Description3 = tk.Label(win,text='输入小说源网址',font=('微软雅黑',13))
Ent_url = tk.Entry(win,width=32,font=('微软雅黑',10))
Ent_url.insert(0,'一定要有斜杠啊')
But_ChoosePath = tk.Button(win,text='选择保存路径',font=('微软雅黑',13),command=ChoosePath)

# Cmb_Source = tk.OptionMenu(win, variable, *choices)
But_Get = tk.Button(win,text='开始获取',font=('微软雅黑',13),command=GetStarted)
Prg_Getting = ttk.Progressbar(win,orient='horizontal',length=200,mode='determinate',style='blue.Horizontal.TProgressbar',maximum=100)
But_LetPrgBigger = tk.Button(win,text='使进度条更显眼',command=changePrg,font=('微软雅黑',13))
But_howToUse = tk.Button(win,text='如何使用',command=lambda:Img_howToUse.show(),font=('微软雅黑',13))

Lab_MainTitle.place(x=32,y=16)
Lab_Description1.place(x=32,y=70)
Ent_Number.place(x=32,y=120)
# Lab_Description2.place(x=32,y=170)
# Cmb_Source.place(x=32,y=200)
Lab_Description3.place(x=32,y=260)
Ent_url.place(x=32,y=290)
But_ChoosePath.place(x=32,y=350)

But_Get.place(x=300,y=70)
Prg_Getting.place(x=300,y=120)
But_LetPrgBigger.place(x=300,y=170)
But_howToUse.place(x=300,y=220)

win.mainloop()
