def read_tour(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    n = int(lines[0])
    tour_data = [line.strip().split(',') for line in lines[1:]]
    
    # Convert year and distance to integers
    tour_data = [[name, int(year), x, int(distance)] for name, year, x, distance in tour_data]

    return n, tour_data

# find every possible detour 
def find_detours(n, places):
    possible_detours = []
    for i, current_place in enumerate(places):
        for j in range(i + 1, n):
            other_place = places[j]

            # compare every place coming after the current one until the place name is same
            if other_place[0] == current_place[0]:
                # add the possible detour to an array and save the start, end and possible saved distance
                possible_detours.append([i, j, other_place[3] - current_place[3]])

                # if the end of the detour is an essential place then stop searching for more detours
                if other_place[2] == "X":
                    break

            # if there is an essential place coming up before a possible detour, then break
            elif other_place[2] == "X":
                break

    return possible_detours

# filter out detours with overlapping time periods to get the largest saved distance
def filter_detours(possible_detours):
    filtered_detours = []

    # sort from biggest saved distance to lowest
    sorted_detours = sorted(possible_detours, key=lambda x: x[2], reverse=True)

    visited_places = set()
    for detour in sorted_detours:
        # check if there is no overlap with previously visited places
        # (respectively places that will be skipped due to detour getting removed)
        # because we first sorted the detours with largest saved distance, we can
        # be sure that the most efficient detours get removed and the rest is left on route
        # because the places are (possibly) overlapping
        if all(p not in visited_places for p in range(detour[0], detour[1])):
            visited_places.update(range(detour[0], detour[1]))
            filtered_detours.append(detour)
    
    return filtered_detours

# remove the given detours from the route to create the most efficient one
def create_efficient_route(detours, places):
    indices_to_remove = set()
    saved_distances = {}

    # fill the set with places that will get skipped due to detour
    for detour in detours:
        start_index, end_index, saved_distance = detour
        indices_to_remove.update(range(start_index + 1, end_index))
        saved_distances[end_index] = saved_distance

    # update the distances by subtracting saved distances from the places in the final route
    for detour_end, saved_distance in saved_distances.items():
        for i in range(detour_end, len(places)):
            if i not in indices_to_remove:
                places[i][3] = places[i][3] - saved_distance

    # create a new list with the original places, not including those in a detour
    route = [list(place) for i, place in enumerate(places) if i not in indices_to_remove]

    return route, sum(saved_distances.values())

# output the final tour to a file
def write_tour(file_path, n, tour_data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(n) + '\n')
            for data in tour_data:
                line = ','.join(map(str, data))
                file.write(line + '\n')
        return "Success: Most efficient tour has been written to {}".format(file_path)
    except Exception as e:
        return f"Error: {str(e)}"

n, tour = read_tour("tour3_mod.txt")

possible_detours = find_detours(n, tour)  
to_be_removed_detours = filter_detours(possible_detours)
final_route, saved_distance = create_efficient_route(to_be_removed_detours, tour)

result = write_tour("output.txt", len(final_route), final_route)

print(result)
print("Total saved distance:", saved_distance)