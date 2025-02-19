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
from typing import Optional, Any
import time
import pygame
import threading
from game_entities import Location, Item, Player
from proj1_event_logger import Event, EventList


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: the id of the current location
        - ongoing: status of game

    Representation Invariants:
        - current_location_id is not None
        - ongoing is a boolean
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int
    ongoing: bool
    player: Player
    game_log: EventList

    def __init__(self, game_data_file: str, initial_location: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """
        self._locations, self._items = self._load_game_data(game_data_file)
        self.current_location_id = initial_location  # game begins at king's college circle
        self.ongoing = True  # whether the game is ongoing
        self.player = Player()  # game player
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
        item_dict = {}
        items = []
        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['description'], 
                            item_data['start_position'], item_data['target_position'],
                            item_data['target_points'])
            items.append(item_obj)
            item_dict[item_data["name"].lower()] = item_obj

        for loc_data in data['locations']:
            item_objects = [item_dict[item_name.lower()] for item_name in loc_data['items'] if item_name.lower() in item_dict]

            dialogue = loc_data.get('dialogue', None)

            location_obj = Location(loc_data['id'], loc_data["name"], loc_data['brief_description'],
                                    loc_data['long_description'], loc_data['available_commands'], 
                                    item_objects, dialogue=dialogue, music=loc_data.get('music', None))
            locations[loc_data['id']] = location_obj

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """
        Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """
        if loc_id is None or loc_id not in self._locations:
            return self._locations[self.current_location_id]
        return self._locations[loc_id]

    def get_item(self, target_item: str) -> Any:
        """
        Return Item object associated with the provided item name.
        If item not found, return None.
        """
        return next((item for item in game._items if item.name.lower() == target_item.lower()), None)


def handle_undo(game: AdventureGame) -> None:
    """
    Handle undoing the last command. If the last command is None, reset the game.
    """
    last_event = game.game_log.last

    if last_event is game.game_log.first:  # In case the player undoes an action that doesnt even exist
        print("No valid actions to undo.")
        return
    
    # Process undo logic for item-based actions
    command_parts = last_event.description.split()
    action = command_parts[0]
    item_name = " ".join(command_parts[1:]) if len(command_parts) > 1 else ""

    last_event = game.game_log.remove_last_event()
    game.current_location_id = last_event.prev.id_num
    
    location = game.get_location()

    if action not in ("pick", "drop", "deposit"):
        return
    else:
        item = game.get_item(item_name)
        if item:
            if action == "pick":
                game.player.remove_item(item)
                location.items.append(item)
                print(f"Returned {item_name} to {location.name}")

            elif action == "drop":
                game.player.add_item(item)
                location.items.remove(item)
                print(f"Picked up {item_name} again")

            elif action == "deposit":
                game.player.add_item(item)
                game.player.score -= item.target_points
                print(f"Returned {item_name} to your inventory and deducted {item.target_points} points.")

    print(f"Undid most recent event. You returned to: {location.name}.")


def go(game: AdventureGame, direction: str) -> None:
    """
    Handle the go command according to a given direction.
    """
    location = game.get_location()
    if f"go {direction}" in location.available_commands:
        new_location_id = location.available_commands[f"go {direction}"]
        if new_location_id == dorm_room_id and not \
            any(item.name.lower() == "dorm keys" for item in game.player.inventory):
            print("Your dorm room seems to be locked and you don't have your keys with you.")
            print("You must first look for your keys then you may enter.")
            return
        previous_location_id = game.current_location_id  # Store current location before moving
        game.current_location_id = new_location_id
        new_location = game.get_location(new_location_id)
        print(f"You are now in: {new_location.name}!")

        # Log event: Store where we came from!
        event = Event(
            id_num=new_location_id, 
            description=f"go {direction}", 
            prev=game.game_log.last
        )
        event.previous_location = previous_location_id  # Store the previous location!
        game.game_log.add_event(event, f"go {direction}")

    else:
        print(f"Unable to move towards the {direction}")


def handle_score(player: Player) -> None:
    """
    Handles the score method of the player class to display the current score.
    """
    print(f"Your current score is: {player.score}")


def pick_up_item(game: AdventureGame, given_item_name: str) -> None:
    """
    Allows the user to pick up a specific item if it is present in the current location.
    """
    location = game.get_location()

    # Find the item by name
    item_to_pick_up = game.get_item(given_item_name)

    if item_to_pick_up is not None:
        game.player.add_item(item_to_pick_up)
        location.items.remove(item_to_pick_up)  # Ensure item is removed from location
        print(f"You have successfully picked up: {item_to_pick_up.name}!")
        # remove item from the location after picking it up:
        # Log the event
        event = Event(
            id_num=game.current_location_id, 
            description=f"pick {item_to_pick_up.name}", 
            prev=game_log.last
        )
        game.game_log.add_event(event, f"pick {item_to_pick_up.name}")
    else:
        print(f"Cannot find '{given_item_name}'. Check spelling and try again.")


def drop_item(game: AdventureGame, given_item_name: str) -> None:
    """
    Allows the user to drop a specific item if it is present in their inventory
    """
    # Find the item by name (case-insensitive)
    item_to_drop = game.get_item(given_item_name)  #next((item for item in game.player.inventory if item.name.lower() == given_item_name.lower()), None)

    if item_to_drop is not None:
        game.player.inventory.remove(item_to_drop)
        game.get_location().items.append(item_to_drop)  # Add item back to the location
        print(f"You have successfully dropped: {item_to_drop.name}!")
        # log the event
        event = Event(
            id_num=game.current_location_id, 
            description=f"drop {item_to_drop.name}",  
            prev=game_log.last
        )
        game.game_log.add_event(event, f"drop {item_to_drop.name}")
    else:
        print("You don't have an item by that name to drop.")


def deposit(game: AdventureGame, given_item_name: str) -> None:
    """
    Allows the user to deposit the items they have collected all over campus to claim their points
    The designated deposit room is the user's dorm (loc_id = 34)
    """
    location = game.get_location()
    if location.id_num != 34:
        print("Unable to deposit items in current location, you must deposit everything in your\
               dorm (HINT: it's in Knox College)")
        return

    item_to_deposit = game.get_item(given_item_name)  # next((item for item in game.player.inventory if item.name.lower() == given_item_name.lower()), None)

    if item_to_deposit is not None:
        game.player.score += item_to_deposit.target_points
        game.player.inventory.remove(item_to_deposit)
        print(f"You have successfully deposited {item_to_deposit.name} and received {item_to_deposit.target_points}")
        deposited_items.add(str(item_to_deposit.name))
        # log event
        event = Event(
            game.current_location_id,
            f"deposit {item_to_deposit.name}",
            None,
            None,
            game.game_log.last
        )
        game.game_log.add_event(event, f"deposit {item_to_deposit.name}")
    else:
        print("You have no items to deposit.")


def display_location_options(game: AdventureGame) -> None:
    """Display available actions at the current location."""
    location = game.get_location()
    print("What to do? Choose from: look, inventory, score, undo, log, quit")
    print("At this location, you can also:")

    for action in location.available_commands:
        print("-", action)

    for item in location.items:
        if item.name.lower() == "lucky mug" and not location.conversation_success:
            continue  # Skip "pick up lucky mug" if the conversation failed
        print(item.description)
        print(f"- pick up {item.name}")

    if game.player.inventory:
        for item in game.player.inventory:
            print(f"- drop {item.name}")

    if location.id_num == dorm_room_id:
        for item in game.player.inventory:
            print(f"- deposit {item.name}")


def play_music(game: AdventureGame) -> None:
    """
    Plays background music based on the player's current location.
    """
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1)  # Set volume

    current_music = None  # Track currently playing music
    previous_location = None  # Track last known location

    while game.ongoing:
        if game.current_location_id != previous_location:
            previous_location = game.current_location_id
            location = game.get_location()

            if location.music:
                if location.music != current_music:  # Only change if needed
                    pygame.mixer.music.load(location.music)
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                    current_music = location.music
            else:
                pygame.mixer.music.stop()  # Stop if no music is assigned

        time.sleep(0.1)  # Check location every second


if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    game.game_log = game_log  # initializing game_log 
    music_thread = threading.Thread(target=play_music, args=(game,), daemon=True)
    music_thread.start()
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    choice = None
    first_event = Event(
        id_num = 1,
        description="game start"
    )
    game_log.add_event(first_event)
    deposited_items = set()
    dorm_room_id = 34

    while game.ongoing:
        location = game.get_location()
        if not location.visited:
            event = Event(
                id_num=location.id_num,
                description=location.long_description,
                next_command=choice
                )
            location.visited = True
            print(location.long_description)
            location.start_dialogue(game)
        else:
            event = Event(
                id_num=location.id_num,
                description=location.brief_description,
                next_command=choice
                )
            print(location.brief_description)

        display_location_options(game)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)
        if choice in menu:
            if choice == "log":
                game_log.display_events()
            elif choice == "inventory":
                game.player.display_inventory()
            elif choice == "undo":
                handle_undo(game)
            elif choice == "look":
                location.look()
            elif choice == "score":
                handle_score(game.player)
            elif choice == "quit":
                print("Quiting game...")
                game.ongoing = False
                
        else:  # Handle non-menu actions
            if choice.startswith("go"):
                direction = choice[3:].strip()  # Extract the direction
                go(game, direction)  # move to location
            elif choice.startswith("pick up"):
                given_item = choice[8:].strip()
                pick_up_item(game, given_item)
            elif choice.startswith("drop"):
                given_item = choice[5:].strip()
                drop_item(game, given_item)
            elif choice.startswith("deposit"):
                given_item = choice[8:].strip()
                deposit(game, given_item)
            else:
                print("Invalid input. Try again.")
                choice = input("\nEnter action: ").lower().strip()

        if len(game.game_log.get_id_log()) >= 50:
            print("You have exceeded the amount of steps you can perform.")
            print("Game Over")
            game.ongoing = False

        if {"usb drive", "laptop charger", "lucky mug"} in deposited_items:
            print("You have successfully found all the items you lost!")
            print("Congratulations, the game has ended...")
            game.ongoing = False
