#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk, GdkPixbuf
import feedparser
import subprocess
import os
import html

APP_VERSION = "1.0.0"
APP_NAME = "Linux Magnet Distro"
APP_AUTHOR = "smal"
APP_LICENSE = "MIT"
APP_DEPENDENCIES = [
    ("feedparser", "BSD", "https://pypi.org/project/feedparser/"),
    ("PyGObject", "LGPLv2.1+", "https://pygobject.readthedocs.io/"),
]

os.environ["GTK_CSD"] = "1"

# CSS loader
css_provider = Gtk.CssProvider()
css_provider.load_from_path("theme.css")
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER,
)

FEED_URL = "https://smal82.netsons.org/feed/distros/"

class FeedWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title=APP_NAME)
        self.set_border_width(0)
        self.set_default_size(740, 500)

        # HEADERBAR
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)

        # LOGO
        logo = Gtk.Image()
        try:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("logo.png", 40, 40)
            logo.set_from_pixbuf(pixbuf)
        except:
            logo.set_from_icon_name("image-missing", Gtk.IconSize.DIALOG)
        logo.get_style_context().add_class("header-logo")

        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        title_lbl = Gtk.Label(label=APP_NAME)
        title_lbl.get_style_context().add_class("title")
        title_lbl.set_xalign(0)
        subtitle_lbl = Gtk.Label(label="Le ultime distribuzioni con Magnet Link")
        subtitle_lbl.get_style_context().add_class("subtitle")
        subtitle_lbl.set_xalign(0)
        title_box.pack_start(title_lbl, False, False, 0)
        title_box.pack_start(subtitle_lbl, False, False, 0)

        left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        left_box.pack_start(logo, False, False, 0)
        left_box.pack_start(title_box, False, False, 0)

        header.pack_start(left_box)

        # Pulsante Info (stellina)
        about_btn = Gtk.Button()
        about_btn.set_tooltip_text("Info")
        about_btn.set_image(Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.BUTTON))
        about_btn.connect("clicked", self.show_about)
        header.pack_end(about_btn)

        # Pulsante Aggiorna
        refresh_btn = Gtk.Button()
        refresh_btn.set_tooltip_text("Aggiorna feed")
        refresh_btn.set_image(Gtk.Image.new_from_icon_name("view-refresh", Gtk.IconSize.BUTTON))
        refresh_btn.connect("clicked", self.on_refresh_clicked)
        header.pack_end(refresh_btn)

        self.set_titlebar(header)

        # Layout principale
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        self.add(vbox)

        # Lista feed
        self.liststore = Gtk.ListStore(str, str, str)
        self.treeview = Gtk.TreeView(model=self.liststore)
        renderer = Gtk.CellRendererText()
        renderer.props.weight = 700
        renderer.props.size_points = 13
        column = Gtk.TreeViewColumn("Titolo", renderer, text=0)
        self.treeview.append_column(column)
        self.treeview.connect("row-activated", self.on_row_activated)
        self.treeview.set_headers_visible(False)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_shadow_type(Gtk.ShadowType.IN)
        scrolled.add(self.treeview)
        vbox.pack_start(scrolled, True, True, 0)

        self.feed_entries = []
        self.load_feed()

    def load_feed(self):
        self.liststore.clear()
        self.feed_entries = []
        feed = feedparser.parse(FEED_URL)
        if feed.bozo:
            self.liststore.append(["❌ Errore nel caricamento del feed", "", ""])
            return
        for entry in feed.entries:
            magnet = ""
            if "enclosures" in entry and entry.enclosures:
                for enclosure in entry.enclosures:
                    if enclosure.get("type", "").startswith("application/x-bittorrent") or enclosure.get("href", "").startswith("magnet:"):
                        magnet = enclosure.get("href", "")
                        break
            self.liststore.append([entry.title, entry.get("summary", ""), magnet])
            self.feed_entries.append(entry)

    def on_refresh_clicked(self, button):
        self.load_feed()

    def on_row_activated(self, treeview, path, column):
        model = treeview.get_model()
        treeiter = model.get_iter(path)
        if treeiter is not None:
            title, summary, magnet = model[treeiter]
            DetailWindow(title, summary, magnet)

    def show_about(self, button):
        dep_string = "\n".join([f"{name}: {license} ({url})" for (name, license, url) in APP_DEPENDENCIES])
        about = Gtk.AboutDialog()
        about.set_program_name(APP_NAME)
        about.set_version(APP_VERSION)
        about.set_authors([APP_AUTHOR])
        about.set_license_type(Gtk.License.MIT_X11)
        about.set_comments(
            "Sviluppato da smal\n\n"
            "Dipendenze:\n" + dep_string
        )
        about.set_website("https://github.com/smal82/linux-magnet-distro")
        about.set_website_label("Pagina GitHub")
        about.set_copyright("© 2024-2025 smal")
        try:
            about.set_logo(GdkPixbuf.Pixbuf.new_from_file("logo.png"))
        except:
            pass
        about.run()
        about.destroy()

class DetailWindow(Gtk.Window):
    def __init__(self, title, summary, magnet):
        super().__init__(title=title)
        self.set_border_width(24)
        self.set_default_size(420, 270)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        self.add(vbox)

        title_label = Gtk.Label()
        try:
            from gi.repository import GLib
            safe_title = GLib.markup_escape_text(title)
        except ImportError:
            safe_title = html.escape(title)
        title_label.set_markup(f'<span size="x-large" weight="bold">{safe_title}</span>')
        title_label.set_xalign(0)
        vbox.pack_start(title_label, False, False, 0)

        summary_label = Gtk.Label(label=html.unescape(summary))
        summary_label.set_xalign(0)
        summary_label.set_line_wrap(True)
        summary_label.set_margin_bottom(8)
        vbox.pack_start(summary_label, False, False, 0)

        if magnet:
            magnet_button = Gtk.Button(label="Scarica via Magnet 🧲")
            magnet_button.get_style_context().add_class("suggested-action")
            magnet_button.set_margin_top(12)
            magnet_button.connect("clicked", self.on_magnet_clicked, magnet)
            vbox.pack_start(magnet_button, False, False, 0)

        self.show_all()

    def on_magnet_clicked(self, button, magnet):
        subprocess.Popen(["xdg-open", magnet])

if __name__ == "__main__":
    win = FeedWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
