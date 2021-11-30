#!/bin/bash
/usr/bin/cp certs/10.0.0.5.* ../reverse_proxy/ssl/
/usr/bin/cp certs/10.0.0.10.* ../core/ssl/
/usr/bin/cp certs/10.0.0.20.* ../web/ssl/ 
/usr/bin/cp certs/10.0.0.30.* ../mysql/ssl/ 
/usr/bin/cp certs/10.0.0.31.* ../mysql_store/ssl/ 
/usr/bin/cp certs/10.0.0.40.* ../logging_store/ssl/
/usr/bin/cp certs/10.0.0.41.* ../logging_view/ssl/
/usr/bin/cp certs/10.0.0.42.* ../logging_rsyslog/ssl/
/usr/bin/cp certs/10.0.0.50.* ../backup/ssl/

/usr/bin/cp myCA.pem ../backup/imovies_internal.crt
/usr/bin/cp myCA.pem ../core/imovies_internal.crt
/usr/bin/cp myCA.pem ../logging_store/imovies_internal.crt
/usr/bin/cp myCA.pem ../logging_view/imovies_internal.crt
/usr/bin/cp myCA.pem ../logging_rsyslog/imovies_internal.crt
/usr/bin/cp myCA.pem ../mysql/imovies_internal.crt
/usr/bin/cp myCA.pem ../mysql_store/imovies_internal.crt
/usr/bin/cp myCA.pem ../reverse_proxy/imovies_internal.crt
/usr/bin/cp myCA.pem ../web/imovies_internal.crt








