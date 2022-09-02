import openrouteservice


def proximity(start, end, api_key):

    client = openrouteservice.Client(key=api_key)  # Specify your personal API key
    routes = client.directions((start, end))

    distance = routes["routes"][0]["summary"]["distance"]
    duration = routes["routes"][0]["summary"]["duration"]

    return distance, duration
