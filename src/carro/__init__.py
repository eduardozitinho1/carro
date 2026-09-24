from decimal import Decimal
import typer
from rich.progress import track
from time import sleep

app = typer.Typer()

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
            print(f"Carro acelerou {speed}km/h! Agora ele está a {self.speed}km/h")
        except ValueError:
            print("Velocidade do carro é muito grande, o carro pode quebrar")

    def decelerate(self, speed):
        try:
            self.speed -= speed
            print(f"Carro desacelerou {speed}km/h! Agora ele está a {self.speed}km/h")
        except ValueError:
            print("O carro não tem potência o suficiente para ir muito para trás")

    def stop(self):
        if not self.running():
            print("Já está parado")
        else:
            self.speed = 0

    def travel(self, place):
        if place not in places:
            print("Não existe esse lugar, pô")
            return

        if self.speed <= 0:
            print("O carro precisa estar andando para viajar")
            return

        if place == self.place:
            print("O carro já está nesse lugar")
            return

        distance = abs(places[self.place] - places[place])
        travel_hours = distance / float(self.speed)

        simulation_seconds = min(travel_hours * 60, 60)

        steps = 100

        for _ in track(
            range(steps),
            description=f"Viajando para {place}...",
        ):
            sleep(simulation_seconds / steps)

        self._place = place
        print(f"Você chegou em {place}!")

carro = Car()


@app.command()
def main():
    while True:
        opt = input(
            'O que deseja fazer com o carro atualmente? (digite "s" para sair)\n'
            '1. Ver velocidade atual\n'
            '2. Acelerar\n'
            '3. Desacelerar\n'
            '4. Parar\n'
            '5. Viajar\n'
            '> '
        )

        match opt:
            case "1":
                print(f"Localização atual: {carro.place}")
                print(f"A velocidade atual do seu carro é de {carro.speed}km/h")

            case "2":
                speed = Decimal(
                    input("Quanto é a quantidade que você quer acelerar? (Em km/h): ")
                )
                carro.accelerate(speed)

            case "3":
                speed = Decimal(
                    input(
                        "Quanto é a quantidade que você quer desacelerar? (Em km/h): "
                    )
                )
                carro.decelerate(speed)

            case "4":
                carro.stop()

            case "5":
                destinations = list(places.keys())

                print("\nEscolha o destino:")
                for number, place in enumerate(destinations, start=1):
                    print(f"{number:2}. {place}")

                try:
                    destination = int(input("> "))
                except ValueError:
                    print("Digite o número correspondente ao destino")
                    continue

                if not 1 <= destination <= len(destinations):
                    print("Destino inválido")
                    continue

                carro.travel(destinations[destination - 1])

            case "s":
                break

            case _:
                print("Opção inválida")

if __name__ == "__main__":
    main()
