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

            # Bucle de autonomía: Permite a V.E.G.A. reaccionar a sus propios errores
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
                        
                        # NUEVO: Lógica especial para cambios de directorio (cd) persistentes
                        if comando_limpio.startswith("cd "):
                            try:
                                nueva_ruta = comando_limpio.split(" ", 1)[1].strip()
                                os.chdir(nueva_ruta)
                                print(f"{C_VERDE}[+] Directorio cambiado a: {nueva_ruta}{C_RESET}")
                                continue # Pasa al siguiente comando sin romper el ciclo
                            except Exception as e:
                                error_log = f"Error del sistema de archivos: {e}"
                                proceso = subprocess.CompletedProcess(args=comando_limpio, returncode=1, stderr=error_log, stdout="")
                        else:
                            # Ejecución de comandos normales
                            proceso = subprocess.run(comando_limpio, shell=True, capture_output=True, text=True)
                        
                        if proceso.returncode != 0:
                            # Captura y reenvío automático del error
                            error_log = proceso.stderr.strip() or proceso.stdout.strip()
                            print(f"{C_ROJO}[!] ERROR DETECTADO. ENVIANDO LOG A V.E.G.A...{C_RESET}")
                            
                            prompt_actual = f"El comando '{comando_limpio}' ha fallado. Analiza este Log de error: \n{error_log}\nSi es un fallo por parámetros faltantes dímelo. Si es fallo de código/sintaxis, ejecuta el protocolo de derivación a Desktop."
                            hubo_error = True
                            interaccion_activa = True # NUEVO: Asegura que el ciclo siga vivo para que V.E.G.A. conteste
                            break 
                        else:
                            salida = proceso.stdout.strip()
                            if salida:
                                print(f"{C_SISTEMA}[+] SALIDA CONSOLA:{C_RESET}\n{salida[:500]}... [Trunkated]")
                            print(f"{C_VERDE}[+] Ejecución exitosa.{C_RESET}")
                    
                    # Si todos los comandos corrieron bien, ahí sí esperamos al usuario
                    if not hubo_error:
                        interaccion_activa = False 
                else:
                    interaccion_activa = False 

        except KeyboardInterrupt:
            print(f"\n{C_SISTEMA}Interrupción táctica. Apagando agente...{C_RESET}")
            break
