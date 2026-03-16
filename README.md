# KaliAD-Wrapper

# KaliAD-Wrapper v1.2

Автономный wrapper для пентеста Active Directory на Kali Linux.

**Модули:**
- Certipy-AD
- LDAP Enumeration
- DNS Enumeration
- NetExec (nxc)
- enum4linux-ng
- BloodHound
- Impacket (secretsdump + AS-REP)
- Kerberoasting

Автоматический HTML-отчёт + JSON.


chmod +x setup.sh
./setup.sh
cp .env.example .env
nano .env
python3 main.py
