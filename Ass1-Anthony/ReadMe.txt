Command to run the game: "python3 Ass1.py"  or   "./Ass1.py"
OS: macOS 26.0.1

Description: The source file "Ass1.py" contains three objects and a main function. The first object handles the CLI
             that displays the matrix and messages to the user as well as take inputs from the user. The user plays the
             game by entering the row and column they want to place the next number in. Other options they have are to
             save the game, load a saved game, or quit.
             
             The second object handles the rules and logic for the game. It checks validity of user moves and updates
             the states for the game after every move; it also awards points based on diagonal moves.
             
             The third object handles the file saving and loading. When a user saves a game, the matrix is saved along
             with current number, score and the last position. When a user loads a game, the values are added to the 
             state of the game so the user can continue.
             The user chooses the name for their incomplete game, and .txt is automatically added to the name.
             When the user loads a game, they must input the complete filename including the extension.
             A user can only load a saved game at the first iteration of the game. After the user makes the first move,
             they can no longer load an old game, as the current game will be lost.
             
             The main function handles the while loop that runs the game. It displays the matrix and takes user input
             at every iteration. It calls functions from objects based on the user input. It breaks the loop when a 
             user quits, makes an invalid move or wins. Specific messages are shown to the user explaining on the the 
             invalid move they made.
