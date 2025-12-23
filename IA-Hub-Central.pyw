import tkinter as tk
from tkinter import ttk, scrolledtext
import threading, requests, os
from datetime import datetime

OLLAMA_URL = "http://localhost:11434"
COMET_URL = "http://localhost:5000"
DEFAULT_MODEL = "llama3.2:latest"

MANUS_KW = ["browser","pesquisar","pesquise","internet","site","desktop","arquivo","instalar","executar","api","docker","git","baixar","email","abrir","abra","navegador","obsidian","nota","sistema","windows","powershell"]
LLAMA_KW = ["simples","traduzir","resumir","explicar","definir","calcular","o que","como funciona","quanto","traduza","explique"]

def check_ollama():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        return r.status_code == 200
    except:
        return False

def check_manus():
    try:
        r = requests.get(f"{COMET_URL}", timeout=3)
        return r.status_code == 200
    except:
        return False

def send_ollama(p, m=DEFAULT_MODEL):
    try:
        r = requests.post(f"{OLLAMA_URL}/api/generate", json={"model": m, "prompt": p, "stream": False}, timeout=120)
        return r.json().get("response", "Erro") if r.status_code == 200 else f"Erro {r.status_code}"
    except Exception as e:
        return str(e)

def send_manus(p):
    return f"[MANUS] Abra manus.im e envie:\n{p}"

def decide(p):
    pl = p.lower()
    ms = sum(1 for k in MANUS_KW if k in pl)
    ls = sum(1 for k in LLAMA_KW if k in pl)
    return "manus" if ms > ls else "llama"

class App:
    def __init__(s, r):
        s.root = r
        r.title("Hub IA - Manus+Llama")
        r.geometry("700x500")
        r.configure(bg="#1a1a2e")
        
        tk.Label(r, text="HUB CENTRAL DE IA", font=("Segoe UI", 16, "bold"), fg="#00d4ff", bg="#1a1a2e").pack(pady=10)
        
        sf = tk.Frame(r, bg="#252540")
        sf.pack(fill=tk.X, padx=10)
        s.ost = tk.Label(sf, text="Llama: ...", fg="#888", bg="#252540")
        s.ost.pack(side=tk.LEFT, padx=10, pady=5)
        s.cst = tk.Label(sf, text="Manus: ...", fg="#888", bg="#252540")
        s.cst.pack(side=tk.LEFT, padx=10)
        
        tk.Label(r, text="Manus: / Llama: / ou deixe em branco", fg="#888", bg="#1a1a2e").pack(anchor=tk.W, padx=10, pady=(10, 0))
        s.inp = tk.Text(r, height=2, bg="#252540", fg="#fff", insertbackground="#fff")
        s.inp.pack(fill=tk.X, padx=10, pady=5)
        s.inp.bind("<Return>", s.on_enter)
        
        bf = tk.Frame(r, bg="#1a1a2e")
        bf.pack(fill=tk.X, padx=10)
        s.btn = tk.Button(bf, text="Enviar", command=s.send, bg="#00d4ff", fg="#000")
        s.btn.pack(side=tk.LEFT)
        tk.Button(bf, text="Manus", command=lambda: s.send("manus"), bg="#ff6b6b", fg="#000").pack(side=tk.LEFT, padx=5)
        tk.Button(bf, text="Llama", command=lambda: s.send("llama"), bg="#4ecdc4", fg="#000").pack(side=tk.LEFT)
        
        s.out = scrolledtext.ScrolledText(r, bg="#0d0d1a", fg="#fff", wrap=tk.WORD)
        s.out.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        s.out.tag_config("m", foreground="#ff6b6b")
        s.out.tag_config("l", foreground="#4ecdc4")
        s.out.tag_config("i", foreground="#888")
        
        s.check_status()
        s.auto_check()
        s.log("Hub iniciado! Use Manus: ou Llama: como prefixo", "i")
    
    def check_status(s):
        def c():
            ollama_ok = check_ollama()
            manus_ok = check_manus()
            s.ost.config(text="Llama: OK" if ollama_ok else "Llama: OFF", fg="#4ecdc4" if ollama_ok else "#f44")
            s.cst.config(text="Manus: OK" if manus_ok else "Manus: OFF", fg="#ff6b6b" if manus_ok else "#f44")
        threading.Thread(target=c, daemon=True).start()
    
    def auto_check(s):
        s.check_status()
        s.root.after(5000, s.auto_check)
    
    def log(s, m, t="i"):
        ts = datetime.now().strftime("%H:%M:%S")
        s.out.insert(tk.END, f"[{ts}] {m}\n", t)
        s.out.see(tk.END)
    
    def on_enter(s, e):
        if not e.state & 1:
            s.send()
            return "break"
    
    def send(s, f=None):
        p = s.inp.get("1.0", tk.END).strip()
        if not p:
            return
        s.inp.delete("1.0", tk.END)
        
        r, cp = f, p
        if not r:
            if p.lower().startswith("manus:"):
                r, cp = "manus", p[6:].strip()
            elif p.lower().startswith("llama:"):
                r, cp = "llama", p[6:].strip()
            else:
                r = decide(p)
        
        def proc():
            s.btn.config(state=tk.DISABLED)
            if r == "manus":
                s.log(f"Manus: {cp}", "m")
                s.log(send_manus(cp), "m")
            else:
                s.log(f"Llama: {cp}", "l")
                s.log(send_ollama(cp), "l")
            s.btn.config(state=tk.NORMAL)
        threading.Thread(target=proc, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
