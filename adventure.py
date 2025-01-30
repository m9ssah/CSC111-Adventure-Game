"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item, Player
from proj1_event_logger import Event, EventList



class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: the id of the current location
        - ongoing: status of game

    Representation Invariants:
        - current_location_id is not None
        - TODO
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self.player = Player() #game player
        self.game_log = EventList()  # This is REQUIRED as one of the baseline requirements

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """
        Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects.
        """

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []
        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['description'], item_data['start_position'], item_data['target_position'],
                            item_data['target_points'])
            items += item_obj

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """
        Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """
        if loc_id is None or loc_id not in self._locations:
            return self._locations[self.current_location_id]
        return self._locations[loc_id]

def handle_undo(game: AdventureGame) -> None:
    """
    Handle the undo the command

    Parameters
    ----------
    game : AdventureGame
    """
    last_event = game.game_log.remove_last_event()
    if last_event:
        game.current_location_id = last_event.id_num
        print(f"Undid most recent event")
        print(f"You returned to: {game.get_location().brief_description}")

def go(game: AdventureGame, direction: str) -> None:
    """
    Handle the go command according to a given direction.

    Parameters
    ----------
    game : AdventureGame
    direction : str
    """
    location = game.get_location()
    if direction in location.available_commands:
        new_location_id = location.available_commands[direction]
        game.current_location_id = new_location_id
        new_location = game.get_location(new_location_id)
        print(f"You moved to: {new_location.brief_description}")
        # Log the event
        event = Event(new_location_id, new_location.long_description, f"go {direction}")
        game.game_log.add_event(event, f"go {direction}")
    else:
        print(f"Unable to move towards the {direction}")



if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })


    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    choice = None

    while game.ongoing:

        location = game.get_location()
        game_log = EventList()

        # TODO: Add new Event to game log to represent current game location
        #  Note that the <choice> variable should be the command which led to this event
        # YOUR CODE HERE


        if not location.visited:
            new_event = Event(
                id_num = location.id_num,
                description = location.long_description,
                next_command = choice
            )
            location.visited = True
            print(location.long_description)

        else:
            event = Event(
            id_num = location.id_num,
            description = location.brief_description,
            next_command = choice
        )
            print(location.brief_description)
        
        game.game_log.add_event(event, choice)


        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            # TODO: Handle each menu command as appropriate
            # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
            if choice == "log":
                game_log.display_events()
            elif choice == "inventory":
                game.player.inventory()
            elif choice == "undo":
                handle_undo(game)
            elif choice == "look":
                location.look()
            elif choice == "quit":
                print("Quiting game...")
                game.ongoing = False


        else:
            # Handle non-menu actions
            result = location.available_commands[choice]
            game.current_location_id = result

            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game
