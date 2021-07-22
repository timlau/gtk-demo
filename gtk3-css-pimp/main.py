import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib  # type: ignore


class App(Gtk.Application):
    __gtype_name__ = 'GtkMyApp'

    def __init__(self):
        Gtk.Application.__init__(self, application_id="dk.rasmil.csspimp")
        self.connect("activate", self.on_activate)
        self.builder = Gtk.Builder()
        self.builder.add_from_file('main.ui')

    def on_activate(self, app):
        self.window = self.builder.get_object('mainwin')
        self.window.set_application(app)
        self.window.set_title("CSS Test")
        self.window.set_default_size(800, 800)
        # Setup main box
        self.main = self.builder.get_object('main')
        btn = Gtk.Button()
        btn.props.label = "Toggle Overlay"
        btn.props.valign = Gtk.Align.START
        btn.props.halign = Gtk.Align.CENTER
        btn.connect('clicked', self.on_button_clicked)
        self.main.pack_start(btn, True, True, 0)
        self.main.show_all()
        # setup overlay box
        self.overlay = self.builder.get_object('overlay')
        btn = Gtk.Button()
        btn.props.label = "Touch Me"
        btn.props.valign = Gtk.Align.CENTER
        btn.props.halign = Gtk.Align.CENTER
        btn.connect('clicked', self.on_button_clicked)
        self.overlay.pack_start(btn, True, True, 0)
        self.overlay.show_all()
        self.apply_css()
        self.window.present()

    def apply_css(self):
        screen = Gdk.Screen.get_default()
        css_provider = Gtk.CssProvider()
        try:
            css_provider.load_from_path('main.css')
            context = Gtk.StyleContext()
            context.add_provider_for_screen(screen, css_provider,
                                            Gtk.STYLE_PROVIDER_PRIORITY_USER)
        except GLib.Error as e:
            print(f"Error in theme: {e} ")

    def on_button_clicked(self, widget):
        label = widget.get_label()
        print(f'Button {label} Pressed')
        if label == 'Toggle Overlay':
            visible = self.overlay.get_visible()
            self.overlay.set_visible(not visible)


if __name__ == '__main__':
    app = App()
    app.run(sys.argv)
