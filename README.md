KaliAD-Wrapper — единый удобный CLI-инструмент, объединяющий наиболее актуальные открытые проверки уязвимостей и техник атак на домены Active Directory (2023–2026 гг.).  
Позволяет специалисту по ИБ за одну команду запустить от 1 до 8 целевых проверок с правами обычного доменного пользователя и получить готовые структурированные отчёты (JSON + HTML).

## Главное меню (v1.3)

1. Уязвимости шаблонов сертификатов AD CS (ESC1–ESC16) — Certipy-AD  
2. Конфигурационные ошибки ACL и избыточные права в объектах AD — ldapsearch  
3. Поиск контроллеров домена (Primary DC + все DC + GC) — nslookup SRV-запросы  
4. Полная энумерация пользователей, групп, AdminCount, RID-brute — NetExec (nxc)  
5. Перечисление пользователей, групп и SMB-ресурсов — enum4linux-ng  
6. Граф путей повышения привилегий (BloodHound All) — bloodhound.py  
7. AS-REP Roasting (T1558.004) — получение хэшей без pre-auth — Impacket GetNPUsers  
8. Kerberoasting (T1558.003) — извлечение TGS-хэшей SPN-учёток — GetUserSPNs.py  

**A.** Запустить ВСЕ проверки  
**0.** Выход

## Быстрый старт

```bash
# 1. Клонирование / распаковка проекта
git clone https://github.com/yourname/KaliAD-Wrapper.git && cd KaliAD-Wrapper

# 2. Установка окружения (одной командой)
bash setup.sh

# 3. Настройка учётных данных
cp .env.example .env
nano .env
# Заполните:
# DOMAIN=corp.local
# USERNAME=testuser
# PASSWORD=Pass123!
# DC_IP=192.168.10.10

# 4. Запуск
python3 main.py
