"""Tests unitaires pour le pipeline de reproduction de la Figure 2A."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import figure_2a


def _toy_profiles() -> pd.DataFrame:
    """Construit une petite matrice d'expression deterministe pour les tests."""
    n_points = 20
    time = np.arange(n_points)
    # Deux genes en opposition de phase + un gene constant.
    early = 100 + 50 * np.sin(2 * np.pi * time / n_points)
    late = 100 + 50 * np.sin(2 * np.pi * time / n_points + np.pi)
    flat = np.full(n_points, 42.0)
    return pd.DataFrame(
        [early, late, flat],
        index=["EARLY", "LATE", "FLAT"],
        columns=[f"t{i}" for i in range(n_points)],
    )


# --- load_profiles -----------------------------------------------------------


def test_load_profiles_nominal(tmp_path: Path) -> None:
    """Charge un TSV valide et retourne une matrice indexee par gene."""
    path = tmp_path / "data.tsv"
    _toy_profiles().to_csv(path, sep="\t")
    loaded = figure_2a.load_profiles(path)
    assert list(loaded.index) == ["EARLY", "LATE", "FLAT"]
    assert loaded.shape == (3, 20)


def test_load_profiles_missing_file(tmp_path: Path) -> None:
    """Leve FileNotFoundError si le fichier n'existe pas."""
    with pytest.raises(FileNotFoundError):
        figure_2a.load_profiles(tmp_path / "absent.tsv")


def test_load_profiles_empty_file(tmp_path: Path) -> None:
    """Leve ValueError si le fichier ne contient aucune donnee."""
    path = tmp_path / "empty.tsv"
    path.write_text("gene\tt0\n")  # entete seule, aucune ligne de donnees
    with pytest.raises(ValueError):
        figure_2a.load_profiles(path)


# --- zscore_per_gene ---------------------------------------------------------


def test_zscore_per_gene_mean_zero_std_one() -> None:
    """Chaque gene non constant a une moyenne ~0 et un ecart-type ~1."""
    zscores = figure_2a.zscore_per_gene(_toy_profiles())
    assert np.allclose(zscores.loc["EARLY"].mean(), 0.0, atol=1e-9)
    # std avec ddof=1 (pandas) -> proche de 1.
    assert zscores.loc["EARLY"].std() == pytest.approx(1.0, rel=1e-6)


def test_zscore_per_gene_constant_gene_is_zero() -> None:
    """Un gene constant (ecart-type nul) est ramene a zero sans NaN."""
    zscores = figure_2a.zscore_per_gene(_toy_profiles())
    assert (zscores.loc["FLAT"] == 0.0).all()
    assert not zscores.isna().to_numpy().any()


# --- order_by_peak_phase -----------------------------------------------------


def test_order_by_peak_phase_preserves_genes() -> None:
    """Le reordonnancement conserve l'ensemble des genes et la forme."""
    zscores = figure_2a.zscore_per_gene(_toy_profiles())
    ordered = figure_2a.order_by_peak_phase(zscores)
    assert ordered.shape == zscores.shape
    assert set(ordered.index) == set(zscores.index)


def test_order_by_peak_phase_orders_by_phase() -> None:
    """Deux genes en opposition de phase sont separes dans l'ordre."""
    zscores = figure_2a.zscore_per_gene(_toy_profiles())
    ordered = figure_2a.order_by_peak_phase(zscores, period_min=20, sampling_min=1)
    positions = {gene: i for i, gene in enumerate(ordered.index)}
    assert positions["EARLY"] != positions["LATE"]


# --- make_colormap -----------------------------------------------------------


def test_make_colormap_is_usable() -> None:
    """La colormap est construite et nommee correctement."""
    cmap = figure_2a.make_colormap()
    assert cmap.name == "cyan_black_yellow"


# --- build_figure (integration) ----------------------------------------------


def test_build_figure_creates_output(tmp_path: Path) -> None:
    """Le pipeline complet produit bien un fichier image."""
    data = tmp_path / "data.tsv"
    _toy_profiles().to_csv(data, sep="\t")
    output = tmp_path / "fig.png"
    figure_2a.build_figure(data, output)
    assert output.exists()
    assert output.stat().st_size > 0


# --- parse_args --------------------------------------------------------------


def test_parse_args_defaults() -> None:
    """Sans argument, les chemins par defaut sont utilises."""
    args = figure_2a.parse_args([])
    assert args.input == figure_2a.DEFAULT_DATA_PATH
    assert args.output == figure_2a.DEFAULT_OUTPUT_PATH


def test_parse_args_custom() -> None:
    """Les arguments --input/--output sont correctement analyses."""
    args = figure_2a.parse_args(["--input", "a.tsv", "--output", "b.png"])
    assert args.input == Path("a.tsv")
    assert args.output == Path("b.png")


# --- main (integration) ------------------------------------------------------


def test_main_end_to_end(tmp_path: Path) -> None:
    """main() execute le pipeline complet depuis la ligne de commande."""
    data = tmp_path / "data.tsv"
    _toy_profiles().to_csv(data, sep="\t")
    output = tmp_path / "out.png"
    figure_2a.main(["--input", str(data), "--output", str(output)])
    assert output.exists()
