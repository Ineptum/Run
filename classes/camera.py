class Camera:
    def __init__(self, height):
        self.y_Difference = 0
        self.windowHeight = height

    def apply(self, obj):
        obj.rect.y -= int(self.y_Difference)

    def scroll_for(self, target, slow=True):
        self.y_Difference = int((target.rect.y + target.rect.h / 2 - self.windowHeight * (1 / 2)) /
                                (24 if slow else 1))
        return self.y_Difference
