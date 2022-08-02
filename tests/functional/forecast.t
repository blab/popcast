Functional tests for nextcast model fitting.

  $ pushd "$TESTDIR" > /dev/null

Forecast frequencies with a model trained on simulated data.

  $ nextcast forecast \
  >   --tip-attributes data/simulated_sample_1/tip_attributes.tsv.gz \
  >   --model data/simulated_sample_1/normalized_fitness.json \
  >   --delta-months 12 \
  >   --output-table "$TMP/forecasts.tsv" > /dev/null
  $ deep diff --significant-digits 6 "data/simulated_sample_1/forecasts.tsv" "$TMP/forecasts.tsv"
  {}
  $ rm -f "$TMP/forecasts.tsv"

  $ popd > /dev/null
