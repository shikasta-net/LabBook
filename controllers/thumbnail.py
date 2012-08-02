def call():
	session.forget()
	return service()

import os, time, Image, ImageDraw

scale = 2.4  #assuming 12px per em and thumnail size of 20%

@service.run
def png(page_id):
	apppath = os.path.join(os.getcwd(), request.folder)
	pagepath = os.path.join("static/content", str(page_id))
	file = "thumbnail.png"
	thmbnail = os.path.join(apppath,pagepath,file)

	#~ os.path.getmtime(thmbnail)
	#~ time.mktime(time.strptime(str(db(db.page.id==page_id).select().first().modified_on), "%Y-%m-%d %H:%M:%S"))

	#~ if os.path.getmtime(thmbnail) < time.mktime(time.strptime(str(db(db.page.id==page_id).select().first().modified_on), "%Y-%m-%d %H:%M:%S")) :
	im = Image.new("RGB",(168,120))
	draw = ImageDraw.Draw(im)
	draw.rectangle((0,0) + im.size, fill=(250,250,250))

	for box in db(db.container_box.page_id==page_id).select() :
		draw.rectangle((int(scale*box.position_x),int(scale*box.position_y),int(scale*(box.position_x + box.width)-1),int(scale*(box.position_y + box.height)-1)), outline=(0,0,0))

	#~ draw.rectangle((0,0,im.size[0]-1,im.size[1]-1), outline=(0,0,0))

	im.save(thmbnail)

	redirect(URL(pagepath, file))
