"""
This program is to generate chain reaction game
"""

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from functools import partial
from kivy.vector import Vector

grid_type_critical_mass = {
    'clt': 1,
    'clb': 1,
    'crt': 1,
    'crb': 1,
    'edl': 2,
    'edr': 2,
    'edt': 2,
    'edb': 2,
    'mid': 3
}

grid_type_bubble_index = {
    'clt': [1, 0],
    'clb': [0, 1],
    'crt': [1, 0],
    'crb': [0, 1],
    'edl': [1, 2, 0],
    'edr': [0, 2, 1],
    'edt': [2, 1, 0],
    'edb': [0, 1, 2],
    'mid': [0, 3, 2, 1]
}


class Bubble(Widget):
    def __init__(self, bubble_color=None, **kwargs):
        super().__init__(**kwargs)
        self.bubble_color = bubble_color
        if self.bubble_color == "green":
            with self.canvas.after:
                self.bubble_color_code = Color(rgba=(0, 1, 0, 1))
                self.bubble_ellipse = Ellipse(pos=self.pos, size=self.size)
        elif self.bubble_color == "red":
            with self.canvas.after:
                self.bubble_color_code = Color(rgba=(1, 0, 0, 1))
                self.bubble_ellipse = Ellipse(pos=self.pos, size=self.size)
        elif self.bubble_color is None:
            with self.canvas.after:
                self.bubble_color_code = Color(rgba=(1, 1, 1, 1))
                self.bubble_ellipse = Ellipse(pos=self.pos, size=self.size)

        self.bind(pos=self.update_bubble_func, size=self.update_bubble_func)

    def change_bubble_color_func(self, bubble_color):
        if bubble_color == "green":
            self.bubble_color_code.rgba = (0, 1, 0, 1)
            self.bubble_color = "green"
        elif bubble_color == "red":
            self.bubble_color_code.rgba = (1, 0, 0, 1)
            self.bubble_color = "red"

    def update_bubble_func(self, instance, value):
        self.bubble_ellipse.size = instance.size
        self.bubble_ellipse.pos = instance.pos


