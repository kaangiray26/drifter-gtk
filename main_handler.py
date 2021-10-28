import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk, Gio

import threading

class Handler_for_main:
    def __init__(self, parent, builder, reddit):
        # PARENT IS FROM TYPE class MainApp
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
        if self.parent.pane != "Home":
            # KILL OTHER THREADS
            self.parent.kill = "Posts"

            self.parent.pane = "Home"
            self.parent.clearListBox()

            if len(self.parent.postsBox_origin):
                # COPY PREVIOUSLY FETCHED SUBS
                self.parent.postsBox = self.parent.postsBox_origin
            else:
                # FETCH POSTS
                threading.Thread(target=self.parent.loadFeed).start()

            # START POST LOADER
            threading.Thread(target=self.parent.postsStartup).start()

    def onSubsButtonClicked(self, button):
        if self.parent.pane != "Subs":
            # KILL OTHER THREADS
            self.parent.kill = "Subs"

            self.parent.pane = "Subs"
            self.parent.clearListBox()

            #if not len(self.parent.subreddits):
            #    print("Fetching subreddits.")
            #    # FETCH SUBS
            #    threading.Thread(target=self.parent.getSubs).start()

            # START SUB LOADER
            threading.Thread(target=self.parent.loadSubs).start()


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