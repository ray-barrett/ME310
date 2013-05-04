#! /usr/bin/env python2
import socket
import pygame
import Image
import sys

# Functions ===================================================================
def string2Surface(data):
	# We turn the data we revieved into a 120x90 PIL image
	image = Image.fromstring("RGB",(120,90),data)
	#image = Image.fromstring("RGB",(640,480),data)

	# Resize the image to 640x480
	image = image.resize((640,480))

	# Turn the PIL image into a pygame surface
	image = pygame.image.frombuffer(image.tostring(),(640,480),"RGB")

	return image
#==============================================================================

# Start PyGame:
pygame.init()
# Create a PyGame screen, and set its size to 640x480L
screen = pygame.display.set_mode((640,480))
# Set the window caption:
pygame.display.set_caption('Remote Webcam Viewer')
# Create a PyGame clock which will be used to limit the fps
clock = pygame.time.Clock()

address = ('localhost', 10003)
timer = 0
previousImage = ""
image = ""

while 1:
	# Check if the exit button has been pressed:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()							      
		
	# Timer to limit how many images requested from the server each second
	if timer < 1:
		# Create a socket connection for connecting to the server
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect(address)
		# Recieve data from the server
		data = client_socket.recv(1024000)

		try:
			image = string2Surface(data)
		except:
			# if failed to get image, display last one
			image = previousImage

		# put more time on the clock
		timer = 5
	else:
		timer -= 1
	
	screen.blit(image,(0,0))

	pygame.display.update()
