import sys
import os
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib  # type: ignore


class App(Gtk.Application):
    __gtype_name__ = 'GtkMyApp'

    def __init__(self):
        Gtk.Application.__init__(self, application_id="dk.rasmil.gtk4csspimp")
        self.connect("activate", self.on_activate)
        self.builder = Gtk.Builder()
        self.builder.add_from_file('main.ui')
        self.css_provider = self.load_css('main.css')

    def on_activate(self, app):
        self.window = self.builder.get_object('mainwin')
        self.window.set_application(app)
        self.window.set_title("CSS in GTK4 Test")
        self.window.set_default_size(800, 800)
        # Setup main box
        self.main = self.builder.get_object('main')
        btn = Gtk.Button()
        btn.props.label = "Toggle Overlay"
        btn.props.valign = Gtk.Align.START
        btn.props.halign = Gtk.Align.CENTER
        btn.props.vexpand = True
        btn.props.hexpand = True
        btn.connect('clicked', self.on_button_clicked)
        self.main.append(btn)
        # setup overlay box
        self.overlay = self.builder.get_object('overlay')
        btn = Gtk.Button()
        btn.props.label = "Touch Me"
        btn.props.valign = Gtk.Align.CENTER
        btn.props.halign = Gtk.Align.CENTER
        btn.props.vexpand = True
        btn.props.hexpand = True
        btn.connect('clicked', self.on_button_clicked)
        self.overlay.append(btn)
        self.add_custom_styling(self.window)
        self.window.present()

    def on_button_clicked(self, widget):
        label = widget.get_label()
        print(f'Button {label} Pressed')
        if label == 'Toggle Overlay':
            visible = self.overlay.get_visible()
            self.overlay.set_visible(not visible)

    def load_css(self, css_fn):
        """create a provider for custom styling"""
        css_provider = None
        if css_fn and os.path.exists(css_fn):
            css_provider = Gtk.CssProvider()
            try:
                css_provider.load_from_path(css_fn)
            except GLib.Error as e:
                print(f"Error loading CSS : {e} ")
                return None
            print(f'loading custom styling : {css_fn}')
        return css_provider

    def _add_widget_styling(self, widget):
        if self.css_provider:
            context = widget.get_style_context()
            context.add_provider(
                self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def add_custom_styling(self, widget):
        self._add_widget_styling(widget)
        # iterate children recursive
        for child in widget:
            self.add_custom_styling(child)


if __name__ == '__main__':
    app = App()
    app.run(sys.argv)
