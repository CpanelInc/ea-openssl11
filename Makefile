OBS_PROJECT := EA4
OBS_PACKAGE := ea-openssl11
DISABLE_BUILD := arch=i586 repository=CentOS_8 repository=CentOS_9 repository=xUbuntu_20.04 repository=xUbuntu_22.04 repository=Almalinux_10
include $(EATOOLS_BUILD_DIR)obs.mk
