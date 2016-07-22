# CursorRuler

A plugin for the Sublime Text editor which marks the current cursor position(s) using dynamic rulers.




## Why Is This Useful?

1.  It can be used for alignment purposes in places where Sublime Text's built-in indent guides aren't able to show up.  For example, inside multiple rows of single-line comments or multiple assignment statements across different code blocks.

2.  When used alongside line highlighting it creates a crosshair effect which can be a useful visual aid.




## Features

- Use multiple dynamic rulers to create different highlighting styles including a "thickening" effect which can be used to simulate column highlighting.

- Option to synchronize rulers when using multiple views of the same file.

- Supports multiple cursors.

- Toggle activation through the command palette.

- Compatible with Sublime Text 2 and Sublime Text 3.




## Installation

### With Package Control

The easiest way to install CursorRuler is through [Package Control](https://packagecontrol.io/installation).

After installing Package Control, restart Sublime Text and bring up the Command Palette (`Command+Shift+P` on OS X and `Control+Shift+P` on Linux/Windows).  Select `Package Control: Install Package`, wait while Package Control fetches the latest package list, then select CursorRuler when the list appears.


### Without Git

Download the latest source from [GitHub](https://github.com/icylace/CursorRuler) and then copy the CursorRuler folder to your Sublime Text's packages folder.


### With Git

Clone the CursorRuler repository while in your Sublime Text's packages folder:

```Shell
git clone https://github.com/icylace/CursorRuler.git
```

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

Another way of getting the path of the packages folder is to open up Sublime Text's Python console by pressing `Ctrl+``` (backtick) and then typing `sublime.packages_path()` in it's input field and then pressing enter.




## Usage

Having the plugin enabled is all that's required to start seeing your cursors have rulers track them.


### Available Commands

`CursorRuler: Toggle Enabled/Disabled` - Turns CursorRuler off if it's on and vice versa.

`CursorRuler: Wrap Lines` - Does proper line wrapping.  For details look [here](https://github.com/icylace/CursorRuler/issues/3).




## Settings

The default settings file may be accessed through the menu by going to `Preferences` -> `Package Settings` -> `CursorRuler` -> `Settings – Default`.  The `Settings – User` option may be used to either open up the custom user-specific settings file or to create it if it doesn't exist yet.

The following settings are available.  They are shown here with their default values.

```JSON
{
  "cursor_rulers": [-0.1, 0.2],
  "enabled":       true,
  "synchronized":  true
}
```

To use custom settings first create a file called `CursorRuler.sublime-settings` in your `User` folder which should be located within your packages folder.  Then copy the aforementioned default settings into this file, make your adjustments, and then save the file.  Your changes should take effect the next time the cursor is moved on an open non-previewed file.


### cursor_rulers

A list of column positions relative to the cursor position where dynamic cursor rulers appear.  They can be any decimal number.  0 represents the current cursor position so

```JSON
{
  "cursor_rulers": [0]
}
```

means display a single dynamic ruler exactly where the cursor is.  You could experiment with something like

```JSON
{
  "cursor_rulers": [-0.1, 0, 0.2]
}
```

if you wanted something thicker.  The default (what I personally use) which is

```JSON
{
  "cursor_rulers": [-0.1, 0.2]
}
```

tries to be thick without being too distracting.  You could also try something like

```JSON
{
  "cursor_rulers": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
}
```

if you wanted to simulate **column highlighting!**  It's not perfect and can look a little odd at larger font sizes but it's the next-best thing to the real thing.

Now for some crazy stuff.  The following examples illustrate the silliness that's possible with multiple cursor rulers.

It's possible there might be some people who would consider this first example useful:

```JSON
{
  "cursor_rulers": [-4, -0.1, 0, 0.2, 4]
}
```

The potential usefulness comes from ability to know at a glance what is cleanly indented and outdented relative to the cursor.  In this case the indent spacing is assumed to be 4.  The disadvantage here is that it looks visually cluttered (at least to me).

This next example illustrates a much more experimental "gradient" highlighting style:

```JSON
{
  "cursor_rulers": [-2.4, -1.7, -1.2, -0.8, -0.4, -0.2, -0.1]
}
```

It shows several rulers trailing to the left of your cursor.  It may ultimately be too showy to be practical but it does have its own feel once you get used to it.

This final example is yet another experimental highlighting style.  This one doesn't highlight the cursor position directly but instead creates a "tunnel" which is centered around the cursor:

```JSON
{
  "cursor_rulers": [-4.7, -4, -3.4, -3.1, -3, 3, 3.2, 3.5, 4.1, 4.7]
}
```

As you can see, a variety of sometimes useful, sometimes strange highlighting possibilities are out there.


### enabled

If you have it normally disabled you can enable it for when you need it by using the `CursorRuler: Toggle Enabled/Disabled` command from the Command Palette.  Use the same command again to turn it back off.


### synchronized

Multiple views of the same file will show cursor rulers that move together in synchronized fashion.  This is most useful when using the `Rows: 2`, `Rows: 3`, or `Grid: 4` layout and having multiple views of the same file being used in different groups.




## Tips

You may want to distinguish the cursor rulers from any normal static rulers you may have set.  Unfortunately, I'm not aware of a way to set different visual styles for different rulers.  However, one option to workaround this is to set multiple rulers around where a single ruler would normally be.  For example, if your rulers setting in your user preferences was set like this:

```JSON
{
  "rulers": [80, 150]
}
```

then you could do this:

```JSON
{
  "rulers": [80, 80.25, 150, 150.25]
}
```

to make your normal rulers "thicker" and therefore distinguishable from the cursor rulers.

Also, you may instead consider making your cursor rulers have a thicker style than your normal rulers.


### Ruler Colors

Speaking of ruler visual style, there's apparently no way to set the color of rulers directly.  Rulers get their colors from your color scheme's foreground and background settings.  The background setting overrides the foreground setting.

Despite the current lack of ability to directly set colors for rulers (as of ST2 build 2219 and ST3 build 3030) there's thankfully a workaround for it [described here](http://sublimetext.userecho.com/topic/93504-use-separate-colors-for-the-background-gutter-and-folder-tree/#comment_164903).

Basically, you need to change the overall default foreground color and/or background color of your color scheme and then add a rule for the `text` and `source` scopes which is used to override the default colors.  For example, if we had a default foreground color which is meant to be used as the ruler and gutter foreground color:

```XML
<key>foreground</key>
<string>#00FFFF77</string>
```

then we would add

```XML
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
```

in order for us to define our actual default foreground color.

As a sidenote, gutter text foreground color can be defined directly:

```XML
<key>gutterForeground</key>
<string>#0000FF77</string>
```

as well as the gutter text background color:

```XML
<key>gutter</key>
<string>#0000FF33</string>
```




## Notes

- In ST3 the standard shortcut key for the `Wrap Paragraph at Ruler` menu item (`⌥⌘Q` on OS X, `Alt+Q` on Linux and Windows) is rebound to instead use the `CursorRuler: Wrap Lines` command for doing proper line wrapping.  However, using the `Wrap Paragraph at Ruler` menu item without the shortcut key still uses the normal wrapping command.  It seems there isn't a way to override ST's default menu items in that sort of way.  For details look [here](https://github.com/icylace/CursorRuler/issues/3).

- While moving a selected group of text with the mouse the insertion-point cursor is not shown with its own dynamic ruler.  Though, this is probably preferable since this distinguishes the editing cursors from the insertion-point cursors.

- The positioning of the cursor rulers is scaled according to the font size.  The larger the font size the greater the chance that gaps will get introduced into "thick" cursor ruler styles like the column highlighting style.  The size of the gaps are also dependent upon the font size.

- Using the column-like highlighting style while using a variable-width font looks strange.  Perhaps this should considered a bug?

- In ST3 build 3012 and older the `add_on_change()` method was not implemented and therefore CursorRuler will not use it.  In ST2 and also ST3 build 3013 and later it is available and CursorRuler will use it.

- After you save changes to your user settings or your CursorRuler settings the changes take effect once the cursor state changes.


### Known Minor Bugs

- If CursorRuler is added to the `ignored_packages` list in the user preferences then upon saving the preferences any open files that have cursor rulers on them will retain those rulers as permanent static rulers.  The only way to remove those static rulers would be to either no longer ignore the plugin or reopen the files that are affected.

- On ST2 it doesn't work on previewed files.  Perhaps this is beneficial as an indicator for when you're looking at previewed files?


### Related Plugins

[Cross](https://github.com/chancedai/sublime-cross) - I just found out about this today (2013-02-20).  This predates CursorRuler by about a month.




## Release Notes

2016-07-16:  Version **1.1.5**

- Fix for [#6](https://github.com/icylace/CursorRuler/issues/6) and [#11](https://github.com/icylace/CursorRuler/issues/11):  Crashes were happening in ST2.


2016-07-12:  Version **1.1.4**

- Fix for [#9](https://github.com/icylace/CursorRuler/issues/9):  Empty windows were causing console errors.


2015-03-08:  Version **1.1.3**

- Added [Vintageous](http://guillermooo.bitbucket.org/Vintageous/) support, thanks to [zjc0816](https://github.com/zjc0816)!


2013-10-12:  Version **1.1.2**

- The original fix for [#2](https://github.com/icylace/CursorRuler/issues/2) only worked for ST2.  Hopefully now things will work in ST3 also.


2013-10-12:  Version **1.1.1**

- General code improvement.
- The CursorRuler settings are now accessible from the "Preferences" -> "Package Settings" menu.
- Fix for [#2](https://github.com/icylace/CursorRuler/issues/2):  Custom user settings were not being picked up.
- Fix for [#3](https://github.com/icylace/CursorRuler/issues/3):  Default line wrapping was behaving unexpectedly.  Created a new command called [CursorRuler: Wrap Lines](https://github.com/icylace/CursorRuler#available-commands) for doing line wrapping properly.
- Started using Package Control messages.
- Updated readme:  Made more use of GitHub Flavored Markdown.
- Updated readme:  Noted that one of the minor bugs is ST2-only.
- Updated readme:  Some minor rearrangement.  Also described how to access the settings through the menu.  Noted some stuff about the `Wrap Paragraph at Ruler` menu item.


2013-08-21

- Updated readme:  Added info for using custom settings.


2013-04-27

- Updated readme:  Fixed a typo.  Added info for changing gutter text foreground color ([source](http://www.sublimetext.com/forum/viewtopic.php?f=3&t=6161#p26904)).  Also found out how to change gutter text background color and added that info too.


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
- Included settings file improvements by [adzenith](https://github.com/adzenith).  Closes #1.
- Updated readme:  Made a note about the slightly quirky behavior after settings get updated.


2013-02-09:  Version **1.0.0**

-  First public release.




## License

[MIT](http://opensource.org/licenses/MIT)




Have fun !
