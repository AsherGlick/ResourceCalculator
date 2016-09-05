FROM ruby:2.2.3-slim

MAINTAINER Asher Glick <aglick@aglick.com>

# This seems like alot maybe
# it is a copy paste from https://semaphoreci.com/community/tutorials/dockerizing-a-ruby-on-rails-application
RUN apt-get update && apt-get install -qq -y build-essential nodejs sqlite3 libsqlite3-dev libpq-dev postgresql-client-9.4 --fix-missing --no-install-recommends



ENV INSTALL_PATH /resource_calculator
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH


COPY Gemfile Gemfile
RUN bundle install

COPY . .

VOLUME ["$INSTALL_PATH/public"]


CMD rails server -p 80