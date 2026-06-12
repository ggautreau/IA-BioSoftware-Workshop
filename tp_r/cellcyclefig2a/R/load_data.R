#' Charge la matrice de profils d'expression
#'
#' @description
#' Lit un fichier TSV de profils d'expression normalises. La premiere colonne
#' contient les identifiants de genes (utilisee comme noms de lignes) et les
#' colonnes suivantes correspondent aux echantillons / points temporels.
#'
#' @param path Chemin du fichier TSV a charger.
#'
#' @return Une matrice numerique (genes en lignes, points temporels en
#'   colonnes), indexee par les identifiants de genes.
#'
#' @examples
#' \dontrun{
#' profiles <- load_profiles("../data/oscillating-genes_1705_normalized-profiles.tsv")
#' dim(profiles)
#' }
#'
#' @importFrom utils read.delim
#' @export
load_profiles <- function(path) {
  if (!file.exists(path)) {
    stop("Fichier de donnees introuvable : ", path, call. = FALSE)
  }
  dataframe <- utils::read.delim(path, row.names = 1, check.names = FALSE)
  if (nrow(dataframe) == 0L || ncol(dataframe) == 0L) {
    stop("Le fichier ne contient aucune donnee : ", path, call. = FALSE)
  }
  as.matrix(dataframe)
}