class Grid(Widget):
    def __init__(self, grid_type="mid", **kwargs):
        super().__init__(**kwargs)
        self.grid_type = grid_type
        self.critical_mass = grid_type_critical_mass.get(self.grid_type)
        self.grid_color = ""
        self.bubble = []
        self.bubble_count = len(self.bubble)
        self.exploding_1 = False
        self.exploding_2 = False
        self.exploding_3 = False
        self.exploding_4 = False
        self.exploding = False
        self.bind(size=self.update_grid_func, pos=self.update_grid_func)

    def add_bubble_1_func(self, bubble_color):
        self.bubble.insert(0, Bubble(bubble_color=bubble_color, size=(self.width/3, self.height/3)))
        self.bubble[0].center = self.center
        self.add_widget(self.bubble[0])
        self.grid_color = bubble_color
        self.bubble_count = len(self.bubble)

    def add_bubble_2_func(self, bubble_color):
        if self.grid_color != bubble_color:
            self.bubble[0].change_bubble_color_func(bubble_color)
        self.bubble.insert(1, Bubble(bubble_color=bubble_color, size=(self.width/3, self.height/3)))
        self.bubble[0].center = (self.center_x, (self.center_y - (self.height / 6)))
        self.bubble[1].center = (self.center_x, (self.center_y + (self.height / 6)))
        self.add_widget(self.bubble[1])
        self.grid_color = bubble_color
        self.bubble_count = len(self.bubble)

    def add_bubble_3_func(self, bubble_color):
        if self.grid_color != bubble_color:
            self.bubble[0].change_bubble_color_func(bubble_color)
            self.bubble[1].change_bubble_color_func(bubble_color)
        self.bubble.insert(2, Bubble(bubble_color=bubble_color, size=(self.width/3, self.height/3)))
        self.bubble[0].center = ((self.center_x - (self.width / 6)), (self.center_y - (self.height / 6)))
        self.bubble[1].center = ((self.center_x + (self.width / 6)), (self.center_y - (self.height / 6)))
        self.bubble[2].center = (self.center_x, (self.center_y + (self.height / 6)))
        self.add_widget(self.bubble[2])
        self.grid_color = bubble_color
        self.bubble_count = len(self.bubble)

    def add_bubble_4_func(self, bubble_color):
        if self.grid_color != bubble_color:
            self.bubble[0].change_bubble_color_func(bubble_color)
            self.bubble[1].change_bubble_color_func(bubble_color)
            self.bubble[2].change_bubble_color_func(bubble_color)
        self.bubble.insert(3, Bubble(bubble_color=bubble_color, size=(self.width/3, self.height/3)))
        self.bubble[0].center = ((self.center_x - (self.width / 6)), (self.center_y - (self.height / 6)))
        self.bubble[1].center = ((self.center_x + (self.width / 6)), (self.center_y - (self.height / 6)))
        self.bubble[2].center = ((self.center_x - (self.width / 6)), (self.center_y + (self.height / 6)))
        self.bubble[3].center = ((self.center_x + (self.width / 6)), (self.center_y + (self.height / 6)))
        self.add_widget(self.bubble[3])
        self.grid_color = bubble_color
        self.bubble_count = len(self.bubble)

    def exploding_func(self):
        self.exploding = self.exploding_1 or self.exploding_2 or self.exploding_3 or self.exploding_4
        return self.exploding

    def update_grid_func(self, instance, value):
        for i in range(self.bubble_count):
            self.bubble[i].size = (instance.width/3, instance.height/3)

        if self.bubble_count == 1:
            self.bubble[0].center = instance.center
        elif self.bubble_count == 2:
            self.bubble[0].center = (self.center_x, (self.center_y - (self.height / 6)))
            self.bubble[1].center = (self.center_x, (self.center_y + (self.height / 6)))
        elif self.bubble_count == 3:
            self.bubble[0].center = ((self.center_x - (self.width / 6)), (self.center_y - (self.height / 6)))
            self.bubble[1].center = ((self.center_x + (self.width / 6)), (self.center_y - (self.height / 6)))
            self.bubble[2].center = (self.center_x, (self.center_y + (self.height / 6)))
        elif self.bubble_count == 4:
            self.bubble[0].center = ((self.center_x - (self.width / 6)), (self.center_y - (self.height / 6)))
            self.bubble[1].center = ((self.center_x + (self.width / 6)), (self.center_y - (self.height / 6)))
            self.bubble[2].center = ((self.center_x - (self.width / 6)), (self.center_y + (self.height / 6)))
            self.bubble[3].center = ((self.center_x + (self.width / 6)), (self.center_y + (self.height / 6)))


