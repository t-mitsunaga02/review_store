import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
import time
import datetime
import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import re
import os
import math
 
class Scrape():
 
    def __init__(self,wait=1,max=None):
        self.response = None
        self.df = pd.DataFrame()
        self.wait = wait
        self.max = max
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
        self.timeout = 5
 
    def request(self,url,wait=None,max=None,console=True):
        '''
        指定したURLからページを取得する。
        取得後にwaitで指定された秒数だけ待機する。
        max が指定された場合、waitが最小値、maxが最大値の間でランダムに待機する。
 
        Params
        ---------------------
        url:str
            URL
        wait:int
            ウェイト秒
        max:int
            ウェイト秒の最大値
        console:bool
            状況をコンソール出力するか
        Returns
        ---------------------
        soup:BeautifulSoupの戻り値
        '''
        self.wait = self.wait if wait is None else wait
        self.max = self.max if max is None else max
 
        start = time.time()     
        response = requests.get(url,headers=self.headers,timeout = self.timeout)
        time.sleep(random.randint(self.wait,self.wait if self.max is None else self.max))
        
        if console:
            tm = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            lap = time.time() - start
            print(f'{tm} : {url}  経過時間 : {lap:.3f} 秒')
 
        return BeautifulSoup(response.content, "html.parser")
      
    def get_href(self,soup,contains = None):
        '''
        soupの中からアンカータグを検索し、空でないurlをリストで返す
        containsが指定された場合、更にその文字列が含まれるurlだけを返す
 
        Params
        ---------------------
        soup:str
            BeautifulSoupの戻り値
        contains:str
            抽出条件となる文字列            
 
        Returns
        ---------------------
        return :[str]
            条件を満たすurlのリスト
        '''
        urls = list(set([url.get('href') for url in soup.find_all('a')]))
        if contains is not None:
           return [url for url in urls if self.contains(url,contains)]
        return [url for url in urls if urls is not None or urls.strip() != '']
 
    def get_src(self,soup,contains = None):
        '''
        soupの中からimgタグを検索し、空でないsrcをリストで返す
        containsが指定された場合、更にその文字列が含まれるurlだけを返す
 
        Params
        ---------------------
        soup:str
            BeautifulSoupの戻り値
        contains:str
            抽出条件となる文字列            
 
        Returns
        ---------------------
        return :[str]
            条件を満たすurlのリスト
        '''
        urls = list(set([url.get('src') for url in soup.find_all('img')]))
        if contains is not None:
           return [url for url in urls if contains(url,self.contains)]
        return [url for url in urls if urls is not None or urls.strip() != '']
 
    def contains(self,line,kwd):
        '''
        line に kwd が含まれているかチェックする。
        line が None か '' の場合、或いは kwd が None 又は '' の場合は Trueを返す。
 
        Params
        ---------------------      
        line:str
            HTMLの文字列
        contains:str
            抽出条件となる文字列            
 
        Returns
        ---------------------
        return :[str]
            条件を満たすurlのリスト
        '''
        if line is None or line.strip() == '':
            return False
        if kwd is None or kwd == '':
            return True
        return kwd in line 
    
       
    def omit_char(self,values,omits):
        '''
        リストで指定した文字、又は文字列を削除する
 
        Params
        ---------------------      
        values:str
            対象文字列
        omits:str
            削除したい文字、又は文字列            
 
        Returns
        ---------------------
        return :str
            不要な文字を削除した文字列
        '''
        for n in range(len(values)):
            for omit in omits:
                values[n] = values[n].replace(omit,'')
        return values
    """
    def create_df(self,columnslist):

        df = pd.DataFrame(columns=columnslist)
        #df.to_csv("/content/価格com口コミ.csv")
        #print(df)

    def append_df(self,values,omits = None):
        df = df.append(pd.DataFrame([values], ignore_index=True))
    """
    """
    def add_df(self,values,omits = None):
        '''
        指定した値を　DataFrame に行として追加する
        omits に削除したい文字列をリストで指定可能
 
        Params
        ---------------------      
        values:[str]
            列名
        omits:[str]
            削除したい文字、又は文字列            
        '''
        if omits is not None:
            values = self.omit_char(values,omits)
            #columns = self.omit_char(columns,omits)
        
        df = pd.DataFrame(values)
        self.df = pd.concat([self.df,df.T])

    """
    
    def add_df(self,values,columns,omits = None):
        '''
        指定した値を　DataFrame に行として追加する
        omits に削除したい文字列をリストで指定可能
 
        Params
        ---------------------      
        values:[str]
            列名
        omits:[str]
            削除したい文字、又は文字列            
        '''
        if omits is not None:
            values = self.omit_char(values,omits)
            columns = self.omit_char(columns,omits)
        
        df = pd.DataFrame(values,index=self.rename_column(columns))
        self.df = pd.concat([self.df,df.T])
    
    def to_csv(self,filename,dropcolumns=None):
        '''
        DataFrame をCSVとして出力する
        dropcolumns に削除したい列をリストで指定可能
 
        Params
        ---------------------      
        filename:str
            ファイル名
        dropcolumns:[str]
            削除したい列名            
        '''
        if dropcolumns is not None:
            self.df.drop(dropcolumns,axis=1,inplace=True) 
        
        is_file = os.path.isfile(filename)
        if is_file:
          self.df.to_csv(filename,encoding="shift-jis",errors="ignore",mode='a',header=False,index=False)
        else:
          self.df.to_csv(filename,encoding="shift-jis",errors="ignore",mode='a',index=False)
    
    def get_text(self,soup):
        '''
        渡された soup が Noneでなければ textプロパティの値を返す
 
        Params
        ---------------------      
        soup: bs4.element.Tag
            bs4でfindした結果の戻り値
          
        Returns
        ---------------------
        return :str
            textプロパティに格納されている文字列
        '''
 
        return ' ' if soup == None else soup.text
    
    def rename_column(self,columns):
        '''
        重複するカラム名の末尾に連番を付与し、ユニークなカラム名にする
            例 ['A','B','B',B'] → ['A','B','B_1','B_2']
 
        Params
        ---------------------      
        columns: [str]
            カラム名のリスト
          
        Returns
        ---------------------
        return :str
            重複するカラム名の末尾に連番が付与されたリスト
        '''
        lst = list(set(columns))
        for column in columns:
            dupl = columns.count(column)
            if dupl > 1:
                cnt = 0
                for n in range(0,len(columns)):
                    if columns[n] == column:
                        if cnt > 0:
                            columns[n] = f'{column}_{cnt}'
                        cnt += 1
        return columns
 
    def write_log(self,filename,message):
        '''
        指定されたファイル名にmessageを追記する。
 
        Params
        ---------------------      
        filename: str
            ファイル名
        message: str
            ファイルに追記する文字列          
        '''
        message += '\n'
        with open(filename, 'a', encoding='shift-jis') as f:
           f.write(message)
           print(message)
 
    def read_log(self,filename):
        '''
        指定されたファイル名を読み込んでリストで返す
 
        Params
        ---------------------      
        filename: str
            ファイル名
           
        Returns
        ---------------------
        return :[str]
            読み込んだ結果
        '''
        with open(filename, 'r', encoding='shift-jis') as f:
           lines = f.read()
        return lines

