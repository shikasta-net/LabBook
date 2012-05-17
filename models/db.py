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
                
db.define_table('content',
                Field('file_type', 'string'),
                Field('file_name', 'string'),
                Field('created_on', 'datetime', default=request.now),
                Field('modified_on', 'datetime', default=request.now))              
                                             
db.define_table('container_box',
                Field('page_id', db.page),     
                Field('content_id', db.content),
                Field('position_x', 'double', default='1'),  
                Field('position_y', 'double', default='1'),      
                Field('width', 'double', default='1'),      
                Field('height', 'double', default='1'),         
                Field('created_on', 'datetime', default=request.now),
                Field('modified_on', 'datetime', default=request.now))
                
db.define_table('image_box',
                Field('page_id', db.page),     
                Field('box_id', db.container_box),
                Field('position_x', 'double', default='1'),  
                Field('position_y', 'double', default='1'),      
                Field('width', 'double', default='1'),      
                Field('height', 'double', default='1'),         
                Field('created_on', 'datetime', default=request.now),
                Field('modified_on', 'datetime', default=request.now))
                                
#db.page.created_on.readable = db.page.created_on.writable = False
#db.page.modified_on.readable = db.page.modified_on.writable = False

db.container_box.page_id.readable = db.container_box.page_id.writable = False
db.container_box.content_id.readable = db.container_box.content_id.writable = False
db.container_box.created_on.readable = db.container_box.created_on.writable = False
db.container_box.modified_on.readable = db.container_box.modified_on.writable = False

db.image_box.page_id.readable = db.image_box.page_id.writable = False
db.image_box.box_id.readable = db.image_box.box_id.writable = False
db.image_box.created_on.readable = db.image_box.created_on.writable = False
db.image_box.modified_on.readable = db.image_box.modified_on.writable = False

db.content.created_on.readable = db.content.created_on.writable = False
db.content.modified_on.readable = db.content.modified_on.writable = False
