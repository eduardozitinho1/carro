from decimal import Decimal

import typer
from rich.panel import Panel

from .car import Car
from .places import places
from .ui import console, show_car_panel, show_car_status, show_destinations, show_main_menu

app = typer.Typer()

carro = Car()

@app.command()
def main():
    while True:
        show_car_panel(carro.place, carro.speed)
        show_main_menu()

        opt = console.input("[bold cyan]> [/bold cyan]")

        match opt:
            case "1":
                show_car_status(carro.place, carro.speed)

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

                show_destinations(destinations)

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
