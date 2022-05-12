import pygame, os, random, json
import urllib.error, urllib.request 

from datetime import datetime

from sqlalchemy import true
# Variable for infinite loop of the app
DoIt            =   True

# Constants and variables
DIR_PATH        =   os.path.dirname(os.path.abspath(__file__))
ICON_PATH       =   DIR_PATH + "/config/icons/"
W_ICON_PATH     =   DIR_PATH + "/config/weather_icons/"

WINDOW_SIZE     =   [314,472]   # 8cm (width) x 12 cm(height) x 100 ppp = 13 inches
WINDOW_CAP      =   "Domotic System"
WINDOW_ICON     =   ICON_PATH + "house_icon.png"

WEATHER_WINDOW_WIDTH    =   WINDOW_SIZE[0] - 4
WEATHER_WINDOW_HEIGHT   =   150

CLOUD_ICON          =   W_ICON_PATH + "clouds.png"   
CLOUDY_NIGHT_ICON   =   W_ICON_PATH + "cloudy_night.png"
SUN_ICON            =   W_ICON_PATH + "sun.png"
NIGHT_ICON          =   W_ICON_PATH + "night.png"


# Defining colors 
BLACK               =   [0,0,0,155]
WHITE               =   [255,255,255]
BLUE_SKY            =   [64,207,255]
LIGHT_BLUE          =   [120,120,255]
SUPER_LIGHT_BLUE    =   [150,150,255]
HIPER_LIGHT_BLUE    =   [175,175,255]

BLUE_RAIN           =   [165,180,220]#[255,0,0]
LIGHT_BLUE_RAIN     =   [165,180,200]#[0,255,0]
VERY_LIGHT_BLUE_RAIN=   [165,180,180]#[0,0,255]
RAIN_COLORS         =   [BLUE_RAIN, LIGHT_BLUE_RAIN, VERY_LIGHT_BLUE_RAIN]

# Rain Variables
DROP_NUMBER         =   20

DROP_THICK          =   2
DROP_THIN           =   1
DROP_THICKNESS      =   [DROP_THICK, DROP_THIN]

DROP_LEN_LONG       =   20#5
DROP_LEN_SHORT      =   10#3
DROP_LEN_VERY_SHORT =   5
DROP_LEN            =   [DROP_LEN_LONG, DROP_LEN_SHORT, DROP_LEN_VERY_SHORT]

DROP_FAST           =   2
DROP_SLOW           =   1.5 
DROP_VERY_SLOW      =   1
DROP_VELOCITY       =   [DROP_FAST, DROP_SLOW, DROP_VERY_SLOW]

# Time Variables
TIMESTAMP           =   3 #secs

# API Variables 
API_url             = "https://api.openweathermap.org/data/2.5/weather?"
API_key             = "&appid=7e529a7df215e65c222ec1f24c8fe80c"
API_city            = "&q=Oslo"
API_units           = "&units=metric" 

API                 = API_url + API_city + API_units + API_key

