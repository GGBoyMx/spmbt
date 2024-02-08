from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
import mysql.connector
import correo
import threading

TOKEN = '6503956909:AAHQvwJuNVOZASW7NyocoqRd2SptXO8YINA'
USUARIO = '@Spam_Polar_Bot'
DUENO = '@Polar777XD'

# Configura tus propios parámetros de conexión a la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'spam'
}

# Función para conectar a la base de datos
def connect_to_database():
    return mysql.connector.connect(**db_config)

# Función para buscar un usuario en la base de datos
def buscar_usuario(username):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT id, username, creditos, pruebas FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user

def buscar_creditos(username):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT creditos FROM user WHERE username = %s", (username,))
    resultado = cursor.fetchone()
    cursor.close()
    db.close()

    if resultado:
        # Retorna solo el valor de los créditos
        return resultado[0]
    else:
        # Retorna None o un valor por defecto si el usuario no se encuentra
        return None

def buscar_creditos_prueba(username):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT pruebas FROM user WHERE username = %s", (username,))
    resultado = cursor.fetchone()
    cursor.close()
    db.close()

    if resultado:
        # Retorna solo el valor de los créditos
        return resultado[0]
    else:
        # Retorna None o un valor por defecto si el usuario no se encuentra
        return None

def modificar_creditos(username, nuevos_creditos):
    db = connect_to_database()
    cursor = db.cursor()
    
    # Actualiza los créditos del usuario
    cursor.execute("UPDATE user SET creditos = %s WHERE username = %s", (nuevos_creditos, username))
    
    db.commit()  # Es importante hacer commit de la transacción
    cursor.close()
    db.close()

def modificar_creditos_prueba(username, nuevos_creditos):
    db = connect_to_database()
    cursor = db.cursor()
    
    # Actualiza los créditos del usuario
    cursor.execute("UPDATE user SET pruebas = %s WHERE username = %s", (nuevos_creditos, username))
    
    db.commit()  # Es importante hacer commit de la transacción
    cursor.close()
    db.close()
# Función para crear un usuario en la base de datos
def crear_usuario(username):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("INSERT INTO user (username, creditos) VALUES (%s, %s)", (username, 0))
    db.commit()
    user_id = cursor.lastrowid
    cursor.close()
    db.close()
    return user_id

