import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

def plot_map(df, column, title, cmap="Reds"):
    fig, ax = plt.subplots(figsize=(12, 12))
    df.plot(column=column, cmap=cmap, linewidth=0.6, edgecolor="#333", legend=True, ax=ax)
    ax.set_title(title, fontsize=16, fontweight="bold", pad=20)
    ax.set_axis_off()
    return fig
