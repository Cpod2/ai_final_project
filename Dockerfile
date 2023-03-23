FROM docker.io/ubuntu:22.04 AS development

# Install Base Dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends --yes \
        ca-certificates \
        curl \
        git \
        build-essential \
        libedit-dev \
	libreadline-dev \
	libssl-dev \
	libbz2-dev \
	zlib1g-dev \
	libsqlite3-dev \
	libffi-dev \
	liblzma-dev \
	python3 \
	python3-dev \
	python-is-python3

# Install Pyenv
RUN curl https://pyenv.run | bash \
    && echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc \
    && echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc \
    && echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Install Pipenv
RUN curl https://raw.githubusercontent.com/pypa/pipenv/master/get-pipenv.py | python

# Set Locale information
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
RUN echo "LANG=en_US.UTF-8" >> /etc/environment \
    && echo "LC_ALL=en_US.UTF-8" >> /etc/environment

# Command
CMD bash