set_url = 'https://kakaku.com/kaden/aircon/itemlist.aspx?pdf_Spec103=1&pdf_so=r2'

pagelist = [set_url]
urllist = []

html = requests.get(set_url)
soup = BeautifulSoup(html.content, 'html.parser')

#ランキングページの「最後へ」のリンクを取得
for pages in soup.find_all('div', class_='pagenation'):
  endinfo = soup.find('li', {'class':'end'})
  endpage = endinfo.find('a')
  endpage_num = int(endpage.get('href')[-2:])

for pagecnt in range(2, endpage_num+1):
  page_url = set_url + '&pdf_pg=' + str(pagecnt)
  pagelist.append(page_url)
#print(pagelist)

for cnt in range(0, len(pagelist)):
  html2 = requests.get(pagelist[cnt])
  soup2 = BeautifulSoup(html2.content, 'html.parser')
  itemList = soup2.find(id='itemList')
  for elements in itemList.find_all(class_='tr-border'):
    for element in elements.find_all('a'):
      urls = element.get('href')
      if 'review' in urls:
        urllist.append(urls)

#モデル名から色情報を削除
def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ""
    return answer

def scrape_kakaku(url,productCnt):
    scr = Scrape(wait=2,max=5)

    #レビューのURLから商品IDの手前までを取り出す
    url = url[:url.find('#tab')]

    color = []
    reviewCnt = 1

    for n in range(1,10):
        #商品の指定ページのURLを生成
        target = url+f'?Page={n}#tab'
        print(f'get：{target}')
 
        #レビューページの取得
        soup = scr.request(target)

        priceinfo = soup.find('span', class_='priceTxt')
        price = priceinfo.text[1:]
        print(price)

        foundForDesc = soup.find('meta', attrs={'name': 'keywords'})
        content = foundForDesc.get("content")
        maininfo = content.split(',')
        product = maininfo[0]
        
        if '[' in product:
          colorinfo = soup.find('dd', class_='last')
          for cl in colorinfo.find_all('option'):
            color.append(cl.text)
          
          if 'すべて' in color:
            color.remove('すべて')

            product_nocol = longestSubstringFinder(color[0],color[1])
            product_nocol = product_nocol[:-1]
          
          else:
            r = product[:product.find('[')]
            product_nocol = r[:-3]          

          print(product_nocol)

        else:
          product_nocol = product
        
        maker = maininfo[1]
        print(product)

        specinfo = soup.find('div', class_='variInfo')
        if not specinfo:
          specinfo = soup.find('div', class_='infoBoxNoTtl')
        for rt in specinfo.find_all("span", {'class':"specLinkbtn"}):
          rt.extract()
        spec = specinfo.text.replace(' ', '')

        #年度モデル：〇〇〇〇年モデルの、〇〇〇〇年だけ取得したい
        p = r'年度モデル*:*(.*)モデル'  
        modelinfo = re.search(p, spec)

        #年度モデルの記載がある場合
        if modelinfo:
          model_year = spec[int(modelinfo.start(1)):int(modelinfo.end(1))]
          model = model_year[-5:]

        #年度モデルの記載がない場合
        else:
          #発売日を取得、空白を削除
          modelinfo = soup.find('span', class_='releaseDate')
          release_date = modelinfo.text.replace(' ', '')
          #発売日から、発売年を抽出
          release_year = int(release_date[:4])
          #７文字目が「月」（1～9月）の場合、発売年＝年度モデル
          if release_date[6] == '月':
            model = str(release_year) + "年"
          #10月～12月の場合、発売年の翌年＝年度モデル
          else:
            model = str(release_year + 1) + "年"
        print(model)

        #電源出力の取得
        spec = specinfo.text.replace(' ', '')
        p = r'電源(.*)V'
        dengeninfo = re.search(p, spec)
        if not dengeninfo:
          dengen = "不明"
        else:
          dengen = spec[int(dengeninfo.start(1))+1:int(dengeninfo.end(1))] + 'V'
        print(dengen)

        #畳数の取得
        p = r'おもに(.*)用'
        josuinfo = re.search(p, spec)
        
        if not josuinfo:
          specinfo = soup.find('ul', class_='specSelect')
          if specinfo:
            for rt in specinfo.find_all("a", href=re.compile("kakaku")):
              rt.extract()
          else:
            specinfo = "不明"

        if not specinfo == "不明":
          spec = specinfo.text
          #print(spec)
          josuinfo = re.search(p, spec)

          josu = spec[int(josuinfo.start(1)):int(josuinfo.end(1))]
        else:
          josu = specinfo
        print(josu)

        #ページ内のレビュー記事を一括取得
        reviews = soup.find_all('div',class_='revMainClmWrap')
        #ページ内のすべてと評価を一括取得
        evals = soup.find_all('div',class_='reviewBoxWtInner')
        
        print(f'レビュー数:{len(reviews)}')

        #ページ内の全てのレビューをループで取り出す
        for review,eval in zip(reviews,evals):
            #レビューのタイトルを取得
            title = scr.get_text(review.find('div',class_='reviewTitle'))
            #レビューの内容を取得
            comment = scr.get_text(review.find('p',class_='revEntryCont')).replace('<br>','')
 
            #満足度（デザイン、処理速度、グラフィック性能、拡張性、・・・・・の値を取得
            tables = eval.find_all('table')
            star = scr.get_text(tables[0].find('td'))
            date = scr.get_text(eval.find('p',class_='entryDate clearfix'))
            date = date[:date.find('日')+1]
            ths = tables[1].find_all('th')
            tds = tables[1].find_all('td')

            columns = ['productRank','reviewNo','maker','product(color)','product','year','size','power','price','date','title','comment','満足度']
            values = [productCnt,str(reviewCnt),maker,product,product_nocol,model,josu,dengen,price,date,title,comment,star] 
 
            for th,td in zip(ths,tds):
                columns.append(th.text)
                values.append(td.text)

            #DataFrameに登録
            scr.add_df(values,columns,['<br>'])

            reviewCnt += 1

        #ページ内のレビュー数が15未満なら、最後のページと判断してループを抜ける
        nextpage = soup.find('p', class_='alignC mTop15').find('a')
        #if len(reviews) < 15:
        if not nextpage:
            break

    #スクレイプ結果をCSVに出力
    scr.to_csv("C:\work\口コミ_ローデータ.csv")

for cnt in range(0,5):
  scrape_kakaku(urllist[cnt],str(cnt+1))    
    



