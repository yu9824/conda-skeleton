# Base image
FROM --platform=amd64 continuumio/miniconda3:4.11.0
# FROM --platform=arm64 continuumio/miniconda3:4.11.0

# Update apt-get
RUN apt-get update -y && apt-get upgrade -y

# Install vim
RUN apt-get install -y vim

# Install conda-build
RUN conda install -c conda-forge -y conda-build
# RUN pip install git+https://github.com/conda/conda-build.git

# Install anaconda-client
# RUN conda install -y anaconda-client

# Add user
ARG username="anaconda"
RUN useradd -m -s /bin/bash ${username}
USER ${username}
ARG dir_home="/home/${username}"
WORKDIR ${dir_home}
RUN conda init
ARG fname_conda_skeleton="conda-skeleton.sh"
RUN echo "echo 'Next, \`sh ${fname_conda_skeleton} <package-name>\`'" >> ~/.bashrc

# Add python script to modify meta.yaml
ARG fname_modify_meta_script="modify_meta.py"
ADD ${fname_modify_meta_script} ${dir_home}/${fname_modify_meta_script}

# Create shell script
ARG fpath_conda_skeleton=${dir_home}/${fname_conda_skeleton}
RUN echo "#!/bin/sh" >> ${fpath_conda_skeleton}

# Remove existing meta.yaml
RUN echo "rm -rf ~/output/\$1" >> ${fpath_conda_skeleton}

# conda skeleton
RUN echo "conda skeleton pypi \$1 --python-version 3.6" >> ${fpath_conda_skeleton}

# Modify meta.yaml
RUN echo "python3 ${fname_modify_meta_script} \$1/meta.yaml" >> ${fpath_conda_skeleton}

# cp meta.yaml
RUN echo "mkdir ~/output/\$1" >> ${fpath_conda_skeleton}
RUN echo "cp ~/\$1/meta.yaml ~/output/\$1/meta.yaml" >> ${fpath_conda_skeleton}

# conda build   # for conda-forge, build is not necessary
# RUN echo "conda build -c conda-forge \$1" >> ${fpath_conda_skeleton}