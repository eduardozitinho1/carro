import random


class DeliveryJob:
    def __init__(
        self,
        origin,
        destination,
        payment,
        minimum_quality=0.0,
        acceptance_chance=0.5,
    ):
        self.origin = origin
        self.destination = destination
        self.payment = payment
        self.minimum_quality = minimum_quality
        self.acceptance_chance = acceptance_chance

    def can_apply(self, player):
        return player.quality >= self.minimum_quality

    def accept(self):
        return random.random() < self.acceptance_chance

    def complete(self, player):
        player.earn(self.payment)
        player.complete_delivery()
