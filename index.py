import requests, math
from tkinter import *
from tkinter import ttk
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
        self.root = Toplevel(par)
        self.root.title('Server ' + info['name'] + ' (' + info['id'] + ') - Details')
        cvs = Canvas(self.root, bg = '#ffffff',  width=1200, height=675)
        cvs.pack()
        cvs.create_rectangle(20, 20, 1180, 70, fill='#eeeeee', width=0)
        x = 20
        count = 0
        for i in info['playerRoleCounts']:
            cvs.create_rectangle(x, 20, i['playersInRoleCount']/info['playerCount']*1160 + x, 70, fill=roleColors[i['role']], width=0)
            if(i['playersInRoleCount']/info['playerCount']*1160 < len(i['role'] + ': ' + str(i['playersInRoleCount'])) * 6):
                cvs.create_text((2 * x + i['playersInRoleCount']/info['playerCount']*1160)/2, 80, text = '... ' + str(i['playersInRoleCount']))
            else:
                cvs.create_text((2 * x + i['playersInRoleCount']/info['playerCount']*1160)/2, 80, text = i['role'] + ': ' + str(i['playersInRoleCount']))
            x += i['playersInRoleCount']/info['playerCount']*1160
            count += i['playersInRoleCount']
        if info['playerCount'] - count != 0:
            cvs.create_text((1180 + x)/2, 80, text = 'None: ' + str(info['playerCount'] - count))
        cvs.create_text(50, 80, text = 'Total: ' + str(info['playerCount']))
        self.root.mainloop()
def details(index):
    subWin.append(Subwin(root, servers[index]))
def displayPage():
    for ele in fr.winfo_children():
        ele.destroy()
    i = (pg - 1) * 10
    j = 1
    while i < pg * 10 and i < res.json()['serverCount']:
        ttk.Label(fr, text = 'Server ' + servers[i]['name'] + ' - ' + str(servers[i]['playerCount']) + ' players').grid(column=0, row=j)
        ttk.Button(fr, text = 'Details', command = lambda i=i: details(i)).grid(column=1, row=j)
        i += 1
        j += 1
    if pg != math.ceil(res.json()['serverCount']/10) and pg != 1:
        ttk.Button(fr, text = '< ' + str(pg - 1), command = lambda : pre()).grid(column=0, row=11)
        ttk.Button(fr, text = str(pg - 1) + ' >', command = lambda : nex()).grid(column=1, row=11)
    elif pg == 1:
        ttk.Label(fr, text = 'Page ' + str(pg) + '/' + str(math.ceil(res.json()['serverCount']/10))).grid(column=0, row=11)
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
