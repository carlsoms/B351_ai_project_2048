import pygame

move_speed = 10


class Tile:
    def __init__(self, value, position):
        self.value = str(value)
        self.font_color = (249, 246, 242)
        self.text_size = 40
        self.position = ((position[0] * 60) + 10, (position[1] * 60) + 10)
        self.movable = True

        if value > 64:
            self.color = (237, 207, 114)
        elif value == 64:
            self.color = (246, 94, 59)
        elif value == 32:
            self.color = (246, 124, 95)
        elif value == 16:
            self.color = (245, 149, 99)
        elif value == 8:
            self.color = (242, 177, 121)
        elif value == 4:
            self.color = (237, 224, 200)
            self.font_color = (119, 110, 101)
        else:
            self.color = (238, 228, 218)
            self.font_color = (119, 110, 101)

    def get_tile(self):
        tile = pygame.Surface((50, 50))
        tile.fill(self.color)
        font = pygame.font.SysFont(None, (60 - (len(self.value) * 10)))
        text = font.render(self.value, True, self.font_color)
        text_rect = text.get_rect(center=(tile.get_height() / 2, tile.get_width() / 2))
        tile.blit(text, text_rect)
        return tile
