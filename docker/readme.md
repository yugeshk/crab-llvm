# Building Clam with Docker and running tests

```shell
docker build --build-arg UBUNTU=xenial --build-arg BRANCH=eran --build-arg BUILD_TYPE=Release -t eran_racetrack -f docker/clam-full-size-rel.Dockerfile .
docker run -v `pwd`:/host -it eran_racetrack"
```

This will automatically download all dependencies from a base image
and build Clam under `/clam/build`.

Clam install directory is added to `PATH`.

Build arguments (required):
- UBUNTU: trusty, xenial, bionic
- BUILD_TYPE: Release, Debug

