db = DAL('sqlite://storage.sqlite')
from gluon.tools import *
service = Service()
crud = Crud(db)


db.define_table('page',
                Field('title'),
                Field('created_on', 'datetime', default=request.now),
                Field('modified_on', 'datetime', default=request.now))
                
                
#db.define_table('section',
#                Field('title'),
#                Field('previous_page', db.page),
#                Field('next_page', db.page),
#                Field('parent_page', db.page),
#                format='%(title)s')
                             
                
db.define_table('text_box',
                Field('page_id', db.page),     
                Field('body', 'text'),
                Field('position_x', 'double', default='2'),  
                Field('position_y', 'double', default='2'),      
                Field('width', 'double', default='9'),      
                Field('height', 'double', default='2'),         
                Field('created_on', 'datetime', default=request.now),
                Field('modified_on', 'datetime', default=request.now))
                
#db.page.created_on.readable = db.page.created_on.writable = False
#db.page.modified_on.readable = db.page.modified_on.writable = False

db.text_box.page_id.readable = db.text_box.page_id.writable = False
db.text_box.created_on.readable = db.text_box.created_on.writable = False
db.text_box.modified_on.readable = db.text_box.modified_on.writable = False
