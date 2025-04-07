
from vital import SYSTEMS,GAME_STATE,LEVELS
from level import level
from ui import create


current_level=None
current_ui=None

def update_level():
	if GAME_STATE['level'] in LEVELS:
		return level(name=GAME_STATE['level'])

	return None

def update_ui():
	if current_ui!=None:
		current_ui.remove()
		for elm in current_ui.components:
			elm.remove()

	if type(GAME_STATE['UI'])==str :
		return create(name=GAME_STATE['UI'])


	return None




def running():
    global current_level,current_ui
   
    if GAME_STATE['change'][0]: # for changing uis
        GAME_STATE['change'][0]=0
        current_ui=update_ui()

    if GAME_STATE['change'][1]: # for changing levels
        GAME_STATE['change'][1]=0
        current_level=update_level()

           
            
    if current_level !=None :
            current_level.behavior()

    if current_ui !=None :
            current_ui.behavior()
            # print('currently running')  
 