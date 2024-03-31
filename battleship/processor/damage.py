from math import sqrt

import esper
from battleship.component import Hazard, Health, Position
from battleship.config import logger
from battleship.utils import Status, get_distance  # noqa: F401

from . import AbstractProcessor

_logger = logger.getChild(__name__)


class DamageProcessor(AbstractProcessor):
    """
    Processor that computes and applies damages.
    """

    def process(self) -> bool:
        for _, (ship_position, ship_health) in esper.get_components(Position, Health):
            #
            # Iterate over all ships (position + health)
            #
            self._ship_damage(ship_position, ship_health)
        return True

    def _ship_damage(self, ship_position: Position, ship_health: Health) -> None:
        _logger.debug(f"[BEFORE] Ship health={ship_health.health}")

        for hazard_entity, (hazard_position, hazard) in esper.get_components(
            Position, Hazard
        ):
            #
            # Iterate over all hazards (position + hazard)
            #
            damage = get_damage(ship_position, hazard_position, hazard)
            ship_health.health -= damage

            _logger.debug(f"Hazard[entity={hazard_entity}] inflicted damage={damage}")

        _logger.debug(f"[AFTER] Ship health={ship_health.health}")

        if ship_health.health < 0:
            ship_health.status = Status.DEAD
            _logger.info("Ship died")


def get_damage(
    ship_position: Position, hazard_position: Position, hazard: Hazard
) -> float:
    """
    Compute the damage to be inflicted to ship by this hazard.

    :param ship_position: current position of the ship
    :param hazard_position: current position of this hazard
    :param hazard: metadata of this hazard
    """

    # Compute distance from ship to hazard
    distance = sqrt(
        (ship_position.x - hazard_position.x) ** 2
        + (ship_position.y - hazard_position.y) ** 2
    )

    # Check if ship is safe from hazard
    if distance >= hazard.safe_dist:
        return 0

    # Compute the actual damage
    damage = (hazard.safe_dist - distance) / hazard.safe_dist

    # Return the damage you computed
    # <!!! REPLACE THE LINE BELLOW WITH YOUR OWN !!!>
    return damage
