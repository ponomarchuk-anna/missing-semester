FROM python:3
WORKDIR /"bot"
COPY requirements.txt /"bot"
RUN python3 -m pip install -r requirements.txt
COPY . /"bot"
EXPOSE 8888
CMD ["python", "bot.py"]
