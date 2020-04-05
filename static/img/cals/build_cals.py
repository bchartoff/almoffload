import os

convertPath = "/usr/local/bin/convert"

fin = open("template.svg", "rt")
fout = open("svg/out.svg", "wt")


grey = "#d2d2d2"
white = "#ffffff"
colors = ["#f36b21","#febe10"]
# day = "fri"
rxCircle = 100
rxSquare = 1
dayAbbrs = ["mon","tues","wed","thurs","fri","sat","sun"]

for color in colors:
	if color == colors[0]:
		name = "ben"
	else:
		name = "nat"

# <rect class = "day-fri" id="d10" x = "51.7" y = "46" width = "8.2" height = "8.2" RX_RULE_fri ></rect>>

	for num in [10]:
		fin = open("template.svg", "rt")
		fout = open("svg/%s_cal_monthly_day%i.svg"%(name,num), "wt")
		lastRule = ""
		for line in fin:
			if("\"d%i\""%num in line):
				print("asdfasdf")
				lastRule = line.replace('class = "day-fri" id="d10"', "style=\"fill:#ff0000;stroke-width:10;stroke:#ff0000;\"").replace("RX_RULE_fri","rx=\"100\"")
				line = ""

			else:
				cssRule = ""
				for d in dayAbbrs:
					cssRule += ".day-%s{fill:%s;stroke:%s;stroke-width:1;}"%(d, white, grey)
					rxRule = "rx=\"%i\""%rxSquare
					line = line.replace("RX_RULE_%s"%d, rxRule)
				

			fout.write(line.replace("CSS_RULE", cssRule).replace("LAST_RULE",lastRule) )
			
		fin.close()
		fout.close()

		os.system("rsvg-convert -h 300 svg/%s_cal_monthly_day%i.svg > png/%s_cal_monthly_day%i.png"%(name,num,name,num))




	fin = open("template.svg", "rt")
	fout = open("svg/%s_cal_daily.svg"%(name), "wt")

	for line in fin:
		cssRule = ""
		for d in dayAbbrs:
			cssRule += ".day-%s{fill:%s;stroke:%s;stroke-width:2;}"%(d, color, color)
			rxRule = "rx=\"%i\""%rxCircle

			line = line.replace("RX_RULE_%s"%d, rxRule)

		fout.write(line.replace("CSS_RULE", cssRule).replace("LAST_RULE","") )
		
	fin.close()
	fout.close()

	os.system("rsvg-convert -h 300 svg/%s_cal_daily.svg > png/%s_cal_daily.png"%(name,name))





	for abbr in dayAbbrs:
		fin = open("template.svg", "rt")
		fout = open("svg/%s_cal_weekly_%s.svg"%(name,abbr), "wt")

		for line in fin:
			cssRule = ""
			# .day{fill:none;opacity:1;stroke:#353535;stroke-miterlimit:10;}
			for d in dayAbbrs:
				if d == abbr:
					cssRule += ".day-%s{fill:%s;stroke:%s;stroke-width:4;}"%(d, color, color)
					rxRule = "rx=\"%i\""%rxCircle
				else:
					cssRule += ".day-%s{fill:%s;stroke:%s;stroke-width:1;}"%(d, white, grey)
					rxRule = "rx=\"%i\""%rxSquare
				line = line.replace("RX_RULE_%s"%d, rxRule)

			fout.write(line.replace("CSS_RULE", cssRule).replace("LAST_RULE","") )
			
		fin.close()
		fout.close()

		os.system("rsvg-convert -h 300 svg/%s_cal_weekly_%s.svg > png/%s_cal_weekly_%s.png"%(name,abbr,name, abbr))
