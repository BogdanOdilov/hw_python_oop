from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        """Выводит информацию о тренировке."""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    SECUNDE: int = 60
    CF_RUN_1: int = 18
    CF_RUN_2: int = 20

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        return ((self.CF_RUN_1 * self.get_mean_speed()
                 - self.CF_RUN_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.SECUNDE
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CF_WALK_1: float = 0.035
    CF_WALK_2: float = 2
    CF_WALK_3: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories_1 = self.CF_WALK_1 * self.weight
        calories_2 = self.get_mean_speed()**2 // self.height
        calories_3 = calories_2 * self.CF_WALK_3 * self.weight
        calories = (calories_1 + calories_3) * self.duration * self.SECUNDE
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    CF_SW_1: float = 1.1
    CF_SW_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Прочитать среднюю скорость человека."""
        speed_1 = self.length_pool * self.count_pool
        self.speed = speed_1 / self.M_IN_KM / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories_1 = self.get_mean_speed() + self.CF_SW_1
        calories = calories_1 * self.CF_SW_2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    operating_modes: type[Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
        }
    redirection = operating_modes.get(workout_type)
    if redirection is None:
        raise
    else:
        return redirection(*data)


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
