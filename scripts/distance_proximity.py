import openrouteservice
from geopy import distance


def proximity(subject_lat, subject_long, compare_lat, compare_long):
    distances = []
    for i in range(len(compare_lat)):  
        distances.append(
            distance.distance(
                (subject_lat, subject_long), (compare_lat[i], compare_long[i])
            ).km
        )

    sorted_distances = sorted(distances, reverse=False)
    min_index_1 = distances.index(sorted_distances[0])
    min_index_2 = distances.index(sorted_distances[1])

    return min_index_1, min_index_2


def travel_time(subject_lat, subject_long, compare_lat, compare_long, api_key):

    client = openrouteservice.Client(key=api_key)  # Specify your personal API key
    routes = client.directions(
        ((subject_lat, subject_long), (compare_lat, compare_long))
    )

    distance = routes["routes"][0]["summary"]["distance"]
    duration = routes["routes"][0]["summary"]["duration"]

    return distance, duration
