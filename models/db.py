db = DAL('sqlite://storage.sqlite')
from gluon.custom_import import track_changes; track_changes(True)
from gluon.tools import *
from gluon import current
import os, shutil
current.db = db

service = Service()
crud = Crud(db)

#db.define_table('sections',
#				Field('title', 'text', requires=IS_NOT_EMPTY()),
#				Field('number', 'integer', requires=IS_NOT_EMPTY()),
#				Field('created_on', 'datetime', default=request.now),
#				Field('modified_on', 'datetime', update=request.now),
#				Field('parent', 'reference sections', requires=IS_NULL_OR(IS_IN_DB(db, 'sections.id', 'sections.title'))),
#				format='%(title)s')

db.define_table('object_tree',
				Field('next_object', 'reference object_tree', requires=IS_NULL_OR(IS_IN_DB(db, 'object_tree.id', 'object_tree.id')), ondelete='NO ACTION'),
				Field('parent_object', 'reference object_tree', requires=IS_NULL_OR(IS_IN_DB(db, 'object_tree.id', 'object_tree.id')), ondelete='NO ACTION'),
				Field('page_id', 'reference pages', requires=IS_NULL_OR(IS_IN_DB(db, 'pages.id', 'pages.id'))),
				Field('created_on', 'datetime', default=request.now),
				Field('modified_on', 'datetime', update=request.now))

def get_parent(current):
	return db(db.object_tree.id == current).select().first().parent_object

def get_branch(parent=None):
	objects_in_branch = db(db.object_tree.parent_object == parent).select()
	ordered_objects = [None] # None is to terminate while when reaching end of section
	for object in objects_in_branch:
		temp_list = [object]
		if object.next_object is not None :
			while temp_list[-1].next_object.ALL not in ordered_objects:
				 temp_list.append(temp_list[-1].next_object.ALL)
		ordered_objects = temp_list + ordered_objects
	del ordered_objects[-1]
	return ordered_objects[::-1]


def insert_section(parent=None) :
	db.object_tree.insert(parent_object=parent)

def move_section(section_object_id, after) :
	section = db(db.object_tree.id == section_object_id).select().first()
	db(db.object_tree.next_object == section_object_id).update(next_object=section.next_object)

	new_prev_object = db(db.object_tree.id == after).select().first()
	section.update_record(next_object=new_prev_object.next_object.id)
	new_prev_object.update_record(next_object=section_object_id)

def move_page_to_section(page_id, section_id, after) :
	page_leaf = db(db.object_tree.page_id == page_id).select().first()
	db(db.object_tree.next_object == page_leaf.id).update(next_object=page_leaf.next_object)

	new_prev_object = db(db.object_tree.id == after).select().first()
	db(db.object_tree.page_id == page_id).update(parent_object=section_id, next_object=new_prev_object.next_object.id)
	new_prev_object.update_record(next_object=page_id)


def delete_section(section_id):
	children = db(db.object_tree.parent_object == section_id).select()
	for child in children :
		if child.page_id is None :
			delete_section(child.id)
		else :
			delete_page(child.page_id)
	db(db.object_tree.next_object == section_id).update(next_object=db(db.object_tree.id == section_id).next_object)
	db(db.object_tree.id == section_id).delete()



db.define_table('pages',
				Field('title', 'string'),
				Field('created_on', 'datetime', default=request.now),
				Field('modified_on', 'datetime', update=request.now))

# Raise exception on malformed page_id - can possibly be included with other page operations?
def check_page_id(page_id):
	try:
		assert db(db.pages.id == page_id).count() != 0
	except Exception, e:
		raise HTTP(400, 'Malformed page ID: %s' % page_id)

# Add a new entry to the box table
def insert_new_page(section):
	new_page_id = db.pages.insert(title='')
	new_leaf_id = db.object_tree.insert(page_id=new_id, parent_object=section)
	db((db.object_tree.parent_object == section) & (db.object_tree.next_object == None)).update(next_object=new_leaf_id)
	return new_page_id

# Return the page row object
def get_page(page_id):
	return db(db.pages.id == page_id).select().first()

