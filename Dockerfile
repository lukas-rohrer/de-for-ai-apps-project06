FROM python:3.8
LABEL maintainer="Lukas Rohrer"
COPY ./ /app
RUN ls -la /app
WORKDIR /app/techtrends
RUN pip install -r requirements.txt
RUN python init_db.py
CMD ["python", "app.py"]
EXPOSE 3111