# Change log

## 2.0.0

### Major changes

- Make [OpenCV](https://pypi.org/project/opencv-python/) an optional dependency, simplifying installation requirements for forecasting from an existing model. This change requires users to specify the "full" package version at installation to get support for model fitting. [#4](https://github.com/blab/popcast/pull/4) (@huddlej)

## 1.1.0

### Features

- fit: export `optimal_projected_frequency` field corresponding to strain frequencies for the optimal distance between timepoints when testing an existing model with the `--fixed-model` argument [#2](https://github.com/blab/popcast/pull/2) (@huddlej)

### Bug fixes

- fix broken numpy and deepdiff dependencies [#3](https://github.com/blab/popcast/pull/3) (@huddlej)

## 1.0.2

### Bug fixes

 - Fix parsing of Augur frequencies JSONs [#1](https://github.com/blab/popcast/pull/1) (@huddlej)
