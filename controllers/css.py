def base():
     response.headers['Content-Type']='text/css'
     boxes = db(db.container_box.page_id==request.vars.id).select()
     contents = ""
     for box in boxes :
         contents += ".cbox#c%(id)s { top:%(y)sem; left:%(x)sem; height:%(h)sem; width:%(w)sem; } \n"%dict(id=box.id, x=box.position_x, y=box.position_y, h=box.height, w=box.width)
     return dict(contents=contents)
