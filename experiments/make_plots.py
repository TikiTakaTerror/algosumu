import csv
import os
import matplotlib.pyplot as plt

os.makedirs("plots", exist_ok=True)


def read_data(file_name, column):
    x = []
    y = []
    with open("results/" + file_name) as file:
        for row in csv.reader(file):
            x.append(int(row[1]))
            y.append(float(row[column]))
    return x, y


def plot_ops(ax, name):
    x, y = read_data(name + "_naive.csv", 3)
    ax.plot(x, y, "o-", label="Naive", markersize=10,
            markerfacecolor="none", markeredgewidth=1.5, linewidth=2)

    x, y = read_data(name + "_topdown.csv", 3)
    ax.plot(x, y, "s--", label="Top-down", markersize=6, linewidth=2)

    x, y = read_data(name + "_bottomup.csv", 3)
    ax.plot(x, y, "^:", label="Bottom-up", markersize=7, linewidth=2)

    ax.set_xlabel("Input length n")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.25)

# balanced parentheses
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
plot_ops(ax[0], "01_parentheses_repeated")
plot_ops(ax[1], "01_parentheses_nested")
ax[0].set_title("Repeated: ()()()...")
ax[1].set_title("Nested: ((...))")
ax[0].set_ylabel("Operation count")
ax[1].legend()
plt.tight_layout()
plt.savefig("plots/01_parentheses_comparison.png", dpi=300)
plt.close()

# position of a
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
plot_ops(ax[0], "02_start_a")
plot_ops(ax[1], "02_end_a")
ax[0].set_title("a b...b   (e.g. abbbb)")
ax[1].set_title("b...b a   (e.g. bbbba)")
ax[0].set_ylabel("Operation count")
ax[1].legend()
plt.tight_layout()
plt.savefig("plots/02_symbol_order_comparison.png", dpi=300)
plt.close()

# runtime
fig, ax = plt.subplots(figsize=(7, 4.5))
x, y = read_data("03_runtime_scaling_topdown.csv", 4)
ax.plot(x, y, "s--", label="Top-down", color="tab:orange",
                                 markersize=6, linewidth=2)

x, y = read_data("03_runtime_scaling_bottomup.csv", 4)
ax.plot(x, y, "^:", label="Bottom-up", color="tab:green",
                                 markersize=7, linewidth=2)

ax.set_title("Measured runtime")
ax.set_xlabel("Input length n")
ax.set_ylabel("Time (seconds)")
ax.grid(True, alpha=0.25)
ax.legend()
plt.tight_layout()
plt.savefig("plots/03_runtime_scaling.png", dpi=300)
plt.close()

print("Plots created.")
