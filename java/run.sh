#! env /bin/zsh

set -e
mvn package
clear
java -cp target/bfi-1.0-SNAPSHOT.jar app.App $@
