# AIRVA Driver

1 - Build Dockerfile
`docker build -t airva_driver -f Dockerfile .`

2 - Run docker image
`docker run -d --name airva_driver --privileged -p 2022:22 -t airva_driver`

3 - Run SSH server
`ssh -p 2022 user@127.0.0.1`

4 - Run
``