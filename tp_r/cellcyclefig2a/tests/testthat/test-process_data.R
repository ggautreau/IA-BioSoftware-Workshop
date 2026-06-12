test_that("zscore_per_gene donne une moyenne ~0 et un ecart-type ~1", {
  zscores <- zscore_per_gene(toy_profiles())
  expect_equal(mean(zscores["EARLY", ]), 0, tolerance = 1e-9)
  expect_equal(sd(zscores["EARLY", ]), 1, tolerance = 1e-6)
})

test_that("zscore_per_gene ramene un gene constant a zero sans NA", {
  zscores <- zscore_per_gene(toy_profiles())
  expect_true(all(zscores["FLAT", ] == 0))
  expect_false(any(is.na(zscores)))
})

test_that("order_by_peak_phase conserve l'ensemble des genes et la forme", {
  zscores <- zscore_per_gene(toy_profiles())
  ordered <- order_by_peak_phase(zscores)
  expect_equal(dim(ordered), dim(zscores))
  expect_setequal(rownames(ordered), rownames(zscores))
})

test_that("order_by_peak_phase separe deux genes en opposition de phase", {
  zscores <- zscore_per_gene(toy_profiles())
  ordered <- order_by_peak_phase(zscores, period_min = 20, sampling_min = 1)
  pos_early <- which(rownames(ordered) == "EARLY")
  pos_late <- which(rownames(ordered) == "LATE")
  expect_false(pos_early == pos_late)
})
