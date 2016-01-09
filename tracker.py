"""Magic behind the madness: Software for ES50 ShuttleLED Project
For questions and inquiry please contact gmerz@college.harvard.edu"""
import time 
import math 
from collections import OrderedDict
import requests
import minutes
from datetime import datetime
from neopixel import *

# LED strip configuration:
LED_COUNT      = 156      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# different shuttle IDS (change depending on time -- the track is only built
# for QUAD_EXPRESS but for testing when the shuttles aren't running the other
# shuttles also run to the quad)
QUAD_EXPRESS = "4003894"
QUAD_STADIUM = "4003898"
SIXTEEN = "4003926"
OVERNIGHT = "4003938"
QUAD_STOP = "4070614"

# num_list = the number of LEDS in each region
# add_list = the number each region of the LED starts at
NUM_LIST = [0, 7, 14, 7, 53, 27, 11, 27, 10]
ADD_LIST = [0, 7, 21, 28, 81, 108, 119, 146, 156]

# declare the colors we want to use for the shuttles and the tracks (in case we 
# want to use different colors for each shuttle, etc.)
SHUTTLE_COLOR = [Color(204, 0, 204 ), Color(204, 0, 204), Color(204, 0, 204)]
TRACK_COLOR = Color(0, 128, 255)
STOP_COLOR = Color(0, 255, 0)

# declare which LEDs are the stops we want 
STOPS = [14, 15, 17, 76, 138, 139]

# LED_list: this is needed so that we can remember the last coordinates of 
# the shuttle, and make sure that when the shuttle is no longer there
# we turn those LEDs back to the track_color. There are at most 3 shuttles
# running at a time, so we initialize it with a 3 x 3 matrix.
LED_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# define the endpoint lat, lng for each segment in the track
r1_start = (42.380097, -71.125045)
r1_end = (42.380477, -71.124273)
r2_start = r1_end
r2_end = (42.382379, -71.125989)
r3_start = r2_end
r3_end = (42.382062, -71.126762)
r4_start = r3_end
r4_end = (42.374993, -71.118951)
r5_start = r4_end
r5_end = (42.380002, -71.119981) 
r6_start = r5_end
r6_end = (42.379811, -71.116505)  
r7_start = r6_end
r7_end = (42.375468, -71.114402)
r8_start = r7_end
r8_end = r4_end

# declare the dictionary that maps coordinates to LEDS
# keys: (lat, lng) type: tuple
# vales: LED type: int 
lat_lng_dict = OrderedDict()


def generate_points(start, end, region, d): 
    """ function that is called to populate lat_lng_dict 
        takes in the start point, end point, and region number. 
        Works by taking the difference in latitude and longitude 
        between two LEDs in a region, dividing each by the number of LEDS
        in that region, and that adding that number to latitude and longitude
        to get the LED that corresponsds to that lat and long. returns null """
    # extract lat and lng from start tuples
    lat, lng = start
    # extract lat and lng from end tuple 
    lat1, lng1 = end
    # find difference between lats
    lat_range = lat1 - lat
    # find difference between lngs 
    lng_range = lng1 - lng 
    # find value we're going to add so that each LED has a unique coordinate 
    lat_toadd = lat_range / NUM_LIST[region]
    lng_toadd = lng_range / NUM_LIST[region]
    # iterate through the LEDs in the region, adding their respctive coordinates
    # to the dictionary as keys and the LEDs themselves as values 
    for i in xrange(ADD_LIST[region - 1], ADD_LIST[region]): 
        d[(lat, lng)] = i 
        lat = lat + lat_toadd
        lng = lng + lng_toadd 
    return 


def distance(p1, p2): 
    """returns the euclidean distance between two lat, lng coordinates"""
    x1, y1 = p1
    x2, y2 = p2
    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return dist


# this function may not be the most efficient way to get where the LED is, 
# but it worked the most reliably as compared to a vector projection, and
# for this project reliability is more important than efficiency. future
# improvements to improve efficieny may be only calling this function 
# once for finding the initial location, and taking advantage of the fact we have an
# ordered dictionary by finding the next closest point in a set of 5 LEDs, 
# instead of re-checking the whole dictionary the whole time
def get_closest(p1, d): 
    """ gets the closest point in our dictionary to a lat and lng"""
    # get the distance from each point and the distance, and the origin
    # point in a list 
    dist_list = [(distance(p1, x),x) for x in d.iterkeys()]

    # extract the minimum distance and the point that it's at from the list
    dist, pt = min(dist_list, key = lambda x: x[0])

    # bad practice -- accesses hidden attributes, but it works 
    # this part gets the previous and next points in the dictionary 
    # so that we can make the shuttle look like a shuttle (a line of 3 LEDs)
    # instead of just one LED moving around the track 
    prev, nxt, _ = lat_lng_dict._OrderedDict__map[pt]

    # error checking -- if we're at the first or last point it's going to 
    # return None (at the first and last LEDs, our shuttle will just be two points)
    if prev is None: 
        prev = d[pt]
    else: 
        prev = d[prev[2]]
    if nxt is None: 
        nxt = d[pt]
    else: 
        nxt = d[nxt[2]]
    return (prev, d[pt], nxt)
        

