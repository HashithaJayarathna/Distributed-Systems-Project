import math
import random

def distance(a, b):
    ### Get the Euclidean distance between the two nodes ###
    return math.sqrt((a.x_coord - b.x_coord)**2 + (a.y_coord - b.y_coord)**2)

def alive(nodes):
    ### Check whether the node is alive or not ###
    return [n for n in nodes if n.energy > 0]

def remove_dead(nodes):
    return [n for n in nodes if n.energy > 0]

def select_leaders(nodes, k=5):
    sorted_nodes = sorted(nodes, key=lambda n: n.energy, reverse=True)

    leaders = []
    for n in sorted_nodes:
        if all(distance(n, l) > 20 for l in leaders):
            leaders.append(n)
        if len(leaders) == k:
            break

    return leaders

def form_groups(nodes, leaders):

    alive_nodes = [n for n in nodes if n.energy > 0]
    alive_leaders = [l for l in leaders if l.energy > 0]

    groups = {l: [] for l in alive_leaders}

    for n in alive_nodes:

        # skip if node is a leader
        if n in alive_leaders:
            continue

        best_leader = None
        best_distance = float("inf")

        for l in alive_leaders:

            d = distance(n, l)

            if d <= 20 and d < best_distance:
                best_distance = d
                best_leader = l

        if best_leader:
            groups[best_leader].append(n)

    return groups

def baseline_energy(nodes):
    for n in nodes:
        n.energy -= 1

def replace_leaders(leaders, nodes):

    new_leaders = leaders.copy()

    for i, leader in enumerate(new_leaders):

        if leader.energy <= 0:

            candidates = [
                n for n in nodes
                if n.energy > 0 and n not in new_leaders
            ]

            best_candidate = None
            best_energy = -1

            for c in candidates:

                if all(distance(c, l) > 20 for l in new_leaders if l != leader):

                    if c.energy > best_energy:
                        best_candidate = c
                        best_energy = c.energy

            if best_candidate:
                new_leaders[i] = best_candidate

    return new_leaders

def decide_transmissions(nodes, groups, leaders):
    events = []

    for leader, members in groups.items():
        for m in members:

            if random.random() < 0.7:

                m.energy -= 2
                events.append(f"{m} sent message to {leader}")

                leader.energy -= 2
                events.append(f"{leader} responded to {m}")

    return events

def remove_dead_leaders(leaders):
    new_leaders = [l for l in leaders if l.energy > 0]
    return new_leaders
