class GameShape:
    def __init__(self, id, start_p, end_p):
        self.id = id
        self.start_p = start_p
        self.end_p = end_p
        self.height = end_p[1] - start_p[1]
        self.width = end_p[0] - start_p[0]
        self.is_dragged = False
        self.center_point = self.get_center_point()

    def __str__(self):
        return "id = " + str(self.id) + " start = " + str(self.start_p) + " end = " + str(
            self.end_p) + " height = " + str(self.height) + " width = " + str(self.width) + " center = " + str(
            self.center_point) + " is_dragged = " + self.is_dragged

    def get_center_point(self):
        return (self.start_p[0] + self.end_p[0]) / 2, (self.start_p[1] + self.end_p[1]) / 2

    def is_point_in_area(self, point):
        area_left = self.center_point[0] - self.width // 2
        area_right = self.center_point[0] + self.width // 2
        area_above = self.center_point[1] - self.height // 2
        area_below = self.center_point[1] + self.height // 2
        if area_left < point[0] < area_right and area_above < point[1] < area_below:
            return True

    def update_position(self, point):
        h, w = self.height, self.width
        start_p = point[1] - w // 2, point[2] - h // 2
        end_p = point[1] + w // 2, point[2] + h // 2
        self.start_p = start_p
        self.end_p = end_p
        self.center_point = self.get_center_point()
