from collections import deque
import heapq
import random

def LoadDictionary(filename):
    try:
        with open(filename, "r") as file:
            words = set(word.strip().lower() for word in file)
        return words
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None

def Gettransformations(word, dictionary, bannedletters=None):
    wordlist = list(word)  
    validwords = set()  # Store valid transformations here

    # Loop through each letter in the word
    for i in range(len(word)):

        originalletter = wordlist[i] 
        # Try replacing the letter with every letter from 'a' to 'z'
        for char in "abcdefghijklmnopqrstuvwxyz":

            # Skip if the new letter is the same as the original or is banned
            if char != originalletter and (bannedletters is None or char not in bannedletters):
                wordlist[i] = char  # Replace the letter
                newword = "".join(wordlist)  # Convert the list back to a string
                # Check if the new word is in the dictionary and doesn't contain banned letters
                if newword in dictionary and (bannedletters is None or not any(letter in newword for letter in bannedletters)):
                    validwords.add(newword)  # Add the valid word to the set
                    
        wordlist[i] = originalletter  # Restore the original letter
    return validwords  # Return all valid transformations

# Checking whether the path between two words exists or not 
def Pathpossible(start, target, dictionary, bannedletters=None):
    # Both words must be in the dictionary and not contain banned letters
    return start in dictionary and target in dictionary and (bannedletters is None or not any(letter in start or letter in target for letter in bannedletters))

def BreadthFirstsearch(start, target, dictionary, bannedletters=None):
    queue = deque([[start]]) 
    visited = set([start]) 

    while queue:
        path = queue.popleft()  
        currentword = path[-1] 
        if currentword == target: 
            return path
        
        for nextword in Gettransformations(currentword, dictionary, bannedletters):
            if nextword not in visited:  # Avoid revisiting words
                visited.add(nextword)
                queue.append(path + [nextword])  # Add the new path to the queue

    return None  # If no path is found, return None

def ucs(start, target, dictionary, bannedletters=None):
    pqueue = [(0, [start])]  
    visited = set()  # Track visited words

    while pqueue:
        cost,path=heapq.heappop(pqueue)
        currentword = path[-1]  
        if currentword == target:  
            return path
        if currentword in visited:  
            continue
        visited.add(currentword)  
        for nextword in Gettransformations(currentword, dictionary, bannedletters):
            if nextword not in visited:  # Avoid revisiting words
                heapq.heappush(pqueue, (cost + 1, path + [nextword])) 
    return None  

def heuristic(word, target):
    return sum(1 for a, b in zip(word, target) if a != b)

def Astar(start, target, dictionary, bannedletters=None):
    pqueue = [(heuristic(start, target), 0, [start])] 
    visited = set() 

    while pqueue:
        _, cost, path = heapq.heappop(pqueue) 
        currentword = path[-1]  # Get the last word in the path
        if currentword == target: 
            return path
        if currentword in visited: 
            continue
        visited.add(currentword)  
      
        for nextword in Gettransformations(currentword, dictionary, bannedletters):
            if nextword not in visited:  # Avoid revisiting words
                newcost = cost + 1  # Increment the cost
                priority = newcost + heuristic(nextword, target)  # Calculate f(n) = g(n) + h(n)
                heapq.heappush(pqueue, (priority, newcost, path + [nextword]))  
    return None  
def DisplayMain():
    while True:
        print("------------------------------------ Word Ladder Adventure ------------------------------------")
        print("\t\t1. Beginner Mode (3-letter words)")
        print("\t\t2. Medium Mode (4-letter words)")
        print("\t\t3. Advanced Mode (5-letter words)")
        print("\t\t4. Challenge Mode (Random banned letters)")
        print("\t\t5. Custom Word Ladder")
        print("\t\t6. Multiplayer Mode")
        print("\t\t7. Exit")
        choice = input("Choose a mode (1-7): ")
        if choice.isdigit() and 1 <= int(choice) <= 7:  # Validate the input
            return choice
        print("Invalid input! Please enter a number between 1 and 7.")

