from abc import ABC, abstractmethod


class EnergyDrink(ABC):
    def __init__(self, description: str) -> None:
        self.description = description

    @abstractmethod
    def get_description(self) -> str: ...

    def add_bubbles(self, pressure: int) -> None:
        print(f"adding bubbles with pressure: {pressure} bar")

    @abstractmethod
    def get_caffeine_level(self) -> int: ...


class NOCCO(EnergyDrink):
    def __init__(self, description: str) -> None:
        super().__init__(description)

    def get_description(self) -> str:
        return self.description

    def get_caffeine_level(self) -> int:
        return 180


class SupplementsDecorator(EnergyDrink, ABC):
    def __init__(self, energy_drink: EnergyDrink) -> None:
        super().__init__(energy_drink.get_description())

        self.energy_drink = energy_drink


class BCAA(SupplementsDecorator):
    def __init__(self, energy_drink: EnergyDrink) -> None:
        super().__init__(energy_drink)

    def get_description(self) -> str:
        return self.energy_drink.get_description() + ", add BCAA"

    def get_caffeine_level(self) -> int:
        return self.energy_drink.get_caffeine_level() + 0


class Vitamins(SupplementsDecorator):
    def __init__(self, energy_drink: EnergyDrink) -> None:
        self.energy_drink = energy_drink

    def get_description(self) -> str:
        return self.energy_drink.get_description() + ", add lots of vitamins"

    def get_caffeine_level(self) -> int:
        return self.energy_drink.get_caffeine_level() + 0


class CelsiusEmulator(SupplementsDecorator):
    def __init__(self, energy_drink: EnergyDrink) -> None:
        self.energy_drink = energy_drink

    def get_description(self) -> str:
        return self.energy_drink.get_description() + ", add more caffeine and worse taste"

    def get_caffeine_level(self) -> int:
        return self.energy_drink.get_caffeine_level() + 20


def main():
    nocco = NOCCO("Starting with a refreshing energy drink with amazing taste")
    nocco = BCAA(nocco)
    nocco = Vitamins(nocco)
    celsius = CelsiusEmulator(nocco)
    print("The drink: " + celsius.get_description())
    print(f"The caffeine level {celsius.get_caffeine_level()}")


if __name__ == "__main__":
    main()
