class Actor:
    def __init__(self, image, coords):
        self.image = image
        self.coords = coords
    
    def draw(self, screen):
        screen.blit(self.image, (self.coords[0], self.coords[1]))