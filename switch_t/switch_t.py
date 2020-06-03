#!/usr/bin/env python
"""
Switch_Tのパラメータ調整
"""

if '__file__' in globals():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import json
from random import randrange, random, randint
from copy import deepcopy

from reversi import Player, Simulator
from reversi.strategies.switch import Switch
from reversi.strategies.table import Table
from reversi.genetic_algorithm.chromosome import Chromosome
from reversi.genetic_algorithm.genetic_algorithm import GeneticAlgorithm

class Switch_T(Chromosome):
    """
    Switch_Tのパラメータ調整
    """
    def __init__(self, corner=None, c=None, a1=None, a2=None, b=None, x=None, o=None):
        self.setting = self._load_setting('./switch_setting.json')
        self.corner = corner
        self.c = c
        self.a1 = a1
        self.a2 = a2
        self.b = b
        self.x = x
        self.o = o
        self.fitness_value = None

    def _load_setting(self, setting_json):
        """
        設定値読み込み
        """
        setting = {
            "turns": [36, 48, 60],
            "threshold": 60,
            "mutation_value": 1,
            "large_mutation_value": 10,
            "board_size": 8,
            "matches": 5,
            "board_type": "bitboard",
            "processes": 2,
            "random_opening": 6,
            "characters": [
                "Challenger",
                "Opponent"
            ]
        }

        if setting_json is not None and os.path.isfile(setting_json):
            with open(setting_json) as f:
                setting = json.load(f)

        return setting

    def fitness(self):
        """
        適応度
        """
        if self.fitness_value is not None:
            return self.fitness_value

        # 遺伝個体(Table-Switch)
        challenger = Switch(
            turns=self.setting['turns'],
            strategies=[
                Table(
                    corner=self.corner[i],
                    c=self.c[i],
                    a1=self.a1[i],
                    a2=self.a2[i],
                    b=self.b[i],
                    o=self.o[i],
                    x=self.x[i],
                ) for i in range(len(self.setting['turns']))
            ],
        )

        # 対戦相手(Table)
        opponent = Table()

        # シミュレータ準備
        simulator = Simulator(
            {
                'Challenger': challenger,
                'Opponent': opponent,
            },
            './switch_setting.json',
        )

        # 対戦させ勝率を返す
        simulator.start()
        print(simulator)
        self.fitness_value = ((simulator.result_ratio['Challenger'] - simulator.result_ratio['Opponent']) + 100) / 2

        return self.fitness_value

    def reset_fitness(self):
        """
        適応度のリセット
        """
        self.fitness_value = None

    def is_optimal(self):
        """
        最適解が見つかったか判定
        """
        return self.fitness() >= self.setting['threshold']

    @classmethod
    def random_instance(cls):
        """
        初期パラメータ設定
        """
        switch_num = len(Switch_T().setting['turns'])

        corner = [randrange(250) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]
        c = [randrange(250) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]
        a1 = [randrange(250) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]
        a2 = [randrange(250) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]
        b = [randrange(250) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]
        x = [randrange(250) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]
        o = [randrange(250) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]

        return Switch_T(corner, c, a1, a2, b, x, o)

    def crossover(self, other):
        """
        交叉
        """
        num1, num2 = randrange(7), randrange(7)
        (num1, num2) = (num1, num2) if num1 < num2 else (num2, num1)

        switch_num = len(self.corner)

        child = deepcopy(self) if random() > 0.5 else deepcopy(other)
        child.reset_fitness()

        if num1 <= 0 and num2 >= 0:
            num3, num4 = randrange(switch_num), randrange(switch_num)
            (num3, num4) = (num3, num4) if num3 < num4 else (num4, num3)
            for i in range(num3, num4+1):
                a, b = self.corner[i], other.corner[i]
                (a, b) = (a, b) if a < b else (b, a)
                child.corner[i] = randint(a, b)
        if num1 <= 1 and num2 >= 1:
            num3, num4 = randrange(switch_num), randrange(switch_num)
            (num3, num4) = (num3, num4) if num3 < num4 else (num4, num3)
            for i in range(num3, num4+1):
                a, b = self.c[i], other.c[i]
                (a, b) = (a, b) if a < b else (b, a)
                child.c[i] = randint(a, b)
        if num1 <= 2 and num2 >= 2:
            num3, num4 = randrange(switch_num), randrange(switch_num)
            (num3, num4) = (num3, num4) if num3 < num4 else (num4, num3)
            for i in range(num3, num4+1):
                a, b = self.a1[i], other.a1[i]
                (a, b) = (a, b) if a < b else (b, a)
                child.a1[i] = randint(a, b)
        if num1 <= 3 and num2 >= 3:
            num3, num4 = randrange(switch_num), randrange(switch_num)
            (num3, num4) = (num3, num4) if num3 < num4 else (num4, num3)
            for i in range(num3, num4+1):
                a, b = self.a2[i], other.a2[i]
                (a, b) = (a, b) if a < b else (b, a)
                child.a2[i] = randint(a, b)
        if num1 <= 4 and num2 >= 4:
            num3, num4 = randrange(switch_num), randrange(switch_num)
            (num3, num4) = (num3, num4) if num3 < num4 else (num4, num3)
            for i in range(num3, num4+1):
                a, b = self.b[i], other.b[i]
                (a, b) = (a, b) if a < b else (b, a)
                child.b[i] = randint(a, b)
        if num1 <= 5 and num2 >= 5:
            num3, num4 = randrange(switch_num), randrange(switch_num)
            (num3, num4) = (num3, num4) if num3 < num4 else (num4, num3)
            for i in range(num3, num4+1):
                a, b = self.x[i], other.x[i]
                (a, b) = (a, b) if a < b else (b, a)
                child.x[i] = randint(a, b)
        if num1 <= 6 and num2 >= 6:
            num3, num4 = randrange(switch_num), randrange(switch_num)
            (num3, num4) = (num3, num4) if num3 < num4 else (num4, num3)
            for i in range(num3, num4+1):
                a, b = self.o[i], other.o[i]
                (a, b) = (a, b) if a < b else (b, a)
                child.o[i] = randint(a, b)

        return child

    def mutate(self):
        """
        変異(摂動)
        """
        parameter_index = randrange(7)
        switch_num = len(self.setting['turns'])
        stage_index = randrange(switch_num)
        sign = 1 if random() > 0.5 else -1
        mutation_value = self.setting['mutation_value']

        if parameter_index == 0:
            self.corner[stage_index] += mutation_value * sign
        elif parameter_index == 1:
            self.c[stage_index] += mutation_value * sign
        elif parameter_index == 2:
            self.a1[stage_index] += mutation_value * sign
        elif parameter_index == 3:
            self.a2[stage_index] += mutation_value * sign
        elif parameter_index == 4:
            self.b[stage_index] += mutation_value * sign
        elif parameter_index == 5:
            self.o[stage_index] += mutation_value * sign
        elif parameter_index == 6:
            self.x[stage_index] += mutation_value * sign

    def large_mutate(self):
        """
        大変異(摂動)
        """
        parameter_index = randrange(7)
        switch_num = len(self.setting['turns'])
        stage_index = randrange(switch_num)
        sign = 1 if random() > 0.5 else -1
        large_mutation_value = self.setting['large_mutation_value']

        if parameter_index == 0:
            self.corner[stage_index] += large_mutation_value * sign
        elif parameter_index == 1:
            self.c[stage_index] += large_mutation_value * sign
        elif parameter_index == 2:
            self.a1[stage_index] += large_mutation_value * sign
        elif parameter_index == 3:
            self.a2[stage_index] += large_mutation_value * sign
        elif parameter_index == 4:
            self.b[stage_index] += large_mutation_value * sign
        elif parameter_index == 5:
            self.o[stage_index] += large_mutation_value * sign
        elif parameter_index == 6:
            self.x[stage_index] += large_mutation_value * sign

    def __str__(self):
        return f"corner: {self.corner}\nc: {self.c}\na1: {self.a1}\na2: {self.a2}\nb: {self.b}\no: {self.o}\nx: {self.x}\nFitness: {self.fitness()}"

    @classmethod
    def load_population(cls, json_file):
        """
        母集団の取得
        """
        generation, population = 0, {}

        if json_file is not None and os.path.isfile(json_file):
            with open(json_file) as f:
                json_setting = json.load(f)

                generation = json_setting["generation"]
                corner = json_setting["corner"]
                c = json_setting["c"]
                a1 = json_setting["a1"]
                a2 = json_setting["a2"]
                b = json_setting["b"]
                o = json_setting["o"]
                x = json_setting["x"]

                population = [Switch_T(corner[i], c[i], a1[i], a2[i], b[i], x[i], o[i]) for i in range(len(corner))]

        return generation, population

    @classmethod
    def save_population(cls, ga, json_file):
        """
        母集団の保存
        """
        generation = ga._generation
        population = ga._population

        parameters = {
            "generation": generation,
            "corner": [individual.corner for individual in population],
            "c": [individual.c for individual in population],
            "a1": [individual.a1 for individual in population],
            "a2": [individual.a2 for individual in population],
            "b": [individual.b for individual in population],
            "o": [individual.o for individual in population],
            "x": [individual.x for individual in population],
            "fitness": [individual.fitness() for individual in population],
        }

        with open(json_file, 'w') as f:
            json.dump(parameters, f)


if __name__ == '__main__':
    import timeit

    ga = GeneticAlgorithm('./ga_setting.json', Switch_T)
    elapsed_time = timeit.timeit('ga.run()', globals=globals(), number=1)

    print('>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(ga.best)
    print(elapsed_time, '(s)')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>')
