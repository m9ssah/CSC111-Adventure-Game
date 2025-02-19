"""CSC111 Project 1: Text Adventure Game - Event Logger

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

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
from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    """
    A node representing one event in an adventure game.

    Instance Attributes:
    - id_num: Integer id of this event's location
    - description: Long description of this event's location
    - next_command: String command which leads this event to the next event, None if this is the last game event
    - next: Event object representing the next event in the game, or None if this is the last game event
    - prev: Event object representing the previous event in the game, None if this is the first game event
    """

    id_num: int
    description: str
    next_command: Optional[str] = None
    next: Optional[Event] = None
    prev: Optional[Event] = None


class EventList:
    """
    A linked list of game events.

    Instance Attributes:
        - first: Event object representing the first event in the game, None if the game hasn't started
        - last: Event object representing the last event in the game, None if the game hasn't started

    Representation Invariants:
        - if the list is not empty, then first and last should not be "None"
        - if first is not none, then last should not be none
        - if the list is empty, then both first and last should be none

    """
    first: Optional[Event]
    last: Optional[Event]

    def __init__(self) -> None:
        """
        Initialize a new empty event list.
        """

        self.first = None
        self.last = None

    def display_events(self) -> None:
        """
        Display all events in chronological order.
        """
        if self.first is None:
            print("No events to display.")
        else:
            curr = self.first
            while curr is not None:
                print(f"Location: {curr.id_num}, Action Preformed: {curr.description}")
                curr = curr.next

    def is_empty(self) -> bool:
        """
        Return whether this event list is empty.
        """
        return self.first is None

    def add_event(self, event: Event, command: str = None) -> None:
        """
        Add the given new event to the end of this event list.
        The given command is the command which was used to reach this new event, or None if this is the first
        event in the game.
        """
        if self.first is None:
            self.first = event
            self.last = event

        else:
            self.last.next_command = command
            self.last.next, event.prev = event, self.last
            self.last = event

    def remove_last_event(self) -> Optional[None]:  # updated this method to return the event removed
        """
        Remove the last event from this event list.
        If the list is empty, do nothing.
        """
        if self.is_empty():
            return None

        elif self.first == self.last:
            last_event = self.first
            self.first = None
            self.last = None
            return last_event

        else:
            last_event = self.last
            self.last.prev.next_command = None
            self.last.prev.next = None
            self.last = self.last.prev
            return last_event

    def get_id_log(self) -> list[int]:
        """
        Return a list of all location IDs visited for each event in this list, in sequence.
        """

        locations = []
        curr = self.first
        while curr is not None:
            locations.append(curr.id_num)
            curr = curr.next
        return locations


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
