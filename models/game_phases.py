from enum import Enum

from orchestration import night
from orchestration import discussion
from orchestration import judgement


class game_phases(Enum):
    NIGHT = night
    DISCUSSION = discussion
    JUDGEMENT = judgement
