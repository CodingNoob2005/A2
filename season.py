from __future__ import annotations
from data_structures.bset import BSet
from data_structures.referential_array import ArrayR
from dataclasses import dataclass
from team import Team
from typing import Generator, Union
from data_structures.array_sorted_list import ArraySortedList
from data_structures.hash_table import LinearProbeTable
from constants import TeamStats
from data_structures.linked_list import LinkedList
from constants import ResultStats, PlayerStats, GameResult
from game_simulator import GameSimulator



@dataclass
class Game:
    """
    Simple container for a game between two teams.
    Both teams must be team objects, there cannot be a game without two teams.

    Note: Python will automatically generate the init for you.
    Use Game(home_team: Team, away_team: Team) to use this class.
    See: https://docs.python.org/3/library/dataclasses.html
    """
    home_team: Team = None
    away_team: Team = None
    def __repr__(self) -> str:
        return f"home={self.home_team} away={self.away_team}"


class WeekOfGames:
    """
    Simple container for a week of games.

    A fixture must have at least one game.
    """

    def __init__(self, week: int, games: ArrayR[Game]) -> None:
        """
        Container for a week of games.

        Args:
            week (int): The week number.
            games (ArrayR[Game]): The games for this week.
        """
        self.games: ArrayR[Game] = games
        self.week: int = week

    def get_games(self) -> ArrayR:
        """
        Returns the games in a given week.

        Returns:
            ArrayR: The games in a given week.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.games

    def get_week(self) -> int:
        """
        Returns the week number.

        Returns:
            int: The week number.

        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        return self.week

    def __iter__(self):
        """
        Complexity:
        Best Case Complexity: O(1) initialiasation and return both have O(1) complexity respectively
        Worst Case Complexity: O(1) initialisation and return both have O(1) complexity respectively
        """
        self.i=0
        return self
        #raise NotImplementedError

    def __next__(self):
        """
        Complexity:
        Best Case Complexity: O(1) games acess, compasision, incrementing index all have O(1)
        Worst Case Complexity:O(1) games acess, compasision, incrementing index all have O(1)
        """
        if self.i <len(self.games):
            game=self.games[self.i]
            self.i+=1 
            return game
        else: 
            raise StopIteration
        #raise NotImplementedError
    
    def __repr__(self) -> str:
        return f'{self.week} {self.games}'




