import numpy as np
import matplotlib.pyplot as pyp


class SteelPlate:
    def __init__(self, x_dim, y_dim, ambiant_temperature, object_temp):
        self.x_dim = x_dim + 2
        self.y_dim = y_dim + 2

        outer_and_inner_temp = np.zeros((self.x_dim, self.y_dim)) + object_temp
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                if self._coords_are_on_side(x, y):
                    outer_and_inner_temp[x, y] = ambiant_temperature
        self.grid = outer_and_inner_temp

    def get_inner_grid(self):
        ret = np.zeros((self.x_dim - 2, self.y_dim - 2))
        for x in range(self.x_dim):
            for y in range(self.y_dim):
                if not self._coords_are_on_side(x, y):
                    ret[x - 1, y - 1] = self.grid[x, y]
        return ret

    def draw_picture(self):
        pyp.imshow(steel_plate.get_inner_grid(), origin="upper", extent=[0, self.x_dim - 2, 0, self.y_dim - 2],
                   interpolation="nearest")
        pyp.axis('off')

    def change_temp_inside_once(self):
        future_grid = self.grid

        for x in range(self.x_dim):
            for y in range(self.y_dim):
                if not self._coords_are_on_side(x, y):
                    new_value = (self.grid[x - 1, y] + self.grid[x + 1, y] + self.grid[x, y + 1] + self.grid[x, y - 1] +
                                 self.grid[x, y]) / 5
                    future_grid[x, y] = new_value
        self.grid = future_grid

    def change_temp_outside(self, x, y, temp):
        if self._coords_are_on_side(x, y):
            self.grid[x, y] = temp
        else:
            raise ValueError("the coords given aren't on the side of the plate")

    def _coords_are_on_side(self, x, y):
        return x == 0 or x + 1 == self.x_dim or y == 0 or y + 1 == self.y_dim

# steel_plate = np.array([[None, 0, 25, 25, 25, None],
#                        [0, 25, 25, 25, 25, 25],
#                        [25, 25, 25, 25, 25, 25],
#                        [25, 25, 25, 25, 25, 25],
#                        [25, 25, 25, 25, 25, 1000],
#                        [None, 25, 25, 25, 1000, None]])


steel_plate = SteelPlate(4, 4, 25, 13)


print(steel_plate.grid)
steel_plate.change_temp_outside(0, 1, 0)
steel_plate.change_temp_outside(1, 0, 0)
steel_plate.change_temp_outside(5, 4, 1000)
steel_plate.change_temp_outside(4, 5, 1000)
steel_plate.change_temp_inside_once()
print(steel_plate.grid)

print(steel_plate.get_inner_grid())
steel_plate.draw_picture()
pyp.show()
