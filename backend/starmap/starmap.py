import os
import svgwrite
import random
import math
import argparse

PATH = os.path.dirname(os.path.abspath(__file__))
############ DEFAULT VALUES AND CONSTS ####################################

fontFamily1 = "Anton"
fontFamily2 = "Anton"
fontFamily3 = "Anton"

fontSize1 = 42
fontSize2 = 42
fontSize3 = 42

fontColor1 = "#ffffff"
fontColor2 = "#ffffff"
fontColor3 = "#ffffff"

font_style = "font-size:12px; letter-spacing:0.7px; font-family:sans-serif; stroke-width:4;"
font_style2 = "font-size:8px; letter-spacing:autopx; font-family:sans-serif; stroke-width:1;"

line1Style = f"font-size:{fontSize1}px;letter-spacing:0;font-family:\"{fontFamily1}\";stroke-width:4;text-align:center;text-anchor:middle;fill:{fontColor1}"
line2Style = f"font-size:{fontSize2}px;letter-spacing:0;font-family:\"{fontFamily2}\";stroke-width:4;text-align:center;text-anchor:middle;fill:{fontColor2}"
line3Style = f"font-size:{fontSize3}px;letter-spacing:0;font-family:\"{fontFamily3}\";stroke-width:4;text-align:center;text-anchor:middle;fill:{fontColor3}"

is_heart = "False"

background_color = "rgb(0,0,0)"
line_color = "rgb(255,255,255)"
star_color = "rgb(255,255,255)"
constellation_color = "rgb(255,255,255)"

output_file = 'starmap.svg'

#Date & Time
date = '01.01.2000'
time = '12.00.00'
utc = 3
summertime = False

# Coordinates
coord = "35.6892,51.3890"

fullview = False
guides = False
constellation = False
constellationText = False
showDot = False
showStar = False

line1 = ""
line2 = ""
line3 = ""

bg = ''
bg_x = 0
bg_y = 0
bg_opacity = 40

# placetext for leftdown corner
info = 'Tehran'

# Size of poster in mm
width = 200
height = 275

# empty space in left and right of the starmap
borders = 30


def mm_to_px(mm):
    px = mm*96/25.4
    return px


# Smaller the star bigger the magnitude
magnitude_limit = 6.5
aperture = 0.4

############ STARDATAFILE ################################################

# Stars declination and hour data file "Yale Bright Star Catalog 5"
file1 = os.path.join(PATH, "datafiles/ybsc5.txt")
file2 = os.path.join(PATH,"datafiles/extradata.txt")  # extra star data for magnitude 6,5 and higher
file3 = os.path.join(PATH,"datafiles/constellation_lines.txt")
file4 = os.path.join(PATH,"datafiles/constellation.txt")

data = []
constellation_lines = []
constellation_names = []
constellation_drawing = []


def hours_to_decimal(ra):  # use this for ybsc5

    seconds = float(ra[0:2])*60*60  # hour
    seconds += float(ra[3:5])*60  # minute
    seconds += float(ra[5:7])  # seconds
    degree = seconds*360/(24*60*60)
    return degree


def read_ybsc5():
    global data
    with open(file1, 'rt') as f:
        for line in f:
            # RA,DEC,mag,constellation

            if line[75:83].isspace() is False:
                ra = line[75:77]+'.'+line[77:81]
                ra = hours_to_decimal(ra)
                dec = float(line[83:86]+'.'+line[87:90])
                mag = float(line[103:107])
                constellation = line[11:14]
                greek = line[7:10]
                data.append([ra, dec, mag, constellation, greek])


def read_extra_star_coordinate_file():
    global data
    with open(file2, 'rt') as f:
        for line in f:
            if (',' in line):
                tmp = ([n for n in line.strip().split(',')])
                if float(tmp[2]) > 6.5:
                    tmp[0] = hours_to_decimal(tmp[0])
                    data.append([float(tmp[0]), float(
                        tmp[1]), float(tmp[2]), " ", " "])


