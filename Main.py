import matplotlib.pyplot as plt
import json
from Node import Node
from Helpers import *

filename = input("Enter file name: ")

filepath = f"input/{filename}"

with open(filepath, 'r') as f:
    data = f.read()

print(data)

parsed_data = eval("[" + data + "]")
nodes = [Node(x, y, e) for x, y, e in parsed_data]
print(nodes)

log = []
plt.ion()
fig, ax = plt.subplots(figsize=(7, 7))

leaders = select_leaders(nodes)

for t in range(5000):
    nodes = alive(nodes)
    if not nodes:
        print("SYSTEM DEAD")
        break
    
    leaders = remove_dead_leaders(leaders)
    groups = form_groups(nodes, leaders)

    baseline_energy(nodes)
    events = decide_transmissions(nodes, groups, leaders)

    leaders = replace_leaders(leaders, nodes)

    log.append({
        "time": t,
        "leaders": [(l.x_coord, l.y_coord, l.energy) for l in leaders],
        "groups": {str(k): v for k, v in groups.items()},
        "events": events,
        "nodes": [(n.x_coord, n.y_coord, n.energy) for n in nodes]
    })

    ax.clear()

    for l in leaders:
        ax.scatter(l.x_coord, l.y_coord,
                   c="red", s=200, marker="*")

    for leader, members in groups.items():
        for m in members:
            ax.scatter(m.x_coord, m.y_coord, c="blue")
            ax.plot([leader.x_coord, m.x_coord],
                    [leader.y_coord, m.y_coord],
                    c="gray", linewidth=0.7)

    ax.set_title(f"Time Step {t}")
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 60)
    ax.grid(True)

    fig.canvas.draw()
    fig.canvas.flush_events()

    plt.pause(0.01)

plt.ioff()
plt.show()

with open(f"output/simulation_log_{filename}.json", "w") as f:
    json.dump(log, f, indent=4, default=str)

