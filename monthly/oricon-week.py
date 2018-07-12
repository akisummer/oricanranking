import np
import re
import pandas as pd
import requests


class oricon():


# def __init__(self, data1, data2):
#      self.data1 = data1
#      self.data2 = data2



  def monthrank(month):   

    ranks = lambda n: np.linspace(n*10-9, n*10, 10, dtype= int)
    list1 = []
    url_loc = 'https://www.oricon.co.jp/rank/js/m/' + month + '/' 
    print(url_loc)

    req1 = requests.get(url_loc)
    result1 = re.findall('<p class="status (.*?)">.*?<a href="(.*?)".*?itemprop="name">(.*?)</h2>\s*<p class="name">(.*?)</p>.*?<li>発売日：\s*(.*?)\s*</li>\s*<li>推定売上枚数：(.*?)</li>', req1.text, re.S)
    ranks1 = np.linspace(1, 10, 10, dtype= int)
    s1 = pd.DataFrame(result1, index=ranks1, columns= ["state", "href", "title", "name", "selldata", "num"])

    for i in range(2,6):
      locals()['req'+ str(i)] = requests.get(url_loc + 'p/'+ str(i) + '/')
      locals()['result'+ str(i)] = re.findall('<p class="status (.*?)">.*?<a href="(.*?)".*?itemprop="name">(.*?)</h2>\s*<p class="name">(.*?)</p>.*?<li>発売日：\s*(.*?)\s*</li>\s*<li>推定売上枚数：(.*?)</li>', locals()['req'+str(i)].text, re.S)
      locals()['result1'+str(i)] = re.findall('<p class="status (.*?)">.*?itemprop="name">(.*?)</h2>\s*<p class="name">(.*?)</p>.*?<li>発売日：\s*(.*?)\s*</li>\s*<li>推定売上枚数：(.*?)</li>', locals()['req'+str(i)].text, re.S)
   # locals()['s'+str(i)] = pd.DataFrame(locals()['result'+ str(i)], index=locals()['ranks'+str(i)], columns= ["state", "href", "title", "name", "selldata", "num"])
   # stotal = pd.concat([s1, locals()['s2'], locals()['s3'], locals()['s4'], locals()['s5']])
      if len(locals()['result'+ str(i)]) == len(locals()['result1' + str(i)]):  #some ablum do not contain detail pages
        list1.append(locals()['result'+ str(i)])
      else:
        for c in range(len(locals()['result' + str(i)])):
          if locals()['result'+ str(i)][c][2] != locals()['result1' + str(i)][c][1]:
            temp = ( locals()['result1'+ str(i)][c][0], 'nan', locals()['result1' + str(i)][c][1], locals()['result1'+ str(i)][c][2], locals()['result1'+str(i)][c][3], locals()['result1'+str(i)][c][4]) #stupid but simple,lol
            locals()['result'+ str(i)].insert(c, temp)
        list1.append(locals()['result'+str(i)])

    s2 = pd.DataFrame(list1[0], index = ranks(2), columns=["state", "href", "title", "name", "selldata", "num"])
    s3 = pd.DataFrame(list1[1], index = ranks(3), columns=["state", "href", "title", "name", "selldata", "num"])
    s4 = pd.DataFrame(list1[2], index = ranks(4), columns=["state", "href", "title", "name", "selldata", "num"])
    s5 = pd.DataFrame(list1[3], index = ranks(5), columns=["state", "href", "title", "name", "selldata", "num"])
    s = pd.concat([s1, s2, s3, s4, s5])  #seems tedious, but i have no good idea to handle them right now.
    return s



  def musicdetails(href): 

    list2 = []
    for i in range(1,51): 
      if href[i] != 'nan':
        locals()['tmp' + str(i)] = requests.get( 'https://www.oricon.co.jp' + href[i]) 
        locals()['res1' + str(i)] = re.findall('music-title">[0-9].(.*?)</div>', locals()['tmp' + str(i)].text, re.S)
        locals()['res2' + str(i)] = re.findall('composition-info-content">(.*?)</', locals()['tmp' + str(i)].text, re.S)
      else:
        locals()['res1' + str(i)] = ['nan']
        locals()['res2' + str(i)] = ['nan', 'nan', 'nan', 'nan', 'nan', 'nan']
     # locals()['num' + str(i)] = locals()['tmp' + str(i)].text.count('music-title')
     # locals()['rks' + str(i)] = np.linspace(1, locals()['num' + str(i)], locals()['num' + str(i)], dtype= int)
     # locals()['ss1' + str(i)] = pd.DataFrame(locals()['res1'+ str(i)], index=locals()['rks'+ str(i)], columns=["music"])
      if len(locals()['res2' + str(i)]) == 4:
        locals()['res2' + str(i)].insert(0, '<span>nan')
        locals()['res2' + str(i)].insert(0, '<span>nan')  #fufill two columns with '<span>nan' when the detail pages are not informed
      list2.append(np.append(np.array(locals()['res2'+ str(i)]).reshape(1, 6), locals()['res1' + str(i)][0])) 

    rank = np.linspace(1, 50 ,50, dtype=int)
    ss = pd.DataFrame(list2, index = rank, columns=["highestrank", "rankingtime", "selldata", "publisher", "PN", "price", "main"])
    return ss

#the data of month ranking can only spider from 2018-01 to 2018-06, sad
#  month = np.linspace(1, 6, 6, dtype = int)
#  for i in month:
#    if i > 9:
#      data = '2018-' + str(i)
#    else:
#      data = '2018-0' + str(i)

  month = '2018-06' #the month which you want to spider.
  s = monthrank(month)
  href = s["href"]
  ss = musicdetails(href)
#  print(s)
#  print(ss)
#    locals()['s' + str(i)] = pd.merge(s, ss.drop(["selldata"], axis=1), left_index=True, right_index=True)  #delete the repeat data
#    print(locals()['s' + str(i)])    
#      locals()['s'+ str(i)].to_excel("test.csv",index=False,sep=',')
  monthrank = pd.merge(s, ss.drop(["selldata"], axis=1), left_index=True, right_index=True)  #delete the repeat data
  monthrank.to_excel("2018-06.xls", index=False, sep=',') #output to the file, do no forget change the name.
  print(monthrank) 