def make_requests(route, stop): 
    """ the function that handles requests to the API, takes in which route we're following and 
    returns a list of tuples of current latitude and location for each shuttle we get from the API """ 
    # make the request
    r = requests.get("https://transloc-api-1-2.p.mashape.com/vehicles.json?agencies=52&routes=" + route,
      headers={
        "X-Mashape-Key": 'kn0hopZZ6kmshgIsTkySFeTiBi1sp1TPOp4jsneOzIhODSwMC3',
        "Accept": "application/json"
      }
    )
    # turn the reqeust into something we can deal with 
    r = r.json()
    # initialize variables
    lst = []
    # error checking -- make sure we have a shuttle running 
    for i in xrange(0, len(r['data']['52'])): 
        # extract the latitude and longitude (these are floats)
        lat = r['data']['52'][i]['location']['lat']
        lng = r['data']['52'][i]['location']['lng']
        # extract the arrival estimates (this is a list of dicts)
        arrival_estimates = r['data']['52'][i]['arrival_estimates']
        # variable "arival_best" to keep track of when the 
        # closest shuttle will get there
        arrival_best = 100 
        for d in list(arrival_estimates): 
            # find the time until the stop we want 
            if d['stop_id'] == stop: 
                # extract arrival time 
                arrival_time = d['arrival_at']
                # find minutes until it arrives 
                arrival_time = find_time_difference(arrival_time)
                # if it's the best arrival time, store it as such 
                if arrival_time < arrival_best: 
                    arrival_best = arrival_time 
        lst.append((lat, lng))
    return lst, arrival_best


def flash(p1, p2, p3, color): 
    """ sets three LEDs to be a given color """
    strip.setPixelColor(p1, color)
    strip.setPixelColor(p3, color)
    strip.setPixelColor(p2, color)


def simulate_helper(strip, pt, i): 
    """ helper function for simulate_shuttle, takes in a lat_lng, 
    returns the three closest LEDs, turns them the correct color, 
    turns previous location to be color of track """
    # for some reason error checking that happens in the get_closest
    # function doesn't always work, so we use a try except statement
    # if the error checking doesn't work, we can just set the shuttle
    # to be at it's last known location (LED_list)
    try: 
        prev, pt, nxt = get_closest(pt, lat_lng_dict)
    except: 
        [prev, pt, nxt] = LED_list[i]
    # set previous LEDs to be same color as track
    if (prev, pt, nxt) != (LED_list[i][0], LED_list[i][1], LED_list[i][2]): 
        flash(LED_list[i][0], LED_list[i][1], LED_list[i][2], TRACK_COLOR)
    # remember current location of shuttle  
    LED_list[i][0] = prev
    LED_list[i][1] = pt
    LED_list[i][2] = nxt
    # set current LEDs to be the color we've designated for the shuttle 
    if pt in STOPS: 
        flash(prev, pt, nxt, STOP_COLOR)
    else: 
        flash(prev, pt, nxt, SHUTTLE_COLOR[i])
    strip.show()


def simulate_shuttle(strip, route, stop): 
    """ actual function that simulates the route """ 
    lst, tme = make_requests(route, stop)
    if tme in range(0,9): 
        minutes.display_num(tme)
    for i in xrange(len(lst)):
        pt = lst[i]
        simulate_helper(strip, pt, i)
    


def test(strip, d): 
    """ checks that everything works the way we would expect 
    by just iterating through values in lat_lng_dict and 
    simulating the shuttle """
    for ind, x in enumerate(list(d.iterkeys())):
        x2 = list(d.iterkeys())[::-1][ind]
        simulate_helper(strip, x, 0)
        simulate_helper(strip, x2, 1)
        time.sleep(1)

def find_time_difference(tme): 
    """ parses the arrival time retrieved from the API, subtracts the current
    time, and returns the amount of time until the next shuttle """
    date = (tme.encode('utf-8').split('T'))[0].split('-')
    tme = (((tme.encode('utf-8').split('T'))[1].split('-'))[0]).split(":")
    arrival_time = datetime.strptime(date[0] + ' ' + date[1] + ' ' +  date[2] + ' ' + tme[0] + ' ' + tme[1] + ' ' + tme[2], "%Y %m %d %H %M %S")
    td = arrival_time - datetime.now() 
    return (td.seconds//60)%60

# Main program logic follows:
if __name__ == '__main__':
    # setup seven-seg display
    minutes.setup()
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    # populate lat_lng_dict 
    generate_points(r1_start, r1_end, 1, lat_lng_dict)
    generate_points(r2_start, r2_end, 2, lat_lng_dict)
    generate_points(r3_start, r3_end, 3, lat_lng_dict)
    generate_points(r4_start, r4_end, 4, lat_lng_dict)
    generate_points(r5_start, r5_end, 5, lat_lng_dict)
    generate_points(r6_start, r6_end, 6, lat_lng_dict)
    generate_points(r7_start, r7_end, 7, lat_lng_dict)
    generate_points(r8_start, r8_end, 8, lat_lng_dict)

    print 'Press Ctrl-C to quit.'
    start(strip)
    while True:
        test(strip, lat_lng_dict)
        # simulate_shuttle(strip, OVERNIGHT, QUAD_STOP)
