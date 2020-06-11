#Auther: Xiaoliuer Li
from sqlalchemy import Column, String , Integer,BIGINT,TEXT,DECIMAL,DATETIME,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
from sqlalchemy.pool import NullPool

Base = declarative_base()

cp = configparser.RawConfigParser()
cp.read("db.conf")

#主站库
main_section = cp.sections()[0]
main_host = cp.get(main_section, "host")
main_db = cp.get(main_section, "db")
main_user = cp.get(main_section, "user")
main_passwd = cp.get(main_section, "passwd")
main_port = cp.get(main_section, "port")

main_sql = 'mysql+pymysql://' + main_user + ':' + main_passwd + '@' + main_host + ':' + main_port + '/' + main_db + '?charset=utf8'
engine = create_engine(main_sql,pool_recycle=600,poolclass=NullPool)
MainDBSession = sessionmaker(bind=engine)


#采集库
spider_section = cp.sections()[1]
spider_host = cp.get(spider_section, "host")
spider_db = cp.get(spider_section, "db")
spider_user = cp.get(spider_section, "user")
spider_passwd = cp.get(spider_section, "passwd")
spider_port = cp.get(spider_section, "port")

spider_sql = 'mysql+pymysql://' + spider_user + ':' + spider_passwd + '@' + spider_host + ':' + spider_port + '/' + spider_db + '?charset=utf8'
spider_engine = create_engine(spider_sql,pool_recycle=600,poolclass=NullPool)
SpiderDBSession = sessionmaker(bind=spider_engine)

# print(SpiderDBSession
# 本地库
spider_section = cp.sections()[2]
spider_host = cp.get(spider_section, "host")
spider_db = cp.get(spider_section, "db")
spider_user = cp.get(spider_section, "user")
spider_passwd = cp.get(spider_section, "passwd")
spider_port = cp.get(spider_section, "port")
spider_sql = 'mysql+pymysql://' + spider_user + ':' + spider_passwd + '@' + spider_host + ':' + spider_port + '/' + spider_db + '?charset=utf8'
spider_engine = create_engine(spider_sql,pool_recycle=600,poolclass=NullPool)
LocalDBSession = sessionmaker(bind=spider_engine)
# print(LocalDBSession)
#
# m_ainsession = LocalDBSession()
# # sql = "INSERT INTO v_user (uid, `status`) VALUES (66666, 0)"
# sql = "SELECT *from zsjd WHERE phone = '13620062762'"
# conn = m_ainsession.execute(sql)
# result = conn.fetchall()
# print(result)
# m_ainsession.commit()
# m_ainsession.close()

