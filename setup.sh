#!/bin/bash
echo "╔════════════════════════════════════════╗"
echo "║     Установка KaliAD-Wrapper v1.2      ║"
echo "║        + NetExec      ║"
echo "╚════════════════════════════════════════╝"

sudo apt update -qq
sudo apt install -y ldap-utils dnsutils netexec enum4linux-ng bloodhound.py python3-pip python3-venv impacket-scripts

pip3 install -r requirements.txt
pip3 install certipy-ad bloodhound impacket

mkdir -p reports templates bloodhound

echo "✅ Установка завершена!"
echo "➜ cp .env.example .env && nano .env"
echo "➜ Запуск: python3 main.py"