def getRandwordpair(dictionary, wordlen, bannedletters=None):
    wordsoflength = [word for word in dictionary if len(word) == wordlen and (bannedletters is None or not any(letter in word for letter in bannedletters))]
    if not wordsoflength: 
        return None, None
    startword = random.choice(wordsoflength)
    targetword= random.choice(wordsoflength)
    while targetword== startword:  
        targetword = random.choice(wordsoflength)
    return startword, targetword if Astar(startword, targetword, dictionary, bannedletters) else getRandwordpair(dictionary, wordlen, bannedletters)

def CustomGame(dictionary, bannedletters=None):
    while True:
        startword = input("Enter the start word: ").strip().lower()
        targetword = input("Enter the target word: ").strip().lower()
        # Check if the words are valid and of the same length
        if not Pathpossible(startword, targetword, dictionary, bannedletters):
            print("Invalid words! Please choose words from the dictionary.")
            continue
        if len(startword) != len(targetword):
            print("Words must be of the same length!")
            continue
        return startword, targetword

def calculatescore(moves, maxmove):
    return max(0, 100 - (moves * 5))  # Deduct 5 points per move

def SinglePlayer(startword, targetword, dictionary, maxmove, bannedletters=None):
    print(f"\nTransform '{startword}' to '{targetword}'!")
    if bannedletters:
        print(f"Banned letters: {', '.join(bannedletters)}")
    currentword = startword
    moves = 0
    
    while currentword != targetword:
        print(f"\nCurrent word: {currentword}")
        print(f"Moves left: {maxmove - moves}")
        print("1. Enter next word")
        print("2. Get a hint")
        print("3. Quit")
        choice = input("Choose an option (1-3): ")
        
        if choice == "1":
            nextword = input("Enter the next word: ").strip().lower()
            if nextword in Gettransformations(currentword, dictionary, bannedletters):
                currentword = nextword
            else:
                print("Invalid transformation! That still counts as a move.")
            moves += 1
            if moves >= maxmove:
                print(f"\nOut of moves! You lost. The target word was '{targetword}'.")
                return
        elif choice == "2":
            print("\nChoose a hint algorithm:")
            print("1. BreadthFirstsearch")
            print("2. UCS")
            print("3. A*")
            Algochoice = input("Choose an algorithm (1-3): ")
            if Algochoice == "1":
                path = BreadthFirstsearch(currentword, targetword, dictionary, bannedletters)
            elif Algochoice == "2":
                path = ucs(currentword, targetword, dictionary, bannedletters)
            elif Algochoice == "3":
                path = Astar(currentword, targetword, dictionary, bannedletters)
            else:
                print("Invalid choice! Try again.")
                continue
            if path:
                print(f"Hint: Next word could be '{path[1]}'")
            else:
                print("No path found! Try different word pair.")
        elif choice == "3":
            print("Thanks!")
            return
        else:
            print("Invalid choice! Try again.")
    score = calculatescore(moves, maxmove)
    print(f"\nCongratulations! You transformed '{startword}' to '{targetword}' in {moves} moves!")
    print(f"Your score: {score}")

