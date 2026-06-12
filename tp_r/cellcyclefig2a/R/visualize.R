#' Palette de couleurs de la heatmap
#'
#' @description
#' Renvoie les trois couleurs de la colormap de l'article : cyan (expression
#' basse) vers noir (moyenne) vers jaune (expression haute).
#'
#' @return Un vecteur de trois couleurs hexadecimales.
#'
#' @examples
#' heatmap_palette()
#'
#' @export
heatmap_palette <- function() {
  c("#00FFFF", "#000000", "#FFFF00")
}

#' Trace la heatmap facon Figure 2A
#'
#' @description
#' Construit la heatmap des genes (lignes) au cours du temps (colonnes) a
#' partir d'une matrice de z-scores deja ordonnee.
#'
#' @param zscores Matrice de z-scores ordonnee (genes en lignes, points en
#'   colonnes).
#' @param sampling_min Intervalle d'echantillonnage en minutes (defaut 5).
#' @param clip Borne absolue de l'echelle de couleur (defaut 1.5).
#'
#' @return Un objet `ggplot`.
#'
#' @examples
#' set.seed(1)
#' mat <- matrix(rnorm(200), nrow = 20)
#' plot_heatmap(mat, sampling_min = 5)
#'
#' @importFrom ggplot2 ggplot aes geom_raster scale_fill_gradientn labs theme_minimal element_blank theme
#' @importFrom scales squish
#' @importFrom rlang .data
#' @export
plot_heatmap <- function(zscores, sampling_min = 5, clip = 1.5) {
  values <- as.matrix(zscores)
  n_genes <- nrow(values)
  n_points <- ncol(values)
  time <- rep((seq_len(n_points) - 1L) * sampling_min, each = n_genes)
  gene_rank <- rep(seq_len(n_genes), times = n_points)
  long_data <- data.frame(
    time = time,
    gene_rank = gene_rank,
    value = as.vector(values)
  )

  ggplot2::ggplot(
    long_data,
    ggplot2::aes(x = .data$time, y = .data$gene_rank, fill = .data$value)
  ) +
    ggplot2::geom_raster() +
    ggplot2::scale_fill_gradientn(
      colours = heatmap_palette(),
      limits = c(-clip, clip),
      oob = scales::squish,
      name = NULL
    ) +
    ggplot2::labs(
      title = "Saccharomyces cerevisiae",
      x = "time (minutes)",
      y = sprintf("Top Periodic Genes (%d)", n_genes)
    ) +
    ggplot2::theme_minimal() +
    ggplot2::theme(
      axis.text.y = ggplot2::element_blank(),
      panel.grid = ggplot2::element_blank()
    )
}

#' Execute le pipeline complet de reproduction de la Figure 2A
#'
#' @description
#' Enchaine le chargement des donnees, la normalisation z-score, le tri par
#' phase et la generation de la heatmap, puis sauvegarde l'image.
#'
#' @param data_path Chemin du fichier TSV de profils normalises.
#' @param output_path Chemin de sauvegarde de la figure (PNG).
#' @param period_min Periode du cycle cellulaire en minutes (defaut 75).
#' @param sampling_min Intervalle d'echantillonnage en minutes (defaut 5).
#'
#' @return Le chemin de sortie, de maniere invisible.
#'
#' @examples
#' \dontrun{
#' build_figure(
#'   "../data/oscillating-genes_1705_normalized-profiles.tsv",
#'   "figure_2a.png"
#' )
#' }
#'
#' @importFrom ggplot2 ggsave
#' @export
build_figure <- function(data_path, output_path,
                         period_min = 75, sampling_min = 5) {
  profiles <- load_profiles(data_path)
  zscores <- zscore_per_gene(profiles)
  ordered <- order_by_peak_phase(zscores, period_min, sampling_min)
  plot <- plot_heatmap(ordered, sampling_min)
  ggplot2::ggsave(output_path, plot, width = 4, height = 6, dpi = 150)
  invisible(output_path)
}
