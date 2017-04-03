import gi
import os
from os import path
from game import Game

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GLib, Gdk

GAME_SPEED = 35
THUG_SCORE = 100

class Window(Gtk.Window):

    def __init__(self, game=None):
        Gtk.Window.__init__(self, title='Flappy Bird Evolution Strategies')

        (width, height) = self.get_size()
        self.width = width
        self.height = height

        if game:
            self.game = game
        else:
            self.game = Game(width, height)

        self.fixed = Gtk.Fixed()
        self.birdie = Gtk.Image.new_from_file(path.join(path.dirname(__file__), 'assets/birdie.png'))
        self.fixed.add(self.birdie)

        self.wall_top = Gtk.Box()
        self.wall_bottom = Gtk.Box()

        bg = Gdk.RGBA(0.1, 1, 0.1, 1)
        self.wall_top.override_background_color(0, bg)
        self.wall_bottom.override_background_color(0, bg)

        self.fixed.add(self.wall_top)
        self.fixed.add(self.wall_bottom)

        self.add(self.fixed)

        self.gameover = Gtk.Label.new('')
        self.gameover.override_color(0, Gdk.RGBA(1, 0.2, 0.2, 1))

        self.score = Gtk.Label.new('')

        self.thug = Gtk.Image.new_from_file(path.join(path.dirname(__file__), 'assets/thug-text.png'))

        self.fixed.add(self.gameover)
        self.fixed.add(self.score)
        self.fixed.add(self.thug)
        self.fixed.move(self.gameover, width / 2, height / 2)
        self.fixed.move(self.score, 10, 10)
        self.fixed.move(self.thug, -75, -75)

        self.update()

        if not game:
            GLib.timeout_add(GAME_SPEED, self.update)

            self.connect("key-press-event", self.on_key)

    def update(self):
        if self.game.lost:
            self.gameover.set_text('Game Over!')
            return True
        else:
            self.gameover.set_text('')

        self.score.set_text(str(round(self.game.score, 2)))

        self.game.update()

        if self.game.score > THUG_SCORE:
            self.birdie.set_from_file(path.join(path.dirname(__file__), 'assets/birdie-thug.png'))
            self.fixed.move(self.thug, 10, self.height - 60)

        self.wall_top.set_size_request(self.game.wall.width, self.game.wall.gate.y)
        self.wall_bottom.set_size_request(self.game.wall.width, self.height - self.game.wall.gate.y - self.game.wall.gate.height)

        self.fixed.move(self.birdie, self.width / 2, self.game.bird.y)
        self.fixed.move(self.wall_top, self.game.wall.x, 0)
        self.fixed.move(self.wall_bottom, self.game.wall.x, self.game.wall.gate.y + self.game.wall.gate.height)

        return True

    def on_key(self, win, key):
        if key.keyval == Gdk.KEY_space:
            self.game.bird.jump()

        if key.keyval == Gdk.KEY_Return and self.game.lost:
            self.game = Game(self.game.width, self.game.height)


# win = Window()
# win.connect('delete-event', Gtk.main_quit)
# win.show_all()
# Gtk.main()
