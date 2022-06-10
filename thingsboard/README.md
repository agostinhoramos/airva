# Thigsboard CE 3.3.4.1 # airva.local

sudo service thingsboard start
sudo service thingsboard stop
sudo service thingsboard restart

http://airva.local
http://localhost:1333/

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