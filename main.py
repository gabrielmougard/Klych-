


# TODO : add identification step ( the number of the isep student is put a the end of the file name)
# TODO : trigger the ligthingTrigger before the picture is captured
# TODO : condition of cleanup ('off-line' mode) ==> `everyFilesSent`
# TODO : implement mailing.py processus (line 331)

import os
import glob
import time
import RPi.GPIO as GPIO
import picamera
import atexit
import sys
import socket
import pygame
import config
from signal import alarm, signal, SIGALRM, SIGKILL

### PINS ###
buzzer = 18 # Red button 

getReady = 7 # led indicating to get ready
pose = 11 # led indicating to take the pose !
uploading = 13 # led indicating that the images are being processed...
done = 15 # led indicating that the images are successfully sent !

lightingTrigger = 16 # trigger the lighting system before the pictures are taken !
############

### CONSTANTS ###

total_pics = 4 # number of pics to be taken
capture_delay = 1 # delay between pics
prep_delay = 5 # number of seconds at step 1 as users prep to have photo taken
gif_delay = 100 # How much time between frames in the animated gif
restart_delay = 10 # how long to display finished message before beginning a new session

high_res_w = 1920 # width of high res image, if taken
high_res_h = 1152 # height of high res image, if taken
#################

### NOT CONSTANTS ###

# Do not change these variables, as the code will change it anyway
transform_x = config.monitor_w # how wide to scale the jpg when replaying
transfrom_y = config.monitor_h # how high to scale the jpg when replaying
offset_x = 0 # how far off to left corner to display photos
offset_y = 0 # how far off to left corner to display photos
replay_delay = 1 # how much to wait in-between showing pics on-screen after taking
replay_cycles = 2 # how many times to show each photo on-screen after taking
test_server = 'www.google.com'

#####################

### OTHER CONFIG ###

