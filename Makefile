OBS_PROJECT := EA4
OBS_PACKAGE := ea-openssl11
DISABLE_BUILD := arch=i586 repository=CentOS_8 repository=CentOS_9 repository=Almalinux_10
include $(EATOOLS_BUILD_DIR)obs.mk
