from __future__ import annotations
from constants import PlayerPosition, PlayerStats
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining


class Player:

    def __init__(self, name: str, position: PlayerPosition, age: int) -> None:
        """
        Constructor for the Player class

        Args:
            name (str): The name of the player
            position (PlayerPosition): The position of the player
            age (int): The age of the player

        Returns:
            None

        Complexity:
            Best Case Complexity: Assigining name , age and position all have complexity of  O(1). The hash 
            table iterates through the entire length on the PlayerStats and creates arrays for each stat 
            this means the time compexity. 
            O(M) where M is the size of the hash table.  
            Inserting values into a hash table will take O(N) as the for loop iteraters over PlaerSatsts.Given that 
            there are N elements in PlayerStats. 
            Thus the best case becomes O(N+M)
            Worst Case Complexity: In the worst case there maybe collision in the linked list thus the worst 
            time complexity will be O(N+M*L) where M is the number of elements in the PlayerStats and L is the length 
            of the linked list at each position. 

        """
        if age<18: 
            raise ValueError
        self.name= name
        self.position=position
        self.age=age 
        self.statistics=HashTableSeparateChaining(len(PlayerStats))
        # iniialising the value of the statistics to zero 
        for stat in PlayerStats: 
            self.statistics[stat.value]=0

    def reset_stats(self) -> None:

        """
        Reset the stats of the player

        Returns:
            None

        Complexity:
            Best Case Complexity: In the caase that there are no collisions the best case will be O(1)
            as updating and declaring have constant time complexity. Since it has to go through all of the players 
            in stat the best time complexity will be O(M) where M is the number of elements in PlayerStats
            Worst Case Complexity: The worts time complexity is having to iterate through all of the cases and therre is collision in everything 
            thus the worst time compleexity woulld be having to iterate through the linked lists. 
            The worst case will be O(N*L ) where N is the number of elements in PlayerStats and L is the lnegth of a linked List 
            int he hashtable. 

        """
        for stat in PlayerStats: 
            self[stat]=0
        

        

    def get_name(self) -> str:
        """
        Get the name of the player

        Returns:
            str: The name of the player

        Complexity:
            Best Case Complexity:  O(1) as retunring a value has constant time complexity. 
            Worst Case Complexity:O(1) as retunring a value has constant time complexity. 
        """
        return self.name 
    

    def get_position(self) -> PlayerPosition:
        """
        Get the position of the player

        Returns:
            PlayerPosition: The position of the player

        Complexity:
            Best Case Complexity:O(1) as retunring a value has constant time complexity. 
            Worst Case Complexity:O(1) as retunring a value has constant time complexity. 
        """
        return self.position

    def get_statistics(self):
        """
        Get the statistics of the player

        Returns:
            statistics: The players' statistics

        Complexity:
            Best Case Complexity: returning from hash table has a constant time complexity thus it will remain O(1)
            Worst Case Complexity:returning from hash table has a constant time complexity thus it will remain O(1)
        """
        return self.statistics

    def __setitem__(self, statistic: PlayerStats, value: int) -> None:
        """
        Set the value of the player's stat based on the key that is passed.

        Args:
            statistic (PlayerStat): The key of the stat
            value (int): The value of the stat

        Returns:
            None

        Complexity:
            Best Case Complexity: The bests complexity would be just setting the value in the hash table without collsion thus
              giving constant time complexity O(1)
            Worst Case Complexity: The worst time complexity wpuld happen in the case of collision thus resulting in traversal through linked list 
              which would give a time complexity of O(L) where L is the length of a linked list. 
        """
        self.statistics[statistic.value] = value


    def __getitem__(self, statistic: PlayerStats) -> int:
        """
        Get the value of the player's stat based on the key that is passed.

        Args:
            statistic (PlayerStat): The key of the stat

        Returns:
            int: The value of the stat

        Complexity:
            Best Case Complexity:The bests complexity would be just getting the value in the hash table without collsion thus
              giving constant time complexity O(1)
            Worst Case Complexity:The worst time complexity wpuld happen in the case of collision thus resulting in traversal through linked list 
              which would give a time complexity of O(L) where L is the length of a linked list.
        """
        return self.statistics[statistic.value]

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the player object.

        Complexity:
            Analysis not required.
        """
        return f"Player(name={self.name}, position={self.position}, age={self.age})"


    def __repr__(self) -> str:
        """Returns a string representation of the Player object.
        Useful for debugging or when the Player is held in another data structure."""
        return str(self)
