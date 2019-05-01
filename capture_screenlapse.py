# #!/usr/bin/env python    

"""
Description: 
	A simple screen capture utility, built with ease of use in mind, possibly buggy. 
	- Adjust capture speed on the fly (1x,5x,10x)
	- Choose which screen to capture (main,external)
	- Visual counter of captured images

Instruction:
	First make sure you have changed the Record_Path below to a location you wish to save images.
	To run on Mac:
		open Terminal, type 'python' leave a space and then drop this file onto the terminal window and press enter.
	To run on Windows:
		open Terminal, type 'python' leave a space and then drop this file onto the terminal window and press enter. - untested

Source: https://twitter.com/KubeDev
Owner: https://twitter.com/KubeDev
"""

import Tkinter as tk 
import threading
import time
import sys
import os

import subprocess

from AppKit import NSWorkspace
from time import gmtime, strftime


Record_Path = [ '/Users/kevinflynn/Tools/ScreenCapture/Output/Screen/' ]
Record_Apps = [ 'MonoDevelop-Unity' , 'Unity' , 'Sublime Text' , 'Notepad' ] ## Which Apps are allowed to trigger recording (note you must also select correct screen to record from!)
Record_Speed = 2 ## 1.0 = 1 second ..


Speed_Adjust = 0.0 ## Adjusted value do not edit. 
Background_Execute = False
Screen_Type = [ "Main" , "External" ]
Screen_Type_Selected = Screen_Type[0]

Threads = None
image_Count = 0
AppFocus = True

def Thread_Work( id , bgExecute , label ):

	def Thread_Exit():
		print("  Exiting loop.")

	global Background_Execute
	global Speed_Adjust

	while True:                       
		if bgExecute() == False:
			Thread_Exit()
			break

		Image_Shot()
		label()
		time.sleep( Speed_Adjust )

	print("Thread {}, signing off".format(id))

def Thread_Start( label ):
	print "Starting"
	global image_Count
	global Background_Execute
	global Threads
	Background_Execute = True
	tmp = threading.Thread(target = Thread_Work, args=( id , lambda: Background_Execute , label ))
	Threads = tmp
	tmp.start()

def Thread_Stop():
	global Background_Execute
	global Threads
	Background_Execute = False
	time.sleep(0.1)
	if Threads is not None:
		Threads.join
	print('Stopped.')

def Image_CurrentApp():
	appInUse = ''
	if sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
		active_window_name = (NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'])
		appInUse = active_window_name
	return appInUse	

def getImageCount( inVar ):

	def addZero( t ):
		return '0' + t	

	maxLength = 2
	temp = str(inVar)
	diff = maxLength - len(temp)

	if( diff < 0):
		temp = temp[abs(diff):]

	if( diff > 0):
		for x in range(0, diff):
			temp = addZero(temp)

	return temp


def Image_Shot():
	global AppFocus
	if Image_CurrentApp() in Record_Apps or AppFocus == 0:		

		global Screen_Type
		global Screen_Type_Selected
		global image_Count
		image_Count += 1

		bash_PathChar = '"'
		bash_FileName = 'Screen'
		bash_FileNameExt = '.jpg'
		bashCommand_Full = ""
		bash_BaseOptions = 'screencapture -C -t jpg -x ' ## -t = type, -x = make no sound .. https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man1/screencapture.1.html

		bash_ImageCount = '-' + getImageCount(image_Count)

		bash_FileDate = strftime("%j-%H-%M-%S", gmtime())
		bash_FilePath = bash_PathChar + Record_Path[0] + bash_FileDate + bash_ImageCount + bash_FileNameExt + bash_PathChar

		if Screen_Type_Selected == Screen_Type[0]:
			bashCommand_Full =  bash_BaseOptions + bash_FilePath + ";"
		else:
			bashCommand_Full =  bash_BaseOptions + bash_FilePath + " " + bash_FilePath + ";"

		output = subprocess.call( [ 'bash' , '-c' , bashCommand_Full ] )


class Capture_Gui( tk.Frame ):

	inProgress = False
	currentSpeed = 1.0

	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.Create_Gui()
		self.Adjust_Speed()
		self.Toggle_OnFocus()	

		
	def Create_Gui(self):	
		global Screen_Types
		var = tk.StringVar()
		self.checkVar = tk.IntVar()

		self.captureButton = tk.Button( self, text='Capture', command = self.Button_StartPause, width = 5 )		
		self.ScreenOpts = tk.OptionMenu(self, var, *Screen_Type , command = self.Screen_Option )
		self.ScreenOpts.config(width= 8)
		var.set( Screen_Type[0] )

		self.speedButton = tk.Button( self, text='1X', command = self.Button_Speed , width = 2 )	
		self.AppFocusToggle = tk.Checkbutton( self, text='AppFocus', variable=self.checkVar, command = self.Toggle_OnFocus , width = 9 )	
		self.countValue = tk.Label( self, text="00" , width = 5 )	
		self.close_button = tk.Button(self, text="Close", command = self.Button_Close , width = 3 )	

		self.captureButton.grid(row=0, column=0 , sticky="ew" )
		self.ScreenOpts.grid(row=0, column=1 , sticky="ew" )
		self.speedButton.grid(row=0, column=2 , sticky="ew" )
		self.AppFocusToggle.grid(row=0, column=3 , sticky="ew" )
		self.countValue.grid(row=0 , column =4 , sticky="ew" )
		self.close_button.grid(row=0, column=5, sticky="ew" )

	def Screen_Option( self , selectedList ):
		global Screen_Type_Selected
		Screen_Type_Selected = selectedList

	def Label_Count_Update(self):
		global image_Count
		self.countValue.config( text = image_Count )

	def Button_StartPause(self):
		if self.inProgress == False:	
			self.captureButton.config( text = "Pause  " )
			self.inProgress = True
			Thread_Start( self.Label_Count_Update )
		else:	
			self.captureButton.config( text = "Capture" )
			self.inProgress = False
			Thread_Stop()

	def Toggle_OnFocus(self):
		global AppFocus
		AppFocus = self.checkVar.get()

	def Button_Speed(self):
		if self.currentSpeed == 0.1:	
			self.currentSpeed = 1.0
			self.speedButton.config( text = "1X" )
		elif self.currentSpeed == 0.5:	
			self.currentSpeed = 0.1
			self.speedButton.config( text = "10X" )
		else:	
			self.currentSpeed = 0.5
			self.speedButton.config( text = "5X" )
		self.Adjust_Speed()

	def Adjust_Speed( self ):
		global Speed_Adjust
		Speed_Adjust = Record_Speed * self.currentSpeed
		
	def Button_Stop(self):	
		Thread_Stop()

	def Button_Close(self):
		Thread_Stop()
		print("Closing!")
		time.sleep(0.1)
		sys.exit()

# if a path is injected in, override?
if( len( os.environ["captureLocation"] ) > 2 ):
	Record_Path[0] = os.environ["captureLocation"]

print( "Capturing to location: " + str(Record_Path) );	

my_gui = Capture_Gui()
my_gui.master.title( 'ScreenCapture: ' )
my_gui.master.geometry('400x28')
my_gui.master.resizable(0, 0)
my_gui.mainloop()



