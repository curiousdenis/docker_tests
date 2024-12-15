FROM mcr.microsoft.com/playwright/python:v1.49.1-noble
COPY . .
CMD ["pytest", "tests.py","--alluredir=allure-results"]
RUN mkdir allure-results
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt