
# Purpose

This repository is just a simple tester client with some sample client code for
working with the Current Intelligent Environment APIs with Python.  It is not
intended as a production example but an illustration so lacks error handling,
pep8, etc.

# Setup

After pulling down this repo, you can build a docker image for the runtime
environment and run in a container with the same python environment I used.

For example the following command run in this repos will build your image:
```
docker build -t current-api-demo .
```

You then find the image in your `docker images` and can run it:
```
docker run --rm --volume=$(pwd):/root -it current-api-demo
```

If you don't know **docker** or have issues with a network firewall requiring a
proxy you can find other better resources to go into those issues.

# Dependencies

It is expected you've already created UAA and IE Traffic Planning services
bound to an application.  You'll then want to set some environment variables
based on the `cf env` results you get.

- UAA_URI
- UAA_CLIENT
- UAA_CLIENT_SECRET
- TRAFFIC_URI
- TRAFFIC_ZONE (Predix-Zone-Id for ie-traffic)

# Running

Once you are in your container, you can just run the client and should see
output like this:
```
root@43b8f51c1e31:~# ./client.py
{"event-uid":"fe5742c0-aff2-4747-8cb2-54e2dac8c758","timestamp":1468481476061,"event-type":"TFEVT","device-uid":"HYP1040-75","location-uid":"HYP1040-75-Lane2","properties":{"vehicle-type":"car"},"measures":[{"tag":"vehicleCount","value":4},{"tag":"speed","value":19,"unit":"MPS"},{"tag":"direction","value":271,"unit":"DEGREE"}]}
```

