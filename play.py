from win import Window
import gi
from gi.repository import Gtk, GLib, Gdk

win = Window()
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()
