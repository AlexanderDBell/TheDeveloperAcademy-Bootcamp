from typing_extensions import Literal

def main():
    outside = Room('outside', (0, 0), 'placeholder')
    living_room = Room('living room', (0, 1), 'placeholder')
    dining_room = Room('dining room', (0, 2), 'placeholder')
    kitchen = Room('kitchen', (0, 3), 'placeholder')
    hallway = Room('corridor', (-1, 2), 'placeholder')
    master_bedroom = Room('master bedroom', (-1, 3), 'placeholder')
    child_bedroom = Room("children's bedroom", (-1, 1), 'placeholder')
    bathroom = Room('bathroom', (-2, 2), 'placeholder')
    rooms = {
        outside,
        living_room,
        dining_room,
        kitchen,
        hallway,
        master_bedroom,
        child_bedroom,
        bathroom
    }
    map = Map(rooms)
    map.connect_rooms(outside, {living_room})
    map.connect_rooms(living_room, {dining_room, outside})
    map.connect_rooms(dining_room, {kitchen, living_room, hallway})
    map.connect_rooms(kitchen, {dining_room})
    map.connect_rooms(hallway, {master_bedroom, child_bedroom, bathroom, dining_room})
    map.connect_rooms(master_bedroom, {hallway})
    map.connect_rooms(child_bedroom, {hallway})
    map.connect_rooms(bathroom, {hallway})

class Room:
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

if __name__ == '__main__':
    main()