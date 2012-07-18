import random

def index():
	if not session.testdict:
		session.testdict = dict()
		session.testdict['sections'] = [dict() for a in range(random.randint(2,5))]
		for i, section in enumerate(session.testdict['sections']):
			section['title'] = 'Section ' + str(i+1)
			section['subsections'] = [dict() for a in range(random.randint(2,7))]
			for j, subsection in enumerate(section['subsections']):
				subsection['title'] = 'Subsection ' + str(j+1)
				subsection['id'] = 's'+str(i)+'ss'+str(j)
				subsection['colour'] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
				subsection['pages'] = [a for a in range(random.randint(3,20))]

	return dict(labbook=session.testdict)

def css():
	colours = dict()
	lengths = dict()
	for i, section in enumerate(session.testdict['sections']):
		for j, subsection in enumerate(section['subsections']):
			colours[subsection['id']] = subsection['colour']
			lengths[subsection['id']] = len(subsection['pages'])
	return dict(colours=colours, lengths=lengths)

