# Script d'execution principal.
# Reproduit la Figure 2A a partir des donnees du dossier ../../data.
#
# Usage : Rscript run.R [chemin_donnees] [chemin_sortie]

library(cellcyclefig2a)

args <- commandArgs(trailingOnly = TRUE)
data_path <- if (length(args) >= 1) {
  args[[1]]
} else {
  "../../data/oscillating-genes_1705_normalized-profiles.tsv"
}
output_path <- if (length(args) >= 2) args[[2]] else "figure_2a.png"

build_figure(data_path, output_path)
message(sprintf("Figure sauvegardee : %s", output_path))
