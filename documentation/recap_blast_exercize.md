# Repeated 'trivial search' vs BLAST vs BWA exercize

1. Instantiated RHEL-7.6\_HVM\_GA-20190128-x86\_64-0-Hourly2-GP2 from scratch
2. Searched for BDP1 volume in 'Public Snapshots'
	* Actions
	* Create Image
		* us east 1 b (!)
3. Go to 'Volumes' tab
	* Select
	* Actions
	* Attach Volume
		* Select my new instance (name = main)
4. Attach Volume to the new instance in the terminal
Careful do NOT format !!!

'sudo su -'

'yum install -y vim'

'df -h'

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/xvda2       10G  923M  9.1G  10% /
devtmpfs        473M     0  473M   0% /dev
tmpfs           495M     0  495M   0% /dev/shm
tmpfs           495M   13M  482M   3% /run
tmpfs           495M     0  495M   0% /sys/fs/cgroup
tmpfs            99M     0   99M   0% /run/user/1000
```

'fdisk -l'


```
fdisk -l
WARNING: fdisk GPT support is currently new, and therefore in an experimental phase. Use at your own discretion.

Disk /dev/xvda: 10.7 GB, 10737418240 bytes, 20971520 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: gpt
Disk identifier: B45D8550-49E7-49A1-91C3-B53A07DFD691


#         Start          End    Size  Type            Name
 1         2048         4095      1M  BIOS boot       
 2         4096     20971486     10G  Microsoft basic 

Disk /dev/xvdf: 107.4 GB, 107374182400 bytes, 209715200 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x4a070c91

    Device Boot      Start         End      Blocks   Id  System
/dev/xvdf1            2048   209715199   104856576   83  Linux
```

	* /dev/xvdf1 needs to be attached
	*  'vim /etc/fstab'

Appending the following line:

```
/dev/xvdf1     /data  ext4 defaults 0 0
```

That way the disk will be automatically mounted on /data upon boot

Mounting: 'mount -a'
`ll`  `/data` to see if it worked.

5. Installing BLAST
 `yum localinstall ncbi-blast-2.7.1+-1.x86_64.rpm`
6. Copying data into home (he's still in root mode dont know why...)
`cp /data/BDP1_2020/trivial/trivial_str_search.py .`
`cp /data/BDP1_2020/trivial/shining.txt.gz .`

6. Inspecting the gunzipped shining.txt
```
head -4 shining.txt
All work and no play makes Jack a dull boy
All work and no play makes Jack a dull boy
All work and no play makes Jack a dull boy
All work and no play makes Jack a dull boy
```

Generating a checksum to be compared to the one in other repo:
```
md5sum shining.txt
bef7a21132a8a1f16d4b87d08e2298ae  shining.txt
[root@~]# cat /data/BDP1_2020/trivial/md5_shining.txt
bef7a21132a8a1f16d4b87d08e2298ae  shining.txt
```
7. Running the trivial python search:
```
[~]# ./trivial_str_search.py
Reading from file: shining.txt
File read.
First characters of reference =  
current_reference_length =  42000000
mem used by reference = 42000037 bytes
Searchinig the word dull
in reference string 
word length =  4

1 Iteration took: 5.15992808342 seconds
current_reference_length =  42000000
mem used by reference = 42000037 bytes
Number of occurrences = 1000000
```

8. Indexing the database:
`makeblastdb -in entire_hg19.fa -out entire_hg19BLAST -dbtype nucl  -parse_seqid`
ALLREADY done do not run - takes time
DB file is in: `ll /data/BDP1_2020/hg19/`

9. Inspecting patient files:
```
less /data/BDP1_2020/hg19/Patients/patient1/read_98.fa
>chr1_read_20
aaaaccacaatgagataccacctcacaccagtcaaatggctattactaaaaagtgaaaaacaaaaaacaaaaaaacagattctggtaacgttgcagagaaatgggaaatagttcagccactgtggaaagcagtttggaggtttctcagag
>chr1_read_21
aacttaaaatagaactacgattcaacccaacaaccctattactgggtatacagccaaaggaatataagtcattctaccataaagacacatgcacgtgaatgttcatcgcagcactattcagaatagcaaagacatagaatcaacctggat
>chr1_read_22
tcccatcaacagtggactggataaagagaacatggtacatatacaccatgcaatactacatagccataaaaatgagattatgtcttttgcaataacatggatggagttggagccattatcctaagtaaattaatgcaggaacagaaaacc
>chr1_read_23
aaataccacatgttctcacttataagtgagtgctaaacatcgtgtacgcatggacacaaaaaaagggaacaatagatactggggcctacttgagggtggacagtgggaaagtgtgaggaatgtaaacctacaggttgggtactacgctga
[ ~]# 
[ ~]# wc -l /data/BDP1_2020/hg19/Patients/patient1/read_98.fa 
2000 /data/BDP1_2020/hg19/Patients/patient1/read_98.fa
```

9. Moving query to home:
`cp /data/BDP1_2020/hg19/myread.fa .`

10. Running BLAST using the time module in bash
```
[~]# time blastn -db /data/BDP1_2020/hg19/entire_hg19BLAST -query myread.fa -out blast_myread.out

real	3m10.420s
user	0m0.531s
sys	0m0.473s
```
&rarr; forgot to upgrade instance from micro - so mine took longer...

11. In the mean time we can check the load with 'top' in a new tab :)

12. Checking out the output: `less blast_myread.out'
```
Query= myread

Length=150
                                                                      Score     E
Sequences producing significant alignments:                          (Bits)  Value

chrY                                                                  278     7e-73
chrX                                                                  278     7e-73
chr16                                                                 267     2e-69
chr9                                                                  167     2e-39
chr18                                                                 167     2e-39


>chrY 
Length=59373566

 Score = 278 bits (150),  Expect = 7e-73
 Identities = 150/150 (100%), Gaps = 0/150 (0%)
 Strand=Plus/Plus

Query  1         CCAAAGTGCTAGGATTACGGGCGTTAGCCACCACACACTGCCTGATTTTCTTTCTATCAT  60
                 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
Sbjct  59350301  CCAAAGTGCTAGGATTACGGGCGTTAGCCACCACACACTGCCTGATTTTCTTTCTATCAT  59350360

Query  61        CAGCAATAATGTATAGGAATAATTTGAACTTGAAATTTGaaaaaaaTACCATTTACAATA  120
                 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
Sbjct  59350361  CAGCAATAATGTATAGGAATAATTTGAACTTGAAATTTGAAAAAAATACCATTTACAATA  59350420

Query  121       GCATTCCCAAATTTAATTTATTAGGTATAA  150
                 ||||||||||||||||||||||||||||||
Sbjct  59350421  GCATTCCCAAATTTAATTTATTAGGTATAA  59350450

```

13. Installing BWA `cp /data/BDP1_2020/hg19/bwa-0.7.15.tar .` and `yum install -y gcc gcc-c++`


