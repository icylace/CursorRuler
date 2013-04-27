CursorRuler
===========

A plugin for the Sublime Text editor which marks the current cursor position using dynamic rulers.




Why Is This Useful?
-------------------

1.  It can be used for alignment purposes in places where Sublime Text's built-in indent guides aren't able to show up.  For example, inside multiple rows of single-line comments or multiple assignment statements across different code blocks.

2.  When used alongside line highlighting it creates a crosshair effect which can be a useful visual aid.




Features
--------

- Use multiple dynamic rulers to create different highlighting styles including a "thickening" effect which can be used to simulate column highlighting.

- Option to synchronize rulers when using multiple views of the same file.

- Supports muliple cursors.

- Toggle activation through the command palette.

- Compatible with Sublime Text 2 and Sublime Text 3.




Installation
------------

### With Package Control

The easiest way to install CursorRuler is through Package Control which is available here:

    http://wbond.net/sublime_packages/package_control

After installing Package Control, restart Sublime Text and bring up the Command Palette (`Command+Shift+P` on OS X and `Control+Shift+P` on Linux/Windows).  Select `Package Control: Install Package`, wait while Package Control fetches the latest package list, then select CursorRuler when the list appears.


### Without Git

Download the latest source from [GitHub](https://github.com/icylace/CursorRuler) and then copy the CursorRuler folder to your Sublime Text's packages folder.


### With Git

Clone the CursorRuler repository while in your Sublime Text's packages folder:

    git clone https://github.com/icylace/CursorRuler.git


### The Packages Folder for Sublime Text 2 and Sublime Text 3

- OS X:

        ~/Library/Application Support/Sublime Text 2/Packages
        ~/Library/Application Support/Sublime Text 3/Packages

- Linux:

        ~/.Sublime Text 2/Packages
        ~/.Sublime Text 3/Packages

- Windows:

        %APPDATA%\Sublime Text 2\Packages
        %APPDATA%\Sublime Text 3\Packages

Another way of getting the path of the packages folder is to open up Sublime Text's Python console by pressing ``Ctrl+` `` (backtick) and then typing `sublime.packages_path()` in it's input field and then pressing enter.


Settings
--------

The following settings are available and optional.  They are shown here with their default settings.

    {
      "cursor_rulers":  [-0.1, 0.2],
      "enabled":        true,
      "synchronized":   true
    }


### cursor_rulers

A list of column positions relative to the cursor position where dynamic cursor rulers appear.  They can be any decimal number.  0 represents the current cursor position so

    "cursor_rulers": [0]

means display a single dynamic ruler exactly where the cursor is.  You could experiment with something like

    "cursor_rulers": [-0.1, 0, 0.2]

if you wanted something thicker.  The default (what I personally use) which is

    "cursor_rulers": [-0.1, 0.2]

tries to be thick without being too distracting.  You could also try something like

    "cursor_rulers": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

if you wanted to simulate **column highlighting!**  It's not perfect and can look a little odd at larger font sizes but it's the next-best thing to the real thing.

Now for some crazy stuff.  The following examples illustrate the silliness that's possible with multiple cursor rulers.

It's possible there might be some people who would consider this first example useful:

    "cursor_rulers": [-4, -0.1, 0, 0.2, 4]

The potential usefulness comes from ability to know at a glance what is cleanly indented and outdented relative to the cursor.  In this case the indent spacing is assumed to be 4.  The disadvantage here is that it looks visually cluttered (at least to me).

This next example illustrates a much more experimental "gradient" highlighting style:

    "cursor_rulers": [-2.4, -1.7, -1.2, -0.8, -0.4, -0.2, -0.1]

It shows several rulers trailing to the left of your cursor.  It may ultimately be too showy to be practical but it does have its own feel once you get used to it.

This final example is yet another experimental highlighting style.  This one doesn't highlight the cursor position directly but instead creates a "tunnel" which is centered around the cursor:

    "cursor_rulers": [-4.7, -4, -3.4, -3.1, -3, 3, 3.2, 3.5, 4.1, 4.7]

As you can see, a variety of sometimes useful, sometimes strange highlighting possibilities are out there.


### enabled

If you have it normally disabled you can enable it for when you need it by using the `CursorRuler: Toggle Enabled/Disabled` command from the Command Palette.  Use the same command again to turn it back off.


### synchronized

Multiple views of the same file will show cursor rulers that move together in synchronized fashion.  This is most useful when using the `Rows: 2`, `Rows: 3`, or `Grid: 4` layout and having multiple views of the same file being used in different groups.




Usage
-----

Having the plugin enabled is all that's required to start seeing your cursors have rulers track them.


### Available Commands

`CursorRuler: Toggle Enabled/Disabled` - Turns the plugin off if it's on and vice versa.




Tips
----

You may want to distinguish the cursor rulers from any normal static rulers you may have set.  Unfortunately, I'm not aware of a way to set different visual styles for different rulers.  However, one option to workaround this is to set multiple rulers around where a single ruler would normally be.  For example, if your rulers setting in your user preferences was set like this:

    "rulers": [80, 150]

then you could do this:

    "rulers": [80, 80.25, 150, 150.25]

to make your normal rulers "thicker" and therefore distinguishable from the cursor rulers.

Also, you may instead consider making your cursor rulers have a thicker style than your normal rulers.


### Ruler Colors

Speaking of ruler visual style, there's apparently no way to set the color of rulers directly.  Rulers get their colors from your color scheme's foreground and background settings.  The background setting overrides the foreground setting.

Despite the current lack of ability to directly set colors for rulers (as of ST2 build 2219 and ST3 build 3030) there's thankfully a workaround for it [described here](http://sublimetext.userecho.com/topic/93504-use-separate-colors-for-the-background-gutter-and-folder-tree/#comment_164903).

Basically, you need to change the overall default foreground color and/or background color of your color scheme and then add a rule for the `text` and `source` scopes which is used to override the default colors.  For example, if we had a default foreground color which is meant to be used as the ruler and gutter foreground color:

    <key>foreground</key>
    <string>#00FFFF77</string>

then we would add

    <dict>
      <key>name</key>
      <string>Text and Source Base Colors</string>
      <key>scope</key>
      <string>text, source</string>
      <key>settings</key>
      <dict>
        <key>foreground</key>
        <string>#E6E1DC</string>
      </dict>
    </dict>

in order for us to define our actual default foreground color.

As a sidenote, gutter text foreground color can be defined directly:

    <key>gutterForeground</key>
    <string>#0000FF77</string>

as well as the gutter text background color:

    <key>gutter</key>
    <string>#0000FF33</string>



Notes
-----

- In ST2 there is a major bug which is described below.

- While moving a selected group of text with the mouse the insertion-point cursor is not shown with its own dynamic ruler.  Though, this is probably preferable since this distinguishes the editing cursors from the insertion-point cursors.

- The positioning of the cursor rulers is scaled according to the font size.  The larger the font size the greater the chance that gaps will get introduced into "thick" cursor ruler styles like the column highlighting style.  The size of the gaps are also dependent upon the font size.

- Using the column-like highlighting style while using a variable-width font looks strange.  Perhaps this should considered a bug?

- In ST3 build 3012 and older the `add_on_change()` method was not implemented and therefore CursorRuler will not use it.  In ST2 and also ST3 build 3013 and later it is available and CursorRuler will use it.

- After you save changes to your user settings or your CursorRuler settings the changes take effect once the cursor state changes.


### Known Major Bug for Sublime Text 2 Only

While the plugin is enabled and a selection is attempted to be extended with mouse dragging it freezes the entire editor when moving the mouse pointer out of the view or onto the view's minimap.  This also occurs on empty views.  The freeze in this scenario is caused by `on_selection_modified()` attempting to call the ST2 API or even attempting to print to the console.

The workaround is to do selection without mouse dragging or use mouse dragging while keeping the pointer within the view.

I have attempted to use threading and other potential solutions to no avail. I have not found a proper solution to this in ST2.

ST3 seems to completely avoid this problematic scenario.  I suppose it's due to its API being thread-safe.


### Known Minor Bugs

- If CursorRuler is added to the "ignored_packages" list in the user preferences then upon saving the preferences any open files that have cursor rulers on them will retain those rulers as permanent static rulers.  The only way to remove those static rulers would be to either no longer ignore the plugin or reopen the files that are affected.

- Doesn't work on previewed files.  Perhaps this is beneficial as an indicator for when you're looking at previewed files?


### Similar Plugins

[Cross](https://github.com/chancedai/sublime-cross) - I just found out about this today (2013-02-20).  This predates CursorRuler by about a month.




Release Notes
-------------

2013-04-27

- Updated readme:  Fixed a typo.  Also added info for changing gutter text foreground color ([source](http://www.sublimetext.com/forum/viewtopic.php?f=3&t=6161#p26904)).


2013-02-21:  Version **1.1.0**

- I decided to start using [Semantic Versioning](http://semver.org/) and have updated the readme and comments in the code where appropriate in order to reflect this.

- Changed the way the Sublime Text version number is used in order to account for the build number.  This was done to take advantage of ST3 build 3013 now implementing the `add_on_change()` method.

- Updated readme:  Removed the "(coming soon)" from the "With Package Control" section because CursorRuler is now available through Package Control!


2013-02-20

- Updated readme:  Added a reference to the Cross plugin.


2013-02-14

- Updated readme:  Added more information about bugs.


2013-02-12

- Updated readme:  Updated the "Ruler Colors" section with more details about setting ruler colors.

- Updated readme:  Updated the "The Packages Folder for Sublime Text 2 and Sublime Text 3" section with details about another way of getting the packages folder path.


2013-02-10:  Version **1.0.1**

- Fixed a missing attribute error at startup.  Thanks for catching it, [adzenith](https://github.com/adzenith)!

- Included settings file improvements by [adzenith](https://github.com/adzenith).

- Updated readme:  Made a note about the slightly quirky behavior after settings get updated.


2013-02-09:  Version **1.0.0**

-  First public release.




License
-------

[MIT](http://opensource.org/licenses/MIT)




Have fun !
