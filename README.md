# Mohr's Circle Manim Plugin
A plugin that allows for the representation of Mohr's Circle (along with key properties of the circle) as a [Manim](https://www.manim.community/) Mobject.

## Why did I make this plugin?
The main reason for developing this plugin was a realisation that online tools for creating Mohr's circle generally focus
on the final product, rather than the method to produce it. 

Hence, this plugin allows for the creation method of the circle to be shown as an easy-to-understand animation.

## What can it currently do? 
- Create a Mohr's Circle, based on the 3 tensor stresses (x,y and shear)
- Show the 2 points that make the diameter of the circle. 
- Show the creation of the circle via the 2 points. 
- Show the position of the principle stresses and max / min shear stresses. 

## TODO-List (Contributors Welcome)
- Creating some "default animations" for each of the primary Mohr's Circle tasks (such as a nice "protractor" animation for the circle creation)
- Sorting out the axes vs raw data relationship between fields (so it is easier to create new points that fit on the axes correctly)
- Moving the rotated tensor points to the new `MohrCirclePoint(VGroup)` class instance.
- Improve the logic for allowing dynamic options for individual aspects of the Circle (e.g: Different colour for each Point specified, different label positions etc.)