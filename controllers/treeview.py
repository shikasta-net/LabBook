
import thumbnail

def sections():
	#returns ordered by section then number, fortuantely NONE counts at the top of the list.
	#TODO: mix the lists into a single correctly ordered list of rows to make rendering possible

	#~ layout = db().select(db.section.ALL, db.page.ALL, left=[db.section.on(db.page.section == db.section.id)], orderby=db.section.title|db.section.number|db.page.number)

	#~ Sparent = db.section.with_alias('parent')
	#~ layout = db().select(db.section.ALL, db.page.ALL, Sparent.ALL, left=(Sparent.on(db.page.section == Sparent.id), Sparent.on(db.section.parent == Sparent.id)), orderby=db.section.number)


	#~ print ''
	#~ print layout
	#~ print ''
	#~ for entry in layout :
		#~ print entry.section.title, entry.page.title

	#Hacky way of getting the list returned in a usefully ordered way.

	#~ layout = sectionContent(None)

	#~ print ''
	#~ for entry in layout :
		#~ print entry['title'], entry['contains']

	return dict(layout=sectionContent(None))


def sectionContent(sec):

	contents = []

	for item in db(db.pages.section == sec).select():
		entry = dict()
		entry['id'] = item.id
		entry['title'] = item.title
		entry['number'] = item.number
		entry['contains'] = None
		entry['thumbnail'] = thumbnail.pngPath(item.id)
		contents.append(entry)

	for item in db(db.sections.parent == sec).select() :
		entry = dict()
		entry['id'] = item.id
		entry['title'] = item.title
		entry['number'] = item.number
		entry['contains'] = sectionContent(item.id)
		if entry['contains'] :
			frontpage = thumbnail.pngPath(entry['contains'][0]['id'])
		else :
			frontpage = URL('static/images','sec'+str(entry['number'])+'.svg')
		entry['thumbnail'] = frontpage
		contents.append(entry)

	return sorted(contents, key=lambda pg: pg['number'])
