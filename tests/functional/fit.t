Functional tests for popcast model fitting.

  $ pushd "$TESTDIR" > /dev/null

Test a model to with a subset of simulated data.

  $ popcast fit \
  >   --tip-attributes data/simulated_sample_1/tip_attributes.tsv.gz \
  >   --fixed-model "data/simulated_sample_1/normalized_fitness.json" \
  >   --output "$TMP/normalized_fitness.json" > /dev/null
  $ diff -u "data/simulated_sample_1/test_normalized_fitness.json" "$TMP/normalized_fitness.json"

  $ popd > /dev/null
