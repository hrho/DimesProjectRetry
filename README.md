DimezFinalProject:
==================

	- From the Creators of 2016's Game of the Year, We Goin' Golfin'....

	- Chris Rho(hrho) and Joey Curci(jcurci) proudly present our next immersive sports sim....


NBA 2K18:
=========

	- OH NO!!

	- Crying Jordan is here to ruin your day!

	- Only the greatest basketball teams of all time can stop him!

	- Pick from a wide variety of ELITE basketball teams in order to stop Crying Jordan and avoid blowing a 3-1 Lead.

Setup:
======

	- Both players log onto ash.campus.nd.edu
	- Player 1 runs "python nba1.py"
	- Then, Player 2 runs "python nba2.py"
	- Player 1 has the options to choose from 8 teams, and will see a message "Waiting for Player 2 to connect brah". Obviously, when Player 2 connects, the message will chagne to "Player 2 connected" and the game can be started by clicking on a team.
	- Player 2's window will show "Waiting for P1", which waits for Player 1 to choose a team. Once a team is chosen, the game will start.
	- If a player wants to rage quit, Ctrl+C in the terminal or close the window

How to Play:
============

	- Player One controls the player at the bottom of the screen using the arrow keys.  Try and catch as many basketballs as possible! Avoid catching bombs though! 
	Each basketball adds 1 to your score, while each bomb subtracts 1 from your score.

	- Player Two controls crying jordan.  Use the mouse to aim and fire tears at the basketballs. You can only shoot one tear at a time on the screen! Go for combo shots. Shoot down as many basketballs as possible! Avoid shooting bombs though! 
	Each basketball adds 1 to your score, while each bomb subtracts 2 from your score.

	- To balance the game for both players (after testing out the gameplay, it was deemed Player 2 was OP with the old setup),
	player 1 must get a score of 7 to win, while player 2 must get a score of 10 to win.

Important Notes:
==============

	- Due to the way the TCP connections are set-up, nba1.py must be run before nba2.py.
	- The game runs very slow unless in one of the machines in Cushing/Fitzpatrick
	- Stackoverflow, pygame tutorial pages, cPickle, and tcp manual pages were often sought to get the connections running and the game to work.

