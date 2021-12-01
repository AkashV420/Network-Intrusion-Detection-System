# Network Intrusion Detection System

We built a traffic flow classifier and a monitoring app which analyses all the flows passed through a switch and flags the one which seem to be an anomaly.

The classifier takes eight features of a flow as input 

	1. Protocol
	2. Transfer Rate
	3. Packet Size
	4. Ratio of number of hosts that source host has connection to total hosts
	5. Number of hosts that source host has connection to
	6. Number of flows having same protocol, source and destination IP addresses.
	7. Number of flows having the same network protocol, source IP Address, destination IP Address and destination port or the number of ports that the source host uses to connect to the same port in destination host.
	8. The ratio of the opposite flow (same protocol but opposite IP Address and port)’s packet num to the flow’s packet number.

and classify into one of these following categories:

	1. Normal Traffic
	2. IP Sweep
	3. Port Scan
	4. ICP Flood
	5. Ping of Death
	6. UDP Flood
	7. TCP SYN Flood

## Running

### Training the model

```
	cd training/
	python3 train.py
```

Trained model would be saved as `trained_model.h5`

### Running mininet and generating traffic simulation

#### Installing mininet

```
	git clone https://github.com/mininet/mininet
	PYTHON=python3 mininet/util/install.sh -a
```

#### Creating topology and generating traffic

```
	cd mininet/
	sudo python3 gen_traffic.py
```

#### Running controller

```
	cd sdn-controller/
	<path_to_pox>/pox.py forwarding app
```

#### Running monitoring web application

##### Backend
```
	cd web/backend
	python3 server.py
```

##### Frontend
```
	cd web/frontend
	npm install
	npm start
```
