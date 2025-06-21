import heapq

def dijkstra(graph, start, end):
    start = start.strip()
    end = end.strip()

    if not graph:
        raise ValueError("Graph is empty!")

    if start not in graph or end not in graph:
        raise ValueError(f"Invalid nodes: {start}, {end}")

    pq = [(0, start)]
    distances = {start: 0}
    previous_nodes = {start: None}
    visited = set()

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end:
            path = []
            while previous_nodes[current_node] is not None:
                path.append(current_node)
                current_node = previous_nodes[current_node]
            path.append(start)
            path.reverse()
            return distances[end], path

        for neighbor, weight in graph.get(current_node, []):
            if neighbor in visited:
                continue

            new_distance = current_distance + weight
            if neighbor not in distances or new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))

    return float('inf'), []

def k_shortest_paths(graph, start, end, k):
    start = start.strip()
    end = end.strip()

    first_cost, first_path = dijkstra(graph, start, end)
    if not first_path:
        return []

    paths = [(first_cost, first_path)]
    candidates = []

    for _ in range(1, k):
        for i in range(len(paths[-1][1]) - 1):
            spur_node = paths[-1][1][i]
            root_path = paths[-1][1][:i + 1]
            removed_edges = []
            # Remove edges that create previous paths
            for path in paths:
                if path[1][:i + 1] == root_path and i + 1 < len(path[1]):
                    u = path[1][i]
                    v = path[1][i + 1]
                    for idx, (neighbor, weight) in enumerate(graph.get(u, [])):
                        if neighbor == v:
                            removed_edges.append((u, (neighbor, weight)))
                            del graph[u][idx]
                            break

            spur_cost, spur_path = dijkstra(graph, spur_node, end)
            # Restore removed edges
            for u, edge in removed_edges:
                graph[u].append(edge)

            if spur_path:
                total_path = root_path[:-1] + spur_path
                total_cost = 0
                for n1, n2 in zip(total_path, total_path[1:]):
                    for neighbor, weight in graph.get(n1, []):
                        if neighbor == n2:
                            total_cost += weight
                            break

                candidate = (total_cost, total_path)
                if candidate not in candidates:
                    heapq.heappush(candidates, candidate)

        if candidates:
            paths.append(heapq.heappop(candidates))
        else:
            break

    return paths
