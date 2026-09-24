from decimal import Decimal
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn
from rich.table import Table
from time import sleep

app = typer.Typer()
console = Console()

places = {
    "Rio de Janeiro": 435,
    "Minas Gerais": 585,
    "Espírito Santo": 880,
    "Paraná": 405,
    "Santa Catarina": 705,
    "Rio Grande do Sul": 1130,
    "Mato Grosso do Sul": 1015,
    "Goiás": 926,
    "Distrito Federal": 1007,
    "Mato Grosso": 1430,
    "Bahia": 1960,
    "Sergipe": 2140,
    "Alagoas": 2250,
    "Pernambuco": 2590,
    "Paraíba": 2680,
    "Rio Grande do Norte": 2860,
    "Ceará": 2945,
    "Piauí": 2770,
    "Maranhão": 3030,
    "Tocantins": 1350,
    "Rondônia": 2450,
    "Pará": 2930,
    "Acre": 3140,
    "Amazonas": 3500,
    "Roraima": 3980,
    "Amapá": 3320,
    "São Paulo": 0,
}


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


carro = Car()


@app.command()
def main():
    while True:
        console.print(
            Panel(
                f"[bold cyan]CARRO[/bold cyan]\n\n"
                f"[bold]Localização:[/bold] {carro.place}\n"
                f"[bold]Velocidade:[/bold] {carro.speed} km/h",
                title="Painel do veículo",
                border_style="cyan",
            )
        )

        table = Table(
            title="O que deseja fazer com o carro atualmente?",
            border_style="blue",
            show_header=True,
            header_style="bold cyan",
        )

        table.add_column("Opção", style="bold yellow", justify="center")
        table.add_column("Ação", style="white")

        table.add_row("1", "Ver velocidade atual")
        table.add_row("2", "Acelerar")
        table.add_row("3", "Desacelerar")
        table.add_row("4", "Parar")
        table.add_row("5", "Viajar")
        table.add_row("s", "Sair")

        console.print(table)

        opt = console.input("[bold cyan]> [/bold cyan]")

        match opt:
            case "1":
                console.print(
                    Panel(
                        f"[bold]Localização atual:[/bold] [cyan]{carro.place}[/cyan]\n"
                        f"[bold]Velocidade atual:[/bold] "
                        f"[cyan]{carro.speed}km/h[/cyan]",
                        title="Status do carro",
                        border_style="cyan",
                    )
                )

            case "2":
                speed = Decimal(
                    console.input(
                        "[bold cyan]Quanto é a quantidade que você quer "
                        "acelerar? (Em km/h): [/bold cyan]"
                    )
                )
                carro.accelerate(speed)

            case "3":
                speed = Decimal(
                    console.input(
                        "[bold cyan]Quanto é a quantidade que você quer "
                        "desacelerar? (Em km/h): [/bold cyan]"
                    )
                )
                carro.decelerate(speed)

            case "4":
                carro.stop()

            case "5":
                destinations = list(places.keys())

                table = Table(
                    title="Escolha o destino",
                    border_style="green",
                    show_header=True,
                    header_style="bold green",
                )

                table.add_column("#", style="bold yellow", justify="right")
                table.add_column("Destino", style="white")

                for number, place in enumerate(destinations, start=1):
                    table.add_row(str(number), place)

                console.print(table)

                try:
                    destination = int(
                        console.input("[bold green]> [/bold green]")
                    )
                except ValueError:
                    console.print(
                        "[bold red]Digite o número correspondente ao destino[/bold red]"
                    )
                    continue

                if not 1 <= destination <= len(destinations):
                    console.print("[bold red]Destino inválido[/bold red]")
                    continue

                carro.travel(destinations[destination - 1])

            case "s":
                console.print(
                    Panel(
                        "[bold cyan]Até a próxima![/bold cyan]",
                        border_style="cyan",
                    )
                )
                break

            case _:
                console.print("[bold red]Opção inválida[/bold red]")


if __name__ == "__main__":
    main()