real_path = os.path.dirname(os.path.realpath(__file__))

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(getReady,GPIO.OUT)
GPIO.setup(pose,GPIO.OUT) 
GPIO.setup(uploading,GPIO.OUT) 
GPIO.setup(done,GPIO.OUT)  
GPIO.setup(buzzer, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(getReady,False) 
GPIO.output(pose,False)
GPIO.output(uploading,False)
GPIO.output(done,False)

# initialize pygame

pygame.init()
pygame.display.set_mode((config.monitor_w, config.monitor_h))
screen = pygame.display.get_surface()
pygame.display.set_caption("Klych'é")
pygame.mouse.set_visible(False) # hide mouse cursor
pygame.display.toggle_fullscreen()

####################

### FUNCTIONS ###

# clean up running programs as needed when main program exits
def cleanup():
  print('Ended abruptly')
  pygame.quit()
  GPIO.cleanup()
  atexit.register(cleanup)


# A function to handle keyboard/mouse/device input events
# (backdoor for us, the developpers in case of problems)    
def input(events):
    for event in events:  # Hit the ESC key to quit the slideshow.
        if (event.type == QUIT or
            (event.type == KEYDOWN and event.key == K_ESCAPE)):
            pygame.quit()


#delete files in folder
def clear_pics():
	files = glob.glob(config.file_path + '*') 
	for f in files:
		os.remove(f) # delete the images

    gifs = glob.glob(config.gif_path + '*')
    for g in gifs:
        os.remove(g) # delete the gif(s)

	#light the lights in series to show completed
	print "Deleted previous pics"
	for x in range(0, 3): #blink light
		GPIO.output(getReady,True) 
	    sleep(0.1)
		GPIO.output(getReady,False)
		sleep(0.1)
        GPIO.output(pose,True) 
		sleep(0.1)
		GPIO.output(pose,False)
		sleep(0.1)
        GPIO.output(uploading,True)
		sleep(0.1)
		GPIO.output(uploading,False)
		sleep(0.1)
        GPIO.output(done,True)
		sleep(0.1)
		GPIO.output(done,False)
		sleep(0.1)


# check if connected to the internet   
def is_connected():
  try: 
    # see if we can resolve the host name -- tells us if there is a DNS listening  
    host = socket.gethostbyname(test_server)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

# set variables to properly display the image on screen at right ratio
def set_demensions(img_w, img_h):
	# Note this only works when in booting in desktop mode. 
	# When running in terminal, the size is not correct (it displays small). Why?

    # connect to global vars
    global transform_y, transform_x, offset_y, offset_x

    # based on output screen resolution, calculate how to display
    ratio_h = (config.monitor_w * img_h) / img_w 

    if (ratio_h < config.monitor_h):
        #Use horizontal black bars
        #print "horizontal black bars"
        transform_y = ratio_h
        transform_x = config.monitor_w
        offset_y = (config.monitor_h - ratio_h) / 2
        offset_x = 0
    elif (ratio_h > config.monitor_h):
        #Use vertical black bars
        #print "vertical black bars"
        transform_x = (config.monitor_h * img_w) / img_h
        transform_y = config.monitor_h
        offset_x = (config.monitor_w - transform_x) / 2
        offset_y = 0
    else:
        #No need for black bars as photo ratio equals screen ratio
        #print "no black bars"
        transform_x = config.monitor_w
        transform_y = config.monitor_h
        offset_y = offset_x = 0

    # uncomment these lines to troubleshoot screen ratios
    #     print str(img_w) + " x " + str(img_h)
    #     print "ratio_h: "+ str(ratio_h)
    #     print "transform_x: "+ str(transform_x)
    #     print "transform_y: "+ str(transform_y)
    #     print "offset_y: "+ str(offset_y)
    #     print "offset_x: "+ str(offset_x)

# display one image on screen
def show_image(image_path):

	# clear the screen
	screen.fill( (0,0,0) )

	# load the image
	img = pygame.image.load(image_path)
	img = img.convert() 

	# set pixel dimensions based on image
	set_demensions(img.get_width(), img.get_height())

	# rescale the image to fit the current display
	img = pygame.transform.scale(img, (transform_x,transfrom_y))
	screen.blit(img,(offset_x,offset_y))
	pygame.display.flip()

# display a blank screen
def clear_screen():
	screen.fill( (0,0,0) )
	pygame.display.flip()

# display a group of images
def display_pics(jpg_group):
    for i in range(0, replay_cycles): #show pics a few times
		for i in range(1, total_pics+1): #show each pic
			show_image(config.file_path + jpg_group + "-0" + str(i) + ".jpg")
			time.sleep(replay_delay) # pause 


def start_photobooth():

    input(pygame.event.get()) # press escape to exit pygame. Then press ctrl-c to exit python.

    ### START of Step 1 ###

    print "Get Ready"
    GPIO.output(getReady,True)
    show_image(real_path + "/res/instructions.png")
    sleep(prep_delay)

    # clear the screen
    clear_screen()

    camera = picamera.PiCamera()
    camera.vfip = False
    camera.hflip = True # flip for preview, showing the user a mirror image
    camera.iso = config.camera_iso

    pixel_width = 0 # local variable declaration
    pixel_height = 0 # local variable declaration

    if config.hi_res_pics :
        camera.resolution = (high_res_w, high_res_h) # set camera resolution foir high res
    else:
        pixel_width = 500
        pixel_height = config.monitor_h * pixel_width // config.monitor_w
		camera.resolution = (pixel_width, pixel_height) # set camera resolution to low res


    ### START of Step 2 ###

    print "taking pictures..."
    now = time.strftime("%Y-%m-%d-%H-%M-%S") #get the current date and time for the start of the filename

    if config.capture_count_pics:
        try: # take the photos
            for i in range(1,total_pics+1):
                camera.hflip = True # preview a mirror image
                camera.start_preview(resolution=(config.monitor_w,config.monitor_h)) #  start preview at low res but the right ratio
                time.slepp(2)
                GPIO.output(pose,True) # turn on the LED
                filename = config.file_path + now + '-0' + str(i) +'.jpg'

                filenameGIF = config.gif_path + filename[len(config.gif_path):]
                
                camera.hflip = False # flip back when taking photo
                camera.capture(filename)

                os.system("cp "+filename+" "+filenameGIF) # create a copy of the image in the /gifs folder to generate a GIF at the same time.

                print(filename)
                GPIO.output(pose,False) # turn off the led
                camera.stop_preview()
                show_image(real_path + "/res/pose" + str(i) + ".png")
                time.sleep(capture_delay) # pause in-between shots
                clear_screen()
                if i == total_pics+1:
                    break
        
        finally:
            camera.close()
    else:
        camera.start_preview(resolution=(config.monitor_w,config.monitor_h)) # start preview at low res but the right ratio
        time.sleep(2) # warming up camera

        try: # take the photos
            for i,filename in enumerate(camera.capture_continuous(config.file_path + now + '-' + '{counter:02d}.jpg')):
                GPIO.output(pose,True) # turn on the LED
                print(filename)
                time.sleep(capture_delay)
                GPIO.output(pose,False) # turn off the LED
                if i == total_pics-1:
                    break
        finally:
            camera.stop_preview()
            camera.close()


    ### START of Step 3 ###

    input(pygame.event.get()) # press escape to exit pygame. Then press ctrl-c to exit python.

    print "Sending photos and creating animated GIF then send it."

    if config.post_online and is_connected():
        show_image(real_path + "/res/uploading.png")
    else:
        show_image(real_path + "/res/processing.png")

    if config.make_gifs: # make the gifs
        if config.hi_res_pics:
            # first make a small version of each image. We do it 500 pixels wide for the sake of speed...
			for x in range(1, total_pics+1): #batch process all the images
				graphicsmagick = "gm convert -size 500x500 " + config.gif_path + now + "-0" + str(x) + ".jpg -thumbnail 500x500 " + config.gif_path + now + "-0" + str(x) + "-sm.jpg"
				os.system(graphicsmagick) #do the graphicsmagick action

            graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + config.gif_path + now + "*-sm.jpg " + config.gif_path + now + ".gif" 
			os.system(graphicsmagick) #make the .gif

        else:

            # make an animated gif with the low resolution images
			graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + config.gif_path + now + "*.jpg " + config.gif_path + now + ".gif" 
			os.system(graphicsmagick) #make the .gif

    if config.post_online: # is online posting is allowed in config.py
        connected = is_connected() # check to see if we have an internet connection

        if (connected==False):
            print "bad internet connection"

        while connected:
            # TODO : send email with the gifs and/or the images with emailing.py











    ### START of Step 4 ###

    input(pygame.event.get()) # press escape to exit pygame. Then press ctrl-c to exit python.
	
	try:
		display_pics(now)
    except Exception e:
        tb = sys.exc_info()[2]
		traceback.print_exception(e.__class__, e, tb)
		pygame.quit()

    print "Done"
    GPIO.output(done,True)
    show_image(real_path + "/res/finished.png")
    time.sleep(restart_delay)
    show_image(real_path + "/res/intro.png")
    GPIO.output(done,False)
    GPIO.output(getReady, True) # turn on the getReady LED for the next shot !


### MAIN ROUTINE ###

if (config.clear_on_startup and everyFilesSent):
    clear_pics()

print "Klych'é is running..."

GPIO.output(lightingTrigger,True) #blink light to show the app is running
for x in range(0,5):
    GPIO.output(getReady,True)
	sleep(0.1)
	GPIO.output(getReady,False)
	sleep(0.1)
    GPIO.output(pose,True)
	sleep(0.1)
	GPIO.output(pose,False)
	sleep(0.1)
    GPIO.output(uploading,True)
	sleep(0.1)
	GPIO.output(uploading,False)
	sleep(0.1)
    GPIO.output(done,True) 
	sleep(0.1)
	GPIO.output(done,False)
	sleep(0.1)

GPIO.output(lightingTrigger,False)
show_image(real_path + "/res/intro.png")

while True:
    GPIO.output(getReady,True) #turn on the light showing users they can push the button
    input(pygame.event.get()) # press escape to exit pygame. Then press ctrl-c to exit python.
    GPIO.wait_for_edge(btn_pin, GPIO.FALLING)
    time.sleep(config.debounce) #debounce
    start_photobooth()























