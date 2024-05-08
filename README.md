# Evilx
remote access tool with python
### about :
EVILX.py is a C2 tool that offers generating an obfuscated payload and receiving reverse shell from compromised machines.
### features :
- generating an obfuscated python code (payload.py)
- offers a one liner stager to stage the payload and execute it in memory ( filess infection )
- download/upload files to or from the compromised machine
- execute shell commands on compromised machine

### installation :
clone the github repo 
```
git clone https://github.com/o-sec/Evilx.git
```
install dependencies 
```
pip install -r requirements.txt
```

### usage :
run 
```
python3 EVILX.py
```
<img src='https://raw.githubusercontent.com/o-sec/Evilx/main/Screenshot_main.png' />
1) - generate a payload (obfuscated payload)
<img src='https://raw.githubusercontent.com/o-sec/Evilx/main/Screenshot_payload_creator.png' />

2) - start a listener
<img src='https://raw.githubusercontent.com/o-sec/Evilx/main/Screenshot_listener.png' />

<img src='https://raw.githubusercontent.com/o-sec/Evilx/main/Screenshot_reverse_shell.png' />

### disclaimer :
i am not responsable for whatever you do with this tool !
