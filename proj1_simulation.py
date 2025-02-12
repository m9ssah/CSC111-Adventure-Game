"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

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
from proj1_event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)

        initial_location = self._game.get_location()
        first_event = Event(
            initial_location.id_num,
            initial_location.long_description
        )
        self._events.add_event(first_event)
        self.generate_events(commands, initial_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        for command in commands:
            if command in current_location.available_commands:
                next_location_id = current_location.available_commands[command]
                next_location = self._game.get_location(next_location_id)
                if next_location_id in self.get_id_log():
                    description = next_location.brief_description
                else:
                    description = next_location.long_description
                event = Event(
                    next_location.id_num,
                    description
                )
                self._events.add_event(event, command)
                current_location = next_location

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east"])
        >>> sim.get_id_log()
        [1, 2]

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east", "go east", "buy coffee"])
        >>> sim.get_id_log()
        [1, 2, 3, 3]
        """
        return self._events.get_id_log()

    def run(self) -> None:
        """
        Run the game simulation and log location descriptions.
        """
        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You chose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    win_walkthrough = [
        'go east',
        'go east',
        'go west',
        'pick up usb drive',
        'go south',
        'go south',
        'go south',
        'go north east',
        'go west',
        'go west',
        1,
        1,
        1,
        'I LOVE CSC111',
        'pick up lucky mug'
        'go south',
        'go south',
        'go south',
        'go north',
        'go north',
        'go east',
        'go north',
        'pick up dorm keys',
        'go south',
        'go south',
        'go south',
        'go south',
        'go south east',
        'go west',
        'go east',
        'pick up laptop charger',
        'go south',
        'go south',
        'go south',
        'go west',
        'go north',
        'go north',
        'go west',
        'deposit usb drive',
        'deposit laptop charger',
        'deposit lucky mug'

    ]  # Create a list of all the commands needed to walk through your game to win it
    expected_log = [1, 2, 3, 4, 3, 2, 1, 10, 12, 14, 12, 10, 11, 10, 1, 50, 1, 60, 61, 62, 61, 60, 1, 30, 32, 33, 34]
    assert expected_log == AdventureGameSimulation('game_data.json', 1, win_walkthrough).get_id_log()

    # Create a list of all the commands needed to walk through your game to reach a 'game over' state
    lose_demo = [
        'pick up toonie',
        'go east',
        'go east',
        'go west',
        'pick up usb drive',
        'go south',
        'go south',
        'drop usb drive',
        'go south',
        'go west',
        'go north',
        'go north',
        'go east',
        'pick up pokemon card',
        'go south',
        'go south',
        'go south',
        'go south',
        'go south west',
        'drop toonie',
        'go north',
        'go south',
        'go south',
        'go south',
        'go north east',
        'go south',
        'go south',
        'go north east',
        'go west',
        'go west',
        3,
        2,
        2,
        1,
        "Random",
        'go south',
        'drop pokemon cord',
        'go south',
        'go south',
        'go north',
        'go north',
        'go east',
        'go north',
        'pick up dorm keys',
        'go south',
        'go south',
        'go south',
        'go south',
        'go west',
        'go north',
        'go north',
        'go west',
        'deposit dorm keys',
        'go south'
    ]
    
    expected_log = [1, 2, 3, 4, 3, 2, 1, 30, 32, 33, 35, 35, 33, 32, 30, 1, 40, 41, 40, 1, 50, 53, 50, 1, 10, 12, 14, 12, 10, 1, 20, 24, 25, 26, 25, 24, 20, 1, 30, 32, 33, 34, 33]
    assert expected_log == AdventureGameSimulation('game_data.json', 1, lose_demo).get_id_log()

    inventory_demo = [
        "go east",        # Move to Gerstein 1F
        "go east",        # Move to Gerstein -1F
        "go west",        # Enter MADLab
        "pick up usb drive",  # Pick up USB Drive
        "inventory"
        ]    # Check inventory
    expected_log = [1, 2, 3, 4]
    assert expected_log == AdventureGameSimulation('game_data.json', 1, inventory_demo).get_id_log()

    scores_demo = [
        'pick up toonie',
        'go north',
        'go north',
        'go east',
        'go north',
        'pick up dorm keys',
        'go south',
        'go south',
        'go south',
        'go south',
        'go west',
        'go north',
        'go north',
        'go west',
        'deposit toonie',
        'score'
    ]
    expected_log = [1, 20, 24, 25, 26, 25, 24, 20, 1, 30, 32, 33, 34]
    assert expected_log == AdventureGameSimulation('game_data.json', 1, scores_demo).get_id_log()

    # enhancement_demo = ['

    # Add more enhancement_demos if you have more enhancements
    # enhancement1_demo = [...]
    # expected_log = []
    # assert expected_log == AdventureGameSimulation(...)
