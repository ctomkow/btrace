# btrace

Run container locally

docker build -t btrace .
docker run -d -p 8080:8080 -e PORT='8080' --name btrace btrace