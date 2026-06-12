test_that("heatmap_palette renvoie trois couleurs", {
  pal <- heatmap_palette()
  expect_length(pal, 3)
  expect_true(all(grepl("^#", pal)))
})

test_that("plot_heatmap renvoie un objet ggplot", {
  zscores <- zscore_per_gene(toy_profiles())
  plot <- plot_heatmap(zscores)
  expect_s3_class(plot, "ggplot")
})

test_that("build_figure cree bien un fichier image", {
  path <- tempfile(fileext = ".tsv")
  mat <- toy_profiles()
  write.table(mat, path, sep = "\t", col.names = NA, quote = FALSE)
  output <- tempfile(fileext = ".png")

  result <- build_figure(path, output, period_min = 20, sampling_min = 1)
  expect_equal(result, output)
  expect_true(file.exists(output))
  expect_gt(file.info(output)$size, 0)
})
