import random, sys
from person import Person
from logger import Logger
from virus import Virus
random.seed(42)

class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        self.file_name = f'{virus.name}__PopSize_{pop_size}__Vac%_{vacc_percentage}__Infected_{initial_infected}.txt'
        self.logger = Logger(self.file_name)
        self.virus = virus
        self.pop_size = pop_size
        self.current_pop = pop_size
        self.vacc_percentage = vacc_percentage
        self.inital_infected = initial_infected
        self.population = []
        self.newly_infected = []
        self._create_population()
        self.vaccinated = 0
        self.dead = 0
        self.interactions = 0
        self.new_infections = 0

    def _create_population(self):
        total_size = self.pop_size
        infected_ppl = self.inital_infected
        vaccinated_ppl = round(self.vacc_percentage * (total_size - infected_ppl))
        self.vaccinated = vaccinated_ppl

        for i in range(1, total_size + 1):
            if vaccinated_ppl > 0:
                person = Person(i, True)
                self.population.append(person)
                vaccinated_ppl -= 1
            elif infected_ppl > 0:
                person = Person(i, False, self.virus)
                self.population.append(person)
                infected_ppl -= 1
            else:
                person = Person(i, False)
                self.population.append(person)
        
        return self.population

    def _simulation_should_continue(self):
        if self.dead == self.pop_size:
            self.logger.log_end(self.pop_size, self.dead, self.vaccinated)
            return False
        elif (self.dead + self.vaccinated) == self.current_pop:
            self.vaccinated += self.pop_size - (self.dead + self.vaccinated)
            self.logger.log_end(self.pop_size, self.dead, self.vaccinated)
            return False
        else:
            return True

    def run(self):
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)
        time_step_counter = 0
        should_continue = True

        while should_continue:
            time_step_counter += 1
            self.time_step()
            self.logger.log_results(time_step_counter, self.new_infections, self.vaccinated, self.dead)
            should_continue = self._simulation_should_continue()
            self.new_infections = 0
            self.interactions = 0
        

    def time_step(self):
        for person in self.population:
            if person.infection != None:
                for i in range(100):
                    random_index = random.randint(0, self.current_pop - 1)
                    random_person = self.population[random_index]
                    self.interaction(person, random_person)
                self.check_if_dead()
                    

    def interaction(self, infected_person, random_person):
        if random_person.is_vaccinated:
            pass
        elif random_person.infection != None:
            pass
        else:
            survival_rate = random.uniform(0.0, 1.0)
            if survival_rate < infected_person.infection.repro_rate:
                random_person.infection = infected_person.infection
                self.newly_infected.append(random_person)
                self.new_infections += 1



    def check_if_dead(self):
        for person in self.newly_infected:
            if person.did_survive_infection():
                self.vaccinated += 1
                person.is_vaccinated = True
                person.infection = None
            else:
                self.dead += 1
                self.population.remove(person)
                self.current_pop -= 1
        self.newly_infected = []
        

if __name__ == "__main__":
    parameters = sys.argv[1:]

    population_size = int(parameters[0])
    percent_vaccinated = float(parameters[1])
    virus_name = str(parameters[2])
    mortality_rate = float(parameters[3])
    repro_rate = float(parameters[4])
    initally_infected = int(parameters[5])

    virus = Virus(virus_name, repro_rate, mortality_rate)
    sim = Simulation(virus, population_size, percent_vaccinated, initally_infected)
    sim.run()