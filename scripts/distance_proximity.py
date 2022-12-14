import openrouteservice
from geopy import distance


def proximity(subject_lat, subject_long, compare_lat, compare_long, top_only=None):
    """Calculate geographical distance between a subject and target locations"""
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
    if top_only:
        return min_index_1
    else:
        return min_index_1, min_index_2


def travel_time(subject_lat, subject_long, compare_lat, compare_long, api_key):
    """Makes ORS API call to calculate travel time"""
    client = openrouteservice.Client(
        key=api_key)  # Specify your personal API key
    routes = client.directions(
        ((subject_lat, subject_long), (compare_lat, compare_long))
    )

    distance = routes["routes"][0]["summary"]["distance"]
    duration = routes["routes"][0]["summary"]["duration"]

    return distance, duration
