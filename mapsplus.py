import pygame
import pygame.locals
import ConfigParser
import BRB
import warhammer

def load_tile_table(filename, width, height):
    image = pygame.image.load(filename).convert()
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width/width):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height/height):
            rect = (tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))
    return tile_table


class Level(object):
    def load_file(self, filename="level.map"):
        self.map = []
        self.key = {}
        parser = ConfigParser.ConfigParser()
        parser.read(filename)
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
        self.items = {}
        for y, line in enumerate(self.map):
            for x, c in enumerate(line):
                if not self.is_wall(x, y) and 'sprite' in self.key[c]:
                    self.items[(x, y)] = self.key[c]
        self.width = len(self.map[0])
        self.height = len(self.map)

    def get_tile(self, x, y):
        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_tile(self, x, y):
        """Tell what's at the specified position of the map."""

        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def get_bool(self, x, y, name):
        """Tell if the specified flag is set for position on the map."""

        value = self.get_tile(x, y).get(name)
        return value in (True, 1, 'true', 'yes', 'True', 'Yes', '1', 'on', 'On')

    def is_wall(self, x, y):
        """Is there a wall?"""

        return self.get_bool(x, y, 'wall')

    def is_blocking(self, x, y):
        """Is this place blocking movement?"""

        if not 0 <= x < self.width or not 0 <= y < self.height:
            return True
        return self.get_bool(x, y, 'block')

    def is_wall(self, x, y):
        return self.get_bool(x, y, 'wall')

    def render(self):
        wall = self.is_wall
        tiles = MAP_CACHE[self.tileset]
        image = pygame.Surface((self.width*MAP_TILE_WIDTH, self.height*MAP_TILE_HEIGHT))
        overlays = {}
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                if wall(map_x, map_y):
                    # Draw different tiles depending on neighbourhood
                    if not wall(map_x, map_y+1):
                        if wall(map_x+1, map_y) and wall(map_x-1, map_y):
                            tile = 1, 2
                        elif wall(map_x+1, map_y):
                            tile = 0, 2
                        elif wall(map_x-1, map_y):
                            tile = 2, 2
                        else:
                            tile = 3, 2
                    else:
                        if wall(map_x+1, map_y+1) and wall(map_x-1, map_y+1):
                            tile = 1, 1
                        elif wall(map_x+1, map_y+1):
                            tile = 0, 1
                        elif wall(map_x-1, map_y+1):
                            tile = 2, 1
                        else:
                            tile = 3, 1
                    # Add overlays if the wall may be obscuring something
                    if not wall(map_x, map_y-1):
                        if wall(map_x+1, map_y) and wall(map_x-1, map_y):
                            over = 1, 0
                        elif wall(map_x+1, map_y):
                            over = 0, 0
                        elif wall(map_x-1, map_y):
                            over = 2, 0
                        else:
                            over = 3, 0
                        overlays[(map_x, map_y)] = tiles[over[0]][over[1]]
                else:
                    try:
                        tile = self.key[c]['tile'].split(',')
                        tile = int(tile[0]), int(tile[1])
                    except (ValueError, KeyError):
                        # Default to ground tile
                        tile = 0, 3
                tile_image = tiles[tile[0]][tile[1]]
                image.blit(tile_image,
                           (map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT))
        return image, overlays

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), frames=None):
        super(Sprite, self).__init__()
        self.image = frames[0][0]
        self.rect = self.image.get_rect()
        self.pos = pos
        self.frames = frames
        self.animation = self.stand_animation()

    def stand_animation(self):
        while True:
            for frame in self.frames[0]:
                self.image = frame
                yield None
                yield None

    def update(self, *args):
        self.animation.next()

    def _get_pos(self):
        """Check the current position of the sprite on the map."""

        return (self.rect.midbottom[0]-12)/24, (self.rect.midbottom[1]-16)/16

    def _set_pos(self, pos):
        """Set the position and depth of the sprite on the map."""

        self.rect.midbottom = pos[0]*24+12, pos[1]*16+16
        self.depth = self.rect.midbottom[1]

    pos = property(_get_pos, _set_pos)

    def move(self, dx, dy):
        """Change the position of the sprite on screen."""

        self.rect.move_ip(dx, dy)
        self.depth = self.rect.midbottom[1]

