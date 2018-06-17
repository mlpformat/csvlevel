#!/usr/bin/python3
#This is a level viewer that takes a CSV spreadsheet with
#unquoted text and draws it with PySDL2.
#Sloan Gardner 2018/Jun/16
from sdl2 import *
from sdl2.sdlimage import *
import sys
import ctypes
def bye():
	IMG_Quit()
	SDL_Quit()
def check(hope,fn):
	if hope:
		print('%s: OK!'%fn)
	else:
		print('%s: Not OK! %s'%(fn,SDL_GetError().decode('UTF-8')))
		bye()
		sys.exit(1)
def csvparse(f):
	return [x.split(',') for x in f.split('\n')]
def loop():
	global win,fb,csv
	for y,i in enumerate(csv):
		for x,j in enumerate(i):
			s=spr[j]
			w=s.contents.w
			h=s.contents.h
			SDL_BlitSurface(s,None,fb,SDL_Rect(x*w,y*h,w,h))
	SDL_UpdateWindowSurface(win)
	ev=SDL_Event()
	while SDL_PollEvent(ctypes.byref(ev)):
		if ev.type==SDL_QUIT:
			bye()
			sys.exit(0)
def main():
	global win,fb,spr,csv
	check(SDL_Init(SDL_INIT_VIDEO|SDL_INIT_EVENTS)==0,'SDL_Init')
	check(IMG_Init(IMG_INIT_PNG),'IMG_Init')
	try:
		csv=csvparse(open('level.csv').read())
	except ex:
		print('Load and Parse Level: Not OK! %s'%ex)
		bye()
		sys.exit(1)
	spr={}
	for i in csv:
		for j in i:
			if j not in spr:
				spr[j]=IMG_Load(bytes('assets/'+j+'.png','UTF-8'))
				check(spr[j],'IMG_Load')
	first=list(spr.values())[0]
	win=SDL_CreateWindow(b'CSV Level Viewer',SDL_WINDOWPOS_UNDEFINED,SDL_WINDOWPOS_UNDEFINED,first.contents.w*len(csv[0]),first.contents.h*len(csv),0)
	check(win,'SDL_CreateWindow')
	fb=SDL_GetWindowSurface(win)
	check(fb,'SDL_GetWindowSurface')
	while True:
		loop()
if __name__=='__main__':
	main()
