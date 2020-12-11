docker run --rm --name selenoid -p 4444:4444 \
-v /var/run/docker.sock:/var/run/docker.sock \
-v $PWD/selenoid/config:/etc/selenoid \
--net test_network aerokube/selenoid:1.10.0 \
-conf /etc/selenoid/browsers.json -container-network test_network