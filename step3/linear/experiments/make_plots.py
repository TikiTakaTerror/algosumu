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
    x, y = read_data(name + "_method1.csv", 3)
    ax.plot(x, y, "o-", label="Method 1")

    x, y = read_data(name + "_method2.csv", 3)
    ax.plot(x, y, "s--", label="Method 2")

    ax.set_xlabel("Input length n")
    ax.grid(True)


# Small valid and invalid inputs.
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)

plot_ops(ax[0], "01_valid_small")
plot_ops(ax[1], "01_invalid_small")

ax[0].set_title("Valid inputs")
ax[1].set_title("Invalid inputs")
ax[0].set_ylabel("Operation count")
ax[1].legend()

plt.tight_layout()
plt.savefig("plots/01_structure_comparison.png", dpi=300)
plt.close()


# Operation-count scaling.
fig, ax = plt.subplots(figsize=(7, 4.5))

x, y = read_data("02_runtime_scaling_method1.csv", 3)
ax.plot(x, y, "o-", label="Method 1")

x, y = read_data("02_runtime_scaling_method2.csv", 3)
ax.plot(x, y, "s--", label="Method 2")

ax.set_title("Operation count growth")
ax.set_xlabel("Input length n")
ax.set_ylabel("Operation count")
ax.grid(True)
ax.legend()

plt.tight_layout()
plt.savefig("plots/02_operation_scaling.png", dpi=300)
plt.close()


# Runtime scaling.
fig, ax = plt.subplots(figsize=(7, 4.5))

x, y = read_data("02_runtime_scaling_method1.csv", 4)
ax.plot(x, y, "o-", label="Method 1")

x, y = read_data("02_runtime_scaling_method2.csv", 4)
ax.plot(x, y, "s--", label="Method 2")

ax.set_title("Measured runtime")
ax.set_xlabel("Input length n")
ax.set_ylabel("Time (seconds)")
ax.grid(True)
ax.legend()

plt.tight_layout()
plt.savefig("plots/03_runtime_scaling.png", dpi=300)
plt.close()


def read_grammar_data(file_name, column):
    x = []
    y = []

    with open("results/" + file_name) as file:
        for row in csv.reader(file):
            x.append(int(row[0]))
            y.append(float(row[column]))

    return x, y


# Grammar-size scaling.
fig, ax = plt.subplots(figsize=(7, 4.5))

x, y = read_grammar_data("03_grammar_size_method1.csv", 4)
ax.plot(x, y, "o-", label="Method 1")

x, y = read_grammar_data("03_grammar_size_method2.csv", 4)
ax.plot(x, y, "s--", label="Method 2")

ax.set_title("Grammar size and operation count")
ax.set_xlabel("Number of nonterminals")
ax.set_ylabel("Operation count")
ax.grid(True)
ax.legend()

plt.tight_layout()
plt.savefig("plots/04_grammar_size.png", dpi=300)
plt.close()


print("Plots created.")
