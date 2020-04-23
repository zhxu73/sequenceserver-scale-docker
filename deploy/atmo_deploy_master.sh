#!/bin/bash


WORKQUEUE_PASSWORD=
PROJECT_NAME=
CPU_PER_WORKER=8

DATABASE=nt


if [ -z $PROJECT_NAME ]; then
    PROJECT_NAME="$ATMO_USER-starBLAST"
fi
if [ -z $WORKQUEUE_PASSWORD ]; then
    WORKQUEUE_PASSWORD="$(echo $PROJECT_NAME | sha1sum | cut -d' ' -f1)"
fi

DEBIAN_FRONTEND=noninteractive apt-get -qq -y update
DEBIAN_FRONTEND=noninteractive apt-get -qq -y install nginx wget

command -v docker
if [ $? != 0 ]; then
    ezd
fi
systemctl start nginx

#
# Download progress script
git clone -b dev https://github.com/zhxu73/sequenceserver-scale-docker.git
cp sequenceserver-scale-docker/deploy/starBLAST-master.service /etc/systemd/system
cp sequenceserver-scale-docker/deploy/*.py /root
rm -rf sequenceserver-scale-docker

#
# Environment variable
echo "PROJECT_NAME=$PROJECT_NAME" >> /etc/starBLAST-environment
echo "WORKQUEUE_PASSWORD=$WORKQUEUE_PASSWORD" >> /etc/starBLAST-environment
echo "CPU_PER_WORKER=$CPU_PER_WORKER" >> /etc/starBLAST-environment
echo "DATABASE=$DATABASE" >> /etc/starBLAST-environment

echo "source /etc/starBLAST-environment" >> /etc/profile
source /etc/profile


#
# Pull docker container
echo " " > /var/www/html/index.html
python progress_reporter.py div "Start download docker container"
docker pull ncbi/blast
docker pull zhxu73/sequenceserver-scale:no-irods
python progress_reporter.py div "Finish download docker container"

#
# Permission for /scratch
mkdir /scratch
chown -R $ATMO_USER /scratch
chmod u=7 /scratch

#
# Download DB via NCBI docker (GCP)
python progress_reporter.py div "Start download $DATABASE database from NCBI (GCP)" " "
python index_page_gen.py &
docker run --rm \
  -v /scratch:/blast/blastdb:rw \
  -w /blast/blastdb \
  ncbi/blast \
  update_blastdb.pl --source gcp $DATABASE
python progress_reporter.py div "Finish download $DATABASE database from NCBI (GCP)"

systemctl stop nginx
systemctl daemon-reload
systemctl enable starBLAST-master
systemctl restart starBLAST-master


