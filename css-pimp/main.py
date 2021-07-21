# Load Gtk
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

builder = Gtk.Builder()
builder.add_from_file('main.ui')

def apply_css():
    screen = Gdk.Screen.get_default()
    css_provider = Gtk.CssProvider()
    try:
        css_provider.load_from_path('main.css')
    except GLib.Error as e:
        print(f"Error in theme: {e} ")
    context = Gtk.StyleContext()
    context.add_provider_for_screen(screen, css_provider,
                                    Gtk.STYLE_PROVIDER_PRIORITY_USER)
    

def on_button_clicked(widget):
    label = widget.get_label()
    print(f'Button {label} Pressed')    
    if label == 'Toggle Overlay':
        overlay = builder.get_object('overlay')
        visible = overlay.get_visible()
        overlay.set_visible(not visible)
        
        
    
# When the application is launched…
def on_activate(app):
    win = builder.get_object('mainwin')
    win.set_application(app)
    win.set_title("CSS Test")
    win.set_default_size(800, 800)
    # Setup main box
    main = builder.get_object('main')
    btn = Gtk.Button()
    btn.props.label = "Toggle Overlay"
    btn.props.valign = Gtk.Align.START
    btn.props.halign = Gtk.Align.CENTER
    btn.connect('clicked', on_button_clicked)
    main.pack_start(btn, True, True, 0)
    main.show_all()
    # setup overlay box
    overlay = builder.get_object('overlay')
    btn = Gtk.Button()
    btn.props.label = "Touch Me"
    btn.props.valign = Gtk.Align.CENTER
    btn.props.halign = Gtk.Align.CENTER
    btn.connect('clicked', on_button_clicked)
    overlay.pack_start(btn, True, True, 0)
    overlay.show_all()
    apply_css()
    win.present()


# Create a new application
app = Gtk.Application(application_id='dk.rasmil.CssTest')
app.connect('activate', on_activate)

# Run the application
app.run(None)