def Multiplayer(startword, targetword, dictionary, maxmove, bannedletters=None):
    print(f"\nTransform '{startword}' to '{targetword}'!")
    if bannedletters:
        print(f"Banned letters: {', '.join(bannedletters)}")
    
    player1 = input("Enter Player 1's name: ").strip()
    player2 = input("Enter Player 2's name: ").strip()
    
    p1Word = startword
    p2Word = startword
    p1Moves = 0
    p2Moves = 0
    
    while True:
        print(f"\n{player1}'s turn:")
        print(f"Current word: {p1Word}")
        print(f"Moves left: {maxmove - p1Moves}")
        print("1. Enter next word")
        print("2. Get a hint")
        print("3. Quit")
        choice = input("Choose an option (1-3): ")
        
        if choice == "1":
            nextword = input("Enter the next word: ").strip().lower()
            if nextword in Gettransformations(p1Word, dictionary, bannedletters):
                p1Word = nextword
            else:
                print("Invalid transformation!")
            p1Moves += 1
            if p1Word == targetword:
                print(f"\n{player1} wins! They transformed '{startword}' to '{targetword}' in {p1Moves} moves!")
                return
            if p1Moves >= maxmove:
                print(f"\n{player1} is out of moves!")
        elif choice == "2":
            print("\nChoose a hint algorithm:")
            print("1. BreadthFirstsearch")
            print("2. UCS")
            print("3. A*")
            Algochoice = input("Choose an algorithm (1-3): ")
            if Algochoice == "1":
                path = BreadthFirstsearch(p1Word, targetword, dictionary, bannedletters)
            elif Algochoice == "2":
                path = ucs(p1Word, targetword, dictionary, bannedletters)
            elif Algochoice == "3":
                path = Astar(p1Word, targetword, dictionary, bannedletters)
            else:
                print("Invalid choice! Try again.")
                continue
            if path:
                print(f"Hint: Next word could be '{path[1]}'")
            else:
                print("No path found! Try a different word pair.")
        elif choice == "3":
            print("Thanks for playing! Goodbye!")
            return
        else:
            print("Invalid choice! Try again.")
        
        # Player 2's turn
        print(f"\n{player2}'s turn:")
        print(f"Current word: {p2Word}")
        print(f"Moves left: {maxmove - p2Moves}")
        print("1. Enter next word")
        print("2. Get a hint")
        print("3. Quit")
        choice = input("Choose an option (1-3): ")
        
        if choice == "1":
            nextword = input("Enter the next word: ").strip().lower()
            if nextword in Gettransformations(p2Word, dictionary, bannedletters):
                p2Word = nextword
            else:
                print("Invalid transformation!")
            p2Moves += 1
            if p2Word == targetword:
                print(f"\n{player2} wins! They transformed '{startword}' to '{targetword}' in {p2Moves} moves!")
                return
            if p2Moves >= maxmove:
                print(f"\n{player2} is out of moves!")
        elif choice == "2":
            print("\nChoose a hint algorithm:")
            print("1. BreadthFirstsearch")
            print("2. UCS")
            print("3. A*")
            Algochoice = input("Choose an algorithm (1-3): ")
            if Algochoice == "1":
                path = BreadthFirstsearch(p2Word, targetword, dictionary, bannedletters)
            elif Algochoice == "2":
                path = ucs(p2Word, targetword, dictionary, bannedletters)
            elif Algochoice == "3":
                path = Astar(p2Word, targetword, dictionary, bannedletters)
            else:
                print("Invalid choice! Try again.")
                continue
            if path:
                print(f"Hint: Next word could be '{path[1]}'")
            else:
                print("No path found! Try a different word pair.")
        elif choice == "3":
            print("Thanks for playing! Goodbye!")
            return
        else:
            print("Invalid choice! Try again.")
        
        # Check if both players are out of moves
        if p1Moves >= maxmove and p2Moves >= maxmove:
            print(f"\nIt's a tie! Both players ran out of moves. The target word was '{targetword}'.")
            return

# Main function to run the game
def main():
    dictionary = LoadDictionary("dictionary.txt")  # Load the dictionary
    if not dictionary:
        return
    while True:
        choice = DisplayMain()  # Show the menu and get the user's choice
        if choice == "7":
            print("Thanks for playing! Goodbye!")
            break
        if choice == "5":
            startword, targetword = CustomGame(dictionary)
            maxmove = 15
            bannedletters = None
            SinglePlayer(startword, targetword, dictionary, maxmove, bannedletters)
        elif choice == "4":
            bannedletters = random.sample("abcdefghijklmnopqrstuvwxyz", k=3)  # Ban 3 random letters
            wordlen = random.choice([3, 4, 5])
            maxmove = 10 + 5 * (wordlen - 3)
            startword, targetword = getRandwordpair(dictionary, wordlen, bannedletters)
            SinglePlayer(startword, targetword, dictionary, maxmove, bannedletters)
        elif choice == "6":
            wordlen = random.choice([3, 4, 5])
            maxmove = 10 + 5 * (wordlen - 3)
            bannedletters = None
            startword, targetword = getRandwordpair(dictionary, wordlen)
            Multiplayer(startword, targetword, dictionary, maxmove, bannedletters)
        else:
            wordlen = int(choice) + 2
            maxmove = 10 + 5 * (wordlen - 3)
            bannedletters = None
            startword, targetword = getRandwordpair(dictionary, wordlen)
            SinglePlayer(startword, targetword, dictionary, maxmove, bannedletters)

if __name__ == "__main__":
    main()