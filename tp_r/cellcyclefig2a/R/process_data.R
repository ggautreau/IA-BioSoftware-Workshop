#' Normalise chaque gene en z-score
#'
#' @description
#' Transforme chaque ligne (gene) en z-score : `(x - moyenne) / ecart-type`.
#' Les genes constants (ecart-type nul) sont ramenes a zero pour eviter les
#' divisions par zero.
#'
#' @param profiles Matrice numerique (genes en lignes, points temporels en
#'   colonnes).
#'
#' @return Une matrice de meme dimension, normalisee par ligne.
#'
#' @examples
#' mat <- matrix(c(1, 2, 3, 4, 5, 6), nrow = 2, byrow = TRUE)
#' zscore_per_gene(mat)
#'
#' @importFrom stats sd
#' @export
zscore_per_gene <- function(profiles) {
  values <- as.matrix(profiles)
  means <- rowMeans(values)
  stds <- apply(values, 1, stats::sd)
  safe_stds <- ifelse(stds == 0, NA_real_, stds)
  zscores <- (values - means) / safe_stds
  zscores[is.na(zscores)] <- 0
  zscores
}

#' Ordonne les genes par phase du pic d'expression
#'
#' @description
#' Extrait la phase de la composante de Fourier a la frequence du cycle
#' cellulaire, ce qui donne le moment du pic d'expression de chaque gene, puis
#' trie les genes par phase croissante. Cela reproduit la vague diagonale
#' caracteristique de la transcription periodique.
#'
#' @param zscores Matrice de z-scores (genes en lignes, points en colonnes).
#' @param period_min Periode du cycle cellulaire en minutes (defaut 75).
#' @param sampling_min Intervalle d'echantillonnage en minutes (defaut 5).
#'
#' @return La matrice `zscores` avec ses lignes reordonnees par phase.
#'
#' @examples
#' set.seed(1)
#' mat <- matrix(rnorm(40), nrow = 4)
#' order_by_peak_phase(mat, period_min = 10, sampling_min = 1)
#'
#' @importFrom stats fft
#' @export
order_by_peak_phase <- function(zscores, period_min = 75, sampling_min = 5) {
  values <- as.matrix(zscores)
  n_points <- ncol(values)
  total_time <- n_points * sampling_min
  target_cycles <- total_time / period_min
  bin_index <- round(target_cycles)
  coeffs <- apply(values, 1, function(row) stats::fft(row)[bin_index + 1L])
  phase <- Arg(coeffs)
  zscores[order(phase), , drop = FALSE]
}
