# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.widget import Widget

# kivymd imports
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRound


class AddContactScreen(Screen):
    def __init__(self, **kwargs):
        super(AddContactScreen, self).__init__(name=kwargs.get('name'))
        self.util = kwargs.get('util')
        self.ui_layout()

    def ui_layout(self):
        add_contact_card = MDCard(padding=dp(24),
                                  spacing=dp(24),
                                  orientation='vertical',
                                  size_hint=(0.75, 0.45),
                                  pos_hint={'top': 0.75, 'center_x': 0.5}
                                  )

        add_contact_label = MDLabel(text='Enter In a User Name', font_style='H4', halign='center')
        add_contact_label.theme_text_color = 'Custom'
        add_contact_label.text_color = [1, 1, 1, 1]

        self.info_text = MDLabel(text='', halign='center')
        self.info_text.theme_text_color = 'Error'

        self.contact_input = MDTextFieldRound(size_hint=(0.75, None), pos_hint={'center_x': 0.5})
        # Hides left icon
        self.contact_input.icon_left_dasabled = True
        # Moves widget out of the field of view
        self.contact_input.children[2].children[2].pos_hint = {'center_x': 500, 'center_y': 500}
        self.contact_input.icon_right = 'send'
        self.contact_input.children[2].children[0].bind(
            on_press=lambda x: self.check_name(self.contact_input.text))

        add_contact_card.add_widget(add_contact_label)
        add_contact_card.add_widget(self.info_text)
        add_contact_card.add_widget(Widget())
        add_contact_card.add_widget(Widget())
        add_contact_card.add_widget(self.contact_input)

        toolbar_anchor = AnchorLayout(anchor_x='center', anchor_y='top')
        toolbar = MDToolbar(title='Add Contact', anchor_title='center')
        toolbar.md_bg_color = App.get_running_app().theme_cls.primary_color
        toolbar.left_action_items = [['arrow-left', lambda x: self.change_screen('contact')]]
        toolbar_anchor.add_widget(toolbar)

        self.add_widget(add_contact_card)
        self.add_widget(toolbar_anchor)

    def change_screen(self, screen):
        self.manager.current = screen

    def check_name(self, user_name):
        self.util.morse_app_api.query_user_req(self.check_name_cb, user_name)

    def check_name_cb(self, request, result):
        if request.resp_status == 200:
            if self.contact_input.text in self.util.user_data['contacts']:
                self.info_text.text = 'User Already in contacts!'
            else:
                self.util.save_contact(self.contact_input.text)
                self.contact_input.text = ''
                self.info_text.text = ''
                for screen in App.get_running_app().root.content.screens:
                    if screen.name == 'contact':
                        screen.ui_layout()
                self.manager.current = 'contact'
        else:
            self.info_text.text = 'User Not found! Do you not have any friends? :('