def get_page_dir(page_id):
	return os.path.join(request.folder, "static/content", str(page_id))

# get page title
def get_page_title(page_id):
	return get_page(page_id).title

# Generic method to update aspects of a page
def update_page(page_id, **field_dict):
	db(db.pages.id==page_id).update(**field_dict)

def delete_page(page_id) :
	#~ page = db(db.pages.id == page_id).select().first()
	#TODO: delete page propegates surrounding tree structure
	db(db.pages.id == page_id).delete()



# Defines an abstract box model. Fields are self-explanatory and in units of em.
# ondelete='CASCADE' by default, which causes all referring records to be deleted on a delete
db.define_table('boxes',
				Field('page_id', 'reference pages'),
				Field('position_x', 'double', default='1'),
				Field('position_y', 'double', default='1'),
				Field('width', 'double', default='1'),
				Field('height', 'double', default='1'),
				Field('content_type', 'string', default=''),
				Field('content_id', 'string', default=''),
				Field('created_on', 'datetime', default=request.now),
				Field('modified_on', 'datetime', update=request.now))

# HTML id is 'box' + db id number - ignore the 'box' bit
def html_id_to_db_id(html_id):
	try:
	   db_id = int(html_id[3:])
	   box = db(db.boxes.id==db_id).select()
	   assert box != None
	except Exception, e:
	   raise HTTP(400, 'Malformed box ID: %s' % e)
	return db_id

# Return a record for a given box id
def get_box(box_db_id):
	return db(db.boxes.id == box_db_id).select().first()

# Return all box records for a given page_id
def get_boxes_on_page(page_id):
	return db(db.boxes.page_id == page_id).select()

# Update a specific box entry
def update_box(box_db_id, **field_dict):
	db(db.boxes.id == box_db_id).update(**field_dict)

# Add a new entry to the box table
def insert_new_box(page_id, x, y, w, h):
	check_page_id(page_id)
	new_id = db.boxes.insert(page_id=page_id, position_x=x, position_y=y, width=w, height=h)
	return new_id

# Delete an entry from the box table
def delete_box(db_id):
	box = db(db.boxes.id == db_id).select().first()
	if box.content_type != '':
		raise HTTP(400, 'Attempted to delete non-empty content box: %s' % db_id)
	db(db.boxes.id == db_id).delete()

# Delete content from a container and return the container to empty
def delete_content(container_id):
	content_dir = get_content_reldir(container_id)
	if os.path.isdir(content_dir) :
		shutil.rmtree(content_dir)
	update_box(container_id, content_type='', content_id='')

# Get the (application relative) path to a content directory for a box
def get_content_reldir(box_id):
	box = get_box(box_id)
	if not (box): raise KeyError('Box id %s does not exist in database' % box_id)
	return os.path.join(request.folder, "static/content", str(box.page_id), str(box_id))

# Get relative path to a particular content file
def get_content_relpath(box_id):
	box = get_box(box_id)
	if not (box):
		raise KeyError('Box id %s does not exist in database' % box_id)
	if (box.content_type == "box") or (box.content_type == None):
		raise KeyError('Box id %s has no associated file content' % box_id)
	return os.path.join(get_content_reldir(box_id), box.content_id)

#~ def get_content_dir(page_id, box_id):
	#~ return os.path.join(request.folder, get_content_reldir(page_id, box_id))

#~ def get_file_contents(page_id, box_id, content_id):
	#~ content_dir = os.path.join(os.getcwd(), get_content_dir(page_id, box_id))
	#~ f = open(os.path.join(content_dir, content_id), 'r')
	#~ return XML(f.read())

def get_file_url(page_id, box_id, content_id):
	return URL('static', '%s/%s/%s/%s' % ('content', page_id, box_id, content_id))

db.define_table('preferences',
				Field('preference', unique=True),
				Field('value', 'string'),
				Field('type', 'string'),
				format='%(preference)s')

#Function to return the value of the given preference correctly formatted
def get_preference(pref):
	row = db(db.preferences.preference == pref).select().first()

	return {'boolean': {'True': True, 'False': False}[row.value] }[row.type]