def read_constellation_file():
    with open(file3, 'rt') as f:
        for line in f:
            tmp = ([n for n in line.strip().split(' ')])
            tmp[1] = float(tmp[1])*360/24
            tmp[2] = float(tmp[2])
            tmp[3] = float(tmp[3])*360/24
            tmp[4] = float(tmp[4])
            constellation_lines.append(tmp)


def read_constellation_names_file():
    with open(file4, 'rt') as f:
        for line in f:
            tmp = ([n for n in line.strip().split(' ')])
            constellation_names.append(tmp)


############ ARGPARSER ###################################################
parser = argparse.ArgumentParser(description='Generate starmap svg file')
parser.add_argument('-coord', '--coord',
                    help='coordinates in format northern,eastern', default=coord)
parser.add_argument('-time', '--time',
                    help='time in format hour.minute.second', default=time)
parser.add_argument('-date', '--date',
                    help='date in format day.month.year', default=date)
parser.add_argument('-utc', '--utc', nargs='?',
                    help='utc of your location -12 to +12', type=int, default=utc)
parser.add_argument('-magn', '--magn', nargs='?',
                    help='magnitude limit 0.1-12.0', type=float, default=magnitude_limit)

parser.add_argument('-summertime', '--summertime', nargs='?',
                    help='if it is summertime on the date of the starchart', type=bool, default=summertime)
parser.add_argument('-guides', '--guides', nargs='?',
                    help='draw guides True/False', type=bool, default=guides)
parser.add_argument('-constellation', '--constellation', nargs='?',
                    help='show constellation True/False', type=bool, default=constellation)
parser.add_argument(
    '-o', '--output', help='output filename.svg', default='starmap.svg')
parser.add_argument('-width', '--width', nargs='?',
                    help='width in mm', type=int, default=width)
parser.add_argument('-height', '--height', nargs='?',
                    help='height in mm', type=int, default=height)
parser.add_argument('-info', '--info',
                    help='Info text example eame of the place', default=info)

parser.add_argument("-background", "--background", type=str, default=background_color)

parser.add_argument("-constellationText", "--constellationText", type=bool, default=constellationText)
parser.add_argument("-showDot", "--showDot", type=bool, default=showDot)
parser.add_argument("-showStar", "--showStar", type=bool, default=showStar)

parser.add_argument("-line1", "--line1", type=str, default=line1)
parser.add_argument("-line2", "--line2", type=str, default=line2)
parser.add_argument("-line3", "--line3", type=str, default=line3)

parser.add_argument("-fontFamily1", "--fontFamily1", type=str, default=fontFamily1)
parser.add_argument("-fontFamily2", "--fontFamily2", type=str, default=fontFamily2)
parser.add_argument("-fontFamily3", "--fontFamily3", type=str, default=fontFamily3)

parser.add_argument("-fontSize1", "--fontSize1", type=int, default=fontSize1)
parser.add_argument("-fontSize2", "--fontSize2", type=int, default=fontSize2)
parser.add_argument("-fontSize3", "--fontSize3", type=int, default=fontSize3)

parser.add_argument("-fontColor1", "--fontColor1", type=str, default=fontColor1)
parser.add_argument("-fontColor2", "--fontColor2", type=str, default=fontColor2)
parser.add_argument("-fontColor3", "--fontColor3", type=str, default=fontColor3)

parser.add_argument('-bg', '--bg', type=str, default=bg)
parser.add_argument('-bgPosX', '--bgPosX', type=str, default=bg_x)
parser.add_argument('-bgPosY', '--bgPosY', type=str, default=bg_y)
parser.add_argument('-bgOpacity', '--bgOpacity', type=int, default=bg_opacity)

parser.add_argument('-heart', '--heart', type=str, default=is_heart)

parser.add_argument('-qrCode', '--qrCode', type=str, default="")


args = parser.parse_args()