esperando_entrada = {}
busqueda_usuario = {}
agregar_creditos = {}
eliminar_creditos = {}
prueba_entrada = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    usuario = buscar_usuario(username)
    if usuario:
        mensaje = f"*Spam del Polar*\n*ID:* `{usuario[0]}`\n*Nombre:* `{usuario[1]}`\n*Créditos:* `{usuario[2]}`\n*Créditos de Prueba:* `{usuario[3]}`"
    else:
        crear_usuario(username)
        usuario = buscar_usuario(username)
        mensaje = f"*Spam del Polar*\n*ID:* `{usuario[0]}`\n*Nombre:* `{usuario[1]}`\n*Créditos:* `{usuario[2]}`\n*Créditos de Prueba:* `{usuario[3]}`"

    # Definiendo los botones para que cada uno abarque todo el ancho del mensaje
    if username == 'Polar777XD':
        keyboard = [
            [InlineKeyboardButton("Enviar SPAM", callback_data='SPAM')],
            [InlineKeyboardButton("Buscar Usuario", callback_data='Bus_Usu')]
        ]
    else:   
        keyboard = [
            [InlineKeyboardButton("Enviar SPAM", callback_data='SPAM')],
            [InlineKeyboardButton("Enviar SPAM de Prueba", callback_data='Prueba')],
            [InlineKeyboardButton("Recargar Creditos", callback_data='Creditos')]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Ruta del archivo de la imagen local 'polar.jpg'
    ruta_imagen = 'polar.jpg'

    # Enviar foto con texto y botones
    with open(ruta_imagen, 'rb') as archivo_imagen:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=archivo_imagen,
            caption=mensaje,
            reply_markup=reply_markup,
            parse_mode='MarkdownV2'
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Notificar a Telegram que la interacción fue recibida
    data = query.data
    chat_id = update.effective_chat.id

    if data == 'SPAM':
        username = update.effective_user.username
        creditos = buscar_creditos(username)
        creditos = int(creditos)
        if creditos > 0:
            # Indicamos que estamos esperando una entrada para SPAM
            esperando_entrada[chat_id] = True
            await context.bot.send_message(chat_id=chat_id, text="Introduce el Correo:")
        else:
            await context.bot.send_message(chat_id=chat_id, text="No cuentas con suficientes creditos. Te sugerimos Recargar")
            keyboard = [[InlineKeyboardButton("Inicio", callback_data='Inicio')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
    elif data == 'Creditos':
        # Definir el botón de "Inicio"
        keyboard = [[InlineKeyboardButton("Inicio", callback_data='Inicio')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Procesar la selección de "Créditos" y enviar el botón "Inicio"
        await context.bot.send_message(chat_id=chat_id, text=f"Para Recargar Créditos Con: {DUENO}", reply_markup=reply_markup)
    elif data == 'Inicio':
        # Aquí puedes manejar la acción cuando se presiona "Inicio"
        await start(update, context)
    elif data == 'Prueba':
        username = update.effective_user.username
        creditos = buscar_creditos_prueba(username)
        creditos = int(creditos)
        if creditos > 0:
            # Indicamos que estamos esperando una entrada para SPAM
            prueba_entrada[chat_id] = True
            await context.bot.send_message(chat_id=chat_id, text="Introduce el Correo:")
        else:
            await context.bot.send_message(chat_id=chat_id, text="No cuentas con suficientes creditos de Prueba. Te sugerimos Recargar")
            keyboard = [[InlineKeyboardButton("Inicio", callback_data='Inicio')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
    elif data == 'Bus_Usu':
        busqueda_usuario[chat_id] = True
        await context.bot.send_message(chat_id=chat_id, text="Introduce el Nombre de la Persona:")
    elif data == 'Agr_Cred':
        agregar_creditos[chat_id] = True
        await context.bot.send_message(chat_id=chat_id, text="Cuantos Creditos quieres Agregar?")
    elif data == 'Elim_Cred':
        eliminar_creditos[chat_id] = True
        await context.bot.send_message(chat_id=chat_id, text="Cuantos Creditos quieres Eliminar?")
    else:
        await context.bot.send_message(chat_id=chat_id, text="Selección no reconocida.")

        # Eliminar o desactivar el teclado inline del mensaje original
        await query.edit_message_reply_markup(reply_markup=None)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    texto = update.message.text

    if chat_id in esperando_entrada and esperando_entrada[chat_id]:
        # Aquí procesas la entrada para SPAM
        del esperando_entrada[chat_id]  # Limpiar el estado
        # Aquí podrías guardar el valor de 'texto' como necesites
        username = update.effective_user.username
        creditos = buscar_creditos(username)
        creditos = int(creditos)
        creditos = creditos -1
        modificar_creditos(username,creditos)  
        # Crear un hilo para la tarea demorada
        hilo = threading.Thread(target=correo.definitivo, args=(texto,))
        # Iniciar el hilo
        hilo.start()

        await context.bot.send_message(chat_id=chat_id, text=f"Te has gastado 1 crédito \nSe le enviaran correos a {texto} durante los próximos 60min")

        # El programa principal continúa ejecutando otras tareas.
        # El hilo hilo se ejecuta en paralelo y no bloqueamos su ejecución aquí.
        await start(update, context)
    # Aquí puedes añadir más lógica para otros mensajes si es necesario
    elif chat_id in prueba_entrada and prueba_entrada[chat_id]:
        # Aquí procesas la entrada para SPAM
        del prueba_entrada[chat_id]  # Limpiar el estado
        # Aquí podrías guardar el valor de 'texto' como necesites
        username = update.effective_user.username
        creditos = buscar_creditos_prueba(username)
        creditos = int(creditos)
        creditos = creditos -1
        modificar_creditos_prueba(username,creditos)  
        # Crear un hilo para la tarea demorada
        hilo = threading.Thread(target=correo.prueba, args=(texto,))
        # Iniciar el hilo
        hilo.start()

        await context.bot.send_message(chat_id=chat_id, text=f"Te has gastado 1 crédito de prueba \nSe le enviaran correos a {texto} durante el próximo minuto")

        # El programa principal continúa ejecutando otras tareas.
        # El hilo hilo se ejecuta en paralelo y no bloqueamos su ejecución aquí.
        await start(update, context)
    # Aquí puedes añadir más lógica para otros mensajes si es necesario
    elif chat_id in busqueda_usuario and busqueda_usuario[chat_id]:
        # Aquí procesas la entrada para SPAM
        del busqueda_usuario[chat_id]  # Limpiar el estado

        usuario = buscar_usuario(texto)
        context.user_data['usuario'] = usuario

        mensaje = f"*ID:* `{usuario[0]}` \n*Nombre:* `{usuario[1]}` \n*Créditos:* `{usuario[2]}`"

        keyboard = [
            [InlineKeyboardButton("Agregar Creditos", callback_data='Agr_Cred')],
            [InlineKeyboardButton("Eliminar Creditos", callback_data='Elim_Cred')],
            [InlineKeyboardButton("Inicio", callback_data='Inicio')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Ruta del archivo de la imagen local 'polar.jpg'
        ruta_imagen = 'polar.jpg'

        # Enviar foto con texto y botones
        with open(ruta_imagen, 'rb') as archivo_imagen:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=archivo_imagen,
                caption=mensaje,
                reply_markup=reply_markup,
                parse_mode='MarkdownV2'
            )
    elif chat_id in agregar_creditos and agregar_creditos[chat_id]:
        # Limpiar el estado para no esperar más la acción de agregar créditos
        del agregar_creditos[chat_id]

        if 'usuario' in context.user_data:
            usuario = context.user_data['usuario']
            mas_creditos = int(texto)  # Asegúrate de que este valor se ha capturado y validado correctamente

            # Aquí implementas la lógica para actualizar los créditos del usuario
            creditos_actuales = usuario[2]  # Suponiendo que esta es la forma en que accedes a los créditos actuales del usuario
            nuevos_creditos = creditos_actuales + mas_creditos
            modificar_creditos(usuario[1], nuevos_creditos)  # Asume que esta función actualiza los créditos en la base de datos

            # Crear botón de "Inicio"
            keyboard = [[InlineKeyboardButton("Inicio", callback_data='Inicio')]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Enviar mensaje con el botón de "Inicio"
            await context.bot.send_message(
                chat_id=chat_id, 
                text=f"Créditos agregados correctamente. Créditos actuales: {nuevos_creditos}",
                reply_markup=reply_markup
            )            
    elif chat_id in eliminar_creditos and eliminar_creditos[chat_id]:
        # Limpiar el estado para no esperar más la acción de agregar créditos
        del eliminar_creditos[chat_id]

        if 'usuario' in context.user_data:
            usuario = context.user_data['usuario']
            menos_creditos = int(texto)  # Asegúrate de que este valor se ha capturado y validado correctamente

            # Aquí implementas la lógica para actualizar los créditos del usuario
            creditos_actuales = usuario[2]  # Suponiendo que esta es la forma en que accedes a los créditos actuales del usuario
            nuevos_creditos = creditos_actuales - menos_creditos
            modificar_creditos(usuario[1], nuevos_creditos)  # Asume que esta función actualiza los créditos en la base de datos

            # Crear botón de "Inicio"
            keyboard = [[InlineKeyboardButton("Inicio", callback_data='Inicio')]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Enviar mensaje con el botón de "Inicio"
            await context.bot.send_message(
                chat_id=chat_id, 
                text=f"Créditos eliminados correctamente. Créditos actuales: {nuevos_creditos}",
                reply_markup=reply_markup
            )

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Añade los handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
