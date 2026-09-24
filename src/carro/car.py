from time import sleep

from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn

from .places import places
from .ui import console


class Car:
    """
    Classe principal do carro
    """

    def __init__(self):
        self._speed = 0
        self._place = "São Paulo"

    @property
    def speed(self):
        return self._speed

    @property
    def place(self):
        return self._place

    @speed.setter
    def speed(self, speed):
        if speed > 150:
            raise ValueError("Velocidade do carro é muito grande, o carro pode quebrar")
        elif speed < -50:
            raise ValueError(
                "O carro não tem potência o suficiente para ir muito para trás"
            )
        else:
            self._speed = speed

    def running(self):
        return self.speed != 0

    def accelerate(self, speed):
        try:
            self.speed += speed
            console.print(
                f"[bold green]Carro acelerou {speed}km/h![/bold green] "
                f"Agora ele está a [bold cyan]{self.speed}km/h[/bold cyan]"
            )
        except ValueError:
            console.print(
                "[bold red]Velocidade do carro é muito grande, "
                "o carro pode quebrar[/bold red]"
            )

    def decelerate(self, speed):
        try:
            self.speed -= speed
            console.print(
                f"[bold yellow]Carro desacelerou {speed}km/h![/bold yellow] "
                f"Agora ele está a [bold cyan]{self.speed}km/h[/bold cyan]"
            )
        except ValueError:
            console.print(
                "[bold red]O carro não tem potência o suficiente "
                "para ir muito para trás[/bold red]"
            )

    def stop(self):
        if not self.running():
            console.print("[bold yellow]Já está parado[/bold yellow]")
        else:
            self.speed = 0
            console.print("[bold green]Carro parado.[/bold green]")

    def travel(self, place):
        if place not in places:
            console.print("[bold red]Não existe esse lugar, pô[/bold red]")
            return

        if self.speed <= 0:
            console.print(
                "[bold red]O carro precisa estar andando para viajar[/bold red]"
            )
            return

        if place == self.place:
            console.print("[bold yellow]O carro já está nesse lugar[/bold yellow]")
            return

        distance = abs(places[self.place] - places[place])
        travel_hours = distance / float(self.speed)

        simulation_seconds = min(travel_hours * 60, 60)

        steps = 100

        with Progress(
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task(
                f"Viajando para {place}...",
                total=steps,
            )

            for _ in range(steps):
                sleep(simulation_seconds / steps)
                progress.advance(task)

        self._place = place
        console.print(
            Panel(
                f"[bold green]Você chegou em {place}![/bold green]",
                border_style="green",
            )
        )
