import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk, Gio, Pango
from post_handler import Handler_for_post

class Post_View(Gtk.Box):     # Post View Box
    def __init__(self):
        super().__init__()
        self.set_orientation(Gtk.Orientation(1))
        self.set_can_focus(False)

        self.style = Gtk.Style()
        self.stylecontext = Gtk.StyleContext()
        self.stylecontext.add_class("background")
        self.style.context = self.stylecontext
        self.set_style(self.style)
        self.init_upperbox()
        self.init_thumbnail()
        self.init_lowerbox()

    def init_upperbox(self):
        # UPPERBOX
        UpperBox = Gtk.Box()
        UpperBox.set_margin_start(10)
        UpperBox.set_margin_end(10)
        UpperBox.set_orientation(Gtk.Orientation(1))
        UpperBox.set_can_focus(False)

        # Subreddit_UsernameBox
        Subreddit_UsernameBox = Gtk.Box()
        Subreddit_UsernameBox.set_margin_bottom(5)
        Subreddit_UsernameBox.set_can_focus(False)
        #

        # Images
        Star_State = Gtk.Image()
        Star_State.set_from_icon_name("star-new-symbolic", Gtk.IconSize.BUTTON)
        #

        #
        Subreddit = Gtk.Label()
        Subreddit.set_margin_end(5)
        Subreddit.set_selectable(True)
        Subreddit.set_can_focus(False)
        #

        #
        SpacerDash = Gtk.Label()
        SpacerDash.set_text("-")
        SpacerDash.set_margin_end(5)
        SpacerDash.set_can_focus(False)

        SpacerDash_attrList      = Pango.AttrList()
        SpacerDash_attr = Pango.attr_font_desc_new(Pango.font_description_from_string("Serif Bold 12"))
        SpacerDash_attrList.insert(SpacerDash_attr)
        SpacerDash.set_attributes(SpacerDash_attrList)
        #

        #
        Posted_By = Gtk.Label()
        Posted_By.set_margin_end(5)
        Posted_By.set_selectable(True)
        Posted_By.set_can_focus(False)
        #

        #
        Fixed_1 = Gtk.Fixed()
        Fixed_1.set_can_focus(False)
        #

        #
        Star_Button = Gtk.Button()
        Star_Button.connect("clicked", Handler_for_post.onStarButtonClicked)
        Star_Button.set_image(Star_State)
        Star_Button.set_always_show_image(True)
        Star_Button.set_can_focus(True)
        #

        Subreddit_UsernameBox.pack_start(Subreddit, False, True, 0)
        Subreddit_UsernameBox.pack_start(SpacerDash, False, True, 0)
        Subreddit_UsernameBox.pack_start(Posted_By, False, True, 0)
        Subreddit_UsernameBox.pack_start(Fixed_1, True, True, 0)
        Subreddit_UsernameBox.pack_start(Star_Button, False, True, 0)

        # TitleBox
        TitleBox = Gtk.Box()
        TitleBox.set_margin_bottom(5)
        TitleBox.set_can_focus(False)
        #

        #
        Post_Title = Gtk.Label()
        Post_Title.set_selectable(True)
        Post_Title.set_line_wrap(True)
        Post_Title.set_max_width_chars(340)
        Post_Title.set_xalign(0)
        Post_Title.set_can_focus(False)
        #

        #
        Fixed_2 = Gtk.Fixed()
        Fixed_2.set_can_focus(False)
        #

        TitleBox.pack_start(Post_Title, False, True, 0)
        TitleBox.pack_start(Fixed_2, True, True, 0)

        # PostIDBox
        PostIDBox = Gtk.Box()
        PostIDBox.set_margin_bottom(5)
        PostIDBox.set_can_focus(False)
        #

        #
        Post_ID = Gtk.Label()
        Post_ID.set_no_show_all(True)
        Post_ID.set_opacity(0)
        Post_ID.set_justify(Gtk.Justification(1))
        Post_ID.set_can_focus(False)
        #

        PostIDBox.pack_start(Post_ID, False, True, 0)

        UpperBox.pack_start(Subreddit_UsernameBox, False, True, 0)
        UpperBox.pack_start(TitleBox, False, True, 0)
        UpperBox.pack_start(PostIDBox, False, True, 0)

        GLib.idle_add(self.pack_start, UpperBox, False, True, 0)
    
    def init_thumbnail(self):
        # Thumbnail
        Thumbnail = Gtk.Image()
        Thumbnail.set_margin_start(10)
        Thumbnail.set_margin_end(10)
        Thumbnail.set_margin_top(10)
        Thumbnail.set_margin_bottom(10)
        Thumbnail.set_pixel_size(96)
        Thumbnail.set_from_icon_name("image-loading", Gtk.IconSize.DIALOG)
        Thumbnail.set_can_focus(False)
        #

        GLib.idle_add(self.pack_start, Thumbnail, True, True, 0)

    def init_lowerbox(self):
        # LOWERBOX
        LowerBox = Gtk.Box()
        LowerBox.set_margin_start(10)
        LowerBox.set_margin_end(10)
        LowerBox.set_spacing(10)
        LowerBox.set_homogeneous(True)
        LowerBox.set_can_focus(False)
        #

        # Images
        UpvoteImage = Gtk.Image()
        UpvoteImage.set_from_icon_name("go-top-symbolic", Gtk.IconSize.BUTTON)

        DownvoteImage = Gtk.Image()
        DownvoteImage.set_from_icon_name("go-bottom-symbolic", Gtk.IconSize.BUTTON)

        CommentsImage = Gtk.Image()
        CommentsImage.set_from_icon_name("view-paged-symbolic", Gtk.IconSize.BUTTON)
        CommentsImage.set_can_focus(False)

        ShareImage = Gtk.Image()
        ShareImage.set_from_icon_name("send-to-symbolic", Gtk.IconSize.BUTTON)
        ShareImage.set_can_focus(False)

        AwardImage = Gtk.Image()
        AwardImage.set_from_icon_name("emblem-favorite-symbolic", Gtk.IconSize.BUTTON)
        AwardImage.set_can_focus(False)
        #

        #
        Upvote_Button = Gtk.Button()
        Upvote_Button.set_size_request(80, -1)
        Upvote_Button.connect("clicked", Handler_for_post.onUpvoteButtonClicked)
        Upvote_Button.set_image(UpvoteImage)
        Upvote_Button.set_always_show_image(True)
        Upvote_Button.set_can_focus(True)
        Upvote_Button.set_receives_default(True)
        Upvote_Button.set_label("")
        #

        #
        Downvote_Button = Gtk.Button()
        Downvote_Button.set_size_request(80, -1)
        Downvote_Button.connect("clicked", Handler_for_post.onDownvoteButtonClicked)
        Downvote_Button.set_image(DownvoteImage)
        Downvote_Button.set_always_show_image(True)
        Downvote_Button.set_can_focus(True)
        Downvote_Button.set_receives_default(True)
        Downvote_Button.set_label("")
        #

        #
        Comments_Button = Gtk.Button()
        Comments_Button.set_size_request(80, -1)
        Comments_Button.connect("clicked", Handler_for_post.onCommentsButtonClicked)
        Comments_Button.set_image(CommentsImage)
        Comments_Button.set_always_show_image(True)
        Comments_Button.set_can_focus(True)
        Comments_Button.set_label("171")
        #

        #
        Award_Button = Gtk.Button()
        Award_Button.set_size_request(80, -1)
        Award_Button.connect("clicked", Handler_for_post.onAwardButtonClicked)
        Award_Button.set_image(AwardImage)
        Award_Button.set_always_show_image(True)
        Award_Button.set_can_focus(True)
        Award_Button.set_label("Award")
        #

        #
        Share_Button = Gtk.Button()
        Share_Button.set_size_request(80, -1)
        Share_Button.connect("clicked", Handler_for_post.onShareButtonClicked)
        Share_Button.set_image(ShareImage)
        Share_Button.set_always_show_image(True)
        Share_Button.set_can_focus(True)
        Share_Button.set_label("Share")
        #

        LowerBox.pack_start(Upvote_Button, False, True, 0)
        LowerBox.pack_start(Downvote_Button, False, True, 0)
        LowerBox.pack_start(Comments_Button, False, True, 0)
        LowerBox.pack_start(Award_Button, False, True, 0)
        LowerBox.pack_start(Share_Button, False, True, 0)

        GLib.idle_add(self.pack_end, LowerBox, False, True, 0)
