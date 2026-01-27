# langchain_community.utilities 访问MySQL数据库
from langchain_community.utilities import SQLDatabase

# 数据库配置
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'world'
USERNAME = 'root'
PASSWORD = '123456'
MYSQL_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
db = SQLDatabase.from_uri(MYSQL_URI)
print(db.get_usable_table_names())
print(db.run("select * from country limit 1"))

from langchain_community.document_loaders import WebBaseLoader