
class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)


class Light:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def extract_lights(self, grid):
        lights = []
        for i, y in enumerate(grid):
            for l, x in enumerate(y):
                if x == 1:
                    lights.append((l, i))
        return lights

    def extract_obstacles(self, grid):
        obstacles = []
        for i, y in enumerate(grid):
            for l, x in enumerate(y):
                if x == -1:
                    obstacles.append((l, i))
        return obstacles

    def lighten(self, grid):
        self.adaptee.set_dim((len(grid[0]), len(grid)))
        self.adaptee.set_lights(self.extract_lights(grid))
        self.adaptee.set_obstacles(self.extract_obstacles(grid))
        return self.adaptee.generate_lights()
