# Role Netfliter

## Utilisation 

Pousser sur la machine cible, via le role d'installation de chaque COTS un fichier définissant les regles propres à ce COTS. 

Les fichiers doivent être préfixés par `ipt_` et placés dans le dossier `/etc/sysconfig/netfilter.d`

```

###
# Configuration du firewall 
#
# Nom du fichier : ipt_*
#
# Format: (in|out|for).<netif>.<protocol>.(dpt|spt).<port>.(pass|drop)
# OR (in|out|for).<netif>.icmp.type.(any|<icmp_type>).(pass|drop)
#
# ex.: in.eth0.tcp.dpt.ssh.pass
# -A INPUT -i eth0 -m tcp -p tcp --dport ssh -m conntrack \
#   --ctstate NEW,ESTABLISHED -j IN.ETH0.TCP.DPT.SSH.PASS
# -A IN.ETH0.TCP.DPT.SSH.PASS -j LOG --log-level info \
#   --log-prefix  in.eth0.tcp.dpt.ssh.pass
# -A IN.ETH0.TCP.DPT.SSH.PASS -j ACCEPT
# Longueur max d'une chaine 29 caractères.
#
out.eth0.icmp.type.any.pass
out.eth0.tcp.dpt.ssh.pass
out.eth0.tcp.dpt.http.pass
out.eth0.tcp.dpt.https.pass
out.eth0.tcp.dpt.ldap.pass
out.eth0.tcp.dpt.ldaps.pass
out.eth0.tcp.dpt.domain.pass
out.eth0.udp.dpt.domain.pass
out.eth0.tcp.dpt.ntp.pass
out.eth0.udp.dpt.ntp.pass
###
# EOF
#

```