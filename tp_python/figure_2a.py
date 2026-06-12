"""Reproduction de la Figure 2A de Kelliher et al. 2016 (PLOS Genetics).

La figure est une heatmap des genes periodiques de *Saccharomyces cerevisiae*
au cours du cycle cellulaire. Chaque ligne represente un gene, chaque colonne
un point temporel. Les niveaux d'expression sont normalises en z-score (nombre
d'ecarts-types par rapport a la moyenne du gene), et les genes sont ordonnes par
phase (temps du pic d'expression), ce qui fait apparaitre les vagues diagonales
de transcription successives au cours du cycle cellulaire.

Reference
---------
Kelliher CM, Leman AR, Sierra CS, Haase SB (2016) Investigating Conservation of
the Cell-Cycle-Regulated Transcriptional Program in the Fungal Pathogen,
Cryptococcus neoformans. PLOS Genetics 12(12): e1006453.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

# --- Parametres par defaut (article : echantillonnage toutes les 5 min) ---
DEFAULT_DATA_PATH = Path("../data/oscillating-genes_1705_normalized-profiles.tsv")
DEFAULT_OUTPUT_PATH = Path("figure_2a.png")
SAMPLING_MINUTES = 5  # S. cerevisiae : 1 prelevement toutes les 5 minutes
CELL_CYCLE_PERIOD = 75  # minutes (periode du cycle estimee dans l'article)
ZSCORE_CLIP = 1.5  # bornes de la colorbar (High = +1.5, Low = -1.5)


def load_profiles(path: Path) -> pd.DataFrame:
    """Charge la matrice d'expression (genes en lignes, temps en colonnes).

    Parameters
    ----------
    path : Path
        Chemin du fichier TSV. La premiere colonne contient les identifiants
        de genes et sert d'index ; les colonnes suivantes sont les echantillons.

    Returns
    -------
    pandas.DataFrame
        Matrice d'expression indexee par gene.

    Raises
    ------
    FileNotFoundError
        Si le fichier n'existe pas.
    ValueError
        Si le fichier ne contient aucune donnee numerique exploitable.
    """
    if not path.exists():
        raise FileNotFoundError(f"Fichier de donnees introuvable : {path}")
    dataframe = pd.read_csv(path, sep="\t", index_col=0)
    if dataframe.empty:
        raise ValueError(f"Le fichier {path} ne contient aucune donnee.")
    return dataframe


def zscore_per_gene(profiles: pd.DataFrame) -> pd.DataFrame:
    """Normalise chaque gene (ligne) en z-score.

    Parameters
    ----------
    profiles : pandas.DataFrame
        Matrice d'expression (genes en lignes, temps en colonnes).

    Returns
    -------
    pandas.DataFrame
        Matrice z-scoree, de meme forme que l'entree. Les genes constants
        (ecart-type nul) sont mis a zero pour eviter les divisions par zero.
    """
    values = profiles.to_numpy(dtype=float)
    means = values.mean(axis=1, keepdims=True)
    stds = values.std(axis=1, ddof=1, keepdims=True)
    safe_stds = np.where(stds == 0, np.nan, stds)
    with np.errstate(invalid="ignore", divide="ignore"):
        zscores = (values - means) / safe_stds
    result = pd.DataFrame(
        np.nan_to_num(zscores, nan=0.0),
        index=profiles.index,
        columns=profiles.columns,
    )
    return result


def order_by_peak_phase(
    zscores: pd.DataFrame,
    period_min: float = CELL_CYCLE_PERIOD,
    sampling_min: float = SAMPLING_MINUTES,
) -> pd.DataFrame:
    """Ordonne les genes par phase du pic d'expression.

    La phase est extraite de la composante de Fourier a la frequence du cycle
    cellulaire, ce qui donne le moment du pic et reproduit la vague diagonale.

    Parameters
    ----------
    zscores : pandas.DataFrame
        Matrice z-scoree (genes en lignes, temps en colonnes).
    period_min : float, optional
        Periode du cycle cellulaire en minutes.
    sampling_min : float, optional
        Intervalle d'echantillonnage en minutes.

    Returns
    -------
    pandas.DataFrame
        Les memes genes, reordonnes par phase croissante.
    """
    values = zscores.to_numpy()
    n_points = values.shape[1]
    total_time = n_points * sampling_min
    target_cycles = total_time / period_min
    freqs = np.fft.rfftfreq(n_points, d=1.0)  # cycles / point
    target_freq = target_cycles / n_points
    bin_index = int(np.argmin(np.abs(freqs - target_freq)))
    coeffs = np.fft.rfft(values, axis=1)[:, bin_index]
    phase = np.angle(coeffs)
    order = np.argsort(phase)
    return zscores.iloc[order]


def make_colormap() -> LinearSegmentedColormap:
    """Construit la colormap cyan (bas) -> noir (milieu) -> jaune (haut).

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        Colormap reproduisant celle de l'article.
    """
    return LinearSegmentedColormap.from_list(
        "cyan_black_yellow",
        ["#00FFFF", "#000000", "#FFFF00"],
    )


def plot_heatmap(
    zscores: pd.DataFrame,
    output_path: Path,
    sampling_min: float = SAMPLING_MINUTES,
) -> None:
    """Trace et sauvegarde la heatmap facon Figure 2A.

    Parameters
    ----------
    zscores : pandas.DataFrame
        Matrice z-scoree et ordonnee (genes en lignes, temps en colonnes).
    output_path : Path
        Chemin de sauvegarde de l'image (PNG).
    sampling_min : float, optional
        Intervalle d'echantillonnage en minutes (pour l'axe du temps).
    """
    n_genes, n_points = zscores.shape
    max_time = (n_points - 1) * sampling_min

    fig, ax = plt.subplots(figsize=(4, 6))
    image = ax.imshow(
        zscores.to_numpy(),
        aspect="auto",
        cmap=make_colormap(),
        vmin=-ZSCORE_CLIP,
        vmax=ZSCORE_CLIP,
        extent=(0, max_time, n_genes, 0),
        interpolation="nearest",
    )
    ax.set_title("Saccharomyces cerevisiae", fontstyle="italic")
    ax.set_xlabel("time (minutes)")
    ax.set_ylabel(f"Top Periodic Genes ({n_genes})")
    ax.set_yticks([])
    colorbar = fig.colorbar(image, ax=ax, ticks=[-ZSCORE_CLIP, 0, ZSCORE_CLIP])
    colorbar.ax.set_yticklabels(["Low", "0", "High"])
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def build_figure(data_path: Path, output_path: Path) -> None:
    """Execute le pipeline complet de reproduction de la Figure 2A.

    Parameters
    ----------
    data_path : Path
        Chemin du fichier TSV de profils normalises.
    output_path : Path
        Chemin de sauvegarde de la figure.
    """
    profiles = load_profiles(data_path)
    zscores = zscore_per_gene(profiles)
    ordered = order_by_peak_phase(zscores)
    plot_heatmap(ordered, output_path)
    print(
        f"Figure sauvegardee : {output_path} "
        f"({ordered.shape[0]} genes x {ordered.shape[1]} points)"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Analyse les arguments de la ligne de commande.

    Parameters
    ----------
    argv : list of str, optional
        Liste d'arguments (par defaut ``sys.argv``).

    Returns
    -------
    argparse.Namespace
        Arguments analyses (``input``, ``output``).
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Fichier TSV des profils normalises.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Chemin de sauvegarde de la figure PNG.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Point d'entree du script.

    Parameters
    ----------
    argv : list of str, optional
        Arguments de la ligne de commande.
    """
    args = parse_args(argv)
    build_figure(args.input, args.output)


if __name__ == "__main__":
    main()
