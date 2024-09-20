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
        Best Case Complexity:
        Worst Case Complexity:
        """
        self.i=0
        return self
        #raise NotImplementedError

    def __next__(self):
        """
        Complexity:
        Best Case Complexity:
        Worst Case Complexity:
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
            Best Case Complexity:
            Worst Case Complexity:
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
        """
        if player_list is None:
            return

        # Get all players from home and away teams as a list
        all_players = []
        
        # Add players from the home team
        for player in home_team.get_players():
            all_players.append(player)
        
        # Add players from the away team
        for player in away_team.get_players():
            all_players.append(player)

        # Update the stats for players mentioned in player_list
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
        """

        for player in home_team.get_players():
            player[PlayerStats.GAMES_PLAYED] += 1
            
        for player in away_team.get_players():
            player[PlayerStats.GAMES_PLAYED] += 1
            
        # Update goal scorers
        self.update_individual_player_stats(home_team, away_team, result[ResultStats.GOAL_SCORERS.value], PlayerStats.GOALS)
        
        # Update goal assists
        self.update_individual_player_stats(home_team, away_team, result[ResultStats.GOAL_ASSISTS.value], PlayerStats.ASSISTS)
        
        # Update interceptions
        self.update_individual_player_stats(home_team, away_team, result[ResultStats.INTERCEPTIONS.value], PlayerStats.INTERCEPTIONS)
        
        # Update tackles
        self.update_individual_player_stats(home_team, away_team, result[ResultStats.TACKLES.value], PlayerStats.TACKLES)
    
        
    def update_leaderboard(self) -> None:
        """
        Updates the leaderboard by re-sorting the teams based on points,
        goal difference, and goals for. This should be called after simulating
        the season to reflect the final standings.
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

            Best Case Complexity:
            Worst Case Complexity:
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
            Best Case Complexity:
            Worst Case Complexity:
        """
        '''
        if orig_week!=len(self.schedule)+1:
            original=self.schedule.delete_at_index(orig_week-1)
            if new_week is None:
                self.schedule.append(original)
            else:
                self.schedule.insert(new_week-1,original)
        '''        
        
        '''
        orig_week -= 1 
        original = self.schedule[orig_week]
        n = len(self.schedule)
        if new_week is None: 
            for week in range(orig_week, n-1):
                self.schedule[week] = self.schedule[week+1]
            self.schedule[n-1] = original 
        else:
            new_week -= 1
            for week in range(orig_week, new_week, -1):
                self.schedule[week] = self.schedule[week-1]
            self.schedule[new_week] = original
            for week in range(new_week+1, orig_week+1):
                self.schedule[week] = self.schedule[week-1]
            #raise NotImplementedError
        '''

        
        orig_week-=1 # handling for 0 indexing 
        if new_week is not None: # swapping case
            new_week-=1 # handling for 0 indexing 
        # removing the orig_week_game 
        orig_week_game = self.schedule.delete_at_index(orig_week)  

        # handling the tail case (end of season case)
        
        if new_week is None: 
            # adding it to the end 
            self.schedule.append(orig_week_game)
        else: 
            if new_week>orig_week:
                self.schedule.insert(new_week,orig_week_game)
            else: 
                self.schedule.insert(new_week,orig_week_game)
        
    
        
        '''

        original=self.schedule.delete_at_index(orig_week-1)
        if new_week is None: 
            self.schedule.append(original)
        else: 
            self.schedule.insert(new_week-1,original)
        '''
      
    def get_next_game(self) -> Union[Generator[Game], None]:
        """
        Gets the next game in the season.

        Returns:
            Game: The next game in the season.
            or None if there are no more games left.

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """

       # for week in self.schedule:
    
            #yield week.get_games()[0]

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
            Best Case Complexity:
            Worst Case Complexity:
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
            Best Case Complexity:
            Worst Case Complexity:
        """
        return self.teams
        #raise NotImplementedError

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
