import random
from dataclasses import dataclass
from functools import reduce

data = """1,Кузнецова,,0.2
2,Кузнецова,,0
3,Дежурный,,0
4,Шугурова,,0.2
5,Текутьева,,0.25
6,Вокрячко,,0
7,Борисов,,1
8,Токарев,,1
9,Обухов,,0.25
10,Мурашов,,0
11,Губин,,0.25
12,Киселева,,1
13,Трушина,,0.25
14,Кузнецов,,0.1
15,Кузнецов охрана,,0
16,Шугуров,,0.1
17,,,0
18,Лейчинский,,0.25
19,Ватаман,,1
20,Рязанцев,,1
21,Черников,,0.5
22,Мезин,,0.5
23,Некрасов,,0.5
24,Бойченко,,1
25,Кудаев,,1
26,Кобяков,,1
27,Агапов,,1
28,Чирков,,1
29,Романов,,1
30,Чернышов,,0
31,Киселев,,1
32,Бузоверов,,0
33,Горлова,,1
34,Сысоева,,1
"""


@dataclass
class User:
    id: int
    name: str
    point: float = 1


class ReadSource:
    def __init__(self, source=""):
        self.source = source
        self.users: list[User] = []

    def parse(self):
        list_of_strings = self.source.split()
        for lof in list_of_strings:
            value_of_record = lof.split(',')
            if len(value_of_record) < 4 or len(value_of_record[0]) == 0 or value_of_record[3] == '0':
                continue
            try:
                self.users.append(
                    User(id=int(value_of_record[0]), name=value_of_record[1], point=float(value_of_record[3])))
            except ValueError:
                continue


class Distribution:
    def __init__(self, quantity_teams, users: list[User]):
        self.quantity_teams = quantity_teams
        self.users = users
        self.teams = []
        self.capitains: list[User] = []

    def distributution_by_teams(self):
        for i in range(0, 10):
            random.shuffle(self.users)

        add_value = len(self.users) // self.quantity_teams
        index = 0

        for t in range(0, self.quantity_teams):
            self.teams.append(self.users[index:index + add_value])
            index += add_value
        i = 0
        for t in self.users[index:len(self.users)]:
            self.teams[i].append(t)
            i += 1

    def vote_of_captitains(self):
        for t in self.teams:
            self.capitain_of_teams(t)

    def capitain_of_teams(self, team: list[User]):
        sum_point = reduce(lambda s, x: s + x, [p.point for p in team])

        point_index = round(random.random() * sum_point, 2)
        current_sum_point = 0
        for t in team:
            current_sum_point += t.point
            if point_index <= current_sum_point:
                self.capitains.append(t)
                break


if __name__ == '__main__':
    rs = ReadSource(source=data)
    rs.parse()
    d = Distribution(quantity_teams=5, users=rs.users)
    d.distributution_by_teams()
    d.vote_of_captitains()
    teams = iter(d.teams)

    for c in d.capitains:
        index=1
        print(f'{index} {c.name}')
        #participants = "\n".join([i.name for i in next(teams) if i.id!=c.id])
        #print(f"Участники: {participants}")
        participants = [i.name for i in next(teams) if i.id!=c.id]

        for p in participants:
            index+=1
            print(f"{index} {p}")
        print()
