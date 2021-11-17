from typing import ClassVar
from dataclasses import dataclass


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_H: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(type(self).__name__, self.duration,
                              self.get_distance(), self.get_mean_speed(),
                              self.get_spent_calories())
        return message


@dataclass
class Running(Training):
    """Тренировка: бег."""
    COEFF1: ClassVar[int] = 18
    COEFF2: ClassVar[int] = 20
    MIN_H: ClassVar[int] = 60

    def get_spent_calories(self) -> float:
        return ((self.COEFF1 * self.get_mean_speed()
                - self.COEFF2) * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_H))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    COEFF3: ClassVar[float] = 0.035
    COEFF4: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        return (self.COEFF3 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF4 * self.weight) * (self.duration * self.MIN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: int
    count_pool: int
    COEFF5: ClassVar[float] = 1.1
    COEFF6: ClassVar[int] = 2
    LEN_STEP: ClassVar[float] = 1.38

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF5)
                * self.COEFF6 * self.weight)


types = {'SWM': Swimming,
         'RUN': Running,
         'WLK': SportsWalking}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in types.keys():
        training = types[workout_type]
        return training(*data)
    raise KeyError("Ошибка!")


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