coord = args.coord
time = args.time
date = args.date
utc = args.utc
info = args.info
output_file = args.output
guides = args.guides
magnitude_limit = args.magn
constellation = args.constellation
summertime = args.summertime

background_color = args.background
background_color = f"rgb({background_color})"

constellationText = args.constellationText
showDot = args.showDot
showStar = args.showStar

line1 = args.line1
line2 = args.line2
line3 = args.line3

is_heart = args.heart
bg_opacity = args.bgOpacity

qrCode = args.qrCode

fontFamily1 = args.fontFamily1
fontSize1 = args.fontSize1
fontColor1 = args.fontColor1
line1Style = f"font-size:{fontSize1}px; letter-spacing:0; font-family:\"{fontFamily1}\"; stroke-width:4;text-align:center;text-anchor:middle;fill:{fontColor1}"

fontFamily2 = args.fontFamily2
fontSize2 = args.fontSize2
fontColor2 = args.fontColor2
line2Style = f"font-size:{fontSize2}px; letter-spacing:0; font-family:\"{fontFamily2}\"; stroke-width:4;text-align:center;text-anchor:middle;fill:{fontColor2}"

fontFamily3 = args.fontFamily3
fontSize3 = args.fontSize3
fontColor2 = args.fontColor2
line3Style = f"font-size:{fontSize3}px; letter-spacing:0; font-family:\"{fontFamily3}\"; stroke-width:4;text-align:center;text-anchor:middle;fill:{fontColor3}"

bg = args.bg
bg_x = args.bgPosX
bg_y = args.bgPosY

height = args.height
width = args.width

# print("coordinates:", coord)
# print("date:", date)
# print("time", time)

#latitude and longitude
northern, eastern = map(float, coord.split(','))

########## DRAWING FUNCTIONS  ###########################################

# Generates random star shape to given coordinate and magnitude and color


def draw_star(x, y, mag, color):

    # randomize the number of points in star
    points = random.randint(4, 8)
    points = points * 2
    angle = 2*math.pi/(points)

    # generate the path
    path = []
    for point in range(0, points, 2):
        # point of star
        path.append(polar_to_cartesian(mag, angle*point, x, y))
        # point between two star points
        path.append(polar_to_cartesian(mag/2, angle*(point+1), x, y))

    # add object to svg
    stars = image.add(image.polygon(
        path, id='star', stroke="none", fill=color))


def draw_dot(x, y, mag, color):
    image.add(image.circle((x, y), mag, id='dot', stroke="none", fill=color))


def draw_line(x0, y0, x1, y1, color):
    image.add(image.line((x0, y0), (x1, y1), id='line',
              stroke=color, stroke_width="0.5"))


########## TIME CALCULATION  ###########################################

# date to days
def date_and_time_to_rad(date, time):

    # J2000 Epoch 01.01.2000 12.00.00
    epochyear = 2000.0
    epochhour = 12.0

    calculation_mistake = -5.1

    days_in_year = 365.2425
    months = [31, 28, 31, 30, 31, 30, 31, 31, 30,
              31, 30, 31]  # Array of days in months

    year = int(date[6:10])
    month = int(date[3:5])
    day = int(date[0:2])
    hour = float(time[0:2])
    minute = float(time[3:5])
    second = float(time[6:8])

    # years to days
    daycounter = (year-epochyear)*days_in_year
    # month to days
    daycounter += sum(months[0:month-1])
    # days
    daycounter += day-1

    secondcounter = (hour - epochhour + calculation_mistake)*60*60
    secondcounter += minute*60
    secondcounter += second

    # Summertime
    if(summertime):
        secondcounter -= (60*60)

    # UTC
    secondcounter -= (60*60*utc)

    # calculate degree from days
    degree = -((daycounter)*360.0/days_in_year) % 360

    # calculate degree from seconds
    degree -= ((secondcounter)*360/(24*60*60)) % 360

    return math.radians(degree)


########## GEOMETRY CALCULATION  ###########################################

