# constants args
ARG DEFAULT_IMAGE_NAME=movie_recomm
ARG DEFAULT_POETRY_VERSION=1.4.2

##############################
# build stage (install libraries)
##############################
FROM python:3.10.8-slim AS build

# recall common arguments
ARG DEFAULT_IMAGE_NAME
ARG DEFAULT_POETRY_VERSION

# set env arg for current build
ENV IMAGE_NAME=${DEFAULT_IMAGE_NAME}
ENV POETRY_VERSION=${DEFAULT_POETRY_VERSION}

RUN mkdir /${IMAGE_NAME}

# required for postgres installation
RUN apt-get update && apt-get install -y \
    libpq-dev \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

# set env PATH and PYTHONPATH
ENV PATH="/${IMAGE_NAME}/.local/bin:${PATH}"
ENV PATH /root/.poetry/bin:$PATH
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# upgrade pip
RUN pip install --upgrade pip

WORKDIR /${IMAGE_NAME}

# install poetry and create .venv (--copies uses copies rather than symlinks)
RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv --copies .venv \
    && poetry config virtualenvs.path /${IMAGE_NAME}/

# add .venv to PATH to use it as default .venv
ENV PATH /${IMAGE_NAME}/.venv/bin:$PATH

# copy .toml and .lock file and install libraries in .venv
COPY ../../pyproject.toml ../../poetry.lock ./
RUN pip install --upgrade pip \
    && poetry install --only main --no-root


##############################
# final stage (copy .venv and codebase)
##############################
FROM python:3.10.8-slim AS final

# recall common arguments
ARG DEFAULT_IMAGE_NAME
ENV IMAGE_NAME=${DEFAULT_IMAGE_NAME}


# additional installations
RUN apt-get update && apt-get install -y \
    vim \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*


# copy .venv form build stage
COPY --from=build /${IMAGE_NAME}/.venv /${IMAGE_NAME}/.venv/
# add .venv to PATH to use it as default .venv
ENV PATH /${IMAGE_NAME}/.venv/bin:$PATH

# copying codebase
WORKDIR /${IMAGE_NAME}

COPY ../../. ./
RUN chmod +x /${IMAGE_NAME}/django_movie_recommendation/docker/entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
