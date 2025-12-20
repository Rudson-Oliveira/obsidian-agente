@echo off
cd /d C:\Users\rudpa\obsidian-agente\frontend
rmdir /s /q dist 2>nul
call npm run build
echo Build concluido!
