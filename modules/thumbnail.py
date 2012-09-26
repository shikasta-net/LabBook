#~ def call():
	#~ session.forget()
	#~ return service()

import os, time, Image, ImageDraw
from gluon import *

scale = 2.4  #assuming 12px per em and thumnail size of 20%

#~ @service.run
def pngPath(page_id):
	apppath = current.request.folder
	pagepath = os.path.join("static/content", str(page_id))
	save_dir = os.path.join(apppath,pagepath)
	if not os.path.isdir(save_dir) :
		os.makedirs(save_dir)
	file = "thumbnail.png"
	thmbnail = os.path.join(save_dir,file)

	#os.path.getmtime(thmbnail)
	#time.mktime(time.strptime(str(current.db(current.db.page.id==page_id).select().first().modified_on), "%Y-%m-%d %H:%M:%S"))

	#TODO top and left margins are not properly accoutned for so boxes appear offset
	if True : #os.path.getmtime(thmbnail) < time.mktime(time.strptime(str(current.db(current.db.page.id==page_id).select().first().modified_on), "%Y-%m-%d %H:%M:%S")) :
		im = Image.new("RGB",(168,120))
		draw = ImageDraw.Draw(im)
		draw.rectangle((0,0) + im.size, fill=(250,250,250))

		for box in current.db(current.db.boxes.page_id==page_id).select() :
			draw.rectangle((int(scale*box.position_x),int(scale*box.position_y),int(scale*(box.position_x + box.width)-1),int(scale*(box.position_y + box.height)-1)), outline=(0,0,0))

		im.save(thmbnail)

	return URL(pagepath, file)
