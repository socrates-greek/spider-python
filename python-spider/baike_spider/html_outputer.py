from spider_main import db_handler as db
from spider_main import sql_utils as slt

class HtmlOutputer(object):
    def __init__(self):
        self.datas = []
        self.dbhandler = db.Dbhandler();
        self.conn = self.dbhandler.dbconnect()
        self.sqlutil = slt.Squtils();

    
    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)
    
    def output_html(self):
        count = 0

        for data in self.datas:
            count = count+1
            if data['title'] is not None:
                self.sqlutil.insertData(self.conn,data)
        self.sqlutil.dbSelect(self.conn)
        # 关闭数据库连接
        self.dbhandler.dbclose(self.conn)

    
    
    
    
