from random import uniform, seed, random

import winsound

print('Euclidean ART 10D f-rate 0.001')
simulations = 3000
failure_rate = 0.001
dimension = 10
seed(random())
input_min = 0.0
input_max = 1.0
avg_f_measure = 0
total_f_measure = 0
f_ratio = 0
total_number_of_candidates = 10
results = []

failure_region_area = input_max * failure_rate
failure_region_length = failure_region_area ** (1 / dimension)
# Generate Failure point
upper_bound = input_max - failure_region_length
failure_point = tuple(uniform(input_min, upper_bound) for d in range(dimension))


def test_program(fp, tc, l):
    failure = None
    for i in range(len(fp)):
        if fp[i] <= tc[i] <= fp[i] + l:
            failure = True
        else:
            failure = False
            break
    return failure


def select_the_best_test_data(selectedSet, candidateSet, totalNumberOfCandidates, dimensionsArg, inputMin,
                              inputMax):
    best_distance = -1.0
    best_data = None
    # Generate unique random candidates
    for i in range(totalNumberOfCandidates):
        candidate = tuple(uniform(inputMin, inputMax) for j in range(dimensionsArg))
        candidateSet.append(candidate)
        min_candidate_distance = 9223372036854775807
        for x in range(len(selectedSet)):
            # distance = math.sqrt(sum(pow(a - b, 2) for a, b in zip(selected_set[x], candidate)))
            distance = (sum(pow(a - b, 2) for a, b in zip(selected_set[x], candidate))) ** (0.5)
            # find minimum distance MIN
            if distance < min_candidate_distance:
                min_candidate_distance = distance
        # find maximum distance from all minimum distances MAX
        if best_distance < min_candidate_distance:
            best_data = candidate
            best_distance = min_candidate_distance
    return best_data

for x in range(simulations):
    initial_test_data = tuple(uniform(input_min, input_max) for d in range(dimension))
    selected_set = [initial_test_data]
    counter = 1
    # use initial data to test the program
    reveal_failure = test_program(failure_point, initial_test_data, failure_region_length)
    while not reveal_failure:
        candidate_set = []
        test_data = select_the_best_test_data(selected_set, candidate_set,
                                              total_number_of_candidates,
                                              dimension, input_min, input_max)
        # use test_data to test the program
        reveal_failure = test_program(failure_point, test_data, failure_region_length)
        selected_set.append(test_data)
        counter = counter + 1
    print(counter)
    total_f_measure = total_f_measure + counter

avg_f_measure = total_f_measure / simulations
f_ratio = avg_f_measure * failure_rate
result = {'simulations': simulations, 'dimension': dimension, 'failure_rate': failure_rate,
          'avg_f_measure': avg_f_measure, 'f_ratio': f_ratio}
results.append(result)
print("\n")
print(result)
winsound.MessageBeep(winsound.MB_OK)
