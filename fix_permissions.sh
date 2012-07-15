#!/bin/bash

set -e

# See http://drupal.org/node/244924 for details on securing Drupal files.
DRUPAL_DIR="$HOME/data50/drupal"

# Since we ran Drush with sudo, any files it created will be owned by root:root
# Change that so that jharvard:apache has access.
sudo chown -R jharvard:apache $DRUPAL_DIR

# Make sure all directories are 750. We use this instead of 755 since everything
# is already part of the apache group, so apache won't have trouble.
find $DRUPAL_DIR -type d -exec sudo chmod u=rwx,g=rx,o= '{}' \;

# Ensure files are 640. Again, since files are part of the apache group, our
# server shouldn't have any trouble.
find $DRUPAL_DIR -type f -exec sudo chmod u=rw,g=r,o= '{}' \;

# Both jharvard and the apache group need read-write-execute access to all
# directories in the $DRUPAL_DIR/sites/files dir and read-write access to all
# files in that directory.
find $DRUPAL_DIR/sites -type d -name files -exec sudo chmod ug=rwx,o= '{}' \;
for d in $DRUPAL_DIR/sites/*/files ; do
    find $d -type d -exec sudo chmod ug=rwx,o= '{}' \;
    find $d -type f -exec sudo chmod ug=rw,o= '{}' \;
done