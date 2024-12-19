FROM mcr.microsoft.com/playwright/python:v1.49.1-noble AS pytest_run
COPY . .
RUN mkdir allure-results
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
RUN pytest tests.py --alluredir=allure-results; exit 0

FROM homebrew/brew:latest AS allure_run
RUN mkdir report
RUN brew install allure
COPY --from=pytest_run allure-results report
CMD ["allure", "serve", "report"]