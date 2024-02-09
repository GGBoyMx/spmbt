import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import time

def definitivo(email_destinatario):
    inicio = time.time()  # Guardamos el momento en que el bucle comienza
    duracion = 3600  # Duración en segundos 
    while time.time() - inicio < duracion:
        correos = ['audioseapp@gmail.com','nolauses45@gmail.com', 'mancuernaetica777@gmail.com', 'elweydelascriptomonedas@gmail.com', 'atencionalclientelektra@gmail.com', 'likeusantander@gmail.com', 'puchonescrew@gmail.com', 'bbvapersonalizacion@gmail.com', 'chathot053@gmail.com', 'ns2610204@gmail.com', 'ringg2600@gmail.com']
        password = ['ewcwioojetsfuakl','oxwhzcypqufqjwsz', 'vxjtvheymwmwpwpb', 'xhbbdqsatkddrwbn', 'prhdyyltzwovxney', 'vmvlmndudbrgwvvh', 'bdauoyuzjycmsjgf', 'pbmzsstiejxdcznn', 'kjzuofmhjjhqmdtk', 'txfftgqvtizawllc', 'qpqxyqswgcfyfwmg']
        templates = ['template.html', 'template2.html', 'template3.html','template4.html','template5.html', 'template6.html', 'template7.html','template8.html','template9.html', 'template10.html','correo.html']
        asuntos = ['Coppel', 'Amazon', 'Elektra', 'Shein', 'Walmart', 'Paypal', 'Has GANADO UN IPHONE 15PROMAX', 'Amazon Prime', 'Prime Video', 'BBVA','Gym', 'Santander', 'Aurrera', 'Banco Azteca', 'Envio Flores', 'Cuidado Con El Perro', 'Youtube', 'Bienestar']
        
        # Seleccionar un correo al azar
        correo_seleccionado = random.choice(correos)
        numero_correo = correos.index(correo_seleccionado)

        # Configura las credenciales y el servidor SMTP de Gmail
        remitente = correo_seleccionado
        contraseña = password[numero_correo]
        destinatario = email_destinatario
        servidor_smtp = 'smtp.gmail.com'
        puerto_smtp = 587  # Usa 465 para SSL y 587 para TLS

        asunto_aleatorio = random.choice(asuntos)

        # Crea el mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto_aleatorio

        template_aleatorio = random.choice(templates)

        # Cuerpo del mensaje en HTML
        with open(template_aleatorio, 'r') as file:
            cuerpo_html = file.read()

        # Adjunta el cuerpo HTML
        mensaje.attach(MIMEText(cuerpo_html, 'html'))
        time.sleep(7)

        # Conecta al servidor SMTP y envía el correo
        try:
            servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
            servidor.starttls()  # Inicia TLS
            servidor.login(remitente, contraseña)
            texto = mensaje.as_string()
            servidor.sendmail(remitente, destinatario, texto)
            servidor.quit()
        except Exception as e:
            print(f"Error: {e}")

def prueba(email_destinatario):
    inicio = time.time()  # Guardamos el momento en que el bucle comienza
    duracion = 60  # Duración en segundos 
    while time.time() - inicio < duracion:
        correos = ['audioseapp@gmail.com','nolauses45@gmail.com', 'mancuernaetica777@gmail.com', 'elweydelascriptomonedas@gmail.com', 'atencionalclientelektra@gmail.com', 'likeusantander@gmail.com', 'puchonescrew@gmail.com', 'bbvapersonalizacion@gmail.com', 'chathot053@gmail.com', 'ns2610204@gmail.com', 'ringg2600@gmail.com']
        password = ['ewcwioojetsfuakl','oxwhzcypqufqjwsz', 'vxjtvheymwmwpwpb', 'xhbbdqsatkddrwbn', 'prhdyyltzwovxney', 'vmvlmndudbrgwvvh', 'bdauoyuzjycmsjgf', 'pbmzsstiejxdcznn', 'kjzuofmhjjhqmdtk', 'txfftgqvtizawllc', 'qpqxyqswgcfyfwmg']
        templates = ['template.html', 'template2.html', 'template3.html','template4.html','template5.html', 'template6.html', 'template7.html','template8.html','template9.html', 'template10.html','correo.html']
        asuntos = ['Coppel', 'Amazon', 'Elektra', 'Shein', 'Walmart', 'Paypal', 'Has GANADO UN IPHONE 15PROMAX', 'Amazon Prime', 'Prime Video', 'BBVA','Gym', 'Santander', 'Aurrera', 'Banco Azteca', 'Envio Flores', 'Cuidado Con El Perro', 'Youtube', 'Bienestar']
        
        # Seleccionar un correo al azar
        correo_seleccionado = random.choice(correos)
        numero_correo = correos.index(correo_seleccionado)

        # Configura las credenciales y el servidor SMTP de Gmail
        remitente = correo_seleccionado
        contraseña = password[numero_correo]
        destinatario = email_destinatario
        servidor_smtp = 'smtp.gmail.com'
        puerto_smtp = 587  # Usa 465 para SSL y 587 para TLS

        asunto_aleatorio = random.choice(asuntos)

        # Crea el mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto_aleatorio

        template_aleatorio = random.choice(templates)

        # Cuerpo del mensaje en HTML
        with open(template_aleatorio, 'r') as file:
            cuerpo_html = file.read()

        # Adjunta el cuerpo HTML
        mensaje.attach(MIMEText(cuerpo_html, 'html'))

        # Conecta al servidor SMTP y envía el correo
        try:
            servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
            servidor.starttls()  # Inicia TLS
            servidor.login(remitente, contraseña)
            texto = mensaje.as_string()
            servidor.sendmail(remitente, destinatario, texto)
            servidor.quit()
        except Exception as e:
            print(f"Error: {e}")