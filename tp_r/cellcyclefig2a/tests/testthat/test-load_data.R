test_that("load_profiles charge un TSV valide indexe par gene", {
  path <- tempfile(fileext = ".tsv")
  mat <- toy_profiles()
  write.table(mat, path, sep = "\t", col.names = NA, quote = FALSE)

  loaded <- load_profiles(path)
  expect_true(is.matrix(loaded))
  expect_equal(rownames(loaded), c("EARLY", "LATE", "FLAT"))
  expect_equal(dim(loaded), c(3L, 20L))
})

test_that("load_profiles leve une erreur si le fichier est absent", {
  expect_error(
    load_profiles(file.path(tempdir(), "absent_xyz.tsv")),
    "introuvable"
  )
})

test_that("load_profiles leve une erreur si le fichier est vide", {
  path <- tempfile(fileext = ".tsv")
  writeLines("gene\tt0", path)
  expect_error(load_profiles(path), "aucune donnee")
})
