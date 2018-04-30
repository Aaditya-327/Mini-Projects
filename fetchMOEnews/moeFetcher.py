class gov_get: 
    """Obtain news and notices from ministy of education,
    change class 'news' to other values for other ministry
    but usually its 'news' 
    """
    def __init__(self, url):
        '''Get URL in self.root and create an instance of object
        '''
        self.root = url
        
    def link_get(self, soup= True):
        '''Process the request and obtain the webpage, and check if successful.
        soup = True causes encoding as well
        '''
        print(self.root)
        temp_get = requests.get(self.root, timeout=10)
        self.get = temp_get.content
        if temp_get.status_code == 200:
            print('Successful ', end='')
            if soup: 
                self.soup = self.soup_get()
                print('& soup')
        else: print('Try again ', end='')
    
    def soup_get(self):
        '''Encode webpage using BS4 module
        '''
        self.soup = BeautifulSoup(self.get, 'html5lib')
        return self.soup
    
    def news_get(self):
        '''Obtain news and links to the page for more information
        store in self.news.
        '''
        self.news = []
        samples = self.soup.find_all('div', {'class':'news'})
        for _ in samples:
            i = _.find('a')
            self.news.append((i['href'], i.text))
        print('Process Successful')
        return self.news
    
    def process(self): 
        '''Processes everything itself.
        '''
#         time.sleep(1)
        self.link_get(soup=True)
#         time.sleep(2)        
        return self.news_get()

# --
class get_gov_files:
    '''For the self.news passed from gov_get, we obtain filenames-
    ready for download
    '''
    def __init__(self, files):
        ''' Break news to namelist and linklist
        '''
        self.namelist = [i[1] for i in files]
        self.linklist = [i[0] for i in files]
        print('Saved {} files'.format(len(self.linklist)))
    
    def filename(self, num):
        '''Obtain top "num" values of linklist,
        For each link in linklist, we search for files saved in government archives 
        and create another list of just pdf values and display nicely.
        '''
        count, self.biglist = 0, {}
        if num<= len(self.linklist):
            for _ in self.linklist[0: num]:
                temp_get = requests.get(_, timeout=10).content
#                 time.sleep(4)
                temp_soup = BeautifulSoup(temp_get, 'html5lib')
                temp_files = [_['href'] for _ in temp_soup.find_all('a') if (("http://moe.gov.np/assets/uploads/files/" in _['href']) or ('.pdf' in _['href']))]
                temp_files = list(set(temp_files))
                count += 1
                
                self.biglist[str(count-1)] = self.namelist[count-1], self.linklist[count-1], temp_files
#                 print('\nCount: {}'.format(count))
#                 print('-' *60)
#                 print('The link to news: {}'.format(self.linklist[count-1]))
#                 print('The title of news: {}'.format(self.namelist[count-1]))
#                 print('The list of pdf: '); pprint(temp_files) 
#                 print('-' *60, '\n')
                
        print('\n{} size "biglist" prepared'.format(len(self.biglist)))
        return self.biglist
    
    # --
    class Notice:
    def __init__(self, url, count= 3):
        self.count = count
        
        get_links = gov_get(url)
        get_links.process()
        data = get_links.news
        
        get_files = get_gov_files(data)
        get_files.linklist
        self.datas = get_files.filename(self.count)
        print('_'*60)
        
    def check_fold(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory); return False
        else: return True
    
    def download_file(self, url, folder):
        '''Src:
        https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
        '''
        self.check_fold(folder)
        local_filename = folder + url.split('/')[-1]
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
        return local_filename
        
    def download(self):
        today = datetime.datetime.now().strftime ("%Y-%m-%d")
        form = '''Count, Folder = {} 
                News Title: {}
                News link: {}\n\n'''
        folder = './MOE {}/Folder {}/'.format(today, '{}')
        
        self.check_fold('./MOE {}/'.format(today))
        with open('./MOE {}/News.txt'.format(today), 'w', encoding="utf-8") as txt:
            for _ in self.datas:
                temp_text = form.format(_, self.datas[_][0], self.datas[_][1])
                print(temp_text)
                pprint(self.datas[_][2])
                txt.write(temp_text)
                
                for i in self.datas[_][2]:
                    self.download_file(i, folder.format(_)) 
                    
        print('Task successively completed!')
    
    
# --

import os
import time
import datetime
import requests
from bs4 import BeautifulSoup
from pprint import pprint

# --
if __name__ == '__main__':
    string = '''
    Choose the website to download the files from:
    [1] --> http://moe.gov.np/category/scholarship-notice.html
    [2] --> http://moe.gov.np/category/notices.html

    Enter a number to download: '''

    ntcxy = None
    value = input(string)
    if value == '1':
        ntcxy = Notice('http://moe.gov.np/category/scholarship-notice.html', count=20)
        ntcxy.download()

    elif value == '2':
        ntcxy = Notice('http://moe.gov.np/category/notices.html', count=20)
        ntcxy.download()

    else: input('Input properly!')
