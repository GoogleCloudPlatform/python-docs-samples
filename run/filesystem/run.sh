#!/bin/sh
# Copy/paste only the section(s) for the file system(s)
# that you have actually set up

# Cloud Filestore
echo "mounting Cloud Filestore"
mount -o nolock 10.45.51.106:/vol1 /mnt/nfs/filestore

# # Cloud Storage FUSE
# echo "mounting Cloud Storage bucket"
# gcsfuse --debug_gcs --debug_fuse <bucket name> /mnt/gcs

# # NFS Server
# echo "mounting NFSv4 share"
# mount -t nfs4 -o nolock <IP_ADDRESS>:/mnt/fileserver /mnt/nfs/fileserver

# # NBD
# echo "mounting ext4 image via NBD"
# nbd-client -L -name image <IP_ADDRESS> /dev/nbd0
# mount /dev/nbd0 /mnt/nbd/image

# # PD-SSD via NBD
# echo "mounting PD-SSD via NBD"
# nbd-client -L -name disk <IP_ADDRESS> /dev/nbd1
# mount /dev/nbd1 /mnt/nbd/disk

# # 9P
# echo "mounting 9p export"
# mount -t 9p \
#   -otrans=tcp,aname=/mnt/diod,version=9p2000.L,uname=root,access=user \
#   <IP_ADDRESS> /mnt/9p/tcp

# # SMB
# echo "mounting SMB public share"
# mount -t cifs -ousername=<USERNAME>,password=<PASSWORD>,ip=<IP_ADDRESS> \
#   //fileserver/public /mnt/smb/public

# echo "mounting SMB home directory"
# mount -t cifs -ousername=<USERNAME>,password=<PASSWORD>,ip=<IP_ADDRESS> \
#   //fileserver/homes /mnt/smb/homes

echo "mounts completed"
exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
