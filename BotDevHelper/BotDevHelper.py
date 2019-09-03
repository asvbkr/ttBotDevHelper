# -*- coding: UTF-8 -*-
import os

from TamTamBot import CallbackButtonCmd, UpdateCmn
from TamTamBotDj.TamTamBotDj import TamTamBotDj
from openapi_client import BotCommand, Intent, NewMessageBody, ChatType, MessageList, MessageLinkType, NewMessageLink
from openapi_client.rest import ApiException


class BotDevHelper(TamTamBotDj):

    @property
    def about(self):
        return 'This bot is an helper in the development and management of bots.'

    @property
    def token(self):
        # type: () -> str
        return os.environ.get('TT_BOT_API_TOKEN')

    @property
    def description(self):
        # type: () -> str
        return 'Этот бот помогает в разработке и управлении ботами.\n\n' \
               'This bot is an helper in the development and management of bots.'

    @property
    def main_menu_buttons(self):
        # type: () -> []
        buttons = [
            [CallbackButtonCmd('About bot', 'start', intent=Intent.POSITIVE)],
            [CallbackButtonCmd('View message properties', 'vmp', intent=Intent.POSITIVE)],
        ]

        return buttons

    def get_commands(self):
        # type: () -> [BotCommand]
        commands = [
            BotCommand('start', 'start (about bot)'),
            BotCommand('menu', 'display menu'),
            BotCommand('vmp', 'viewing message properties'),
        ]
        return commands

    def receive_text(self, update):
        # type: (UpdateCmn) -> bool
        res = self.view_messages(update, [update.message.body.mid], update.link)
        return bool(res)

    def cmd_handler_vmp(self, update):
        # type: (UpdateCmn) -> bool
        res = None
        if not (update.chat_type in [ChatType.DIALOG]):
            return False
        if not update.this_cmd_response:  # Прямой вызов команды
            if update.cmd_args:  # Если сразу передано в команду
                list_id = []
                parts = update.cmd_args.get('c_parts') or []
                if parts:
                    for line in parts:
                        for part in line:
                            list_id.append(str(part))
                if list_id:
                    res = self.view_messages(update, list_id)
            else:  # Вывод запроса для ожидания ответа
                update.required_cmd_response = bool(
                    self.msg.send_message(NewMessageBody(f'Forward *one* chat message to view its properties:'), user_id=update.user_id)
                )
        else:  # Текстовый ответ команде
            message = update.message
            link = message.link
            if link and link.type == MessageLinkType.FORWARD:
                res = self.view_messages(update, [link.message.mid])
            else:
                self.msg.send_message(NewMessageBody(f'Error. You want to forward the message. Repeat, please'), user_id=update.user_id)
                return False

        return bool(res)

    def view_messages(self, update, list_mid, link=None):
        # type: (UpdateCmn, [str], NewMessageLink) -> bool
        res = False
        try:
            msgs = self.msg.get_messages(message_ids=list_mid)
        except ApiException:
            self.msg.send_message(NewMessageBody(f'Error(s) in messages ids {list_mid}', link=link), user_id=update.user_id)
            return False
        if isinstance(msgs, MessageList):
            if len(msgs.messages) < len(list_mid):
                self.msg.send_message(NewMessageBody(
                    f'Unable to receive all requested messages. Check the @{self.username} bot\'s access to the chat with these messages.', link=update.link
                ), user_id=update.user_id)
                return False
            else:
                for msg in msgs.messages:
                    res = res or self.msg.send_message(NewMessageBody(f'Message {msg.body.mid}:\n`{msg}'[:NewMessageBody.MAX_BODY_LENGTH], link=update.link), user_id=update.user_id)
        return res
