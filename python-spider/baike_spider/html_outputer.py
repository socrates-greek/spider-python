class HtmlOutputer(object):
    def __init__(self):
        self.datas = []
        
    
    def collect_data(self, data):
        
        if data is None:
            return
        
        self.datas.append(data)

    
    def output_html(self):
        fout = open('output.html', 'w', 1024, 'UTF-8')
        open
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table border = '1px'>")
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>---</td>")
            fout.write("<td>%s</td>" % data['title'])
            fout.write("<td>---</td>")
            fout.write("<td>%s</td>" % data['summary'].replace(u'\xa0', u' '))
            fout.write("</tr>")
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
    
    
    
    