# change polar coordinates to cartesian coordinates
def polar_to_cartesian(radius, angle, centerx, centery):
    return [centerx + radius*math.cos(angle), centery + radius*math.sin(angle)]


def angle_between(north, east, dec_angle, ra_angle):
    delta_ra = ra_angle - east
    rad = math.acos(math.cos(delta_ra)*math.cos(north) *
                    math.cos(dec_angle) + math.sin(north)*math.sin(dec_angle))
    return rad


def right_ascension_to_rad(ra):
    return math.radians(float(ra))


def declination_to_rad(dec):
    return math.radians(float(dec))


########## PROJECTIONS  ######################################################

def stereographic(latitude0, longitude0, latitude, longitude, R):
    # http://mathworld.wolfram.com/StereographicProjection.html
    k = (2*R)/(1 + math.sin(latitude0)*math.sin(latitude) +
               math.cos(latitude0)*math.cos(latitude)*math.cos(longitude-longitude0))
    x = k * math.cos(latitude) * math.sin(longitude-longitude0)
    y = k * (math.cos(latitude0)*math.sin(latitude) - math.sin(latitude0)
             * math.cos(latitude)*math.cos(longitude-longitude0))

    return x, y

########## STAR AND GUIDE GENERATION  ########################################


def generate_starmap(northern_N, eastern_E, date, time):

    # counter of stars drawn
    counter = 0

    N = math.radians(northern_N)
    E = math.radians(eastern_E)

    raddatetime = date_and_time_to_rad(date, time)
    read_constellation_names_file()

    if(guides is True):
        draw_guides = []

        for degrees in range(-3, 3):
            for lines in range(0, 360):
                draw_guides.append([degrees*30, lines])

        for hours in range(0, 24):
            for lines in range(-160, 160):
                draw_guides.append([lines/2.0, hours/24*360])

        for line in draw_guides:

            ascension = right_ascension_to_rad(line[1])+raddatetime
            declination = declination_to_rad(line[0])

            # magnitude of dot
            brightness = 1.1

            angle_from_viewpoint = angle_between(N, E, declination, ascension)
            x, y = stereographic(N, E, declination, ascension, width-(borders))

            # draw guides inside half sphere
            if ((angle_from_viewpoint <= math.radians(89)) or fullview):
                draw_dot(half_x-x, half_y-y, brightness*aperture, line_color)
                # if(line[0] == 30 and line[1] % 1 == 0):
                # 	image.add(image.text(str(line[1]), insert=(half_x-x,half_y-y), fill=line_color, style=font_style2))

    for line in data:
        if(line[2] < magnitude_limit):

            # star position from datafile
            ascension = right_ascension_to_rad(line[0])+raddatetime
            declination = declination_to_rad(line[1])

            x, y = stereographic(N, E, declination, ascension, width-(borders))

            angle_from_viewpoint = angle_between(N, E, declination, ascension)

            # size of the star in image
            magn = float(line[2])
            if(magn > 7.0):
                magn = 7.0
            brightness = 8-magn

            # draw only stars that are inside half sphere
            if ((angle_from_viewpoint <= math.radians(90)) or fullview):
                if (brightness < 2):
                    if showDot:
                        draw_dot(half_x-x, half_y-y,
                             brightness*aperture, star_color)
                else:
                    if showStar:
                        draw_star(half_x-x, half_y-y,
                              brightness*aperture, star_color)

                if(constellation is True):
                    if(line[4].isspace() is False and magn < 3):
                        for item in constellation_names:
                            for name in item:
                                if(name.strip().lower() == line[3].strip().lower() and not line[3].strip().lower() in constellation_drawing):
                                    constellation_drawing.append(
                                        name.strip().lower())
                                    if constellationText:
                                        # constellation names will draw here
                                        image.add(image.text(item[1], insert=(
                                            half_x-x+3, half_y-y+3), fill=line_color, style=font_style2))
            counter += 1
            if counter % 1000 == 0:
                # print(counter)
                pass


