from typing_extensions import Literal

def main() -> None:
    front_garden = Room('front garden', (0, 0), 'placeholder')
    living_room = Room('living room', (0, 1), 'placeholder')
    dining_room = Room('dining room', (0, 2), 'placeholder')
    kitchen = Room('kitchen', (0, 3), 'placeholder')
    hallway = Room('corridor', (-1, 2), 'placeholder')
    master_bedroom = Room('master bedroom', (-1, 3), 'placeholder')
    child_bedroom = Room("children's bedroom", (-1, 1), 'placeholder')
    bathroom = Room('bathroom', (-2, 2), 'placeholder')
    rooms = {
        front_garden,
        living_room,
        dining_room,
        kitchen,
        hallway,
        master_bedroom,
        child_bedroom,
        bathroom
    }
    map = Map(rooms)
    map.connect_rooms(front_garden, {living_room})
    map.connect_rooms(living_room, {dining_room, front_garden})
    map.connect_rooms(dining_room, {kitchen, living_room, hallway})
    map.connect_rooms(kitchen, {dining_room})
    map.connect_rooms(hallway, {master_bedroom, child_bedroom, bathroom, dining_room})
    map.connect_rooms(master_bedroom, {hallway})
    map.connect_rooms(child_bedroom, {hallway})
    map.connect_rooms(bathroom, {hallway})
    player = Player(front_garden.coordinates, map)
    while True:
        current_room = map.grid[player.coordinates]
        print(f'You are in the {current_room.name}')
        user_input = InputHandler()
        output = user_input.output()
        match output:
            case 'quit':
                break
            case 'help':
                message = '''quit: quit the game
look around: look around the room you are in
move (forward, back, left, right): move in the specified direction'''
                print(message)
            case 'look':
                current_room = map.grid[player.coordinates]
                print(current_room.description)
            case 'forward':
                player.move('forward')
            case 'back':
                player.move('back')
            case 'left':
                player.move('left')
            case 'right':
                player.move('right')
            case 'error':
                print('Invalid')

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
        self.connections = {}

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
        moves the player in the specified direction
    '''

    def __init__(self, coordinates: tuple[int, int], map: Map) -> None:
        self.coordinates = coordinates
        self.map = map
    
    def move(self, direction: Literal['forward', 'back', 'left', 'right']) -> None:
        match direction:
            case 'forward':
                test_coordinates = (self.coordinates[0], self.coordinates[1] + 1)
                self._test_move(test_coordinates)
            case 'back':
                test_coordinates = (self.coordinates[0], self.coordinates[1] - 1)
                self._test_move(test_coordinates)
            case 'left':
                test_coordinates = (self.coordinates[0] - 1, self.coordinates[1])
                self._test_move(test_coordinates)
            case 'right':
                test_coordinates = (self.coordinates[0] + 1, self.coordinates[1])
                self._test_move(test_coordinates)
    
    def _test_move(self, test_coordinates: tuple[int, int]) -> None:
        if self._valid_move(test_coordinates):
            self.coordinates = test_coordinates
        else:
            print('Invalid')

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