#!/bin/bash

set -e

output() {
    printf '\E[36m'; echo "$@"; printf '\E[0m' 
}

# posix compliant sanity check
if [ -z $BASH ] || [  $BASH = "/bin/sh" ]; then
    echo "Please use the bash interpreter to run this script"
    exit 1
fi

# Install Drush (Drupal CLI)
command -v drush &>/dev/null || {
    output "Installing Drush (Drupal shell)"
    sudo pear channel-discover pear.drush.org
    sudo pear install drush/drush
}

output "Installing Drupal site"

# To run Drush, we need to be in the Drupal directory
cd $HOME/data50/drupal
sudo drush site-install --db-su=root --db-su-pw=crimson --db-url=mysql://jharvard:crimson@localhost/data50 --site-name=CS50 --account-name=jharvard --account-pass=crimson
cd $HOME/data50

# chmod ~, ~/data50, and ~/data50/drupal so that Apache can read it
# we keep rw privs for jharvard, but everyone else just gets x
chmod u=rwx,go=x $HOME/{,data50/{,drupal/}}

# make sure we have a logs/ directory; otherwise, Apache won't start
if [ ! -d $HOME/data50/logs ] ; then
    output "Creating directory $HOME/data50/logs"
    mkdir $HOME/data50/logs
fi

output "Configuring data50 vhost"
sudo cp $HOME/data50/config/data50.conf /etc/httpd/conf.d/
sudo chown root:root /etc/httpd/conf.d/data50.conf
sudo chmod u=rw,go=r /etc/httpd/conf.d/data50.conf
sudo /etc/init.d/httpd restart

output "Fixing permissions on $HOME/data50/drupal/"
command $HOME/data50/scripts/fix_permissions.sh

echo "Website should now be available at http://localhost/. Log in with jharvard/crimson."
