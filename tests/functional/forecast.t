Functional tests for popcast model fitting.

  $ pushd "$TESTDIR" > /dev/null

Forecast frequencies with a model trained on simulated data.

  $ popcast forecast \
  >   --tip-attributes data/simulated_sample_1/tip_attributes.tsv.gz \
  >   --model data/simulated_sample_1/normalized_fitness.json \
  >   --delta-months 12 \
  >   --output-table "$TMP/forecasts.tsv" > /dev/null
  $ deep diff --significant-digits 6 "data/simulated_sample_1/forecasts.tsv" "$TMP/forecasts.tsv"
  {}
  $ rm -f "$TMP/forecasts.tsv"

Forecast tips with existing frequencies.

  $ popcast forecast \
  >   --tip-attributes data/simulated_sample_1/2040-10-01/tip_attributes.tsv.gz \
  >   --frequencies data/simulated_sample_1/2040-10-01/frequencies.json \
  >   --model data/simulated_sample_1/normalized_fitness.json \
  >   --delta-months 12 \
  >   --output-table "$TMP/forecasts.tsv"

  $ popd > /dev/null
