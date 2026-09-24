from decimal import Decimal, InvalidOperation
import typer
from rich.panel import Panel
import random
from time import sleep
from rich.progress import BarColumn, Progress, TextColumn

from .car import Car
from .jobs import JOBS
from .places import places
from .player import Player
from .ui import (
    console,
    show_car_panel,
    show_car_status,
    show_destinations,
    show_main_menu,
)
from .upgrades import airbags, lawyer, speed

JAIL_SENTENCE_SECONDS = 90
JAIL_NOMINAL_YEARS = 3
JAIL_DEATH_CHANCE = 0.015

app = typer.Typer()

carro = Car()
player = Player()

def handle_jail(player):
    if not player.jailed:
        return False

    console.print(
        Panel(
            "[bold red]Você está preso.[/bold red]\n"
            f"Pena: [yellow]{JAIL_NOMINAL_YEARS} anos[/yellow]\n"
            f"Tempo de jogo: [yellow]{JAIL_SENTENCE_SECONDS} segundos[/yellow]",
            title="Prisão",
            border_style="red",
        )
    )

    death_chance_per_second = (
        1 - (1 - JAIL_DEATH_CHANCE) ** (1 / JAIL_SENTENCE_SECONDS)
    )

    with Progress(
        TextColumn("[bold red]Cumprindo pena...[/bold red]"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    ) as progress:
        task = progress.add_task(
            "Cumprindo pena...",
            total=JAIL_SENTENCE_SECONDS,
        )

        for _ in range(JAIL_SENTENCE_SECONDS):
            if random.random() < death_chance_per_second:
                player.die()

                console.print(
                    Panel(
                        "[bold red]Você morreu na prisão.[/bold red]\n"
                        "Sua jornada terminou.",
                        title="Fim de jogo",
                        border_style="red",
                    )
                )

                return True

            sleep(1)
            progress.advance(task)

    player.serve_sentence()

    console.print(
        Panel(
            "[bold green]Você cumpriu sua pena.[/bold green]\n"
            "Você está livre novamente.",
            title="Liberdade",
            border_style="green",
        )
    )

    return False

def show_player_status():
    job = player.current_job

    if job is None:
        job_text = "Nenhum"
    else:
        job_text = (
            f"{job.origin} → {job.destination}"
        )

    if player.jailed:
        prison_status = "[bold red]Preso[/bold red]"
    else:
        prison_status = "[bold green]Livre[/bold green]"

    console.print(
        Panel(
            f"[bold]Saldo:[/bold] "
            f"[green]R$ {player.balance:.2f}[/green]\n"
            f"[bold]Entregas:[/bold] "
            f"{player.deliveries_completed}\n"
            f"[bold]Qualidade:[/bold] "
            f"{player.quality:.0%}\n"
            f"[bold]Advogados:[/bold] "
            f"{player.lawyers}\n"
            f"[bold]Situação:[/bold] "
            f"{prison_status}\n"
            f"[bold]Trabalho:[/bold] "
            f"{job_text}",
            title="Status do jogador",
            border_style="magenta",
        )
    )


def work():
    if player.jailed:
        console.print(
            "[bold red]Você está preso e não pode aceitar trabalhos.[/bold red]"
        )
        return

    if player.current_job is not None:
        job = player.current_job

        console.print(
            Panel(
                f"[bold]Entrega atual:[/bold]\n"
                f"{job.origin} → {job.destination}\n\n"
                f"[bold]Pagamento:[/bold] "
                f"R$ {job.payment:.2f}",
                title="Trabalho atual",
                border_style="yellow",
            )
        )
        return

    job = JOBS.get(carro.place)

    if job is None:
        console.print(
            "[bold red]Não existe trabalho neste estado.[/bold red]"
        )
        return

    console.print(
        Panel(
            f"[bold]Origem:[/bold] {job.origin}\n"
            f"[bold]Destino:[/bold] {job.destination}\n"
            f"[bold]Pagamento:[/bold] R$ {job.payment:.2f}\n"
            f"[bold]Qualidade mínima:[/bold] "
            f"{job.minimum_quality:.0%}\n"
            f"[bold]Sua qualidade:[/bold] "
            f"{player.quality:.0%}",
            title="Oferta de trabalho",
            border_style="green",
        )
    )

    if not job.can_apply(player):
        console.print(
            "[bold red]Sua qualidade ainda não é suficiente "
            "para esse trabalho.[/bold red]"
        )
        return

    answer = console.input(
        "[bold cyan]Deseja aceitar a entrega? (s/n): [/bold cyan]"
    ).strip().lower()

    if answer != "s":
        return

    if not player.apply_for_job(job):
        console.print(
            "[bold red]Sua candidatura foi recusada.[/bold red]"
        )
        return

    console.print(
        Panel(
            f"[bold green]Entrega aceita![/bold green]\n"
            f"Destino: [cyan]{job.destination}[/cyan]\n"
            f"Pagamento: [green]R$ {job.payment:.2f}[/green]",
            border_style="green",
        )
    )


def buy_speed_upgrade():
    level = carro.speed_upgrade
    price = speed.cost(level)

    console.print(
        Panel(
            f"[bold]Nível:[/bold] {level}\n"
            f"[bold]Velocidade máxima:[/bold] "
            f"{carro.max_speed} km/h\n"
            f"[bold]Nova velocidade máxima:[/bold] "
            f"{carro.max_speed + speed.SPEED_INCREMENT} km/h\n"
            f"[bold]Preço:[/bold] R$ {price:.2f}\n"
            f"[bold]Saldo:[/bold] R$ {player.balance:.2f}",
            title="Upgrade de velocidade",
            border_style="cyan",
        )
    )

    if not player.spend(price):
        console.print(
            "[bold red]Dinheiro insuficiente.[/bold red]"
        )
        return

    carro.install_speed_upgrade()

    console.print(
        f"[bold green]Upgrade comprado! "
        f"Velocidade máxima: {carro.max_speed} km/h[/bold green]"
    )


def buy_airbag():
    level = carro.airbags
    price = airbags.cost(level)

    console.print(
        Panel(
            f"[bold]Airbags:[/bold] {level}\n"
            f"[bold]Redução por airbag:[/bold] "
            f"{airbags.CHANCE_REDUCTION:.0%}\n"
            f"[bold]Preço:[/bold] R$ {price:.2f}\n"
            f"[bold]Saldo:[/bold] R$ {player.balance:.2f}",
            title="Airbag",
            border_style="yellow",
        )
    )

    if not player.spend(price):
        console.print(
            "[bold red]Dinheiro insuficiente.[/bold red]"
        )
        return

    carro.install_airbag()

    console.print(
        f"[bold green]Airbag instalado! "
        f"Total: {carro.airbags}[/bold green]"
    )


def hire_lawyer():
    level = player.lawyers
    price = lawyer.cost(level)

    console.print(
        Panel(
            f"[bold]Advogados:[/bold] {level}\n"
            f"[bold]Preço do próximo:[/bold] R$ {price:.2f}\n"
            f"[bold]Saldo:[/bold] R$ {player.balance:.2f}",
            title="Advogado",
            border_style="blue",
        )
    )

    if not player.hire_lawyer(price):
        console.print(
            "[bold red]Dinheiro insuficiente.[/bold red]"
        )
        return

    console.print(
        f"[bold green]Advogado contratado! "
        f"Total: {player.lawyers}[/bold green]"
    )


def upgrades_menu():
    while True:
        console.print(
            Panel(
                "1. Upgrade de velocidade\n"
                "2. Comprar airbag\n"
                "3. Contratar advogado\n"
                "s. Voltar",
                title="Upgrades",
                border_style="cyan",
            )
        )

        option = console.input(
            "[bold cyan]> [/bold cyan]"
        ).strip().lower()

        match option:
            case "1":
                buy_speed_upgrade()

            case "2":
                buy_airbag()

            case "3":
                hire_lawyer()

            case "s":
                return

            case _:
                console.print(
                    "[bold red]Opção inválida.[/bold red]"
                )


def refuel():
    if carro.fuel >= 100:
        console.print(
            "[bold yellow]O tanque já está cheio.[/bold yellow]"
        )
        return

    try:
        amount = Decimal(
            console.input(
                "[bold cyan]Quantos % deseja abastecer? [/bold cyan]"
            )
        )
    except InvalidOperation:
        console.print(
            "[bold red]Digite um número válido.[/bold red]"
        )
        return

    if amount <= 0:
        console.print(
            "[bold red]A quantidade precisa ser maior que zero.[/bold red]"
        )
        return

    missing = Decimal(str(100 - carro.fuel))

    amount = min(amount, missing)

    price = amount * Decimal("2.50")

    console.print(
        Panel(
            f"[bold]Combustível:[/bold] {amount:.2f}%\n"
            f"[bold]Preço:[/bold] R$ {price:.2f}\n"
            f"[bold]Saldo:[/bold] R$ {player.balance:.2f}",
            title="Abastecimento",
            border_style="yellow",
        )
    )

    answer = console.input(
        "[bold cyan]Confirmar abastecimento? (s/n): [/bold cyan]"
    ).strip().lower()

    if answer != "s":
        return

    if not player.spend(float(price)):
        console.print(
            "[bold red]Dinheiro insuficiente.[/bold red]"
        )
        return

    carro.refuel(float(amount))

    console.print(
        f"[bold green]Carro abastecido. "
        f"Combustível: {carro.fuel:.2f}%[/bold green]"
    )


def travel():
    destinations = list(places.keys())

    show_destinations(destinations)

    try:
        destination = int(
            console.input(
                "[bold green]> [/bold green]"
            )
        )
    except ValueError:
        console.print(
            "[bold red]Digite o número correspondente ao destino.[/bold red]"
        )
        return

    if not 1 <= destination <= len(destinations):
        console.print(
            "[bold red]Destino inválido.[/bold red]"
        )
        return

    destination_name = destinations[destination - 1]

    success = carro.travel(
        destination_name,
        player,
    )

    if not success:
        return

    job = player.current_job

    if job is None:
        return

    if carro.place != job.destination:
        return

    player.complete_job()

    console.print(
        Panel(
            f"[bold green]Entrega concluída![/bold green]\n"
            f"Pagamento recebido: "
            f"[green]R$ {job.payment:.2f}[/green]\n"
            f"Saldo atual: "
            f"[green]R$ {player.balance:.2f}[/green]\n"
            f"Entregas concluídas: "
            f"[cyan]{player.deliveries_completed}[/cyan]",
            border_style="green",
        )
    )


def handle_jail():
    console.print(
        Panel(
            "[bold red]Você está preso.[/bold red]\n\n"
            "Você precisa cumprir sua pena antes de continuar.",
            title="Prisão",
            border_style="red",
        )
    )

    answer = console.input(
        "[bold yellow]Cumprir pena? (s/n): [/bold yellow]"
    ).strip().lower()

    if answer == "s":
        player.serve_sentence()

        console.print(
            "[bold green]Pena cumprida. Você está livre novamente.[/bold green]"
        )


@app.command()
def main():
    while True:
        if player.dead:
            break
        if player.jailed:
            handle_jail()
            continue

        show_car_panel(
            carro.place,
            carro.speed,
            carro.fuel,
        )

        show_main_menu()

        opt = console.input(
            "[bold cyan]> [/bold cyan]"
        ).strip().lower()

        match opt:
            case "1":
                show_car_status(
                    carro.place,
                    carro.speed,
                )

            case "2":
                try:
                    amount = Decimal(
                        console.input(
                            "[bold cyan]Quanto quer acelerar? "
                            "(km/h): [/bold cyan]"
                        )
                    )
                except InvalidOperation:
                    console.print(
                        "[bold red]Digite um número válido.[/bold red]"
                    )
                    continue

                carro.accelerate(amount)

            case "3":
                try:
                    amount = Decimal(
                        console.input(
                            "[bold cyan]Quanto quer desacelerar? "
                            "(km/h): [/bold cyan]"
                        )
                    )
                except InvalidOperation:
                    console.print(
                        "[bold red]Digite um número válido.[/bold red]"
                    )
                    continue

                carro.decelerate(amount)

            case "4":
                carro.stop()

            case "5":
                travel()

            case "6":
                work()

            case "7":
                show_player_status()

            case "8":
                upgrades_menu()

            case "9":
                refuel()

            case "s":
                console.print(
                    Panel(
                        "[bold cyan]Até a próxima![/bold cyan]",
                        border_style="cyan",
                    )
                )
                break

            case _:
                console.print(
                    "[bold red]Opção inválida.[/bold red]"
                )


if __name__ == "__main__":
    main()
