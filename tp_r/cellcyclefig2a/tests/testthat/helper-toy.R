# Construit une petite matrice d'expression deterministe pour les tests :
# deux genes en opposition de phase et un gene constant.
toy_profiles <- function() {
  n_points <- 20L
  time <- seq_len(n_points) - 1L
  early <- 100 + 50 * sin(2 * pi * time / n_points)
  late <- 100 + 50 * sin(2 * pi * time / n_points + pi)
  flat <- rep(42, n_points)
  mat <- rbind(EARLY = early, LATE = late, FLAT = flat)
  colnames(mat) <- paste0("t", time)
  mat
}