class Game(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 8
        self.columns = 8
        self.grid_size = 55
        self.grid_array = []
        self.any_grid_exploding = False
        self.player_green = True
        self.player_red = False
        self.green_points = 0
        self.red_points = 0
        self.winner = False
        self.build_grid_array_func()
        self.bind(size=self.update_game_func, pos=self.update_game_func)

    def build_grid_array_func(self):
        for i in range(self.rows):
            grid_list = []
            for j in range(self.columns):
                if i == 0 and j == 0:
                    grid_list.append(Grid(grid_type="clb"))
                elif i == 0 and j == self.columns - 1:
                    grid_list.append(Grid(grid_type="clt"))
                elif i == self.rows - 1 and j == 0:
                    grid_list.append(Grid(grid_type="crb"))
                elif i == self.rows - 1 and j == self.columns - 1:
                    grid_list.append(Grid(grid_type="crt"))
                elif i == 0:
                    grid_list.append(Grid(grid_type="edl"))
                elif j == 0:
                    grid_list.append(Grid(grid_type="edb"))
                elif i == self.rows - 1:
                    grid_list.append(Grid(grid_type="edr"))
                elif j == self.columns - 1:
                    grid_list.append(Grid(grid_type="edt"))
                else:
                    grid_list.append(Grid(grid_type="mid"))

            self.grid_array.append(grid_list)

        for grid_list in self.grid_array:
            for grid in grid_list:
                self.add_widget(grid)

    def update_game_func(self, instance, value):
        grid_w = self.grid_size / instance.width
        grid_h = self.grid_size / instance.height
        grid_x = (instance.width - (self.grid_size * self.rows)) / 2

        for grid_list in self.grid_array:
            grid_y = (instance.height - (self.grid_size * self.columns)) / 2
            for grid in grid_list:
                grid.size_hint = (grid_w, grid_h)
                grid.pos = (grid_x, grid_y)
                grid_y += self.grid_size
            grid_x += self.grid_size

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        self.any_grid_exploding_func()
        if not self.any_grid_exploding and not self.winner:
            for grid_list in self.grid_array:
                for grid in grid_list:
                    if grid.collide_point(touch.pos[0], touch.pos[1]):
                        if self.player_green and (len(grid.children) == 0 or grid.grid_color == "green"):
                            bubble_color = "green"
                            self.add_bubble_func(grid, bubble_color)
                            self.player_green = False
                            self.player_red = True
                            self.player_l.text = "Red Player Turn"
                        elif self.player_red and (len(grid.children) == 0 or grid.grid_color == "red"):
                            bubble_color = "red"
                            self.add_bubble_func(grid, bubble_color)
                            self.player_red = False
                            self.player_green = True
                            self.player_l.text = "Green Player Turn"

    def add_bubble_func(self, grid, bubble_color):
        grid.bubble_count = len(grid.children)
        bubble_count_add_bubble = {
            0: partial(grid.add_bubble_1_func, bubble_color),
            1: partial(grid.add_bubble_2_func, bubble_color),
            2: partial(grid.add_bubble_3_func, bubble_color),
            3: partial(grid.add_bubble_4_func, bubble_color)
        }
        if grid.bubble_count < grid.critical_mass:
            callback = bubble_count_add_bubble.get(grid.bubble_count)
            callback()
        elif grid.bubble_count == grid.critical_mass:
            callback = bubble_count_add_bubble.get(grid.bubble_count)
            callback()
            self.explode_func(grid, bubble_color)

        self.point_calc_func()

    def explode_func(self, grid, bubble_color):
        if grid.grid_type == "clt":
            right_grid = self.right_grid_func(grid)
            bottom_grid = self.bottom_grid_func(grid)
            self.corner_grid_explode_func(grid, right_grid, bottom_grid, bubble_color)

        elif grid.grid_type == "clb":
            right_grid = self.right_grid_func(grid)
            top_grid = self.top_grid_func(grid)
            self.corner_grid_explode_func(grid, right_grid, top_grid, bubble_color)

        elif grid.grid_type == "crt":
            left_grid = self.left_grid_func(grid)
            bottom_grid = self.bottom_grid_func(grid)
            self.corner_grid_explode_func(grid, left_grid, bottom_grid, bubble_color)

        elif grid.grid_type == "crb":
            left_grid = self.left_grid_func(grid)
            top_grid = self.top_grid_func(grid)
            self.corner_grid_explode_func(grid, left_grid, top_grid, bubble_color)

        elif grid.grid_type == "edl":
            right_grid = self.right_grid_func(grid)
            top_grid = self.top_grid_func(grid)
            bottom_grid = self.bottom_grid_func(grid)
            self.edge_grid_explode_func(grid, right_grid, top_grid, bottom_grid, bubble_color)

        elif grid.grid_type == "edr":
            left_grid = self.left_grid_func(grid)
            top_grid = self.top_grid_func(grid)
            bottom_grid = self.bottom_grid_func(grid)
            self.edge_grid_explode_func(grid, left_grid, top_grid, bottom_grid, bubble_color)

        elif grid.grid_type == "edt":
            left_grid = self.left_grid_func(grid)
            right_grid = self.right_grid_func(grid)
            bottom_grid = self.bottom_grid_func(grid)
            self.edge_grid_explode_func(grid, left_grid, right_grid, bottom_grid, bubble_color)

        elif grid.grid_type == "edb":
            left_grid = self.left_grid_func(grid)
            right_grid = self.right_grid_func(grid)
            top_grid = self.top_grid_func(grid)
            self.edge_grid_explode_func(grid, left_grid, right_grid, top_grid, bubble_color)

        elif grid.grid_type == "mid":
            left_grid = self.left_grid_func(grid)
            right_grid = self.right_grid_func(grid)
            top_grid = self.top_grid_func(grid)
            bottom_grid = self.bottom_grid_func(grid)
            self.middle_grid_explode_func(grid, left_grid, right_grid, top_grid, bottom_grid, bubble_color)

    def left_grid_func(self, grid):
        for index, grid_list in enumerate(self.grid_array):
            if grid in grid_list:
                j = grid_list.index(grid)
                i = index

        if i != 0:
            left_grid = self.grid_array[i - 1][j]
        else:
            left_grid = None

        return left_grid

    def right_grid_func(self, grid):
        for index, grid_list in enumerate(self.grid_array):
            if grid in grid_list:
                j = grid_list.index(grid)
                i = index

        if i != (self.columns - 1):
            right_grid = self.grid_array[i + 1][j]
        else:
            right_grid = None

        return right_grid

    def top_grid_func(self, grid):
        for index, grid_list in enumerate(self.grid_array):
            if grid in grid_list:
                j = grid_list.index(grid)
                i = index

        if j != (self.columns - 1):
            top_grid = self.grid_array[i][j + 1]
        else:
            top_grid = None

        return top_grid

    def bottom_grid_func(self, grid):
        for index, grid_list in enumerate(self.grid_array):
            if grid in grid_list:
                j = grid_list.index(grid)
                i = index

        if j != 0:
            bottom_grid = self.grid_array[i][j - 1]
        else:
            bottom_grid = None

        return bottom_grid

    def corner_grid_explode_func(self, grid, adj_grid_1, adj_grid_2, bubble_color):
        grid_bubble_index_0 = grid_type_bubble_index.get(grid.grid_type)[0]
        grid_bubble_index_1 = grid_type_bubble_index.get(grid.grid_type)[1]
        adj_move_1 = Vector(adj_grid_1.center) - Vector(grid.bubble[grid_bubble_index_0].center)
        adj_move_2 = Vector(adj_grid_2.center) - Vector(grid.bubble[grid_bubble_index_1].center)
        Clock.schedule_interval(
            partial(self.bubble_explode_func, grid, grid.bubble[grid_bubble_index_0], adj_move_1, adj_grid_1,
                    "explode_1"), 1.0 / 60.0)
        Clock.schedule_interval(
            partial(self.bubble_explode_func, grid, grid.bubble[grid_bubble_index_1], adj_move_2, adj_grid_2,
                    "explode_2"), 1.0 / 60.0)
        Clock.schedule_interval(
            partial(self.grid_2_explode_func, grid, adj_grid_1, adj_grid_2, bubble_color),
            1.0 / 60.0)

    def edge_grid_explode_func(self, grid, adj_grid_1, adj_grid_2, adj_grid_3, bubble_color):
        grid_bubble_index_0 = grid_type_bubble_index.get(grid.grid_type)[0]
        grid_bubble_index_1 = grid_type_bubble_index.get(grid.grid_type)[1]
        grid_bubble_index_2 = grid_type_bubble_index.get(grid.grid_type)[2]
        adj_move_1 = Vector(adj_grid_1.center) - Vector(grid.bubble[grid_bubble_index_0].center)
        adj_move_2 = Vector(adj_grid_2.center) - Vector(grid.bubble[grid_bubble_index_1].center)
        adj_move_3 = Vector(adj_grid_3.center) - Vector(grid.bubble[grid_bubble_index_2].center)
        Clock.schedule_interval(
            partial(self.bubble_explode_func, grid, grid.bubble[grid_bubble_index_0], adj_move_1, adj_grid_1,
                    "explode_1"), 1.0 / 60.0)
        Clock.schedule_interval(
            partial(self.bubble_explode_func, grid, grid.bubble[grid_bubble_index_1], adj_move_2, adj_grid_2,
                    "explode_2"), 1.0 / 60.0)
        Clock.schedule_interval(
            partial(self.bubble_explode_func, grid, grid.bubble[grid_bubble_index_2], adj_move_3, adj_grid_3,
                    "explode_3"), 1.0 / 60.0)
        Clock.schedule_interval(
            partial(self.grid_3_explode_func, grid, adj_grid_1, adj_grid_2, adj_grid_3, bubble_color),
            1.0 / 60.0)

    def middle_grid_explode_func(self, grid, adj_grid_1, adj_grid_2, adj_grid_3, adj_grid_4, bubble_color):
        grid_bubble_index_0 = grid_type_bubble_index.get(grid.grid_type)[0]
        grid_bubble_index_1 = grid_type_bubble_index.get(grid.grid_type)[1]
        grid_bubble_index_2 = grid_type_bubble_index.get(grid.grid_type)[2]
        grid_bubble_index_3 = grid_type_bubble_index.get(grid.grid_type)[3]
        adj_move_1 = Vector(adj_grid_1.center) - Vector(grid.bubble[grid_bubble_index_0].center)
        adj_move_2 = Vector(adj_grid_2.center) - Vector(grid.bubble[grid_bubble_index_1].center)
        adj_move_3 = Vector(adj_grid_3.center) - Vector(grid.bubble[grid_bubble_index_2].center)
        adj_move_4 = Vector(adj_grid_4.center) - Vector(grid.bubble[grid_bubble_index_3].center)
        Clock.schedule_interval(
            partial(self.bubble_explode_func, grid, grid.bubble[grid_bubble_index_0], adj_move_1, adj_grid_1, "explode_1"),
            1.0 / 60.0)
        Clock.schedule_interval(
            partial(self.bubble_explode_func, grid, grid.bubble[grid_bubble_index_1], adj_move_2, adj_grid_2, "explode_2"),
            1.0 / 60.0)
        Clock.schedule_interval(
            partial(self.bubble_explode_func, grid, grid.bubble[grid_bubble_index_2], adj_move_3, adj_grid_3, "explode_3"),
            1.0 / 60.0)
        Clock.schedule_interval(
            partial(self.bubble_explode_func, grid, grid.bubble[grid_bubble_index_3], adj_move_4, adj_grid_4, "explode_4"),
            1.0 / 60.0)
        Clock.schedule_interval(
            partial(self.grid_4_explode_func, grid, adj_grid_1, adj_grid_2, adj_grid_3, adj_grid_4, bubble_color),
            1.0 / 60.0)

    def grid_4_explode_func(self, grid, adj_grid_1, adj_grid_2, adj_grid_3, adj_grid_4, bubble_color, dt):
        grid_exploding = grid.exploding_1 or grid.exploding_2 or grid.exploding_3 or grid.exploding_4
        adj_grid_1_exploding = adj_grid_1.exploding_1 or adj_grid_1.exploding_2 or adj_grid_1.exploding_3 or adj_grid_1.exploding_4
        adj_grid_2_exploding = adj_grid_2.exploding_1 or adj_grid_2.exploding_2 or adj_grid_2.exploding_3 or adj_grid_2.exploding_4
        adj_grid_3_exploding = adj_grid_3.exploding_1 or adj_grid_3.exploding_2 or adj_grid_3.exploding_3 or adj_grid_3.exploding_4
        adj_grid_4_exploding = adj_grid_4.exploding_1 or adj_grid_4.exploding_2 or adj_grid_4.exploding_3 or adj_grid_4.exploding_4
        if not grid_exploding and not adj_grid_1_exploding and not adj_grid_2_exploding and not adj_grid_3_exploding and not adj_grid_4_exploding:
            self.add_bubble_func(adj_grid_1, bubble_color)
            self.add_bubble_func(adj_grid_2, bubble_color)
            self.add_bubble_func(adj_grid_3, bubble_color)
            self.add_bubble_func(adj_grid_4, bubble_color)
            return False
        else:
            return True

    def grid_3_explode_func(self, grid, adj_grid_1, adj_grid_2, adj_grid_3, bubble_color, dt):
        grid_exploding = grid.exploding_1 or grid.exploding_2 or grid.exploding_3 or grid.exploding_4
        adj_grid_1_exploding = adj_grid_1.exploding_1 or adj_grid_1.exploding_2 or adj_grid_1.exploding_3 or adj_grid_1.exploding_4
        adj_grid_2_exploding = adj_grid_2.exploding_1 or adj_grid_2.exploding_2 or adj_grid_2.exploding_3 or adj_grid_2.exploding_4
        adj_grid_3_exploding = adj_grid_3.exploding_1 or adj_grid_3.exploding_2 or adj_grid_3.exploding_3 or adj_grid_3.exploding_4
        if not grid_exploding and not adj_grid_1_exploding and not adj_grid_2_exploding and not adj_grid_3_exploding:
            self.add_bubble_func(adj_grid_1, bubble_color)
            self.add_bubble_func(adj_grid_2, bubble_color)
            self.add_bubble_func(adj_grid_3, bubble_color)
            return False
        else:
            return True

    def grid_2_explode_func(self, grid, adj_grid_1, adj_grid_2, bubble_color, dt):
        grid_exploding = grid.exploding_1 or grid.exploding_2 or grid.exploding_3 or grid.exploding_4
        adj_grid_1_exploding = adj_grid_1.exploding_1 or adj_grid_1.exploding_2 or adj_grid_1.exploding_3 or adj_grid_1.exploding_4
        adj_grid_2_exploding = adj_grid_2.exploding_1 or adj_grid_2.exploding_2 or adj_grid_2.exploding_3 or adj_grid_2.exploding_4
        if not grid_exploding and not adj_grid_1_exploding and not adj_grid_2_exploding:
            self.add_bubble_func(adj_grid_1, bubble_color)
            self.add_bubble_func(adj_grid_2, bubble_color)
            return False
        else:
            return True

    def bubble_explode_func(self, grid, bubble, adj_move, adj_grid, explode_count, dt):
        if explode_count == "explode_1":
            grid.exploding_1 = True
        elif explode_count == "explode_2":
            grid.exploding_2 = True
        elif explode_count == "explode_3":
            grid.exploding_3 = True
        elif explode_count == "explode_4":
            grid.exploding_4 = True

        if round(bubble.center_x, 5) != round(adj_grid.center_x, 5) or round(bubble.center_y, 5) != round(
                adj_grid.center_y, 5):
            bubble.center = Vector(adj_move / 30) + bubble.center
            return True
        else:
            if explode_count == "explode_1":
                grid.exploding_1 = False
            elif explode_count == "explode_2":
                grid.exploding_2 = False
            elif explode_count == "explode_3":
                grid.exploding_3 = False
            elif explode_count == "explode_4":
                grid.exploding_4 = False
            if not grid.exploding_1 and not grid.exploding_2 and not grid.exploding_3 and not grid.exploding_4:
                grid.clear_widgets()
                grid.bubble = []
                return False
            else:
                return True

    def any_grid_exploding_func(self):
        self.any_grid_exploding = False
        for grid_list in self.grid_array:
            for grid in grid_list:
                self.any_grid_exploding = self.any_grid_exploding or grid.exploding_func()

    def point_calc_func(self):
        self.green_points = 0
        self.red_points = 0
        for grid_list in self.grid_array:
            for grid in grid_list:
                if grid.grid_color == "green":
                    self.green_points += len(grid.bubble)
                if grid.grid_color == "red":
                    self.red_points += len(grid.bubble)

        self.green_points_l.text = "Green Points : " + str(self.green_points)
        self.red_points_l.text = "Red Points : " + str(self.red_points)

        if self.green_points == 0 and self.red_points != 1 and not self.winner:
            self.player_l.text = "Red Player Win"
            self.winner = True
        elif self.red_points == 0 and self.green_points != 1 and not self.winner:
            self.player_l.text = "Green Player Win"
            self.winner = True


class ChainReaction(App):
    def build(self):
        game_l = Game()
        return game_l


if __name__ == "__main__":
    ChainReaction().run()
