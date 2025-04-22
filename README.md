# Word Ladder Adventure Game
🎮 Overview
The Word Ladder Adventure Game is a challenging and engaging puzzle game where players transform one word into another by changing one letter at a time, with each intermediate word being valid according to a dictionary. The game offers multiple difficulty levels, various modes, and the option to receive help through advanced search algorithms. Players can aim to solve the puzzle in the fewest moves possible to achieve the highest score.

# 🧩 Game Features
Single-Player Modes
Beginner Mode: 3-letter words.

Medium Mode: 4-letter words.

Advanced Mode: 5-letter words.

Challenge Mode: Some letters are banned to increase the game's difficulty.

Custom Mode: Players can choose their own start and target words.

Multiplayer Mode
Two players can compete against each other, solving the same word ladder.

The player who reaches the target word in fewer moves wins.

AI Assistance
Players can request hints using one of the following algorithms:

Breadth-First Search (BFS)

Uniform Cost Search (UCS)

A* Algorithm

Scoring System
The player’s score is based on the number of moves taken. Fewer moves result in a higher score.

The maximum score is 100, with 5 points deducted for each move.

🧑‍💻 Implementation Details
Dictionary Loading
The game loads a dictionary from a file named dictionary.txt.

Words are stored in a set for fast checking.

If the dictionary file is missing, the game will display an error and stop.

Word Transformations
The game allows players to transform words by changing one letter at a time.

Challenge Mode bans certain letters, making the puzzle more difficult.

Search Algorithms
The game uses three algorithms to help find the shortest path between the start and target words:

Breadth-First Search (BFS):

Explores all paths step by step.

Finds the shortest path in an unweighted graph, though it may be slower for longer word ladders.

Uniform Cost Search (UCS):

Expands paths based on cost (number of changes).

Uses a priority queue to prioritize lower-cost paths.

A* Algorithm:

Combines the path cost (g(n)) with an estimate of the remaining cost (h(n)).

The heuristic is the number of differing letters between the current word and the target word.

Game Modes
Single-Player Modes:

Players solve the word ladder alone and can request AI assistance through BFS, UCS, or A*.

Multiplayer Mode:

Two players take turns to solve the same word ladder.

The player with fewer moves wins.

Challenge Mode:

In this mode, certain letters are banned, and players must avoid using those letters in their transformations.

Scoring System
The score is based on the number of moves made:

The maximum score is 100.

5 points are deducted for each move taken.

🛠️ How We Built It
Dictionary and Graph Structure
Words are treated as nodes in a graph, and valid transformations between words are the edges connecting these nodes.

Search Algorithms:
BFS: Ensures the shortest path but may be slower.

UCS: Effective for paths with varying costs.

A*: Uses heuristics to speed up the search for the shortest path.

Game Modes:
The game features various modes to provide an enjoyable and challenging experience, including multiplayer and challenge modes.

The dictionary file is essential for the game to work, with error handling for missing files.

Multiplayer Logic:
In multiplayer mode, two players compete by taking turns to solve the same word ladder. The player who uses fewer moves to reach the target word wins.

📄 Game Requirements
Python 3.x

dictionary.txt: A text file containing a list of valid words (one per line).

No external libraries are required (pure Python).

📂 Project Structure
bash
Copy
Edit
word-ladder-adventure/
├── game.py              # Main game logic and algorithms
├── dictionary.txt       # List of valid words
└── README.md            # Project documentation
💡 Conclusion
The Word Ladder Adventure Game is a fun and intellectually stimulating puzzle game. It uses intelligent search algorithms to assist players, and it offers various modes to keep the game fresh and challenging. Whether playing solo or with a friend, players can aim to solve the word ladder in as few moves as possible to achieve the highest score!

📬 Contact
For any questions, suggestions, or contributions, feel free to reach out to me via email at: zainjadoon.dev@gmail.com.