class CurrentWeather():
    def __init__(self):
        # Initializing the attributes of the class
        self.name           = ""
        self.country        = ""
        self.description    = ""
        self.temp           = 0
        self.feels_like     = 0
        self.humidity       = 0
        self.temp_min       = 0
        self.temp_max       = 0
        self.wind_speed     = 0
        self.cloud_percent  = 0
        self.rain_volume    = 0
        self.snow_volume    = 0
        self.sunrise_hour   = ""
        self.sunset_hour    = ""
        self.timezone       = ""
        self.its_day        = ""

        self.get_weather_info()        
    
    def __calling_the_API(self):
        try:  
            self.req    = urllib.request.Request(API)
            self.resp   = urllib.request.urlopen(self.req)
            self.info   = json.loads(self.resp.read().decode('utf-8'))

            self.resp.close()

        except urllib.error.HTTPError as e:
            pass

    def get_weather_info(self):   
        # Calling the API
        self.__calling_the_API()
        
        # Getting the city and country
        try: 
            self.name = str(self.info['name'])
            self.country = str(self.info['sys']['country'])
        except: pass

        # Getting info from the JSON response of the API
        try: self.timezone = int(self.info['timezone'])
        except: pass

        # Getting the sunrise and sunset hour info
        if self.timezone:
            try:
                ts = int(self.info['sys']['sunrise'] + self.timezone)
                self.sunrise_hour = datetime.utcfromtimestamp(ts)
            except: pass
            try:
                ts = int(self.info['sys']['sunset'] + self.timezone)
                self.sunset_hour = datetime.utcfromtimestamp(ts)  
            except: pass

        # Getting weather description
        try:
            l = self.info['weather']
            d = dict(l[0]) 
            self.description = str(d['description'])
        except: pass

        # Getting the cloud percentage
        try: self.cloud_percent = int(self.info['clouds']['all'])
        except: pass

        # Getting the rain volume
        try: self.rain_volume = int(self.info['rain']['1h'])
        except: pass

        # Getting the snow volume
        try: self.snow_volume = int(self.info['snow']['1h'])
        except: pass

        # Getting the temperature & humidity
        try: 
            self.temp = int(self.info['main']['temp'])
            self.temp_max = int(self.info['main']['temp_max'])
            self.temp_min = int(self.info['main']['temp_min'])
            self.feels_like = int(self.info['main']['feels_like'])
            self.humidity = int(self.info['main']['humidity'])
        except: pass

        # Getting the wind speed
        try: self.wind_speed = int(self.info['wind']['speed'])
        except: pass

        # Now we change the global variables so we can read them from the interface file
        # and select the simulation to use in the Weather App Button
        now = datetime.now()
        if self.sunrise_hour < now and self.sunset_hour > now:
            self.its_day = True
        else:
            self.its_day = False
        
        

VALID_CLOUD_RATE    = 30 #%
VALID_RAIN_RATE     = 1

# Buttons configuration
BTN_ELEVATION       =   3

BTN_WEATHER_WIDTH   =   WEATHER_WINDOW_WIDTH
BTN_WEATHER_HEIGHT  =   WEATHER_WINDOW_HEIGHT - 4
BTN_WEATHER_POS     =   [2,2]

BTN_LIGHTS_WIDTH    =   WINDOW_SIZE[0]/2 - 2
BTN_LIGHTS_HEIGHT   =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 2 
BTN_LIGHTS_POS      =   [2,0*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT + 2]
BTN_TV_WIDTH        =   WINDOW_SIZE[0]/2 - 4
BTN_TV_HEIGHT       =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 2
BTN_TV_POS          =   [WINDOW_SIZE[0]/2 + 2,0*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT + 2]
BTN_AIR_WIDTH       =   WINDOW_SIZE[0]/2 - 2
BTN_AIR_HEIGHT      =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 2
BTN_AIR_POS         =   [2,1*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT + 2]
BTN_APPLIANCE_WIDTH =   WINDOW_SIZE[0]/2 - 4
BTN_APPLIANCE_HEIGHT=   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 2
BTN_APPLIANCE_POS   =   [WINDOW_SIZE[0]/2 + 2,1*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT + 2]
BTN_BLINDS_WIDTH    =   WINDOW_SIZE[0] - 4
BTN_BLINDS_HEIGHT   =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 4
BTN_BLINDS_POS      =   [2,2*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT +2]
BTN_SETTINGS_WIDTH  =   WINDOW_SIZE[0] - 4
BTN_SETTINGS_HEIGHT =   (WINDOW_SIZE[1] - WEATHER_WINDOW_HEIGHT)/4 - 4
BTN_SETTINGS_POS    =   [2,3*(WINDOW_SIZE[1]-WEATHER_WINDOW_HEIGHT)/4 + WEATHER_WINDOW_HEIGHT + 2]

