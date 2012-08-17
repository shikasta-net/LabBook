import random

def index():
	# Get root sections
	root_secs = db(db.section.parent == None).select()
	labbook = dict()
	labbook['sections'] = []
	for i, sec in enumerate(root_secs):
		section = dict()
		section['title'] = sec.title
		section['subsections'] = []
		ssecs = db(db.section.parent == sec.id).select()
		for j, ssec in enumerate(ssecs):
			subsection = dict()
			subsection['title'] = ssec.title
			subsection['id'] = 'sec' + str(ssec.id)
			subsection['colour'] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
			subsection['pages'] = []
			for pg in db(db.page.section == ssec.id).select():
				page = dict()
				page['title'] = pg.title
				page['id'] = pg.id
				page['number'] = pg.number
				
				subsection['pages'].append(page)

			section['subsections'].append(subsection)

		labbook['sections'].append(section)

	return dict(labbook=labbook)

def css():
	colours = dict()
	lengths = dict()
	for sec in db(db.section.parent == None).select():
		for ssec in db(db.section.parent == sec.id).select():
			id = 'sec' + str(ssec.id)
			colours[id] = ssec.colour
			lengths[id] = len(db(db.page.section == ssec.id).select())
	return dict(colours=colours, lengths=lengths)

