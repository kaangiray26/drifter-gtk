import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk, Gio

class Handler_for_post:
    def __init__(self, builder, reddit, post_id):
        self.post_id = post_id
        self.reddit = reddit
        self.builder = builder

    # HANDLERS
    def onUpvoteButtonClicked(self, button):
        self.reddit.submission(id=self.post_id).upvote()
        print("Upvoted.")

    def onDownvoteButtonClicked(self, button):
        self.reddit.submission(id=self.post_id).downvote()
        print("Downvoted.")

    def onCommentsButtonClicked(self, button):
        print("Comments.")

    def onAwardButtonClicked(self, button):
        print("Awards.")

    def onShareButtonClicked(self, button):
        print("Share.")

    def onStarButtonClicked(self, button):
        if self.reddit.submission(id=self.post_id).saved:
            self.reddit.submission(id=self.post_id).unsave()
            self.builder.get_object("Star_State").set_from_icon_name("star-new-symbolic", Gtk.IconSize.BUTTON)
        else:
            self.reddit.submission(id=self.post_id).save()
            self.builder.get_object("Star_State").set_from_icon_name("starred-symbolic", Gtk.IconSize.BUTTON)
        print("Star.")