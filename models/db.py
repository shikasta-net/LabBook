db = DAL('sqlite://storage.sqlite')
from gluon.custom_import import track_changes; track_changes(True)
from gluon.tools import *
from gluon import current
current.db = db

service = Service()
crud = Crud(db)

db.define_table('section',
				Field('title', 'text', requires=IS_NOT_EMPTY()),
				Field('number', 'integer', requires=IS_NOT_EMPTY()),
				Field('created_on', 'datetime', default=request.now),
				Field('modified_on', 'datetime', default=request.now),
				Field('parent', 'reference section', requires=IS_NULL_OR(IS_IN_DB(db, 'section.id', 'section.title'))),
				format='%(title)s')

db.define_table('page',
				Field('title', 'text'),
				Field('number', 'integer', requires=IS_NOT_EMPTY()),
				Field('created_on', 'datetime', default=request.now),
				Field('modified_on', 'datetime', default=request.now),
				Field('section', db.section, requires=IS_NULL_OR(IS_IN_DB(db, 'section.id', 'section.title'))))

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

db.define_table('preferences',
				Field('preference', unique=True),
				Field('value', 'string'),
				Field('type', 'string'),
				format='%(preference)s')

#~ db.section.parent.requires=IS_NULL_OR(IS_IN_DB(db, db.section.id, '%(title)s'))
#~ db.section.created_on.readable = db.section.created_on.writable = False
#~ db.section.modified_on.readable = db.section.modified_on.writable = False

#~ db.page.section.requires=IS_IN_DB(db, db.section.id, '%(title)s')
#~ db.page.created_on.readable = db.page.created_on.writable = False
#~ db.page.modified_on.readable = db.page.modified_on.writable = False

#~ db.content.created_on.readable = db.content.created_on.writable = False
#~ db.content.modified_on.readable = db.content.modified_on.writable = False

#~ db.container_box.page_id.readable = db.container_box.page_id.writable = False
#~ db.container_box.content_id.readable = db.container_box.content_id.writable = False
#~ db.container_box.created_on.readable = db.container_box.created_on.writable = False
#~ db.container_box.modified_on.readable = db.container_box.modified_on.writable = False

#~ db.image_box.page_id.readable = db.image_box.page_id.writable = False
#~ db.image_box.box_id.readable = db.image_box.box_id.writable = False
#~ db.image_box.created_on.readable = db.image_box.created_on.writable = False
#~ db.image_box.modified_on.readable = db.image_box.modified_on.writable = False

