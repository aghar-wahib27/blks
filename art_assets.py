from vital import pygame
from extractor import DR,ui_assets,FONT


main_surfaces={k:pygame.image.load(v) for (k,v) in DR.items()}


UIS={k:pygame.image.load(v) for (k,v) in ui_assets.items()}



FFF=pygame.font.Font(FONT,30)


# print(main_surfaces)