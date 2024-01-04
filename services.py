# services.py nos ayuda a gestionar el envio de mensajes a wp 

import requests 
import sett
import json 
import time

def obtener_mensaje_whatsapp(message): 
    if 'type' not in message: 
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text': 
        text = message['text']['body']

    elif typeMessage == 'button': 
        text = message['button']['test']


    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

    return text 

def enviar_mensaje_whatsapp(data): 
    try: 
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url 
        headers = {'Content-Type': 'application/json', 
                   'Authorization': 'Bearer' + whatsapp_token}
        response = requests.post(whatsapp_url, 
                                 headeers = headers, 
                                 data = data)
        
        if response.status_code == 200: 
            return 'mensaje enviado', 200
        else: 
            return 'error al enviar mensaje', response.status_code
        
    except Exception as e: 
        return e, 403

def text_message(number, text): 
    data = json.dumps(

        {
    "messaging_product": "whatsapp",    
    "recipient_type": "individual",
    "to": number,
    "type": "text",
    "text": {
        "body": text
    }
}
    )
    return data 



def buttonReply_Message(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data


def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data


def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def administrar_chatbot(text, number, messageId, name):
    text = text.lower() # mensaje que envió el usuario 
    list = []


    if "hola" in text:
        body = "¡Hola! 👋 Bienvenido al chatbot de vida y campo. ¿Cómo podemos ayudarte hoy?"
        footer = "Equipo vida y campo"
        options = ["✅ aprender", "✏️  realizar evaluación"]

    
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        list.append(replyButtonData)

    elif "aprender" in text:
        body = "Tenemos varias áreas de consulta para capacitarte. ¿Cuál de estos sistemas productivos te gustaría explorar?"
        footer = "Equipo vida y campo"
        options = ["Café", "Cacao", "Miel"]

        listReplyData = listReply_Message(number, options, body, footer, "sed2",messageId)

        list.append(listReplyData)

    elif "evaluación" in text:
        calificacion = 0 
        body = "Pregunta prueba. ¿El cacao es una planta?"
        footer = "Equipo vida y campo"
        options = ["✅ Sí, es una planta", "⛔ No, no es una planta"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)

        if "Sí" in text: 
            calificacion += 1 
    

        body = "Buenísima elección. ¿Te gustaría que te enviara un documento PDF con tu certificado?"
        footer = "Equipo vida y campo"
        options = ["✅ Sí, envía el PDF.", "⛔ No, gracias"]
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData)

    elif "sí, envía el pdf" in text:

        textMessage = text_message(number,"Claro, por favor espera un momento.")

        enviar_mensaje_whatsapp(textMessage)
        time.sleep(3)

        document = document_Message(number, sett.document_url, "Listo 👍🏻", "Inteligencia de Negocio.pdf")
        enviar_mensaje_whatsapp(document)
        time.sleep(3)


    else :
        data = text_message(number,"Lo siento, no entendí lo que dijiste. ¿Quieres que te ayude con alguna de estas opciones?")
        list.append(data)

    for item in list:
        enviar_mensaje_whatsapp(item)

#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    if s.startswith("521"):
        return "52" + s[3:]
    else:
        return s



    data = text_message(number, "Saludos del equipo Vida y Campo")
    enviar_mensaje_whatsapp(data) 





