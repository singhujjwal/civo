pip install certbot

certbot certonly \
-d singhjee.in \
-d *.k8s.singhjee.in \
--logs-dir /home/centos/letsencrypt/log  \
--config-dir /home/centos/letsencrypt/config \
--work-dir /home/centos/letsencrypt/work \
-m singhujjwal@gmail.com \
--agree-tos --manual --preferred-challenges dns


openssl pkcs12 -export -out \
	 cert.pfx  \
	-in fullchain.pem \
	-certfile chain.pem \
	-inkey privkey.pem \
	-passin pass:xxxxxxxx \
    -passout pass:xxxxxxxx