def page_layout():
     response.headers['Content-Type']='text/css'
     boxes = get_boxes_on_page(request.vars.id)
     contents = ""
     for box in boxes :
         contents += ".cbox#c%(id)s { top:%(y)sem; left:%(x)sem; height:%(h)sem; width:%(w)sem; } \n"%dict(id=box.id, x=box.position_x, y=box.position_y, h=box.height, w=box.width)
     return dict(contents=contents)
