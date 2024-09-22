from __future__ import annotations
from data_structures.referential_array import ArrayR
from constants import GameResult, PlayerPosition, PlayerStats, TeamStats
from player import Player
from typing import Collection, Union, TypeVar
from data_structures.hash_table import LinearProbeTable
from data_structures.linked_list import LinkedList
from data_structures.array_sorted_list import ArraySortedList

T = TypeVar("T")


class Team:
    # Unique number for each team, will be incremented by each team is initialised
    team_number = 1
    team_length = 0

    def __init__(self, team_name: str, players: ArrayR[Player]) -> None:

        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            players (ArrayR[Player]): The players of the team

        Returns:
            None

        Complexity:
            Best Case Complexity:Operator assignment takes time complexity of O(1) Best complexity O(S+P+N)  where S is the number of statsics, P in the number
            of positions and N is the number of of players. 
            Worst Case Complexity:Best Case Complexity:Operator assignment takes time complexity of O(1) Best complexity O(S+P+N)  where S is the number of statsics, P in the number
            of positions and N is the number of of players.  
              
        """

        self.number = self.team_number 
        self.team_number = self.team_number + 1 
        Team.team_number += 1

        self.team_name = team_name

        self.statistics = LinearProbeTable()

        self.all_players = LinkedList()
        

        for stat in TeamStats:
            if stat.value != "Last Five Results":
                self.statistics[stat.value] = 0
            elif stat.value == "Last Five Results":
                self.statistics[stat.value] = LinkedList()
        
        self.players = LinearProbeTable()
        
        for pos in PlayerPosition:
            self.players[pos.value] = LinkedList()
        
        for player in players:
            self.team_length +=1
            self.players[player.position.value].append(player)
            self.all_players.append(player)
        
        

        

    def reset_stats(self) -> None:
        """
        Resets all the statistics of the team to the values they were during init.

        Complexity:
            Best Case Complexity: O(N) where N is the number of players in TeamStats. 
            In the best case scenario that when clear is used, ie. the last Five results are
            0. Setting all statsic values takes complexity of O(1). Thus the best complexity would be O(N) where N 
            is the number of statistics in TeamStat. 
            Worst Case Complexity: O(N+L) where N is the number of statistics and L in the number of elements in the
            linked list. 
            In the worst case there will be elements reseting when we have to reset the LnkedList for each of the
            Last five results. 
        """
        for stat in TeamStats:
            if stat.value != "Last Five Results":
                self.statistics[stat.value] = 0
            elif stat.value == "Last Five Results":
                self.statistics[stat.value].clear()
        

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1) , adding to a hash table has constant time complexity 
            Worst Case Complexity: O(1), adding to a hash table has constant time complexity
        """
        self.players[player.position.value].append(player)
        self.all_players.append(player)
        self.team_length +=1

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            Best Case Complexity: O(1) constant time complexity as retrival from hash table has complexity O(1)
            and if the data to be removed is at the beginning of the list. 
            Worst Case Complexity: O(1)onstant time complexity as retrival from hash table has complexity O(1). 
        """
        index = self.players[player.position.value].index(player)
        self.players[player.position.value].delete_at_index(index)
        index_1 = self.all_players.index(player)
        self.all_players.delete_at_index(index_1)
        self.team_length -=1

    def get_number(self) -> int:
        """
        Returns the number of the team.

        Complexity:
            Analysis not required.
        """
        return self.team_number

    def get_name(self) -> str:
        """
        Returns the name of the team.

        Complexity:
            Analysis not required.
        """
        return self.team_name

    def get_players(self, position: Union[PlayerPosition, None] = None) -> Union[Collection[Player], None]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (Union[PlayerPosition, None]): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder this includes the ArrayR
            which was previously prohibited.

            None: When no players match the criteria / team has no players

        Complexity:
            Best Case Complexity: O(1) happens when the positions lsit is empty. 
            Worst Case Complexity: O(N) where N is the number of players and the potiiton is at then end of the list
        """
        if position is None:
            
            ordered_players = LinkedList()
            for pos in PlayerPosition:
                for player in self.players[pos.value]:
                    ordered_players.append(player)
        
       
            if ordered_players.is_empty():
                return None
            return ordered_players
        else:
                
            if self.players[position.value].is_empty():
                return None
            return self.players[position.value]
    

    def get_statistics(self):
        """
        Get the statistics of the team

        Returns:
            statistics: The teams' statistics

        Complexity:
            Best Case Complexity: O(1) returning a linear table has constant time complexity 
            Worst Case Complexity: O(1) returning a linear table has constant time complexity
        """
        return self.statistics

    def get_last_five_results(self) -> Union[Collection[GameResult], None]:
        """
        Returns the last five results of the team.
        If the team has played less than five games,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the array should be an array of size 4
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        *Important Note:*
        If this method is called before the team has played any games,
        return None the reason for this is explained in the specefication.

        Returns:
            Collection[GameResult]: The last five results of the team
            or
            None if the team has not played any games.

        Complexity:
            Best Case Complexity: O(1) when none is returned 
            Checking the length has complexity O(1)
            comparing the values has complexity O(1)
            returning none has complexity also O(1)
            Worst Case Complexity: O(1) as accessing elements and returning them all have complexity O(1)
        """
        if len(self.statistics["Last Five Results"]) != 0:
            return self.statistics["Last Five Results"]
        elif self.statistics["Games Played"] == 0:
            return None
        else:
            return None

    def get_top_x_players(self, player_stat: PlayerStats, num_players: int) -> list[tuple[int, str, Player]]:
        """
        Note: This method is only required for FIT1054 students only!

        Args:
            player_stat (PlayerStats): The player statistic to use to order the top players
            num_players (int): The number of players to return from this team

        Return:
            list[tuple[int, str, Player]]: The top x players from this team
        Complexity:
            Best Case Complexity: 
            Worst Case Complexity:
        """
        raise NotImplementedError

    def __setitem__(self, statistic: TeamStats, value: int) -> None:
        """
        Updates the team's statistics.

        Args:
            statistic (TeamStats): The statistic to update
            value (int): The new value of the statistic

        Complexity:
            Best Case Complexity:O(1) 
            Worst Case Complexity: O(1)
        """
        if statistic.value == "Wins":
            dif =  value - self.statistics[statistic.value]
            self.statistics[statistic.value] = value
            self.statistics["Games Played"] += dif
            self.statistics["Points"] = self.statistics["Points"] + (GameResult.WIN*dif)

            if len(self.statistics["Last Five Results"]) >= 5:
                self.statistics["Last Five Results"].delete_at_index(0)

            self.statistics["Last Five Results"].append(GameResult.WIN)
        elif statistic.value == "Losses":
            dif =  value - self.statistics[statistic.value]
            self.statistics[statistic.value] = value
            self.statistics["Games Played"] += dif

            if len(self.statistics["Last Five Results"]) >= 5:
                self.statistics["Last Five Results"].delete_at_index(0)

            self.statistics["Last Five Results"].append(GameResult.LOSS)
        elif statistic.value == "Draws":
            dif =  value - self.statistics[statistic.value]
            self.statistics[statistic.value] = value
            self.statistics["Games Played"] += dif
            self.statistics["Points"] = self.statistics["Points"] + (GameResult.DRAW*dif)

            if len(self.statistics["Last Five Results"]) >= 5:
                self.statistics["Last Five Results"].delete_at_index(0)
            self.statistics["Last Five Results"].append(GameResult.DRAW)
        elif statistic.value == "Goals For" or statistic.value == "Goals Against":
            self.statistics[statistic.value] = value
            self.statistics["Goals Difference"] = self.statistics["Goals For"] - self.statistics["Goals Against"]
        else:
            self.statistics[statistic.value] = value

        
        


    def __getitem__(self, statistic: TeamStats) -> int:
        """
        Returns the value of the specified statistic.

        Args:
            statistic (TeamStats): The statistic to return

        Returns:
            int: The value of the specified statistic

        Raises:
            ValueError: If the statistic is invalid

        Complexity:
            Best Case Complexity: O(1) retruning values in hash have a constant time complexity
            Worst Case Complexity: O(1) returning values in a hash have a constant time compelxity
        """
        return self.statistics[statistic.value]

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity:
            Best Case Complexity: O(1) retuning length has constant time complexity
            Worst Case Complexity: O(1) returning length has constant time complexity
        """
        return self.team_length

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity:
            Analysis not required.
        """
        return f"Team: {self.team_name}"

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure."""
        return str(self)
    
    def __lt__(self,other) -> bool:
        """ 
        lt the function is used to compare values less than  
        Args: 
            self and other, home team and away team

        Returns:
            Teams in descending order 

        Complexity: 
            Best Complexity: O(1)
            Worst Complexity: O(S)Whrre S is the length of the longest strin in TeamStats Being compared. 
        
        """
        
        
        if self[TeamStats.POINTS]==other[TeamStats.POINTS]: 
            if self[TeamStats.GOALS_DIFFERENCE]==other[TeamStats.GOALS_DIFFERENCE]:
                if self[TeamStats.GOALS_FOR]==other[TeamStats.GOALS_FOR]:
                    return self.get_name()<other.get_name() 
                return self[TeamStats.GOALS_FOR]>other[TeamStats.GOALS_FOR]
            return self[TeamStats.GOALS_DIFFERENCE]>other[TeamStats.GOALS_DIFFERENCE]
        return self[TeamStats.POINTS]>other[TeamStats.POINTS]
        


        
    def __le__ (self,other)-> bool:
        """
        magic method less than equals to 
        Args: 
            self and other representing the home team and away team 
        
        Returns:
            Teams in descending order 

        Complexity: 
            Best Complexity: O(1)
            Worst Complexity: O(S)Whrre S is the length of the longest strin in TeamStats Being compared. 
        
        

        """
        if self[TeamStats.POINTS]==other[TeamStats.POINTS]: 
            if self[TeamStats.GOALS_DIFFERENCE]==other[TeamStats.GOALS_DIFFERENCE]:
                if self[TeamStats.GOALS_FOR]==other[TeamStats.GOALS_FOR]:
                    return self.get_name()<=other.get_name() 
                return self[TeamStats.GOALS_FOR]>=other[TeamStats.GOALS_FOR]
            return self[TeamStats.GOALS_DIFFERENCE]>=other[TeamStats.GOALS_DIFFERENCE]
        return self[TeamStats.POINTS]>=other[TeamStats.POINTS]