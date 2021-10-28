#!/usr/bin/python
#-*- encoding: utf-8 -*-

import gi
import sys
import praw
import urllib
import datetime
import threading
import faulthandler

gi.require_version("Gtk", "3.0")
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, GLib, Gdk, Gio, WebKit2
from gi.repository.GdkPixbuf import Pixbuf

from main_handler import Handler_for_main
from post_handler import Handler_for_post

from markdown_view_original import MarkdownRenderer
from markdown_view import MarkdownView

screen = Gdk.Screen.get_default()
provider = Gtk.CssProvider()
provider.load_from_path("gtk-contained-dark.css")
Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

faulthandler.enable()

class MainApp:
    def __init__(self):
        self.pane            = "Home"
        self.section         = "front"
        self.subreddits      = []

        self.post_limit      = 20

        self.postsBox        = []
        self.subsBox         = []

        self.postsBox_origin = []
        self.subsBox_origin  = []

        self.posts_lock      = False
        self.subs_lock       = False

        self.subs_run        = False
        self.kill            = None

        # LOGIN ACTIONS
        self.reddit = praw.Reddit(
            "auth",
            config_interpolation = "basic"
        )
        threading.Thread(target=self.getSubs).start()
        threading.Thread(target=self.loadFeed).start()

        # GETTING MAIN WINDOW GLADE OBJECT
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/main_window.glade")

        # CREATE MAIN EVENT HANDLER
        self.main_handler = Handler_for_main(self, self.builder, self.reddit)

        # SETTING MAIN EVENT HANDLER
        self.builder.connect_signals(self.main_handler)

        # POSTS LISTVIEW
        self.listview = self.builder.get_object("listview")

        # SHOW MAIN WINDOW
        self.window = self.builder.get_object("Main_Window")

        # SETTING KEYBOARD SHORTCUTS HANDLER
        self.window.connect("key-press-event", self._key_press_event)

        self.window.set_border_width(10)

        self.window.show_all()

        # RUN REFRESHFEED ON STARTUP
        threading.Thread(target=self.postsStartup).start()

    # KEYBOARD SHORTCUTS
    def _key_press_event(self, widget, event):
        keyval = event.keyval
        state  = event.state
        keyval_name = Gdk.keyval_name(keyval)

        ctrl = (state & Gdk.ModifierType.CONTROL_MASK)

        if (ctrl and keyval_name == 'q') or (ctrl and keyval_name == 'w'):
            Gtk.main_quit()

    # MAIN FUNCTIONS
    def getSubs(self):
        self.subreddits = sorted(
            list(self.reddit.user.subreddits(limit=None)),
            key=lambda s: s.display_name.lower(),
        )
        self.subs_run = True
        return False

    def postsStartup(self, data=None):
        count = 0
        while count < self.post_limit:
            # KILL FUNCTION
            if self.kill and self.kill != "Posts":
                self.posts_lock = False
                return False

            if len(self.postsBox) and not self.posts_lock:
                GLib.idle_add(self.showFeed)
                self.posts_lock = True
                count += 1
        self.kill = None

    def showFeed(self):
        item = self.postsBox.pop(0)
        self.listview.add(item)
        item.show_all()
        self.posts_lock = False
        return False

    def showSubs(self, subreddit):
        row = Gtk.ListBoxRow()
        row.set_margin_bottom(10)
        sub = Gtk.Label()
        sub.set_halign(Gtk.Align.START)
        sub.set_text(subreddit.display_name)
        row.add(sub)

        self.listview.add(row)
        row.show_all()
        
        return False

    def loadSubs(self):
        # WAIT UNTIL ALL SUBS ARE LOADED
        while not self.subs_run:
            continue

        # ADD EACH SUB TO LISTBOX
        for subreddit in self.subreddits:
            # KILL FUNCTION
            if self.kill and self.kill != "Subs":
                return False
            GLib.idle_add(self.showSubs, subreddit)
        print("Subreddit rows added to subsBox.")
        return False

    def clearListBox(self):
        for row in self.listview.get_children():
            self.listview.remove(row)

    def loadFeed(self):
        self.postsBox        = []
        self.postsBox_origin = []

        # CHECK FOR WHICH SUBREDDIT TO LOAD POSTS FROM
        if self.section == "front":
            subreddit_feed = self.reddit.front.hot(limit = self.post_limit)
        else:
            subreddit_feed = self.reddit.subreddit(self.section).hot(limit = self.post_limit)

        # GO THROUGH THE FEED
        for submission in subreddit_feed:
            # CREATE A NEW POST OBJECT FOR EVERY SUBMISSION
            posts_builder = Gtk.Builder.new_from_file("ui/post_view.glade")
            posts_builder.connect_signals(Handler_for_post(posts_builder, self.reddit, submission.id))
            post = posts_builder.get_object("Post_View")

            posts_builder.get_object("Subreddit").set_text('r/'+submission.subreddit.display_name)
            posts_builder.get_object("Posted_By").set_text(submission.author.name)
            posts_builder.get_object("Post_Title").set_text(submission.title)
            posts_builder.get_object("Post_ID").set_markup(submission.id)

            if submission.is_self:
                if hasattr(submission, 'preview'):
                    preview = submission.preview['images'][0]['source']
                    url = preview['url']

                    response = urllib.request.urlopen(url)
                    pixbuf = Pixbuf.new_from_stream_at_scale(
                        Gio.MemoryInputStream.new_from_data(response.read(), None),
                        preserve_aspect_ratio=True,
                        width=preview['width'], 
                        height=preview['height'])
                    posts_builder.get_object("Thumbnail").set_from_pixbuf(pixbuf)
                    row = Gtk.ListBoxRow()
                    row.set_margin_bottom(10)

                    row.add(post)
                    self.postsBox.append(row)
                else:

                    post.remove(posts_builder.get_object("Thumbnail"))

                    box = Gtk.Box()
                    box.add(MarkdownView(submission.selftext))

                    post.pack_start(box, True, True, 0)
            else:
                self.loadThumbnail(submission, posts_builder.get_object("Thumbnail"))

            row = Gtk.ListBoxRow()
            row.set_margin_bottom(10)

            row.add(post)
            self.postsBox.append(row)
            self.postsBox_origin.append(row)
        return False

    def loadThumbnail(self, submission, image):
        url = submission.url.split("?")[0].replace("preview", "i")
        if url.startswith("https://i.redd.it"):
            response = urllib.request.urlopen(url)
            pixbuf = Pixbuf.new_from_stream_at_scale(
                Gio.MemoryInputStream.new_from_data(response.read(), None),
                preserve_aspect_ratio=True,
                width=462, 
                height=616)
            image.set_from_pixbuf(pixbuf)
        elif url.startswith("https://v.redd.it") or url.startswith("https://gfycat.com"):
            if submission.thumbnail == 'default':
                image.set_from_icon_name("insert-link-symbolic", 96)
            else:
                response = urllib.request.urlopen(submission.thumbnail)
                pixbuf = Pixbuf.new_from_stream_at_scale(
                    Gio.MemoryInputStream.new_from_data(response.read(), None),
                    preserve_aspect_ratio=True,
                    width=462,
                    height=616)
                image.set_from_pixbuf(pixbuf)
        else:
            if submission.thumbnail:
                if submission.thumbnail == 'default':
                    image.set_from_icon_name("insert-link-symbolic", 96)
                else:
                    thumbnail = submission.thumbnail
                    response = urllib.request.urlopen(thumbnail)
                    pixbuf = Pixbuf.new_from_stream_at_scale(
                        Gio.MemoryInputStream.new_from_data(response.read(), None),
                        preserve_aspect_ratio=True,
                        width=462,
                        height=616)
                    image.set_from_pixbuf(pixbuf)

if __name__ == "__main__":
    arg = sys.argv[1:]

    x = MainApp()
    Gtk.main()