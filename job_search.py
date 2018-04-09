import urllib2,urllib
import re
import json


cache_list=[]

def request(url,data):
    req = urllib2.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36")

    data=urllib.urlencode(data)
    req.add_data(data)
    response = urllib2.urlopen(req)
    return response.read()
    
def match_results(regex,content):
    pattern = re.compile(regex)
    return re.findall(pattern,content)

def search(param):
    
    cache=filter(lambda c: c['key'] == param,cache_list)
    if(len(cache)>0):
        return cache[0]["result"]
    
    url="http://www.jobsnepal.com/simple-job-search"
    content = request(url,{"Keywords":param}).replace("\n","")

    regex=r"<a class=\"job-item\"(.*?)href=\"(.*?)\" >(.*?)</a>(.*?)<td >(.*?)class=\"joblist\">(.*?)</a"
    results=match_results(regex,content)
    cache_list.append({"key":param,"result":results,'ttl':30})
    return results

while True:
    param=raw_input("Search Job:")
    if param=='exit':
        exit()
    elif param=='list':
        for rec in cache_list:
            print rec
    elif param=='clear':
        cache_list=[]
    elif param=='export':
        file=raw_input("Enter file name:")
        f=open(file,"w+")
        f.write(json.dumps(cache_list))
        f.close()
    elif param=='help':
        print 'list of commands'
        print 'exit,list,clear,export'
        print 'multiple job search can be done using pipe'
        print 'for eg: php|java|.net'
    else:
        tokens=param.split("|")
        results=[]
        for token in tokens:
            results.append(search(token.strip()))

        for res in results:
            for rec in res:
                print "Title: %s" % rec[2].strip()
                print "Company: %s" %rec[5].strip()

        



