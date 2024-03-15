import requests, math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
headers = {
'Host': 'stepfordcountyrailway.co.uk',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0',
'Accept': '*/*',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding': 'gzip, deflate',
'Referer': 'https://stepfordcountyrailway.co.uk/Servers',
'authorization': open("Authorization.txt").read(),
'Alt-Used': 'stepfordcountyrailway.co.uk',
'Connection': 'keep-alive',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'TE': 'trailers'}
pg = 1
subWin = []
roleColors = {'Guards': '#ebbc25','Drivers': '#d84340', 'Passengers': '#8a889e', 'Dispatchers': '#eb842d', 'Signallers': '#12af86'}
class Subwin:
    def __init__(self, par, info):
        self.createMap(par, info)
    def createMap(self, par, info):
        self.root = Toplevel(par)
        self.root.title('Server ' + info['name'] + ' (' + info['id'] + ') - Map')
        self.cvs = Canvas(self.root, bg = '#d6dee6',  width=900, height=760)
        self.map = ImageTk.PhotoImage(Image.open("scr-22-09-01.png").resize((900, 675), Image.LANCZOS))
        self.cvs.create_image(450, 337.5, image = self.map)
        self.cvs.pack()
        self.cvs.create_rectangle(20, 690, 880, 740, fill='#eeeeee', width=0)
        x = 20
        count = 0
        for i in info['playerRoleCounts']:
            self.cvs.create_rectangle(x, 690, i['playersInRoleCount']/info['playerCount']*860 + x, 740, fill=roleColors[i['role']], width=0)
            if(i['playersInRoleCount']/info['playerCount']*860 < len(i['role'] + ': ' + str(i['playersInRoleCount'])) * 6):
                self.cvs.create_text((2 * x + i['playersInRoleCount']/info['playerCount']*860)/2, 750, text = '... ' + str(i['playersInRoleCount']))
            else:
                self.cvs.create_text((2 * x + i['playersInRoleCount']/info['playerCount']*860)/2, 750, text = i['role'] + ': ' + str(i['playersInRoleCount']))
            x += i['playersInRoleCount']/info['playerCount']*860
            count += i['playersInRoleCount']
        if info['playerCount'] - count != 0:
            self.cvs.create_text((880 + x)/2, 870, text = 'None: ' + str(info['playerCount'] - count))
        self.cvs.create_text(50, 870, text = 'Total: ' + str(info['playerCount']))
        self.root.protocol("WM_DELETE_WINDOW", lambda : self.exitEvent())
        self.createDetailedList(par, info)
        self.root.mainloop()
    def createDetailedList(self, par, info):
        self.rootb = Toplevel(par)
        self.rootb.title('Server ' + info['name'] + ' (' + info['id'] + ') - Details')
        self.fr = ttk.Frame(self.rootb, padding = '10')
        self.fr.grid()
        self.allStopping = IntVar()
        self.allStopping.set(1)
        ttk.Checkbutton(self.fr, variable = self.allStopping, text = 'Show all stopping stations', command = lambda : print(1)).grid(column=0, row=0)
        #ttk.Label(self.fr, text = 'Show all stopping stations').grid(column=1, row=0)
        self.rootb.protocol("WM_DELETE_WINDOW", lambda : self.exitEvent())
        self.rootb.mainloop()
    def exitEvent(self):
        self.root.destroy()
        self.rootb.destroy()
def details(index):
    subWin.append(Subwin(root, servers[index]))
def displayPage():
    for ele in fr.winfo_children():
        ele.destroy()
    i = (pg - 1) * 10
    j = 1
    while i < pg * 10 and i < res.json()['serverCount']:
        ttk.Label(fr, text = 'Server ' + servers[i]['name'] + ' - ' + str(servers[i]['playerCount']) + ' players').grid(column=0, row=j)
        ttk.Button(fr, text = 'Details', command = lambda i = i: details(i)).grid(column=1, row=j)
        i += 1
        j += 1
    if pg != math.ceil(res.json()['serverCount']/10) and pg != 1:
        ttk.Button(fr, text = '< ' + str(pg - 1), command = lambda : pre()).grid(column=0, row=11)
        ttk.Button(fr, text = str(pg - 1) + ' >', command = lambda : nex()).grid(column=1, row=11)
    elif pg == 1:
        ttk.Label(fr, text = 'Page ' + str(pg) + '/' + str(math.ceil(res.json()['serverCount']/10))).grid(column=0, row=11)
        if res.json()['serverCount'] > 10:
            ttk.Button(fr, text = 'Next Page', command = lambda : nex()).grid(column=1, row=11)
    else:
        ttk.Label(fr, text = 'Page ' + str(pg) + '/' + str(math.ceil(res.json()['serverCount']/10))).grid(column=1, row=11)
        ttk.Button(fr, text = 'Previous Page', command = lambda : pre()).grid(column=0, row=11)
    ttk.Label(fr, text = 'Total Servers: ' + str(res.json()['serverCount'])).grid(column=0, row=0)
    ttk.Button(fr, text = 'Refresh', command = lambda : load()).grid(column=1, row=0)
def pre():
    global pg
    pg -= 1
    displayPage()
def nex():
    global pg
    pg += 1
    displayPage()
def descending(lis):
    if lis == []: 
        return []
    lesser = descending([i for i in lis[1:] if i['playerCount'] < lis[0]['playerCount']])
    greater = descending([i for i in lis[1:] if i['playerCount'] >= lis[0]['playerCount']])
    return greater + [lis[0]] + lesser
def load():
    global res, servers
    res = requests.get('https://stepfordcountyrailway.co.uk/api/Game/Servers/Online', headers = headers)
    try:
        res.json()
    except:
        return False
    servers = descending(res.json()['servers'])
    displayPage()
    return True
root = Tk()
root.title('SCR Status')
fr = ttk.Frame(root, padding = '10')
fr.grid()
if not load():
    for ele in fr.winfo_children():
        ele.destroy()
    ttk.Label(fr, text = 'Fetch failed, try to renew Authorization').grid(column=0, row=0)
root.mainloop()
