import matplotlib.pyplot as plt
import json


def load_times(filename):
    with open(filename) as f:
        data = json.load(f)
    sizes = data["sizes"]
    times = data["times"]
    params = data.get("params", {})
    return sizes, times, params


def create_plot(filename, sizes, times, params=None):
    plt.figure(figsize=(8, 6))
    plt.plot(
        sizes,
        times,
        linestyle="-",
        color="tab:blue",
        label="Average response time",
    )
    plt.yscale("log")

    plt.xlabel("Datagram size [B]", fontsize=12)
    plt.ylabel("Response time [s] (log scale)", fontsize=12)
    plt.title("UDP Response Time vs Datagram Size", fontsize=14)

    plt.grid(True, which="both", ls="--", lw=0.5)

    if params:
        param_text = "\n".join(f"{k}: {v}" for k, v in params.items())
        plt.gca().text(
            1.02,
            0.5,
            param_text,
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment="center",
        )

    plt.tight_layout()
    plt.savefig(filename, dpi=300)


if __name__ == "__main__":
    datafile = "z36_dgram_times_add100_100.json"
    plotfile = "z36_dgram_times_add100_100.png"
    sizes, times, params = load_times(datafile)
    create_plot(plotfile, sizes, times, params)
