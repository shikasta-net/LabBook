
import thumbnail

def section():

	parent = request.vars['parent']
	if not parent :
		parent = 'root'

	if get_preference('useLocalMathJax') :
		mathjax_URL = URL('static/js', 'MathJax/MathJax.js')+'?config=TeX-AMS-MML_HTMLorMML'
	else :
		mathjax_URL = 'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'


	return dict(layout=[dict(id='root', page_id='', parent_id='', title='Contents', contains=treeLayout(None))], parent=parent, mathjax_URL=mathjax_URL)





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


def treeLayout(branch):

	contents = []

	leaves = get_branch(branch)

	for leaf in leaves :
		node = dict()
		node['id'] = leaf.id
		if leaf.page_id :
			node['page_id'] = leaf.page_id
			if leaf.parent_object :
				node['parent_id'] = leaf.parent_object.id
			else :
				node['parent_id'] = None
			node['title'] = get_page(leaf.page_id).title
			node['contains'] = None
		else :
			children = treeLayout(leaf.id)
			node['page_id'] = children[0]['page_id']
			node['parent_id'] = leaf.id
			node['title'] = children[0]['title']
			node['contains'] = children

		contents.append(node)

	return contents



def sectionContent(sec):

	contents = []

	leaves = get_branch(sec)

	for leaf in leaves :
		if leaf.page_id :
			entry = get_page(leaf.page_id), None
		else :
			children = sectionContent(leaf.id)
			entry = get_page(children[0][0].id), children

		contents.append(entry)

	return contents




	#~ contents = []

	#~ for item in db(db.pages.section == sec).select():
		#~ entry = dict()
		#~ entry['id'] = item.id
		#~ entry['title'] = item.title
		#~ entry['number'] = item.number
		#~ entry['contains'] = None
		#~ entry['thumbnail'] = thumbnail.pngPath(item.id)
		#~ contents.append(entry)

	#~ for item in db(db.sections.parent == sec).select() :
		#~ entry = dict()
		#~ entry['id'] = item.id
		#~ entry['title'] = item.title
		#~ entry['number'] = item.number
		#~ entry['contains'] = sectionContent(item.id)
		#~ if entry['contains'] :
			#~ frontpage = thumbnail.pngPath(entry['contains'][0]['id'])
		#~ else :
			#~ frontpage = URL('static/images','sec'+str(entry['number'])+'.svg')
		#~ entry['thumbnail'] = frontpage
		#~ contents.append(entry)

	#~ return sorted(contents, key=lambda pg: pg['number'])
