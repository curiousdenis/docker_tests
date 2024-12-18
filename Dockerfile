FROM mcr.microsoft.com/playwright/python:v1.49.1-noble AS pytest_run
RUN echo 'before test'

FROM homebrew/brew:latest AS main
RUN echo pytest_run
RUN echo 'main text'
