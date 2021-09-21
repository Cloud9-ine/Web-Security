# Web-Security Homework #1, Readme

## Part1, Offline version.
Implemented by JavaScript
### Operation Instruction:
1. Simply open the html file "offline.html" in the folder "Part1-Offline". 
2. You will see a page opened by your browser showing the "Five-in-a-Row, Offline", together with the board.
3. The game is started then, just click on any point of intersection lines to put piece.
   1. The first click is always black due to the rule of "Five-in-a-Row".
   2. The second click is then white, and each player will take turn to put pieces on the board.
   3. Anyone who first reaches a "Five-in-a-Row" will win the game and the game is then finished.
   4. Any click on illegal position (outside the board, not the intersection of lines, or places occupied by previous pieces already, or the game is finished) will be denied and the player will received an alert information so that the player needs to choose a legal position.
4. To restart a game, the page should be refreshed.


## Part2, Online version.
Implemented by JavaScript and Python (Flask)
### Operation Instruction:
1. Switch to the folder "Part2-Online".
2. Open a terminal in that folder and execute "python app.py".
3. Open the browser.
4. Open the first page with the link: localhost:5000, this player will be the black one.
5. Open the second page with the same link: localhost:5000, this player will be the white one.
6. You will see a page opened by your browser showing the "Five-in-a-Row, Online", together with the board.
7. The game is started then.
   1. (The rules are similar to the offline version.)
   2. The black player is first to click.
   3. The white player player is second to click, and each player will take turn to put pieces on the board.
   4. Anyone who first reaches a "Five-in-a-Row" will win the game and the game is then finished.
   5. Any click on illegal position (outside the board, not the intersection of lines, or places occupied by previous pieces already, or the game is finished) will be denied and the player will received an alert information so that the player needs to choose a legal position.
   6. Any click not in this player's turn do not have any effect, the player should wait for the other to finish the step.
8. To restart a game. 
   1. The server should be shut down and restarted.
   2. Then refresh pages in the browser to restart a game.