class TileCache:
    """Load the tilesets lazily into global cache"""

    def __init__(self,  width=32, height=None):
        self.width = width
        self.height = height or width
        self.cache = {}

    def __getitem__(self, filename):
        """Return a table of tiles, load it from disk if needed."""

        key = (filename, self.width, self.height)
        try:
            return self.cache[key]
        except KeyError:
            tile_table = self._load_tile_table(filename, self.width,
                                               self.height)
            self.cache[key] = tile_table
            return tile_table

    def _load_tile_table(self, filename, width, height):
        """Load an image and split it into tiles."""

        image = pygame.image.load(filename).convert()
        image_width, image_height = image.get_size()
        tile_table = []
        for tile_x in range(0, image_width/width):
            line = []
            tile_table.append(line)
            for tile_y in range(0, image_height/height):
                rect = (tile_x*width, tile_y*height, width, height)
                line.append(image.subsurface(rect))
        return tile_table

def Movement():
    pass



if __name__ == "__main__":



    level = Level()
    level.load_file('level.map')
    print dir(level), 
    screen = pygame.display.set_mode((len(level.map[0])*24, len(level.map)*16))
    MAP_TILE_WIDTH = 24
    MAP_TILE_HEIGHT = 16
    MAP_CACHE = {
        'ground.png': load_tile_table('ground.png', MAP_TILE_WIDTH,
                                      MAP_TILE_HEIGHT),
    }
    SPRITE_CACHE = TileCache(32, 32)
    sprites = pygame.sprite.RenderUpdates()
    skelly = []
    Unit1 = []
    Unit2 = []
    Unit1.minX = 0
    for pos, tile in level.items.iteritems():
        sprite = Sprite(pos, SPRITE_CACHE[tile["sprite"]])
        if tile['name'] == 'skeleton':
            print pos
            if pos[1] < 12:
                Unit1.append((sprite,BRB.Model(4,3,3,4,4,1,2,2,9,2,1,10)))
            else:
                Unit2.append((sprite,BRB.Model(4,3,3,4,4,1,2,2,9,2,1,10)))
            skelly.append(sprite)
        sprites.add(sprite)

    clock = pygame.time.Clock()

    background, overlay_dict = level.render()
    overlays = pygame.sprite.RenderUpdates()
    sprites.clear(screen, background)
    sprites.update()
    dirty = sprites.draw(screen)
    overlays.draw(screen)
    pygame.display.update(dirty)
    clock.tick(15)
    overlays = pygame.sprite.RenderUpdates()
    for (x, y), image in overlay_dict.iteritems():
        overlay = pygame.sprite.Sprite(overlays)
        overlay.image = image
        overlay.rect = image.get_rect().move(x * 24, y * 16 - 16)
    screen.blit(background, (0, 0))
    overlays.draw(screen)
    pygame.display.flip()
    turn = 0
    mover =0
    moves = 4
    unit = Unit1
    movesleft = 4
    while turn < 6:
        print "turn",turn

        # XXX draw all the objects here
        sprites.clear(screen, background)
        sprites.update()
        dirty = sprites.draw(screen)
        overlays.draw(screen)
        pygame.display.update(dirty)
        clock.tick(15)
        if movesleft <= 0:
            movesleft = moves
            if mover == 0:
                print "player 1's moves"
                mover = 1
                unit = Unit2
                turn += 1
            else:
                print "player 2's moves"
                mover = 0
                unit = Unit1
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
                turn = 6
            elif event.type == pygame.locals.KEYDOWN:
                pressed_key = event.key
                move=(0,0)
                if pressed_key == 273:
                    print 'up'
                    move = (0,-16)
                elif pressed_key == 274:
                    print 'down'
                    move=(0,16)
                elif pressed_key == 275:
                    print 'right'
                    move=(24,0)
                elif pressed_key == 276:
                    print 'left'
                    move=(-24,0)
                elif pressed_key == 27:
                    print "bye"
                    turn = 6
                    game_over = True
                block = True
                blockerpos1 = (sprites.spritedict[unit[0][0]].x+move[0])/24+1,(sprites.spritedict[unit[0][0]].y+move[1])/16+1
                blockerpos2 = (sprites.spritedict[unit[-1][0]].x+move[0])/24+1,(sprites.spritedict[unit[-1][0]].y+move[1])/16+1
                if level.is_blocking(*blockerpos1) or level.is_blocking(*blockerpos2):
                    block = False
                if block:
                    movesleft -= 1
                    for item in unit:
                        item[0].move(*move)
