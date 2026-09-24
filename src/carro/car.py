from time import sleep

from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn

from .events.accident import chance as accident_chance
from .events.random_event import happened
from .events.recklessness import (
    BREATHALYZER_CHANCE,
    RECKLESSNESS_CHANCE,
    arrest_chance,
)
from .events.traffic import CHANCE as TRAFFIC_CHANCE
from .events.traffic import traffic
from .places import places
from .ui import console
from .upgrades.speed import max_speed


SIMULATION_TIME_SCALE = 0.05
TRAVEL_STEPS = 100


class Car:
    def __init__(self):
        self._speed = 0
        self._place = "São Paulo"
        self._fuel = 100.0
        self._airbags = 0
        self._speed_upgrade = 0

    @property
    def speed(self):
        return self._speed

    @property
    def place(self):
        return self._place

    @property
    def fuel(self):
        return self._fuel

    @property
    def airbags(self):
        return self._airbags

    @property
    def speed_upgrade(self):
        return self._speed_upgrade

    @property
    def max_speed(self):
        return max_speed(self.speed_upgrade)

    @speed.setter
    def speed(self, speed):
        if speed > self.max_speed:
            raise ValueError(
                "Velocidade do carro é muito grande, o carro pode quebrar"
            )

        if speed < 0:
            raise ValueError(
                "A velocidade não pode ser negativa"
            )

        self._speed = speed

    def running(self):
        return self.speed != 0

    def accelerate(self, amount):
        amount = float(amount)

        if amount <= 0:
            console.print(
                "[bold red]A aceleração precisa ser maior que zero.[/bold red]"
            )
            return

        try:
            self.speed = self.speed + amount
        except ValueError:
            console.print(
                "[bold red]Velocidade do carro é muito grande, "
                "o carro pode quebrar[/bold red]"
            )
            return

        console.print(
            f"[bold green]Carro acelerou {amount:g}km/h![/bold green] "
            f"Agora ele está a [bold cyan]{self.speed:g}km/h[/bold cyan]"
        )

    def decelerate(self, amount):
        amount = float(amount)

        if amount <= 0:
            console.print(
                "[bold red]A desaceleração precisa ser maior que zero.[/bold red]"
            )
            return

        try:
            self.speed = self.speed - amount
        except ValueError:
            console.print(
                "[bold yellow]O carro não pode ficar abaixo de 0 km/h.[/bold yellow]"
            )
            return

        console.print(
            f"[bold yellow]Carro desacelerou {amount:g}km/h![/bold yellow] "
            f"Agora ele está a [bold cyan]{self.speed:g}km/h[/bold cyan]"
        )

    def stop(self):
        if not self.running():
            console.print(
                "[bold yellow]Já está parado[/bold yellow]"
            )
            return

        self.speed = 0

        console.print(
            "[bold green]Carro parado.[/bold green]"
        )

    def _handle_recklessness(self, player):
        console.print(
            "[bold red]Você foi imprudente durante a viagem![/bold red]"
        )
        console.print(
            "[bold yellow]A polícia percebeu a condução suspeita "
            "e realizou uma abordagem.[/bold yellow]"
        )

        if not happened(BREATHALYZER_CHANCE):
            console.print(
                "[bold green]A polícia não realizou o bafômetro.[/bold green]"
            )
            return False

        console.print(
            "[bold red]O bafômetro detectou álcool.[/bold red]"
        )

        chance = arrest_chance(player.lawyers)

        if happened(chance):
            console.print(
                "[bold red]Você foi preso por dirigir alcoolizado.[/bold red]"
            )
            player.jail()
            return True

        if player.lawyers > 0:
            console.print(
                "[bold green]A assistência jurídica reduziu seu risco "
                "de prisão.[/bold green]"
            )
        else:
            console.print(
                "[bold green]Você não foi preso desta vez.[/bold green]"
            )

        return False

    def travel(self, place, player=None):
        if place not in places:
            console.print(
                "[bold red]Não existe esse lugar, pô[/bold red]"
            )
            return False

        if player is not None and player.jailed:
            console.print(
                "[bold red]Você está preso e não pode dirigir.[/bold red]"
            )
            return False

        if self.speed <= 0:
            console.print(
                "[bold red]O carro precisa estar andando para viajar[/bold red]"
            )
            return False

        if place == self.place:
            console.print(
                "[bold yellow]O carro já está nesse lugar[/bold yellow]"
            )
            return False

        previous_place = self.place

        distance = abs(
            places[self.place] - places[place]
        )

        travel_hours = distance / float(self.speed)

        fuel_consumption = distance / 100
        starting_fuel = self.fuel

        if self.fuel < fuel_consumption:
            console.print(
                "[bold red]Combustível insuficiente para completar "
                "a viagem.[/bold red]"
            )
            return False

        simulation_seconds = (
            travel_hours * 60 * SIMULATION_TIME_SCALE
        )

        step_fuel = fuel_consumption / TRAVEL_STEPS
        step_seconds = simulation_seconds / TRAVEL_STEPS

        with Progress(
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task(
                f"Viajando para {place}...",
                total=TRAVEL_STEPS,
            )

            for _ in range(TRAVEL_STEPS):
                self._fuel = max(0.0, self.fuel - step_fuel)

                if happened(RECKLESSNESS_CHANCE):
                    arrested = False

                    if player is not None:
                        arrested = self._handle_recklessness(player)

                    if arrested:
                        console.print(
                            "[bold yellow]A viagem foi interrompida "
                            "e precisa ser refeita.[/bold yellow]"
                        )
                    else:
                        console.print(
                            "[bold yellow]A viagem precisa ser refeita.[/bold yellow]"
                        )

                    self._fuel = starting_fuel
                    self._place = previous_place
                    return False

                if happened(accident_chance(self.airbags)):
                    console.print(
                        "[bold red]Você sofreu um acidente durante a viagem![/bold red]"
                    )
                    console.print(
                        "[bold yellow]O acidente interrompeu a viagem. "
                        "Você terá que refazê-la.[/bold yellow]"
                    )

                    self._fuel = starting_fuel
                    self._place = previous_place
                    return False

                if happened(TRAFFIC_CHANCE):
                    console.print(
                        "[bold yellow]Trânsito! A viagem está temporariamente parada.[/bold yellow]"
                    )
                    traffic()

                sleep(step_seconds)
                progress.advance(task)

        self._place = place

        console.print(
            Panel(
                f"[bold green]Você chegou em {place}![/bold green]\n"
                f"Distância: [cyan]{distance} km[/cyan]\n"
                f"Combustível restante: [cyan]{self.fuel:.2f}%[/cyan]",
                border_style="green",
            )
        )

        return True

    def refuel(self, amount):
        if amount <= 0:
            return

        self._fuel = min(100.0, self.fuel + amount)

    def install_airbag(self):
        self._airbags += 1

    def install_speed_upgrade(self):
        self._speed_upgrade += 1
