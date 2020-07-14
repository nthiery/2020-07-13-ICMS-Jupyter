# Dockerfile for binder
FROM registry.gitlab.com/sagemath/sage/sagemath:latest-py3

RUN sage -pip install --no-cache-dir --upgrade ipywidgets
RUN sage -pip install --no-cache-dir RISE
RUN sage -pip install --no-cache-dir nbdime
RUN sage -pip install --no-cache-dir sage-combinat-widgets
RUN sage -pip install --no-cache-dir sage-explorer

# Ensure this COPY goes *after* installation of prerequisites; otherwise the
# build cache will be invalidated any time we change a file in this repository.
COPY --chown=sage:sage . ${HOME}
