from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    next_player: int
    positions: tuple[int] = (0, 0, 0, 0, 0, 0, 0, 0, 0)

    @classmethod
    def from_list(cls, positions: list[int], next_player: int):
        assert next_player in (-1, 1), f"Player must be -1 or 1, not {next_player}"
        assert len(positions) == 9, f"State must have length 9, got {len(positions)}"
        assert all(type(p) == int for p in positions), "State must only be comprised of integers"
        assert min(positions) >= -1 and max(positions) <= 1, "State must only have values of -1, 0, and 1"
        assert all(p is not None for p in positions), "State may not contain Null values"
        pos = tuple(positions)
        return cls(positions=pos, next_player=next_player)
    
    def available_positions(self) -> list[int]:
        result = list()
        for n, p in enumerate(self.positions):
            if p == 0:
                result.append(n)
        return result


@dataclass(frozen=True)
class Action:
    position: int
    player: int
