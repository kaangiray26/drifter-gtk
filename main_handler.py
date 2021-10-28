import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk, Gio

import threading

class Handler_for_main:
    def __init__(self, parent, builder, reddit):
        self.parent  = parent
        self.reddit  = reddit
        self.builder = builder

    # HANDLERS
    def onAddButtonClicked(self, button):
        print("Add Button Clicked!")

    def onProfileButtonClicked(self, button):
        print("Profile Button Clicked!")

    def onRefreshButtonClicked(self, button):
        self.parent.refreshFeed()

    def onSearchButtonClicked(self, button):
        print("Search Button Clicked!")

    def onSavedButtonClicked(self, button):
        print("Saved Button Clicked!")

    def onPreferencesButtonClicked(self, button):
        print("Preferences Button Clicked!")

    def onAboutButtonClicked(self, button):
        print("About Button Clicked!")

    def onHomeButtonClicked(self, button):
        self.parent.pane = "Home"
        self.parent.clearListBox()
        if self.parent.postsBox:
            threading.Thread(target=self.parent.ShowFeed).start()

    def onSubsButtonClicked(self, button):
        self.parent.pane = "Subs"
        self.parent.clearListBox()
        if self.parent.subredditsBox:
            for row in self.parent.subredditsBox:
                self.parent.listview.add(row)
            self.parent.listview.show_all()
        else:
            self.parent.subredditsBox = []
            subreddits = sorted(
                list(self.reddit.user.subreddits(limit=None)),
                key=lambda s: s.display_name.lower(),
            )
            for subreddit in subreddits:
                row = Gtk.ListBoxRow()
                row.set_margin_bottom(10)
                sub = Gtk.Label()
                sub.set_halign(Gtk.Align.START)
                sub.set_text(subreddit.display_name)
                row.add(sub)
                self.parent.subredditsBox.append(row)
                self.parent.listview.add(row)
            self.parent.listview.show_all()

    def onMessagesButtonClicked(self, button):
        print("Messages Button Clicked!")

    def onNotificationsButtonClicked(self, button):
        print("Notifications Button Clicked!")

    def onRowActivated(self, row, extra):
        if self.parent.pane == "Home":
            submission = extra.get_child()
            post_id_label = submission.get_children()[0].get_children()[-1].get_children()[-1]
            print(post_id_label.get_text())
        elif self.parent.pane == "Subs":
            submission = extra.get_child()
            self.parent.section = submission.get_text()
            self.parent.clearListBox()
            self.parent.pane = "Home"
            self.parent.refreshStart()

    def Destroyed(self, window, extra):
        Gtk.main_quit()