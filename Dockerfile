FROM python:3.8-buster

MAINTAINER Craig Tomkow "ctomkow@gmail.com"

# deps
RUN apt-get update && apt-get install -y \
    curl                \
    apt-transport-https \
    ssl-cert            \
    ca-certificates     \
    gnupg               \
    lsb-release

# libbgpstream dep (https://bgpstream.caida.org/docs/install/bgpstream)
RUN echo "deb https://dl.bintray.com/wand/general $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/wand.list
RUN curl --silent "https://bintray.com/user/downloadSubjectPublicKey?username=wand" | apt-key add -
RUN echo "deb https://pkg.caida.org/os/$(lsb_release -si|awk '{print tolower($0)}') $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/caida.list
RUN wget -O /etc/apt/trusted.gpg.d/caida.gpg https://pkg.caida.org/os/ubuntu/keyring.gpg
# had to strip the 'sudo' from bootstrap.sh
RUN curl -s https://pkg.caida.org/os/$(lsb_release -si|awk '{print tolower($0)}')/bootstrap.sh | sed -E "s/sudo//g" | bash
RUN apt update && apt-get install -y \
    bgpstream2-tools    \
    libbgpstream2       \
    libbgpstream2-dev

# python deps
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Run a WSGI server to serve the application. gunicorn must be declared as
# a dependency in requirements.txt.
CMD gunicorn -b :$PORT --workers 2 --threads 16 main:app --log-level debug
