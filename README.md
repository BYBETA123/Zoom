# Zoom

Simple zoom macro designed using TKinter and system libraries to allow users to zoom into portions on their screen

This works across multiple desktops

## Requirements

PIL, TKinter

## Usage:

Run the zoom.py file using the command `python zoom.py` and a window will appear on the screen


# Features:

Scale bar: Allows up to 10x zoom

X box-width: The amount of pixels wide the box captures Allows between 10 and 500 px
Y box-width: The amount of pixels high the box captures Allows between 10 and 500 px

Coordinates: The current position of your mouse (negative values are not above, it just means that the cursor is to the left or above the 1st monitor display)

Color: The tuple and Hex versions of the exact pixel that the cursor is currently over