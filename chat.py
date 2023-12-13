import flet as ft

def main(page):
  text = ft.Text('Hash')

  chat = ft.Column()

  user_name = ft.TextField(label='Escreva seu nome:')

  def send_message_tunnel(message): 
    type_message = message['type']
    if type_message == 'message':
      text_message = message['text']
      user_message = message['user']
    # Adicionar a mensagem no chat
      chat.controls.append(ft.Text(f'{user_message}: {text_message}'))
    else:
      user_message = message['user']
      chat.controls.append(ft.Text(f'{user_message} entrou no chat', size=12, italic=True, color=ft.colors.ORANGE_300))
    page.update()

  #PUBSUB
  page.pubsub.subscribe(send_message_tunnel)

  def send_message(event):
    page.pubsub.send_all({'text': message_field.value, 'user': user_name.value, 'type': 'message'})
    # Limpar o campo da mensagem
    message_field.value = ''
    page.update()

  send_message_button = ft.ElevatedButton('Enviar', on_click=send_message)
  message_field = ft.TextField(label='Digite uma mensagem')

  def enter_popup(event):
    page.pubsub.send_all({'user': user_name.value, 'type': 'entry'})
    # Adicionar o chat
    page.add(chat)
    # Fechar o popup
    popup.open = False
    page.remove(init_button)
    page.remove(text)
    page.add(ft.Row(
      [message_field, send_message_button]
    ))
    page.update()

  popup = ft.AlertDialog(
    open=False,
    modal=True,
    title=ft.Text('Bem vindo ao Chat!'),
    content=user_name,
    actions=[ft.ElevatedButton('Entrar', on_click=enter_popup)],
  )

  def enter_chat(event):
    page.dialog = popup
    popup.open = True
    page.update()

  init_button = ft.ElevatedButton('Iniciar chat', on_click=enter_chat)

  page.add(text)
  page.add(init_button)

ft.app(target=main, view=ft.WEB_BROWSER) 

