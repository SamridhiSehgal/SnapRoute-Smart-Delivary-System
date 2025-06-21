import csv

def get_graph():
    graph = {}
    coordinates = {}
    try:
        with open('data.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                node = row[0].strip()
                lat = float(row[1].strip())
                lng = float(row[2].strip())
                coordinates[node] = (lat, lng)

                graph[node] = []
                # neighbors start at index 3 (pairs neighbor + weight)
                for i in range(3, len(row), 2):
                    if i + 1 < len(row):
                        neighbor = row[i].strip()
                        try:
                            weight = int(row[i + 1])
                            graph[node].append((neighbor, weight))
                        except ValueError:
                            continue
    except FileNotFoundError:
        raise ValueError("CSV file not found.")
    return graph, coordinates
