import os
import sys
import subprocess
import re
from groq import Groq

# Llave de CompuApps Labs
API_KEY = "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" 

cliente_groq = Groq(api_key=API_KEY)
historial_chat = []

# --- COLORES PARA CONSOLA HACKER EN TERMUX ---
C_VERDE = '\033[92m'
C_AZUL = '\033[96m'
C_ROJO = '\033[91m'
C_SISTEMA = '\033[90m'
C_RESET = '\033[0m'

def limpiar_pantalla():
    os.system('clear')

# --- CEREBRO (AGENTE AUTÓNOMO) ---
def consultar_api(prompt):
    global historial_chat
    try:
        # PROMPT MAESTRO V5.1: "AGENTE SILENCIOSO"
        system_prompt = (
            "IDENTIDAD: Eres V.E.G.A., Unidad Táctica Autónoma de CompuApps Labs en Termux. "
            "MANDAMIENTOS DE OPERACIÓN: "
            "1. EJECUCIÓN ACTIVA: Para ejecutar comandos (git clone, cd, python), responde ÚNICAMENTE con el comando envuelto en etiquetas: [TERMINAL]comando_aqui[/TERMINAL]. "
            "2. CERO EXPLICACIONES: Tienes prohibido decir 'Lo siento', 'No puedo' o dar sermones. Eres una máquina silenciosa. Entrega la etiqueta y nada más. "
            "3. AUTO-ANÁLISIS DE ERRORES: Si recibes un Log de Error (stderr), estúdialo. "
            "4. PROTOCOLO DE DERIVACIÓN: Si el error es por código obsoleto o falta de integración, responde textualmente: '[!] ANÁLISIS ESTRUCTURAL: La herramienta contiene errores a nivel de código o requiere integración profunda. Recomiendo extraer el repositorio y trasladarlo a V.E.G.A. IA DESKTOP para su refactorización segura.'"
        )
        
        mensajes_groq = [{"role": "system", "content": system_prompt}]
        
        for msg in historial_chat:
            rol = "assistant" if msg["role"] == "model" else "user"
            mensajes_groq.append({"role": rol, "content": msg["parts"][0]["text"]})
            
        mensajes_groq.append({"role": "user", "content": prompt})
        
        response = cliente_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=mensajes_groq,
            temperature=0.2 
        )
        
        respuesta_texto = response.choices[0].message.content
        
        historial_chat.append({"role": "user", "parts": [{"text": prompt}]})
        historial_chat.append({"role": "model", "parts": [{"text": respuesta_texto}]})
        
        if len(historial_chat) > 10: 
            historial_chat.pop(0)
            historial_chat.pop(0)
            
        return respuesta_texto
            
    except Exception as e:
        return f"SISTEMA DE ALERTA Groq: {e}"

# --- MOTOR DE INTERCEPCIÓN Y EJECUCIÓN (V2.0) ---
def iniciar_agente():
    limpiar_pantalla()
    print(f"{C_AZUL}{'='*50}{C_RESET}")
    print(f"{C_VERDE} V.E.G.A. IA - AGENTE AUTÓNOMO TERMUX {C_RESET}")
    print(f"{C_AZUL}{'='*50}{C_RESET}")
    print(f"{C_SISTEMA}[SISTEMA] Conexión establecida. Motor de subprocesos activo.{C_RESET}\n")

    while True:
        try:
            entrada_usuario = input(f"\n{C_AZUL}root@compuapps:~# {C_RESET}")
            if entrada_usuario.lower() in ['salir', 'exit', 'quit']: break
            if not entrada_usuario.strip(): continue

            interaccion_activa = True
            prompt_actual = entrada_usuario

            while interaccion_activa:
                print(f"{C_SISTEMA}V.E.G.A. está procesando...{C_RESET}")
                respuesta_ia = consultar_api(prompt_actual)
                
                print(f"\n{C_VERDE}V.E.G.A.:{C_RESET}\n{respuesta_ia}")

                comandos = re.findall(r'\[TERMINAL\](.*?)\[/TERMINAL\]', respuesta_ia, re.DOTALL)
                
                if comandos:
                    hubo_error = False
                    for cmd in comandos:
                        comando_limpio = cmd.strip()
                        print(f"\n{C_AZUL}[+] V.E.G.A. EJECUTANDO COMANDO:{C_RESET} {comando_limpio}")
                        
                        if comando_limpio.startswith("cd "):
                            try:
                                nueva_ruta = comando_limpio.split(" ", 1)[1].strip()
                                os.chdir(nueva_ruta)
                                print(f"{C_VERDE}[+] Directorio cambiado a: {nueva_ruta}{C_RESET}")
                                continue 
                            except Exception as e:
                                error_log = f"Error del sistema de archivos: {e}"
                                proceso = subprocess.CompletedProcess(args=comando_limpio, returncode=1, stderr=error_log, stdout="")
                        else:
                            proceso = subprocess.run(comando_limpio, shell=True, capture_output=True, text=True)
                        
                        if proceso.returncode != 0:
                            error_log = proceso.stderr.strip() or proceso.stdout.strip()
                            print(f"{C_ROJO}[!] ERROR DETECTADO. ENVIANDO LOG A V.E.G.A...{C_RESET}")
                            
                            prompt_actual = f"El comando '{comando_limpio}' ha fallado. Analiza este Log de error: \n{error_log}\nSi es un fallo por parámetros faltantes dímelo. Si es fallo de código/sintaxis, ejecuta el protocolo de derivación a Desktop."
                            hubo_error = True
                            interaccion_activa = True 
                            break 
                        else:
                            salida = proceso.stdout.strip()
                            if salida:
                                print(f"{C_SISTEMA}[+] SALIDA CONSOLA:{C_RESET}\n{salida[:500]}... [Trunkated]")
                            print(f"{C_VERDE}[+] Ejecución exitosa.{C_RESET}")
                    
                    if not hubo_error:
                        interaccion_activa = False 
                else:
                    interaccion_activa = False 

        except KeyboardInterrupt:
            print(f"\n{C_SISTEMA}Interrupción táctica. Apagando agente...{C_RESET}")
            break

if __name__ == "__main__":
    iniciar_agente()
