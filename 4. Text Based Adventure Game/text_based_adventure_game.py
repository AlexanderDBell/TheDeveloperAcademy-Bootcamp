from typing_extensions import Literal
import textwrap

def main() -> None:
    entrance = Room(
        'entrance',
        (0, 0),
        ('You find yourself outside the house. It looks abandoned but as you '
         'approach the door you hear whispers coming from inside.')
    )
    living_room = Room(
        'living room',
        (0, 1),
        ('The living room is unassuming. A TV, a sofa and a couple of '
         'armchairs. You think about the happy times the family must have spent '
         'together. You hear a faint sound: laughter. Or is it crying? In front '
         'of you is the dining room. Behind you is the entrance to the house.')
    )
    dining_room = Room(
        'dining room',
        (0, 2),
        ("A table and chairs. You don't know what you were expecting. You take "
         "a closer look and see that the head of the table is covered in stab "
         'marks. In front of you is the kitchen. Behind you is the living room. '
         'On your left is a hallway.')
    )
    kitchen = Room(
        'kitchen',
        (0, 3),
        ('The kitchen is small and cramped. A gas stove, a tiny oven, a sink '
         'and a small worksurface. You feel something crunch under your feet. '
         'You look down to see the remains of what appear to be smashed plates '
         'and glasses. Behind you is the dining room.')
    )
    hallway = Room(
        'hallway',
        (-1, 2),
        ('A picture of a happy family hangs on the wall. The frame has been '
         'shattered. In front of you is the master bedroom. Behind you is a '
         "child's bedroom. On your left is the bathroom. On your right is "
         'the living room.')
    )
    master_bedroom = Room(
        'master bedroom',
        (-1, 3),
        ('The king bed lies in the middle of the room backed up against the '
         'wall. The headboard and wall are peppered with shotgun pellets. Every '
         'so often you faintly hear a deep sob. Behind you is the hallway.')
    )
    child_bedroom = Room(
        "child's bedroom",
        (-1, 1),
        ('A wooden rocking horse in the centre of the room slowly comes to a '
         'standstill. There is no bedframe, only a mattress stained with '
         'urine. You take a closer look at the horse and find tiny shards of '
         'bone on its head. In front of you is the hallway.')
    )
    bathroom = Room(
        'bathroom',
        (-2, 2),
        ('The smell of vomit lingers in the air. In the sink are several '
         'packets of paracetamol, all empty. From the corner of your eye you '
         'glimpse a figure curled up in the bathtub, but when you look at it '
         'directly it vanishes. On your right is the hallway.')
    )
    rooms = {
        entrance,
        living_room,
        dining_room,
        kitchen,
        hallway,
        master_bedroom,
        child_bedroom,
        bathroom
    }

    map = Map(rooms)
    map.connect_rooms(entrance, {living_room})
    map.connect_rooms(living_room, {dining_room, entrance})
    map.connect_rooms(dining_room, {kitchen, living_room, hallway})
    map.connect_rooms(kitchen, {dining_room})
    map.connect_rooms(hallway, {master_bedroom, child_bedroom, bathroom, dining_room})
    map.connect_rooms(master_bedroom, {hallway})
    map.connect_rooms(child_bedroom, {hallway})
    map.connect_rooms(bathroom, {hallway})

    player = Player(entrance.coordinates, map)
    print('Welcome to the game, enter help for available commands.')
    player.print_current_room()

    while True:
        user_input = InputHandler()
        output = user_input.output()
        
        match output:
            case 'quit':
                break
            case 'help':
                message = ('help: display list of commands\n'
                           'look around: look around the room you are in\n'
                           'move (forward, back, left, right): move in the '
                           'specified direction\n'
                           'quit: quit the game')
                print(message)
            case 'look':
                current_room = map.grid[player.coordinates]
                text = current_room.description
                print(textwrap.fill(text))
            case 'forward':
                player.move('forward')
            case 'back':
                player.move('back')
            case 'left':
                player.move('left')
            case 'right':
                player.move('right')
            case 'error':
                print('Invalid command.')