class Button:
    def __init__(self,text,pos,width,height,elevation,font, color_on, color_off):
    #Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.color_on = color_on
        self.color_off = color_off

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = self.color_off

        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'
        #text
        self.text_surf = font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self, screen, function):
    # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 6)
        pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 6)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click(function)

    def check_click(self, function):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.color_on
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    function()
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.color_off
        
    def get_Rect(self):
        return self.top_rect
        
# Water drop class - Rain simulation

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
class WaterDrop():
    def __init__(self, start_pos, end_pos, length, thickness, colour, velocity = 1):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.length = length
        self.thickness = thickness
        self.colour = colour
        self.velocity = velocity

    def drop_move():
        pass

def print_sunny_day(screen, rect):
    # Changing the background of the weather API - Sunny day
    sun = pygame.image.load(SUN_ICON)
    sun_rect = sun.get_rect().clip(rect)
    
    screen.blit(sun,sun_rect)


def print_rainy_day(screen, rect, rain):
    # Changing the background of the weather API - Cloudy day
    cloud = pygame.image.load(CLOUD_ICON)
    cloud_rect = cloud.get_rect().clip(rect)
    
    screen.blit(cloud,cloud_rect)

    # Let's move each drop of the rain array to simulate the drop is moving
    # In each iteration of the while loop the drop will move one pixel in 
    # y axis
    for drop in rain:
        pygame.draw.line(screen, 
                        drop.colour, 
                        [drop.start_pos.x,drop.start_pos.y], 
                        [drop.end_pos.x,drop.end_pos.y], 
                        drop.thickness)
        
        drop.start_pos.y = drop.start_pos.y + drop.velocity
        drop.end_pos.y = drop.start_pos.y + drop.length

        if drop.start_pos.y > WEATHER_WINDOW_HEIGHT:
            drop.start_pos.x = random.randrange(2, WEATHER_WINDOW_WIDTH - 4)
            drop.end_pos.x = drop.start_pos.x
            drop.start_pos.y = 2
            drop.end_pos.y = drop.start_pos.y + drop.length


def print_cloudy_day(screen, rect):
    # Changing the background of the weather API - Cloudy day
    cloud = pygame.image.load(CLOUD_ICON)
    cloud_rect = cloud.get_rect().clip(rect)
    
    screen.blit(cloud,cloud_rect)
    

def print_dark_night(screen, rect):
    # Changing the background of the weather API - Night
    night = pygame.image.load(NIGHT_ICON)
    night_rect = night.get_rect().clip(rect)
    
    screen.blit(night,night_rect)


def print_cloudy_night(screen, rect):
    # Changing the background of the weather API - Cloudy night
    cloud_night = pygame.image.load(CLOUDY_NIGHT_ICON)
    cloudy_night_rect = cloud_night.get_rect().clip(rect)
    
    screen.blit(cloud_night,cloudy_night_rect)


def print_rainy_night(screen, rect, rain):
    # Changing the background of the weather API - Cloudy night
    cloud_night = pygame.image.load(CLOUDY_NIGHT_ICON)
    cloudy_night_rect = cloud_night.get_rect().clip(rect)
    
    screen.blit(cloud_night,cloudy_night_rect)

    # Let's move each drop of the rain array to simulate the drop is moving
    # In each iteration of the while loop the drop will move one pixel in 
    # y axis
    for drop in rain:
        pygame.draw.line(screen, 
                        drop.colour, 
                        [drop.start_pos.x,drop.start_pos.y], 
                        [drop.end_pos.x,drop.end_pos.y], 
                        drop.thickness)
        
        drop.start_pos.y = drop.start_pos.y + drop.velocity
        drop.end_pos.y = drop.start_pos.y + drop.length

        if drop.start_pos.y > WEATHER_WINDOW_HEIGHT:
            drop.start_pos.x = random.randrange(2, WEATHER_WINDOW_WIDTH - 4)
            drop.end_pos.x = drop.start_pos.x
            drop.start_pos.y = 2
            drop.end_pos.y = drop.start_pos.y + drop.length




    
        
