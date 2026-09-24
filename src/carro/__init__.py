from decimal import Decimal
import typer

app = typer.Typer()

class Car:
    """
    Classe principal do carro
    """

    def __init__(self):
        self._speed = 0

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        if speed > 150:
            raise ValueError("Velocidade do carro é muito grande, o carro pode quebrar")
        elif speed < -50:
            raise ValueError("O carro não tem potência o suficiente para ir muito para trás")
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


carro = Car()

@app.command()
def main():
    while True:
        opt = input("O que deseja fazer com o carro atualmente? (digite \"s\" para sair)\n1. Ver velocidade atual\n2. Acelerar\n3. Desacelerar\n4. Parar\n> ")
        match opt:
            case "1":
                print(f"A velocidade atual do seu carro é de {carro.speed}km/h")
            case "2":
                speed = Decimal(
                    input("Quanto é a quantidade que você quer acelerar? (Em km/h): ")
                )
                carro.accelerate(speed)
            case "3":
                speed = Decimal(
                    input("Quanto é a quantidade que você quer desacelerar? (Em km/h): ")
                )
                carro.decelerate(speed)
            case "4":
                carro.stop()
            case "s":
                break
            case _:
                print("Opção inválida")


if __name__ == "__main__":
    main()
