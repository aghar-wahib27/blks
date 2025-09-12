from vital import pygame
from extractor import DR,ui_assets,FONT


main_surfaces={k:pygame.image.load(v) for (k,v) in DR.items()}


UIS={k:pygame.image.load(v) for (k,v) in ui_assets.items()}

for img in UIS.values():
	img.set_colorkey((0,0,0))


FFF=pygame.font.Font(FONT,30)
FFFF=pygame.font.Font(FONT,20)

_FONTS_={ k:pygame.font.Font(FONT,int(k)) for k in ['10','15','20','25','30','35','40','45','50','55','60','65'] }

# print(main_surfaces)