def generate_constellations(northern_N, eastern_E, date, time):
    N = math.radians(northern_N)
    E = math.radians(eastern_E)

    raddatetime = date_and_time_to_rad(date, time)

    for line in constellation_lines:
        ascension0 = right_ascension_to_rad(line[1])+raddatetime
        declination0 = declination_to_rad(line[2])
        x0, y0 = stereographic(N, E, declination0, ascension0, width-(borders))

        ascension1 = right_ascension_to_rad(line[3])+raddatetime
        declination1 = declination_to_rad(line[4])
        x1, y1 = stereographic(N, E, declination1, ascension1, width-(borders))

        angle_from_viewpoint1 = angle_between(N, E, declination0, ascension0)
        angle_from_viewpoint2 = angle_between(N, E, declination1, ascension1)

        if ((angle_from_viewpoint1 <= math.radians(90)) and (angle_from_viewpoint2 <= math.radians(90)) or fullview):
            draw_line(half_x-x0, half_y-y0, half_x-x1, half_y-y1, line_color)

########## GENERATE SVG  ###########################################


if __name__ == '__main__':

    read_ybsc5()
    read_extra_star_coordinate_file()
    read_constellation_file()

    half_x = mm_to_px(width/2)
    half_y = mm_to_px(height-height+110)

    # Svgfile
    image = svgwrite.Drawing(output_file, size=(
        str(width)+'mm', str(height)+'mm'))
    
    # Fonts File
    image.embed_stylesheet("@import url('https://fonts.googleapis.com/css2?family=Anton&family=Dancing+Script&family=Fuggles&family=Karla&family=Qahiri&family=Roboto&family=Roboto+Slab');")
    image.embed_stylesheet("@import url('https://v1.fontapi.ir/css/Kamran');")
    image.embed_stylesheet("@import url('https://v1.fontapi.ir/css/Mikhak');")
    image.embed_stylesheet("@import url('https://v1.fontapi.ir/css/Yekan');")

    # Background
    image.add(image.rect(insert=(0, 0), size=('100%', '100%'),
              rx=None, ry=None, fill=background_color))
    
    # Watermark
    image.add(image.image(href="http://localhost:5000/download/watermark.png", size=("100%", "100%"), opacity=".10"))
    
    # Stars generation
    generate_starmap(northern, eastern, date, time)
    if constellation:
        generate_constellations(northern, eastern, date, time)
    
    # Custom image
    if bg.strip():
        mask = image.defs.add(image.mask(id="bg_wrapper"))
        mask.add(image.circle(center=(half_x, half_y), r=340, fill=line_color, opacity=str(bg_opacity/100)))
        image.add(image.image(href=bg, size=("100%", "100%"), mask="url(#bg_wrapper)", insert=(bg_x, bg_y)))

    if is_heart == "True":
        image.add(image.image(href="http://localhost:5000/download/heart.png", size=("100%", "100%"), insert=(0, -80)))
    
    if qrCode.strip():
        image.add(image.image(href=qrCode, size=("64px", "64px"), insert=("170mm", str(height-25)+'mm')))

    # Custom User Text
    image.add(image.text(line1, insert=("100mm", str(height-60)+"mm"), fill=line_color, style=line1Style))
    image.add(image.text(line2, insert=("100mm", str(height-45)+"mm"), fill=line_color, style=line2Style))
    image.add(image.text(line3, insert=("100mm", str(height-30)+"mm"), fill=line_color, style=line3Style))

    # Text in bottom corner
    image.add(image.text(info, insert=("20mm", str(height-18)+'mm'),
              fill=line_color, style=font_style))
    image.add(image.text(str(northern)+" N "+str(eastern)+" E ",
              insert=("20mm", str(height-14)+'mm'), fill=line_color, style=font_style))
    image.add(image.text(date + " " + time + " UTC " + str(utc),
              insert=("20mm", str(height-10)+'mm'), fill=line_color, style=font_style))

    image.save()
    # print(output_file, " generated")
