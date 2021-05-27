import matplotlib.pyplot as plt

def plot_tensor(t, xx, yy, zz, xy, xz, yz, label="", color="", alpha=1.0, xlim=None):
        plt.subplot(231)
        plt.plot(t, xx, color, alpha=alpha, label=label)
        plt.xlim(xlim)
        plt.title(f"xx")
        plt.subplot(232)
        plt.plot(t, yy, color, alpha=alpha, label=label)
        plt.xlim(xlim)
        plt.title(f"yy")
        plt.subplot(233)
        plt.plot(t, zz, color, alpha=alpha, label=label)
        plt.xlim(xlim)
        plt.title(f"zz")
    
        plt.subplot(234)
        plt.plot(t, xy, color, alpha=alpha, label=label)
        plt.xlim(xlim)
        plt.title(f"xy")
        plt.subplot(235)
        plt.plot(t, xz, color, alpha=alpha, label=label)
        plt.xlim(xlim)
        plt.title(f"xz")
        plt.subplot(236)
        plt.plot(t, yz, color, alpha=alpha, label=label)
        plt.xlim(xlim)
        plt.title(f"yz")

