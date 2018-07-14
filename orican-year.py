import re
import pandas as pd
import requests
import np

class oricanyear():

  def yearrank(year):

    url_loc = 'https://www.oricon.co.jp/rank/js/y/' + year + '/'
    ranks = lambda n: np.linspace(n*10-9, n*10, 10, dtype= int)
    list1 = []

    req1 = requests.get(url_loc)
    result1 = re.findall('box-rank-entry.*?href="(.*?)" itemprop.*?name">(.*?)</h2>.*?name">(.*?)</p>.*?<li>発売日：\s+(.*?)\s+</li>\s+<li>(.*?)\s+</li>', req1.text, re.S)
    s1 = pd.DataFrame(result1, index=ranks(1), columns= ["href", "title", "name", "selldata", "publisher"])

    for i in range(2,11):
      locals()['req'+ str(i)] = requests.get(url_loc + 'p/'+ str(i) + '/')
      locals()['result'+ str(i)] = re.findall('box-rank-entry.*?href="(.*?)" itemprop.*?name">(.*?)</h2>.*?name">(.*?)</p>.*?<li>発売日：\s+(.*?)\s+</li>\s+<li>(.*?)\s+</li>', locals()['req'+str(i)].text, re.S)
      locals()['result1'+str(i)] = re.findall('box-rank-entry.*?name">(.*?)</h2>.*?name">(.*?)</p>.*?<li>発売日：\s+(.*?)\s+</li>\s+<li>(.*?)\s+</li>', locals()['req'+str(i)].text, re.S)
      if len(locals()['result'+ str(i)]) == len(locals()['result1' + str(i)]):
        list1.append(locals()['result'+ str(i)])
      else:
        for c in range(len(locals()['result' + str(i)])):
          if locals()['result'+ str(i)][c][1] != locals()['result1' + str(i)][c][0]:
            temp = ( 'nan', locals()['result1' + str(i)][c][0], locals()['result1'+ str(i)][c][1], locals()['result1'+str(i)][c][2], locals()['result1'+str(i)][c][3])
            locals()['result'+ str(i)].insert(c, temp)
        list1.append(locals()['result'+str(i)])

    s2 = pd.DataFrame(list1[0], index = ranks(2), columns=["href", "title", "name", "selldata", "publisher"])
    s3 = pd.DataFrame(list1[1], index = ranks(3), columns=["href", "title", "name", "selldata", "publisher"])
    s4 = pd.DataFrame(list1[2], index = ranks(4), columns=["href", "title", "name", "selldata", "publisher"])
    s5 = pd.DataFrame(list1[3], index = ranks(5), columns=["href", "title", "name", "selldata", "publisher"])
    s6 = pd.DataFrame(list1[4], index = ranks(6), columns=["href", "title", "name", "selldata", "publisher"])
    s7 = pd.DataFrame(list1[5], index = ranks(7), columns=["href", "title", "name", "selldata", "publisher"])
    s8 = pd.DataFrame(list1[6], index = ranks(8), columns=["href", "title", "name", "selldata", "publisher"])
    s9 = pd.DataFrame(list1[7], index = ranks(9), columns=["href", "title", "name", "selldata", "publisher"])
    s0 = pd.DataFrame(list1[8], index = ranks(10), columns=["href", "title", "name", "selldata", "publisher"])


    s = pd.concat([s1, s2, s3, s4, s5, s6, s7, s8, s9, s0])
    return s

  def musicdetails(href):

    list2 = []
    for i in range(1,101):
      if href[i] != 'nan':
        locals()['tmp' + str(i)] = requests.get( 'https://www.oricon.co.jp' + href[i])
        locals()['res1' + str(i)] = re.findall('music-title">[0-9].(.*?)</div>', locals()['tmp' + str(i)].text, re.S)
        locals()['res2' + str(i)] = re.findall('composition-info-content">(.*?)</', locals()['tmp' + str(i)].text, re.S)
#        print(href[1])
#        print(tmp1.text)
#        print(res21)
#        print(res11)
      else:
        locals()['res1' + str(i)] = ['nan']
        locals()['res2' + str(i)] = ['nan', 'nan', 'nan', 'nan', 'nan', 'nan']
      if len(locals()['res2' + str(i)]) == 4:
        locals()['res2' + str(i)].insert(0, '<span>nan')
        locals()['res2' + str(i)].insert(0, '<span>nan')  #fufill two columns with '<span>nan' when the detail pages are not informed
      list2.append(np.append(np.array(locals()['res2'+ str(i)]).reshape(1, 6), locals()['res1' + str(i)][0]))

    rank = np.linspace(1, 100 ,100, dtype=int)
    ss = pd.DataFrame(list2, index = rank, columns=["highestrank", "rankingtime", "selldata", "publisher", "PN", "price", "main"])
    return ss

  year = '2017'
  s = yearrank(year)
  href = s["href"]
  ss = musicdetails(href)
  rankyear = pd.merge(s, ss.drop(["selldata", "publisher"], axis=1), left_index=True, right_index=True)
  print(rankyear)
