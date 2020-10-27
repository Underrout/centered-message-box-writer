# centered-message-box-writer

A small python script I wrote for centering text in Super Mario World message boxes. Supports writing to to the console or a specified file, supports standard and expanded message box sizes, by default it will show you all possible ways of centering the message, but you can also make it filter the boxes that have the least variance in line length (aka the ones that look the most balanced).

This was made specifically for the Super Mario World message box formats, but it could be easily adapted to work for other dimensions too, if you needed it to.

# Usage

Just download the script and put it in a folder, run it with the python interpreter (most versions should work, I tested with 3.8) via the command line, input your text and press enter, the script will output what the box will look like in-game in a square format and print a string you can copy directly into the Lunar Magic overworld message editor to save the centered message (note: you have to untick word wrap for it to work cause LM will by default destroy the formatting)

Note that if your message can't be centered exactly, meaning that one or more lines can't be perfectly centered due to word length, the script will tell you that no valid boxes were found. The same will happen, if you message is too long for the message box format.

# Command Line Options

Option | Argument | Description
-------|----------|------------
-f | filename | Writes the boxes to the specified file in the same directory as the script instead of printing them to stdout, useful if you have a long message that could have a lot of possible ways to be centered
-b |  | Will make the script only show you the boxes with the least variance in line length instead of showing all possible boxes, boxes with the least variance usually look the best so I recommend using this option if you don't want to look through all the options manually
-e |  | Switches the message box format from standard message box size (128 characters [16x8]) to expanded message box size (260 characters [26x10])
