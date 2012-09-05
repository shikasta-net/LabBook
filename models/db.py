db = DAL('sqlite://storage.sqlite')
from gluon.tools import *
service = Service()
crud = Crud(db)


db.define_table('pages',
				Field('title', 'string'),
				Field('created_on', 'datetime', default=request.now),
				Field('modified_on', 'datetime', default=request.now))

#db.define_table('section',
#				Field('title'),
#				Field('previous_page', db.page),
#				Field('next_page', db.page),
#				Field('parent_page', db.page),
#				format='%(title)s')

#db.define_table('content',
#				Field('file_type', 'string'),
#				Field('file_name', 'string'),
#				Field('created_on', 'datetime', default=request.now),
#				Field('modified_on', 'datetime', default=request.now))
#
#container_box = db.define_table('container_box',
#				Field('page_id', db.page),
#				Field('content_id', db.content),
#				Field('position_x', 'double', default='1'),
#				Field('position_y', 'double', default='1'),
#				Field('width', 'double', default='1'),
#				Field('height', 'double', default='1'),
#				Field('created_on', 'datetime', default=request.now),
#				Field('modified_on', 'datetime', default=request.now))
#
#db.define_table('container_box_history', container_box, Field('cbox_id', db.container_box))
#
#db.define_table('image_box',
#				Field('page_id', db.page),
#				Field('box_id', db.container_box),
#				Field('position_x', 'double', default='1'),
#				Field('position_y', 'double', default='1'),
#				Field('width', 'double', default='1'),
#				Field('height', 'double', default='1'),
#				Field('created_on', 'datetime', default=request.now),
#				Field('modified_on', 'datetime', default=request.now))
#
#db.define_table('image_box_history', container_box, Field('ibox_id', db.image_box))

# Defines an abstract box model. Fields are self-explanatory and in units of em.
# ondelete='CASCADE' by default, which causes all referring records to be deleted on a delete
db.define_table('boxes',
				Field('page_id', 'reference pages'),
				Field('position_x', 'double', default='1'),
				Field('position_y', 'double', default='1'),
				Field('width', 'double', default='1'),
				Field('height', 'double', default='1'),
				Field('content_type', 'string', default=''),
				Field('content_id', 'string', default=''))

# Container boxes are boxes which contain content.
# unique=True ensures a one-to-one box <-> content relationship
# content_id can be null if the container box is empty. 
#db.define_table('container_boxes',
#				Field('box_id', 'reference boxes', required=True, notnull=True, unique=True),
#				Field('content_id', 'reference content', unique=True))

# Content has a type and a filename or sub box (for image boxes).
# The path to the file should be constructed from the box id, content id and filename
#db.define_table('content',
#				Field('file_type', 'string'),
#				Field('file_name', 'string'))

# Content boxes are boxes used to place content inside another
#db.define_table('content_bo

db.define_table('preferences',
				Field('preference', unique=True),
				Field('value', 'string'),
				Field('type', 'string'),
				format='%(preference)s')

# HTML id is 'box' + db id number - ignore the 'box' bit
def html_id_to_db_id(html_id):
	try:
	   db_id = int(html_id[3:])
	   box = db(db.boxes.id==db_id).select()
	   assert box != None
	except Exception, e:
	   raise HTTP(400, 'Malformed box ID: %s' % e)
	return db_id

# Raise exception on malformed page_id
def check_page_id(page_id):
    try:
        assert db(db.pages.id == page_id).count() != 0
    except Exception, e:
        raise HTTP(400, 'Malformed page ID: %s' % e)


#db.page.created_on.readable = db.page.created_on.writable = False
#db.page.modified_on.readable = db.page.modified_on.writable = False

#db.container_box.page_id.readable = db.container_box.page_id.writable = False
#db.container_box.content_id.readable = db.container_box.content_id.writable = False
#db.container_box.created_on.readable = db.container_box.created_on.writable = False
#db.container_box.modified_on.readable = db.container_box.modified_on.writable = False
#
#db.image_box.page_id.readable = db.image_box.page_id.writable = False
#db.image_box.box_id.readable = db.image_box.box_id.writable = False
#db.image_box.created_on.readable = db.image_box.created_on.writable = False
#db.image_box.modified_on.readable = db.image_box.modified_on.writable = False
#
#db.content.created_on.readable = db.content.created_on.writable = False
#db.content.modified_on.readable = db.content.modified_on.writable = False
