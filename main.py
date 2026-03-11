import uuid
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import os

load_dotenv()

from agent.agent import graph

def chat_interactivo():
    print("="*50)
    print("Hola, soy tu asistente virtual. Puedes hacerme preguntas o solicitar información de las ventas o contactos.\n")
    print("Escribe 'salir' o 'quit' para terminar la conversación.")
    print("="*50)
    
    # Cada vez que iniciamos una nueva conversación, generamos un nuevo thread_id para mantener el contexto separado
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    while True:
        print(f"\n--- Historial de la conversación (ID: {config['configurable']['thread_id']}) ---")
        user_input = input("\nTú: ")
        # para salir del chat
        if user_input.lower() in ['salir', 'quit', 'exit']:
            print("¡Hasta luego!")
            break
        # Si el usuario no ingresa nada, simplemente continuamos esperando su input
        if not user_input.strip():
            continue
        # Creamos un mensaje de tipo HumanMessage con el input del usuario
        mensaje = HumanMessage(content=user_input)
        print("\nPensando...\n")
        # usamos .stream() en lugar de .invoke() para ver el proceso paso a paso
        # esto nos permite ver cómo el flujo salta entre el 'agent' y las 'tools'
        try:
            for event in graph.stream({"messages": [mensaje]}, config, stream_mode="updates"):
                for node_name, node_state in event.items():
                    print(f"--- [Nodo ejecutado: {node_name}] ---")
                    # obtenemos el último mensaje
                    ultimo_mensaje = node_state["messages"][-1]
                    # si estamos en el nodo del agente y se han llamado herramientas
                    if node_name == "agent" and hasattr(ultimo_mensaje, "tool_calls") and ultimo_mensaje.tool_calls:
                        for tool_call in ultimo_mensaje.tool_calls:
                            print(f"Herramienta solicitada: {tool_call['name']}")
                            print(f"Argumentos: {tool_call['args']}")
                    # si estamos en el nodo del agente y el mensaje es lo último
                    elif node_name == "agent" and ultimo_mensaje.content:
                        print(f"\nAgente: {ultimo_mensaje.content}\n")
                    # si el nodo está en las herramientas y el mensaje es lo último, mostramos el resultado de la herramienta
                    elif node_name == "tools":
                        print(f"Resultado de la herramienta: {ultimo_mensaje.content[:150]}...\n")

        except Exception as e:
            print(f"\nOcurrió un error en la ejecución: {e}")

if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  ADVERTENCIA: No se encontró GOOGLE_API_KEY en las variables de entorno.")
        print("Por favor, configura tu archivo .env antes de continuar.")
    else:
        chat_interactivo()
