
def main():
    if sys.argv[1] == 'crawler':
        crawl()
    elif sys.argv[1] == 'push':
        push(int(sys.argv[2]) , int(sys.argv[3]))
    elif sys.argv[1] == 'popular':
        popular(int(sys.argv[2]), int(sys.argv[3]))
    elif sys.argv[1] == 'keyword':
        keyword(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    else:
        print("Argument Error")

def crawl():
    f_all = open('all_articles.txt', 'w')
    f_pop = open('all_popular.txt', 'w')
    flag = False
    temp = '12/31'
    url = "https://www.ptt.cc/bbs/Beauty/index2000.html"
    while True:
        response = requests.get(url)
        content = response.text

        soup = BeautifulSoup(content, 'html.parser')
        url = 'https://www.ptt.cc/bbs/Beauty/' + re.search('index[0-9]+.html',str(soup.find_all('a', 'btn wide')[2])).group(0)

        for post in soup.find_all('div', 'r-ent'):

            datetime = re.sub('/', '', re.search('[0-9]+/[0-9]+', str(post.find_all('div', 'date')[0])).group(0))

            if datetime == '101' and datetime < temp:
                if flag is False:
                    flag = True
                else:
                    break
            temp = datetime

            if post.find('a') is not None and post.find('a').string is not None and flag is True:
                title = post.find('a').string

                href = re.search('/.*html', str(post.find_all('a')[0])).group(0)

                boom = post.find_all('span')

                if boom and not '公告' in title:
                    if re.sub('<.*?>', '', str(boom[0])) == '爆':
                        f_pop.write(datetime + ',' + title + ',https://www.ptt.cc' + href + '\n')
                        #print('boom~~~~~~~~~~~~~~~~')
                if not '公告' in title:
                    f_all.write(datetime + ',' + title + ',https://www.ptt.cc' + href + '\n')

                print(datetime + ',' + title + ',https://www.ptt.cc' + href)

        if datetime == '101' and datetime < temp:  # condition :
            break

    f_all.close()
    f_pop.close()

def push (start , end):
    d_like={}
    d_boo={}
    like=0
    boo=0
    f = open('all_articles.txt', 'r')
    f_push = open('push['+str(start)+'-'+str(end)+'].txt','w')
    while True:

        line = f.readline()
        data = re.split(',',line)

        while int(data[0]) < start :
            line = f.readline()
            data = re.split(',', line)
        if int(data[0]) > end :
            break
        #print(data)
        in_url = (data[2])[0:-1]

        response = requests.get(in_url)
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        push = soup.find_all (class_="push")

        for i in push:
            id = re.sub('<.*?>', '', i.find(class_="f3 hl push-userid").string)
            if '推' in str(i):
                like+=1
                if d_like.get(id) is None:
                    d_like[id]=1
                else:
                    d_like[id]+=1
            elif '噓' in str(i):
                boo+=1
                if d_boo.get(id) is None:
                    d_boo[id]=1
                else:
                    d_boo[id]+=1

    #print(like)
    #print(boo)
    f_push.write('all like: '+str(like)+'\n')
    f_push.write('all boo: ' +str(boo)+'\n')
    i=0
    for w in sorted(d_like, key=d_like.get, reverse=True)[0:9]:
        i+=1
        print (w, d_like[w])
        f_push.write('like #'+str(i)+': '+w+' '+str(d_like[w])+'\n')
        if i==10:
            break
    i=0
    for w in sorted(d_boo, key=d_boo.get, reverse=True)[0:9]:
        i+=1
        #print(w, d_boo[w])
        f_push.write('boo #' + str(i) + ': ' + w + ' ' + str(d_boo[w])+'\n')
        if i == 10:
            break

    f_push.close()
    f.close()


def popular(start , end):
    f = open('all_popular.txt', 'r')
    f_pop = open('popular['+str(start)+'-'+str(end)+'].txt','w')
    img =[];
    count = 0
    while True:

        line = f.readline()
        data = re.split(',',line)

        while int(data[0]) < start :
            line = f.readline()
            data = re.split(',', line)
        if int(data[0]) > end :
            break

        count+=1
        in_url = re.search('https://.*html', line).group(0)

        response = requests.get(in_url)
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        text = re.sub('<.*?>', '', str(soup.find_all('div', 'bbs-screen bbs-content')[0]))
        url=re.finditer('http.*(jpg|JPG|jpeg|JPEG|gif|GIF|png|PNG)',text)
        #print(in_url)

        for i in url:
            #print(i.group(0))
            img.append(i.group(0))

    f_pop.write('number of popular articles: ' + str(count)+'\n')
    for i in img:
        f_pop.write(i+'\n')
    f_pop.close()

def keyword(keyword , start , end):
    f = open('all_articles.txt', 'r')
    f_key = open('keyword('+keyword+')['+str(start)+'-'+str(end)+'].txt','w')
    while True:

        line = f.readline()
        data = re.split(',',line)
        while int(data[0]) < start :
            line = f.readline()
            data = re.split(',', line)
        if int(data[0]) > end :
            break
        #print(data)
        in_url = re.search('https://.*html',line).group(0)

        response = requests.get(in_url)
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        text = re.sub('<.*?>', '', str(soup.find_all('div', 'bbs-screen bbs-content')[0]))
        print(in_url)
        #print(re.split('--',text)[0])
        if keyword in re.split('--',text)[0]:
            url = re.finditer('http.*(jpg|JPG|jpeg|JPEG|gif|GIF|png|PNG)', text)
            for i in url:
                f_key.write(i.group(0)+'\n')

    f_key.close()



if __name__ == '__main__':
    import requests
    from bs4 import BeautifulSoup
    import re
    import sys
    main()


