# Thigsboard CE 3.3.4.1 # airva.local

# Install JAVA 11 OpenJDK
sudo apt update
sudo apt upgrade
sudo apt install openjdk-11-jdk

sudo update-alternatives --config java
java -version

sudo wget https://github.com/thingsboard/thingsboard/releases/download/v3.3.4.1/thingsboard-3.3.4.1.deb

sudo dpkg -i thingsboard-3.3.4.1.deb

# install **wget** if not already installed:
sudo apt install -y wget

# import the repository signing key:
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# add repository contents to your system:
RELEASE=$(lsb_release -cs)
echo "deb http://apt.postgresql.org/pub/repos/apt/ ${RELEASE}"-pgdg main | sudo tee  /etc/apt/sources.list.d/pgdg.list

# install and launch the postgresql service:
sudo apt update
sudo apt -y install postgresql-12
sudo service postgresql start

sudo su - postgres
psql
\password #over_332244
\q
exit

psql -U postgres -d postgres -h 127.0.0.1 -W
CREATE DATABASE thingsboard;
\q

sudo nano /etc/thingsboard/conf/thingsboard.conf

# DB Configuration 
export DATABASE_TS_TYPE=sql
export SPRING_JPA_DATABASE_PLATFORM=org.hibernate.dialect.PostgreSQLDialect
export SPRING_DRIVER_CLASS_NAME=org.postgresql.Driver
export SPRING_DATASOURCE_URL=jdbc:postgresql://localhost:5432/thingsboard
export SPRING_DATASOURCE_USERNAME=postgres
export SPRING_DATASOURCE_PASSWORD=over_332244
# Specify partitioning size for timestamp key-value storage. Allowed values: DAYS, MONTHS, YEARS, INDEFINITE.
export SQL_POSTGRES_TS_KV_PARTITIONING=MONTHS

# Update ThingsBoard memory usage and restrict it to 256MB in /etc/thingsboard/conf/thingsboard.conf
export JAVA_OPTS="$JAVA_OPTS -Xms256M -Xmx256M"


# --loadDemo option will load demo data: users, devices, assets, rules, widgets.
sudo /usr/share/thingsboard/bin/install/install.sh --loadDemo

sudo service thingsboard start

http://localhost:8080/

System Administrator: sysadmin@thingsboard.org / sysadmin
Tenant Administrator: tenant@thingsboard.org / tenant
Customer User: customer@thingsboard.org / customer

System Administrator: sysadmin@airva.local / sysadmin
Tenant Administrator: tenant@airva.local / tenant
Customer User: customer@airva.local / customer

# Troubleshooting
/var/log/thingsboard
cat /var/log/thingsboard/thingsboard.log | grep ERROR




Read more here https://thingsboard.io/docs/user-guide/install/ubuntu/?ubuntuThingsboardDatabase=postgresql&ubuntuThingsboardQueue=inmemory