class Room:
    '''
    A class used to represent a Room

    ...

    Attributes
    ----------
    name : str
        the name of the room
    coordinates : tuple[int, int]
        the coordinates of the room on the map
    description : str
        the description of the room
    '''

    def __init__(
            self,
            name: str,
            coordinates: tuple[int, int],
            description: str
    ) -> None:
        self.name = name
        self.coordinates = coordinates
        self.description = description

class Map:
    '''
    A class used to represent a Map

    ...

    Attributes
    ----------
    rooms : set[Room]
        the rooms on the map
    grid : dict[tuple[int, int], Room]
        the layout of the map that stores what is at each coordinate
    connections : dict[Room, set[Room]]
        the connections between rooms
    
    Methods
    -------
    connect_rooms(origin_room, connections)
        Connects the origin room to rooms in connections set
    '''

    def __init__(self, rooms: set[Room]) -> None:
        self.rooms = rooms
        self.grid = self._create_grid()
        self.connections: dict[Room, set[Room]] = {}

    def connect_rooms(self, origin_room: Room, connections: set[Room]) -> None:
        rooms_valid = connections.union({origin_room}).issubset(self.rooms)
        if rooms_valid:
            for room in connections:
                self._adjacent(origin_room, room)
            self.connections[origin_room] = connections
        else:
            raise Exception('one or more rooms not present in map')
    
    def _create_grid(self) -> dict[tuple[int, int], Room]:
        coordinates = [room.coordinates for room in self.rooms]
        if len(coordinates) != len(set(coordinates)):
            raise Exception('rooms share coordinates')
        return {room.coordinates: room for room in self.rooms}
        
    def _adjacent(self, origin: Room, destination: Room) -> Literal[True]:
        manhattan_distance = (
            abs(origin.coordinates[0] - destination.coordinates[0])
            + abs(origin.coordinates[1] - destination.coordinates[1])
        )
        if manhattan_distance == 1:
            return True
        raise Exception('rooms not adjacent')

class Player:
    '''
    A class used to represent a Player

    ...

    Attributes
    ----------
    coordinates : tuple[int, int]
        coordinate location of the player on the map
    map : Map
        the map the player is on
    
    Methods
    -------
    move(direction)
        Moves the player in the specified direction
    print_current_room()
        Tells the player what room they are in
    '''

    def __init__(self, coordinates: tuple[int, int], map: Map) -> None:
        self.coordinates = coordinates
        self.map = map
    
    def move(self, direction: Literal['forward', 'back', 'left', 'right']) -> None:
        match direction:
            case 'forward':
                test_coordinates = (self.coordinates[0], self.coordinates[1] + 1)
            case 'back':
                test_coordinates = (self.coordinates[0], self.coordinates[1] - 1)
            case 'left':
                test_coordinates = (self.coordinates[0] - 1, self.coordinates[1])
            case 'right':
                test_coordinates = (self.coordinates[0] + 1, self.coordinates[1])
        self._test_move(test_coordinates)
    
    def print_current_room(self) -> None:
        current_room = self.map.grid[self.coordinates]
        print(f'You are in the {current_room.name}.')
    
    def _test_move(self, test_coordinates: tuple[int, int]) -> None:
        if self._valid_move(test_coordinates):
            self.coordinates = test_coordinates
            self.print_current_room()
        else:
            print("You can't go there.")

    def _valid_move(self, test_coordinates: tuple[int, int]) -> bool:
        current_room = self.map.grid[self.coordinates]
        try:
            test_room = self.map.grid[test_coordinates]
        except KeyError:
            return False
        if test_room in self.map.connections[current_room]:
            return True
        return False
    
class InputHandler:
    '''
    A class used to represent an Input Handler

    ...

    Attributes
    ----------
    user_input : str
        lowercase input from user
    
    Methods
    -------
    output()
        converts user input to literals
    '''

    def __init__(self) -> None:
        self.user_input = input('What would you like to do? ').lower()
    
    def output(self) -> Literal[
        'quit', 'help', 'look', 'forward', 'back', 'left', 'right', 'error'
    ]:
        match self.user_input:
            case 'quit':
                return 'quit'
            case 'help':
                return 'help'
            case 'look around':
                return 'look'
            case 'move forward':
                return 'forward'
            case 'move back':
                return 'back'
            case 'move left':
                return 'left'
            case 'move right':
                return 'right'
            case _:
                return 'error'

if __name__ == '__main__':
    main()