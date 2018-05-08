class HtmlOutputer(object):
    def __init__(self):
        self.datas = []
        
    
    def collect_data(self, data):
        
        if data is None:
            return
        title = data['title']
        if "大学" in title:
            self.datas.append(data)
        if "学院" in title:
            self.datas.append(data)
        if "中学" in title:
            self.datas.append(data)
        if "学校" in title:
            self.datas.append(data)
    
    def output_html(self):
        fout = open('output.html', 'w', 1024, 'UTF-8')
        open
        fout.write("<html>")
        fout.write("<body>")
        #fout.write("<table style='border-collapse:collapse;' border='1'>")
        count = 0
        for data in self.datas:
            #fout.write("<tr>")
            #fout.write("<td>--</td>")
            count = count+1
            st = str(count)
            fout.write("<hr style='height:1px;border:none;border-top:1px solid #555555;' />")
            fout.write("<div style='width:1000px;'>%s</div>" % (data['title']))
            fout.write("<div style='width:1000px;'>%s</div>" % (data['summary_node']))
            fout.write("<div style='width:1000px;'>%s</div>" % (data['basic_node']))
            # fout.write("<td style='width:200px;'>%s</td>" % (st+'.'+data['title']))
            # fout.write("<td>--</td>")
            # fout.write("<td style='width:400px;'>%s</td>" % data['summary'].replace(u'\xa0', u' '))
            # fout.write("<td>--</td>")
            # fout.write("<td style='width:400px;'>%s</td>" % data['catalog'].replace(u'\xa0', u' '))
            # fout.write("<td>--</td>")
            # fout.write("<td style='width:400px;'>%s</td>" % data['basic-info'].replace(u'\xa0', u' '))
            # fout.write("<td style='width:500px;'>%s</td>" % data['reference'].replace(u'\xa0', u' '))
            # fout.write("</tr>")
        #fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
    
    
    
    
