from typing import ClassVar
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


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
        Message1 = InfoMessage(self.__class__.__name__, self.duration,
                               self.get_distance(), self.get_mean_speed(),
                               self.get_spent_calories())
        return Message1


coeff1: int = 18
coeff2: int = 20
min_h: int = 60

class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action, duration, weight) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((coeff1 * self.get_mean_speed()
                - coeff2) * self.weight / self.M_IN_KM
                * (self.duration * min_h))


coeff3: float = 0.035
coeff4: float = 0.029


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action, duration, weight, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (coeff3 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * coeff4 * self.weight) * (self.duration * min_h)


coeff5: float = 1.1
coeff6: float = 2


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self, action, duration, weight,
                 length_pool: float, count_pool) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + coeff5)
                * coeff6 * self.weight)

types = {'SWM': Swimming,
         'RUN': Running,
         'WLK': SportsWalking}


def read_package(workout_type: str, data: list, types: dict) -> Training:
    """Прочитать данные полученные от датчиков."""
    training1 = types[workout_type]
    return training1(*data)

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
        training = read_package(workout_type, data, types)
        main(training)
