FROM joyzoursky/python-chromedriver:3.9

WORKDIR /src
COPY req.txt /src
RUN pip install -r req.txt

COPY . /src

CMD ["python", "main_chrome_38_bing_docker.py"]

#docker build -t full_screenshot .
#docker run -d -v $(pwd)/screenshots:/src/screenshots --name test full_screenshot
#=> naming to docker.io/library/qwe:latest
#docker run -d -v %cd%/bingIMG:/src/bingIMG --name test qwe
#C:\Python developer\CBS_extend\parser\bingIMG
#docker run --name test qwe -d -v C:/Python developer/CBS_extend/parser/bingIMG:/src/bingIMG