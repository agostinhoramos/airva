# AIRVA Driver

1 - Build Dockerfile
`docker build -t airva_driver -f Dockerfile .`

2 - Run docker image
`docker run -d --name airva_driver -p 2022:22 -t airva_driver`