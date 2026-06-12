#' @keywords internal
"_PACKAGE"

# Le pronom `.data` de rlang est utilise dans les appels `ggplot2::aes()`. On le
# declare comme variable globale pour eviter les faux positifs de R CMD check et
# de `object_usage_linter`.
utils::globalVariables(".data")
