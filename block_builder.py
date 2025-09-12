from manager import *
from vital import pygame,scr,GAME_STATE
from entites import ANIM_SYS,Handler,AI_SYS

clock=pygame.time.Clock() 

while GAME_STATE['run']:
	scr.fill((0,0,0))
	for event in pygame.event.get():
		if event.type==pygame.QUIT:        
			GAME_STATE['run']=0

		if event.type==pygame.KEYDOWN:
			Handler.update_event(event='key_down')
			if event.key == pygame.K_ESCAPE:
				Handler.update_event(event='esc')


			if event.key == pygame.K_SPACE:
				Handler.update_event(event='space')

		if event.type==pygame.MOUSEBUTTONDOWN:
			# print(pygame.mouse.get_pos())
			Handler.update_event(event='mouse_down')

		if event.type==pygame.MOUSEBUTTONUP:
			Handler.update_event(event='mouse_released')



	if len(Handler.events['mouse_pos']):
		Handler.update_event(event='mouse_pos',val=pygame.mouse.get_pos())
	
	running()
	ANIM_SYS.Manage()
	clock.tick(18)
	# print(len(ANIM_SYS.lists['ents']))

	pygame.display.update()
	
pygame.quit()
