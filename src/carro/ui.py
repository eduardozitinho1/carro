from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def show_car_status(place, speed):
    console.print(
        Panel(
            f"[bold]Localização atual:[/bold] [cyan]{place}[/cyan]\n"
            f"[bold]Velocidade atual:[/bold] "
            f"[cyan]{speed}km/h[/cyan]",
            title="Status do carro",
            border_style="cyan",
        )
    )


def show_car_panel(place, speed):
    console.print(
        Panel(
            f"[bold cyan]CARRO[/bold cyan]\n\n"
            f"[bold]Localização:[/bold] {place}\n"
            f"[bold]Velocidade:[/bold] {speed} km/h",
            title="Painel do veículo",
            border_style="cyan",
        )
    )


def show_main_menu():
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


def show_destinations(destinations):
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
