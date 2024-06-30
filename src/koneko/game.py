class Event: ...


class Game:
    def __init__(self, players_id: tuple[str]) -> None:
        self.players_id = players_id
        self.events: list[Event] = list()
        self.current_player = players_id[0]
