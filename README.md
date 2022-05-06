# CONDA-SKELETON

As far (as of 2022/05/06), the `conda skeleton pypi <package-name>` is not working in conda-build; v3.21.8 for several reasons. The causes I have confirmed are as follows;

1. Running on a terminal that uses ARM chips (M1 Macbook etc.)
2. Running on a version newer than Python 3.7

There has already been [some discussion](https://github.com/conda/conda-build/issues/4354) on this issue.

We need to improve concerning both causes. But given that Python 3.6 is not compatible with ARM chips, it doesn't work in a local environment. Therefore, it is necessary to work around this by running it on a Linux container on an AMD chip.

Furthermore, even if you could run it if the project name contains hyphens, `conda skeleton pypi <package-name>` will not work correctly, depending on the Github repository name.

I have created a docker container and a Python script to solve these problems.

Hopefully, future versions will eliminate the need for these scripts.

## Build

```bash
sh docker-build.sh
```

## Run

```bash
sh docker-run.sh
```

## After running container

```bash
sh conda-build.sh
```
 <package-name>
After the script is complete, you can get `meta.yaml` in the `output` directory, which binds to the container.