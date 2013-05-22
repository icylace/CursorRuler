'''
CursorRuler 1.1.0

A plugin for the Sublime Text editor which marks the current cursor position
using dynamic rulers.

See README.md for details.

'''

import sublime, sublime_plugin


#
# It's important for us to know if we're running in ST3 or ST2.
#
# In Sublime Text 3 build 3010 and older the API is unavailable during
# program startup.  As of build 3011 `sublime.version()` is available during
# startup.  If we're unable to get the version build number we make the
# assumption that it's 3000.
#
# We're also assuming that if we're not running in ST3 then we're running
# in ST2.
#
st = 3000 if sublime.version() == '' else int(sublime.version())


# ------------------------------------------------------------------------------


class CursorRuler(object):
    @classmethod
    def __draw_on_view(cls, view, active_view):
        cursors         = active_view.sel()
        em_width        = active_view.em_width()
        view_size       = active_view.size()
        dynamic_rulers  = []


        # Setup rulers for each cursor.
        for cursor in cursors:
            #
            # Get the cursor's true horizontal position.
            #
            # To do this we need to know a few things:
            #
            # The cursor position is usually represented technically as an empty
            # region.  While in this case the region's `a` and `b` properties are
            # the same in the case of a selection region being made the "b" property
            # more accurately represents where the cursor is at.
            #
            # A cursor's `xpos` is its target horizontal layout position.
            # It is the position where the cursor would be at if it weren't affected
            # by lack of virtual whitespace, word-wrapping, or varying font widths.
            #
            # If it's non-negative then it represents the position the cursor
            # was just at in the previous line.  It also indicates that the
            # cursor was moved vertically with either the up or down arrow key.
            #
            # If it's negative then it's actually not a position but rather
            # an indicator that the cursor was moved horizontally with either
            # the left or right arrow key or repositioned with a mouse click.
            #

            # First we get what would normally be the current cursor position.
            cur_x = view.text_to_layout(cursor.b)[0]

            # We then take into account the strangeness of word-wrapping.
            # It only matters when we're not at the end of the file.

            next_x  = view.text_to_layout(cursor.b + 1)[0]
            xpos    = cursor.xpos if st >= 3000 else cursor.xpos()

            if xpos >= 0 and xpos < cur_x and cur_x > next_x and cursor.b < view_size:
                if not cls.indent_subsequent_lines:
                    cur_x = 0
                else:
                    line = view.substr(view.line(cursor))
                    if line:
                        line_length           = len(line)
                        stripped_line_length  = len(line.lstrip())

                        # We keep going if the line is not entirely whitespace.
                        if stripped_line_length > 0:
                            # We find out where the first non-whitespace character
                            # of the line is and we use its position.
                            cur_row         = view.rowcol(cursor.b)[0]
                            beginning_pos   = line_length - stripped_line_length
                            beginning_point = view.text_point(cur_row, beginning_pos)
                            cur_x           = view.text_to_layout(beginning_point)[0]

            # Get the cursor position in terms of columns.
            cur_col = cur_x / em_width

            # Setup the current dynamic rulers to be included with the static rulers.
            dynamic_rulers += [cur_col + offset for offset in cls.cursor_rulers]

        # Update the active rulers with the dynamic rulers.
        view.settings().set('rulers', cls.rulers + dynamic_rulers)


    # ..........................................................................


    @classmethod
    def __setup(cls):
        cls.rulers                  = cls.sublime_settings.get('rulers', [])
        cls.indent_subsequent_lines = bool(cls.sublime_settings.get('indent_subsequent_lines', True))
        cls.cursor_rulers           = cls.settings.get('cursor_rulers',  [-0.1, 0.2])
        cls.enabled                 = bool(cls.settings.get('enabled', True))
        cls.synchronized            = bool(cls.settings.get('synchronized', True))


    # ..........................................................................


    @classmethod
    def draw(cls, view):
        if cls.synchronized:
            # Draw the dynamic rulers for every view of the same buffer
            # as the active view.
            view_buffer_id = view.buffer_id()
            for window in sublime.windows():
                for v in window.views():
                    if (v.buffer_id() == view_buffer_id):
                        cls.__draw_on_view(v, view)
        else:
            # Draw the dynamic rulers for the current view.
            cls.__draw_on_view(view, view)


    # ..........................................................................


    @classmethod
    def init(cls):
        cls.sublime_settings  = sublime.load_settings('Preferences.sublime-settings')
        cls.settings          = sublime.load_settings('CursorRuler.sublime-settings')

        # In Sublime Text 3 the `add_on_change()` method was not implemented
        # until build 3013.
        if st < 3000 or st >= 3013:
            cls.sublime_settings.add_on_change('cursorruler-reload', cls.__setup)
            cls.settings.add_on_change('reload', cls.__setup)

        cls.__setup()


    # ..........................................................................


    @classmethod
    def is_enabled(cls, view):
        return cls.enabled and not view.settings().get('is_widget')


    # ..........................................................................


    @classmethod
    def reset(cls, view):
        if cls.synchronized:
            # Reset all the views of the same buffer.
            view_buffer_id = view.buffer_id()
            for window in sublime.windows():
                for v in window.views():
                    if (v.buffer_id() == view_buffer_id):
                        v.settings().set('rulers', cls.rulers)
        else:
            # Reset the current view.
            view.settings().set('rulers', cls.rulers)


# ------------------------------------------------------------------------------


class CursorRulerToggleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if CursorRuler.is_enabled(self.view):
            # About to disable so reset.
            CursorRuler.reset(self.view)
        else:
            # About to enable so restore.
            CursorRuler.draw(self.view)

        CursorRuler.enabled = not CursorRuler.enabled


# ------------------------------------------------------------------------------


class CursorRulerListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        if not view.is_loading() and CursorRuler.is_enabled(view):
            CursorRuler.draw(view)

    def on_close(self, view):
        CursorRuler.reset(view)

    def on_deactivated(self, view):
        if CursorRuler.is_enabled(view):
            CursorRuler.reset(view)

    def on_load(self, view):
        # In ST2 the initialization phase needs to happen here
        # for static rulers to not disappear.
        if st < 3000:
            CursorRuler.init()

        if CursorRuler.is_enabled(view):
            CursorRuler.draw(view)
        else:
            CursorRuler.reset(view)

    def on_selection_modified(self, view):
        active_window = sublime.active_window()
        if active_window is not None:
            # The view parameter doesn't always match the active view
            # the cursor is in.  This happens when there are multiple
            # views of the same file.
            active_view = active_window.active_view()

            if CursorRuler.is_enabled(active_view):
                CursorRuler.draw(active_view)


# ------------------------------------------------------------------------------


# In ST3 this will get called automatically once the full API becomes available.
def plugin_loaded():
    CursorRuler.init()


# ------------------------------------------------------------------------------


# In ST2 this prevents an error from happening if this particular file
# is saved.  This also prevents a missing attribute error from occurring
# at startup.
if st < 3000:
    CursorRuler.init()
