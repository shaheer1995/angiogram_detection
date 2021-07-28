import wabtec_track

file_name = 'images/Caltrain_01-08-20_Page_2.jpg'

wtt = wabtec_track.WabTecTrack(file_name=file_name)

lines = wtt.get_lines()   #gets list of line_track objects

for ln in lines:
    print(ln.point_one(), ', ' , ln.point_two())
    #print(ln.x1)  #can also be accesseds

#only for testing
wtt.draw_lines(lines, 'output/1.jpg', is_new_image =True);

