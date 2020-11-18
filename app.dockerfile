FROM python:3.8-slim
CMD ["python", "/server.py"]
RUN pip install aiohttp[speedups] uvloop
COPY ./server.py ./get_token.py /
