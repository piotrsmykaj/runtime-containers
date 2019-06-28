FROM php:$version

LABEL description="This image is used to create continuousphp containers" vendor="continuousphp" version="1.0"

MAINTAINER Pierre Tomasina <pierre.tomasina@continuousphp.com>
MAINTAINER Oswald De Riemaecker <oswald@continuousphp.com>

;components/debian/init_cphp_env.dm

;components/debian/init_cphp_package.dm
# SSH login fix. Otherwise user is kicked off after login
;components/debian/ssh_login_fix.dm
#
# Setting cphp user
#
;components/debian/setting_cphp_user.dm
#
# Bootstrap CPHP Dependencies
#
;components/debian/bootstrap_cphp_dep.dm
#
# Installing "n" the nodejs mutli versions support
#
;components/debian/n.dm
#
# Install pip and famous tools coid
#
;components/debian/pip_and_coid.dm
#
# Installing Azure Cli
#
;components/debian/azure_cli.dm
#
# Install terraform tools
#
;components/debian/terraform.dm
