from vital import SYSTEMS,GAME_STATE,LEVELS
from level import level
from ui import create


current_level=None
current_ui=None
# GAME_STATE['UI']='ui_3'

def update_level():
	if current_level!=None:
		current_level.clear()

	if GAME_STATE['level'] in LEVELS:
		lvl = level(name=GAME_STATE['level'])
		if lvl.de.data['closed']:
			return None
		else:
			return lvl

	return None

def update_ui():
	if current_ui!=None:
		current_ui.clear()

	if type(GAME_STATE['UI'])==str :
		return create(name=GAME_STATE['UI'])


	return None



def running():
    global current_level,current_ui
   
    if GAME_STATE['change'][0] and not GAME_STATE['fade'][-1]: # for changing uis
        GAME_STATE['change'][0]=0
        current_ui=update_ui()

    if GAME_STATE['change'][1] and not GAME_STATE['fade'][-1] : # for changing levels
        GAME_STATE['change'][1]=0
        current_level=update_level()

           
            
    if current_level !=None :
            current_level.behavior()

    if current_ui !=None :
            current_ui.behavior()
            # print('currently running')  
 
