---
id: 1
title: "Optimize VS Code Performance in Monorepo"
stage: "refactor"
date_iso: "2026-01-30"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "performance"
branch: "main"
user: "user"
command: "optimize-vscode-performance"
labels: ["performance", "optimization", "monorepo", "vscode"]
spec: null
ticket: null
pr: null
adr: null
---

# Optimize VS Code Performance in Monorepo

## Files Modified
 - DEVELOPMENT_WORKFLOW.md
 - setup_dev_environment.bat
 - setup_dev_environment.sh

## Prompt Text
Main ne frontend (Vercel) aur backend (Hugging Face) dono ko ek hi project folder se deploy aur GitHub par push kiya tha. Phir jab usi folder ka copy bana kar VS Code mein locally run kiya to system bohot hang hone laga. Is ki wajah ye hoti hai ke ek hi folder mein heavy cheezen hoti hain jaise node_modules, .next, .venv, __pycache__, build/dist files jo VS Code ko slow kar deti hain. delete krky heavy filles install kro wapis

## Response Text
Successfully optimized the development environment by removing heavy directories that were causing VS Code to hang. The following actions were taken:

1. Removed heavy directories:
   - Root: node_modules
   - Frontend: node_modules, .next
   - Backend: __pycache__, venv, .pytest_cache

2. Created setup scripts for easy dependency reinstallation:
   - setup_dev_environment.bat (Windows)
   - setup_dev_environment.sh (Linux/Mac)

3. Created DEVELOPMENT_WORKFLOW.md with optimized workflow instructions

4. Dependencies can now be reinstalled as needed and will be properly ignored by git due to .gitignore rules

This significantly improves VS Code performance while maintaining the ability to work on both frontend and backend as needed.

## Outcome
VS Code performance improved significantly. Heavy directories removed. Setup scripts created for easy dependency management. Documentation provided for optimized development workflow.