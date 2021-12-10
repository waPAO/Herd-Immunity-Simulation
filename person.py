import random
from virus import Virus


class Person(object):
    def __init__(self, _id, is_vaccinated, infection = None):
        self._id = _id 
        self.is_alive = True
        self.is_vaccinated = is_vaccinated
        self.infection = infection

    def did_survive_infection(self):
        num = random.uniform(0.0, 1.0)
        if self.infection != None:
            if num < self.infection.mortality_rate:
                self.is_alive = False
                return False
            else:
                self.is_vaccinated = True
                return True


if __name__ == "__main__":
    vaccinated_person = Person(1, True)
    assert vaccinated_person._id == 1
    assert vaccinated_person.is_alive is True
    assert vaccinated_person.is_vaccinated is True
    assert vaccinated_person.infection is None

    unvaccinated_person = Person(2, False)
    assert unvaccinated_person._id == 2
    assert unvaccinated_person.is_alive is True
    assert unvaccinated_person.is_vaccinated is False
    assert unvaccinated_person.infection is None

    virus = Virus("Dysentery", 0.7, 0.2)

    infected_person = Person(3, False, virus)
    assert infected_person._id == 3
    assert infected_person.is_alive is True
    assert infected_person.is_vaccinated is False
    assert infected_person.infection is virus

    people = []
    for i in range(1, 101):
        # TODO Make a person with an infection
        infected = Person(i, False, virus)
        people.append(infected)


    survived = 0
    dead = 0

    for person in people:
        survive = person.did_survive_infection()
        if survive:
            survived += 1
        else:
            dead += 1

    print(f'{survived/100}')
    print(f'{dead/100}')

   