class Season:
    



    def __init__(self, teams: ArrayR[Team]) -> None:
        """
        Initializes the season with a schedule.

        Args:
            teams (ArrayR[Team]): The teams played in this season.

        Complexity:
            Best Case Complexity: O(T+S+W)  where T is the number of teams, S is the complexity of generating the schedule and W is the number of weeks.
            Worst Case Complexity: O(T^2 + S + W) where S is the complexity of generating the schedule, 
                                    W is the number of weeks in the schedule. 
        """
        self.teams=teams
        self.leaderboard= ArraySortedList(len(self.teams))
        ##
        for team in self.teams:
            self.leaderboard.add(team)
        
        self.schedule=LinkedList()
        schedule_array=self._generate_schedule() 
        for week in range (len(schedule_array)): 
            self.schedule.append(WeekOfGames(week+1,schedule_array[week]))

    def update_team_stats(self,home_team: Team, away_team: Team, result: LinearProbeTable) -> None:
        """
    Update the team stats (wins, draws, losses, goals for, goals against).
    
    Args:
        home_team (Team): The home team object.
        away_team (Team): The away team object.
        result (LinearProbeTable): The result of the game simulation.

        Complexity:
            Best Case Complexity: O(1) retrieving index values in Linear Probe table and updating also have constant time complexity O(1)
            Worst Case Complexity:  O(1) retrieving index values in Linear Probe table and updating also have constant time complexity O(1)
    """
        home_goals = result[ResultStats.HOME_GOALS.value]
        away_goals = result[ResultStats.AWAY_GOALS.value]
        
        # Update team goals
        home_team[TeamStats.GOALS_FOR] += home_goals
        home_team[TeamStats.GOALS_AGAINST] += away_goals
        away_team[TeamStats.GOALS_FOR] += away_goals
        away_team[TeamStats.GOALS_AGAINST] += home_goals



    def _generate_schedule(self) -> ArrayR[ArrayR[Game]]:
        """
        Generates a schedule by generating all possible games between the teams.

        Return:
            ArrayR[ArrayR[Game]]: The schedule of the season.
                The outer array is the weeks in the season.
                The inner array is the games for that given week.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams in the season.
            Worst Case Complexity: O(N^2) where N is the number of teams in the season.
        """
        num_teams: int = len(self.teams)
        weekly_games: list[ArrayR[Game]] = []
        flipped_weeks: list[ArrayR[Game]] = []
        games: list[Game] = []

        # Generate all possible matchups (team1 vs team2, team2 vs team1, etc.)
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                games.append(Game(self.teams[i], self.teams[j]))

        # Allocate games into each week ensuring no team plays more than once in a week
        week: int = 0
        while games:
            current_week: list[Game] = []
            flipped_week: list[Game] = []
            used_teams: BSet = BSet()

            week_game_no: int = 0
            for game in games[:]:  # Iterate over a copy of the list
                if game.home_team.get_number() not in used_teams and game.away_team.get_number() not in used_teams:
                    current_week.append(game)
                    used_teams.add(game.home_team.get_number())
                    used_teams.add(game.away_team.get_number())

                    flipped_week.append(Game(game.away_team, game.home_team))
                    games.remove(game)
                    week_game_no += 1

            weekly_games.append(ArrayR.from_list(current_week))
            flipped_weeks.append(ArrayR.from_list(flipped_week))
            week += 1

        return ArrayR.from_list(weekly_games + flipped_weeks)
    
    def update_individual_player_stats(self,home_team: Team, away_team: Team, player_list: ArrayR, stat: PlayerStats) -> None:
        """
        Helper function to update individual player stats for goals, assists, interceptions, and tackles.
        
        Args:
            home_team (Team): The home team object.
            away_team (Team): The away team object.
            player_list (ArrayR): ArrayR of player names involved in the stat (goals, assists, etc.).
            stat (PlayerStats): The stat to update (goals, assists, interceptions, or tackles).

        Complexities: 
            Best Case Complexity: O(H+A+P) where H is the nuumber of players in the home team, A is the number od players in the away team and P is the number of people in player_list.
            returning None  has complexity O(1)
            Iterating through home_team has complexity O(P)
            Iterating throuhgh away_team has complexity O(H)
            Iterating through all the players has complexity O(P)
            the best case is when we dont need to run the inner for loop when searching for the player with matching name. 
            This happens under the circumstances that the firs playe in Player_list matches with the first name in all_players



            Worst Case Complexity: O((H+A)*P where H is the number of players in the home team, A is the number of players in the away team and P is th number of pople in the players lsit. 
            returning None  has complexity O(1)
            Iterating through home_team has complexity O(P)
            Iterating throuhgh away_team has complexity O(H)
            Iterating through all the players has complexity O(P)

            The worst case happens when player are found at the end of the all_players list making sure it traverse throughout. 


        """
        if player_list is None:
            return

       
        all_players = []
        
       
        for player in home_team.get_players():
            all_players.append(player)
        
        
        for player in away_team.get_players():
            all_players.append(player)

        
        for player_name in player_list:
            for player in all_players:
                if player.get_name() == player_name:
                    player[stat] += 1  
                    break      


    def update_player_stats(self,home_team: Team, away_team: Team, result: LinearProbeTable) -> None:
        """
        Update the player stats based on the game result.
        
        Args:
            home_team (Team): The home team object.
            away_team (Team): The away team object.
            result (LinearProbeTable): The result of the game simulation.

        Returns: 
            None

        Complexity: 
            Best Case: Uses complexity of update_individual_player_stats as iterating has compelexity O(N) where N is the number of player in player stast 
            Worst Case: Uses complexity of update_individual_player_stats as iterating has compelexity O(N) where N is the number of player in player stast 

        """

        for player in home_team.get_players():
            player[PlayerStats.GAMES_PLAYED] += 1
            
        for player in away_team.get_players():
            player[PlayerStats.GAMES_PLAYED] += 1
            
       
        self.update_individual_player_stats(home_team, away_team, result[ResultStats.GOAL_SCORERS.value], PlayerStats.GOALS)
        
        
        self.update_individual_player_stats(home_team, away_team, result[ResultStats.GOAL_ASSISTS.value], PlayerStats.ASSISTS)
        
        
        self.update_individual_player_stats(home_team, away_team, result[ResultStats.INTERCEPTIONS.value], PlayerStats.INTERCEPTIONS)
        
        
        self.update_individual_player_stats(home_team, away_team, result[ResultStats.TACKLES.value], PlayerStats.TACKLES)
    
        
    def update_leaderboard(self) -> None:
        """
        Updates the leaderboard by re-sorting the teams based on points,
        goal difference, and goals for. This should be called after simulating
        the season to reflect the final standings.

        Complexity: 
            Best Case Complexity: O(T) happens when all elements are sorted and element to be inserted can be inserted without shuffling
            Worst Case Complexity: O(T^2) happens when existing elemtst have to be shuffled to add a new element 
        """
       
        self.leaderboard.clear()

        for team in self.teams:
            self.leaderboard.add(team)

    def simulate_season(self) -> None:
        """
        Simulates the season.

        Complexity:
            Assume simulate_game is O(1)
            Remember to define your variables and their complexity.

            Best Case Complexity:O(W * T * P) where W is the number of weeks, T is the number teams and P is the number of players in the team. 
            Worst Case Complexity:O(W * T^2 + W * T * P) where W is the number of weeks, T is the number teams and P is the number of players in the team.
        """
        for week_num, week_of_games in enumerate(self.schedule, start=1):

            for game_num, game in enumerate(week_of_games, start=1):
                for game in week_of_games:
                    home_team = game.home_team
                    away_team = game.away_team
                    

                    result = GameSimulator.simulate(home_team, away_team)

                    home_goals = result[ResultStats.HOME_GOALS.value]
                    away_goals = result[ResultStats.AWAY_GOALS.value]

                    self.update_team_stats(home_team, away_team, result)

 
                    
  
                    self.update_player_stats(home_team, away_team, result)

                    if home_goals > away_goals:
 
                        home_team[TeamStats.WINS] += 1
                        away_team[TeamStats.LOSSES] += 1
                    elif home_goals < away_goals:

                        away_team[TeamStats.WINS] += 1
                        home_team[TeamStats.LOSSES] += 1
                    else:

                        home_team[TeamStats.DRAWS] += 1
                        away_team[TeamStats.DRAWS] += 1

  
            self.update_leaderboard()



    

    
    def delay_week_of_games(self, orig_week: int, new_week: Union[int, None] = None) -> None:
        """
        Delay a week of games from one week to another.

        Args:
            orig_week (int): The original week to move the games from.
            new_week (Union[int, None]): The new week to move the games to. If this is None, it moves the games to the end of the season.

        Complexity:
            Best Case Complexity: O(W) where W is the number of weeks. When moving games at the end of the schedule 
            
            Worst Case Complexity:O(W) where W is the number of weeks. wehn adding the game to any position in the  middle of the scehdule. 
        """

        orig_week-=1 
        if new_week is not None: 
            new_week-=1 

        orig_week_game = self.schedule.delete_at_index(orig_week)  


        
        if new_week is None: 
            
            self.schedule.append(orig_week_game)
        else: 
            if new_week>orig_week:
                self.schedule.insert(new_week,orig_week_game)
            else: 
                self.schedule.insert(new_week,orig_week_game)
        
    
    
      
    def get_next_game(self) -> Union[Generator[Game], None]:
        """
        Gets the next game in the season.

        Returns:
            Game: The next game in the season.
            or None if there are no more games left.

        Complexity:
            Best Case Complexity: O(1) when it is the first game when accessing the first week 
            Worst Case Complexity:O(W*G) where W is the number of weeks and G is the number of Games happens when you iterate trhough the entire 
        """


        for week in self.schedule:  
            for game in week:  
                yield game       

    def get_leaderboard(self) -> ArrayR[ArrayR[Union[int, str]]]:
        """
        Generates the final season leaderboard.

        Returns:
            ArrayR(ArrayR[ArrayR[Union[int, str]]]):
                Outer array represents each team in the leaderboard
                Inner array consists of 10 elements:
                    - Team name (str)
                    - Games Played (int)
                    - Points (int)
                    - Wins (int)
                    - Draws (int)
                    - Losses (int)
                    - Goals For (int)
                    - Goals Against (int)
                    - Goal Difference (int)
                    - Previous Five Results (ArrayR(str)) where result should be WIN LOSS OR DRAW

        Complexity:
            Best Case Complexity: O(T ) where T is the number of teams.  
            Worst Case Complexity:O(T) where T is the number of teams. 
        """
        print("Generating leaderboard...")
        leaderboard_array = ArrayR(len(self.leaderboard))
        
        for i, team in enumerate(self.leaderboard):
            team_name = team.get_name()
            games_played = team[TeamStats.GAMES_PLAYED]
            points = team[TeamStats.POINTS]
            wins = team[TeamStats.WINS]
            draws = team[TeamStats.DRAWS]
            losses = team[TeamStats.LOSSES]
            goals_for = team[TeamStats.GOALS_FOR]
            goals_against = team[TeamStats.GOALS_AGAINST]
            goal_difference = goals_for - goals_against

 
            last_five_results = team.get_last_five_results()
            if last_five_results is not None:
                last_five_results_str = ArrayR.from_list([res for res in last_five_results])
            else:
                last_five_results_str = ArrayR() 
            
 
            
            leaderboard_array[i] = ArrayR.from_list([team_name, games_played, points, wins, draws, losses,
                                                    goals_for, goals_against, goal_difference,
                                                    last_five_results_str])

        return leaderboard_array
        

    def get_teams(self) -> ArrayR[Team]:
        """
        Returns:
            PlayerPosition (ArrayR(Team)): The teams participating in the season.

        Complexity:
            Best Case Complexity: O(1) returning has a constant time complexity. 
            Worst Case Complexity: O(1) returning has a constatn time complexity. 
        """
        return self.teams
       

    def __len__(self) -> int:
        """
        Returns the number of teams in the season.

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        return len(self.teams)
        #raise NotImplementedError

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the season object.

        Complexity:
            Analysis not required.
        """
        return ""

    def __repr__(self) -> str:
        """Returns a string representation of the Season object.
        Useful for debugging or when the Season is held in another data structure."""
        return str(self)
