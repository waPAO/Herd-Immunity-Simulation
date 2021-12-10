from datetime import datetime

class Logger(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num):
        f = open(self.file_name, 'w')

        metadata = ''

        date_time = datetime.now()
        header = f'Herd Immunity Simulation: {virus_name}\n'
        data = f'Starting Population: {pop_size} | Vaccinated Percentage: {vacc_percentage} | Virus: {virus_name} | Mortality Rate: {mortality_rate} | Reproduction Rate: {basic_repro_num}\n\n'

        metadata += (date_time.strftime("%c") + '\n')
        metadata += header
        metadata += data

        f.write(metadata)
        f.close()

    def log_results(self, step_number, number_of_new_infections, vaccinated, dead):
        f = open(self.file_name, 'a')
        results = f'Step: {step_number}\n New Infections: {number_of_new_infections} | Total Vaccinated: {vaccinated} | Total Dead: {dead}\n'
        f.write(results)
        f.close()

    def log_end(self, population_count, pop_dead, pop_alive):
        f = open(self.file_name, 'a')
        result = f'\n*Simulation Has Ended*\n Results:\n Starting Population: {population_count} | Amount Dead: {pop_dead} | Amount Vaccinated : {pop_alive}\n'
        f.write(result)
        f.close()