-----------
Tic Tac Toe
-----------

======================
Paul Schwendenman
======================


Getting Started
---------------

Run your own tictactoe game call the main method. Like this::

	import tictac
	tictac.main(players)

Players must be a list of length 3. The first spot list[0] is 
ignored. The objects in slots 1 and 2 should be players.





Make Your Own Player
====================

players:
	An object with methods getMove and handleGameOver.

method getMove:
	Should select and return a valid move on a tictactoe board. 

method handleGameOver:
	This is called once the game is over and can handle any
	saving of information about the results here.

The basic player is modeled by::

        class Player():
            '''
            The base player class for a game.
            '''
            def __init__(self, index):
                self.index = index

            def getMove(self, *args):
                '''
                This function should take a variable number
                of inputs and return a single number.

                Typically takes two inputs:
                - the current grid
                - an error raised flag

                Output:
                - should be in [0...8] (3x3 grid)
                '''
                pass

            def handleGameOver(self, *args):
                '''
                The method should handle all end game
                activities for the player.

                Typical Input:
                - winner
                - startingplayer
                - gamegrids
                - index, aidata <-- local
                '''
                pass

Translation
-----------

Because there are 9 spaces and 3 choices for each 
space it follows that there are 3^9 (19,683) possible boards.
However because the game is turn based more games can be eliminated.
For example there cannot ever be a difference of more than one between
the number of X's and the number of O's.

So boards like this can be eliminated::

     X | O | X 
    ---+---+---
     X | X | X 
    ---+---+---
     O |   |   

Because X has clearly played more times than O. Which leaves 6,046 unique
games. Additional games can be eliminated because play stops once the first
player has connect three in a row.

So although this game shows proper alternation it also has two winners 
so the game stop have been stopped already.::

     X | O | X 
    ---+---+---
     X | O | X 
    ---+---+---
     O | O | X 

Removing games that appear to have more than one winner we are left with 5890 games.

This however can still be further reduced and should be. By using common translations
we are able to reduce this number to 826 unique layouts.

Flips
=====

Vertical
++++++++

Fliping over the the vertical axis yields::

       | * |   
    ---+---+---
       | * |   
    ---+---+---
       | * |   

       | O |   
    ---+---+---
     X |   |   
    ---+---+---
       | O | X 

       | O |   
    ---+---+---
       |   | X 
    ---+---+---
     X | O |   

Horizontal
++++++++++

Fliping over the the horizontal axis yields::

       |   |   
    ---+---+---
     * | * | * 
    ---+---+---
       |   |   

       | O |   
    ---+---+---
     X |   |   
    ---+---+---
       | O | X 

       | O | X 
    ---+---+---
     X |   |   
    ---+---+---
       | O |   

First Diagonal
++++++++++++++

Fliping over the top left corner to bottom right corner axis yields::

     * |   |   
    ---+---+---
       | * |   
    ---+---+---
       |   | * 

       | O |   
    ---+---+---
     X |   |   
    ---+---+---
       | O | X 

       | X |   
    ---+---+---
     O |   | O 
    ---+---+---
       |   | X 

Second Diagonal
+++++++++++++++

Fliping over the top right corner to bottom left corner axis yields::

       |   | * 
    ---+---+---
       | * |   
    ---+---+---
     * |   |   

       | O |   
    ---+---+---
     X |   |   
    ---+---+---
       | O | X 

     X |   |   
    ---+---+---
     O |   | O 
    ---+---+---
       | X |   


Turns
=====

Clockwise 90 degrees
++++++++++++++++++++

::

       | O |   
    ---+---+---
     X |   |   
    ---+---+---
       | O | X 

       | X |   
    ---+---+---
     O |   | O 
    ---+---+---
     X |   |   

Counter-Clockwise 90 degrees
++++++++++++++++++++++++++++

::

       | O |   
    ---+---+---
     X |   |   
    ---+---+---
       | O | X 

       |   | X 
    ---+---+---
     O |   | O 
    ---+---+---
       | X |   

Super
=====

This translation can be accomplished both by turning and by flipping. If you flip
both horizontally and vertically or you ture the grid 180 degrees in either direction
you will discover the final translation::

       | O |   
    ---+---+---
     X |   |   
    ---+---+---
       | O | X 

     X | O |   
    ---+---+---
       |   | X 
    ---+---+---
       | O |   

Special Note
============

All of these translations have an inverse. For the flips and the super they are
their own inverse. However in the case of the turns you will need to use the 
counter-clockwise turn to reverse the clockwise turn.





