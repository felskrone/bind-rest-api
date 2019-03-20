# Bind9-restapi using OpenAPI-3.0

A RESTful API to BIND, written in Flask+connexion. 

Provides the ability to add/update/remove A, AAAA, CNAME, MX, TXT, SRV, or SPFM records directly in Bind.

## Requirements
- Bind9+ configured
- nsupdate binary
- python3.5+
- connexion

## Instructions

#### Install latest version of connexion and swagger.

    $ pip3 install connexion[swagger-ui]
    
Setup bind that a single or more zones can be updated using nsupdate. 

#### Create shared-secret for nsupdate

    $ tsig-keygen update_myzone_de
        key "update_myzone_de" {
            algorithm hmac-sha256;
            secret "qfgD/vb0p+UaFDybowTSMGSrwtfRdtZho3oYyv7zvC8=";
        };

#### Allow zone to be updated with the key
This needs to be done for any zone you want to be able to update via the API.

    zone "myzone.de" {
        type master;
        file "named.myzone.de";
        allow-update { key "update_myzone_de"; };
    };

Restart bind


#### Create keyfile for nsupdate

    $ echo "hmac-sha256:update_myzone_de:<key_from_secret_above>" > update_myzone_de.key
    
#### Run nsupdate test

    $ nsupdate -v -k update_myzone_de.key
    > server 127.0.0.1
    > zone myzone.de
    > update add vs3.myzone.de 340 A 10.11.12.103
    > send
    
#### Check result
     $ dig  vs3.myzone.de @10.0.2.15 +short
     10.11.12.103


## Security

The API is protected by way of an API-Key using a custom <code>X-Api-Key</code> HTTP header. The API should also be served over a secure connection.
