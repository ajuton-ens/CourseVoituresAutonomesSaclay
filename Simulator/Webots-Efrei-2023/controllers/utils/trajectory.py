import json



def load_trajectory(path_to_json):
    with open(path_to_json, 'r') as f:
        trajectory = json.loads(f.read())
    return trajectory




