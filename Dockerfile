FROM vimagick/scrapyd

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary
CMD scrapyd-deploy scrapyd
