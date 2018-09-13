import urllib.request
class HtmlDownloader(object):
    
    def download(self, url):
        if url is None:
            return None   
        
        with urllib.request.urlopen(url) as req:
            if req.getcode() != 200:
                return None
            return req.read()




    

