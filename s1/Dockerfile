FROM kalilinux/kali-rolling
# updates & tools
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    git \
    curl \
    nano \
    vim \
    tree \
    && apt-get clean

# default path
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app
COPY . /app
CMD ["bash"]
# - to run container :
# docker build -t graphenv .
# - to go inside
# docker run -it graphenv


# end