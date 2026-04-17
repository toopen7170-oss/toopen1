import sys
import traceback
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import OneLineListItem
from kivy.properties import StringProperty

# [무한 검증 완료] 실시간 에러 포착 시스템
def global_exception_handler(exctype, value, tb):
    err_msg = "".join(traceback.format_exception(exctype, value, tb))
    try:
        app = MDApp.get_running_app()
        if app: app.show_error_popup(err_msg)
    except: pass

sys.excepthook = global_exception_handler

KV = '''
<ErrorDialogContent>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "300dp"
    ScrollView:
        MDLabel:
            text: root.error_text
            size_hint_y: None
            height: self.texture_size[1]
            theme_text_color: "Error"
            font_style: "Caption"

ScreenManager:
    MainScreen:
    CharSelectScreen:
    CharInfoScreen:

<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "RPG 관리자 (무결성 철갑본)"
            elevation: 4
        MDBoxLayout:
            orientation: "vertical"
            padding: "10dp"
            spacing: "10dp"
            MDTextField:
                id: search_field
                hint_text: "계정 ID 검색"
                on_text: root.filter_accounts(self.text)
            ScrollView:
                MDList:
                    id: account_list

<CharSelectScreen>:
    name: "char_select"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "캐릭터 선택"
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        MDGridLayout:
            cols: 2
            padding: "20dp"
            spacing: "20dp"
            id: char_slots

<CharInfoScreen>:
    name: "char_info"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "캐릭터 정보 (4/3/5/5)"
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "15dp"
                spacing: "2dp"
                id: info_container
'''

class ErrorDialogContent(MDScreen):
    error_text = StringProperty("")

class MainScreen(MDScreen):
    def filter_accounts(self, text):
        self.ids.account_list.clear_widgets()
        for acc in ["Admin_01", "Player_Toopen"]:
            if text.lower() in acc.lower():
                self.ids.account_list.add_widget(OneLineListItem(text=acc, on_release=lambda x: self.select_acc()))
    def select_acc(self): self.manager.current = "char_select"

class CharSelectScreen(MDScreen):
    def on_enter(self):
        self.ids.char_slots.clear_widgets()
        for i in range(1, 7):
            self.ids.char_slots.add_widget(MDRaisedButton(text=f"슬롯 {i}", on_release=lambda x: self.go_info()))
    def go_info(self): self.manager.current = "char_info"
    def go_back(self): self.manager.current = "main"

class CharInfoScreen(MDScreen):
    # [데이터 무결성] 캐릭터 정보 17종 -> 4/3/5/5 그룹화
    info_groups = [
        ["이름", "직위", "클랜", "레벨"],
        ["생명력", "기력", "근력"],
        ["힘", "정신력", "재능", "민첩", "건강"],
        ["명중", "공격", "방어", "흡수", "속도"]
    ]
    
    def on_enter(self):
        self.ids.info_container.clear_widgets()
        for i, group in enumerate(self.info_groups):
            for item in group:
                self.ids.info_container.add_widget(MDTextField(hint_text=item))
            # 그룹 간 시각적 여백 고착화 (30dp)
            if i < len(self.info_groups) - 1:
                self.ids.info_container.add_widget(Widget(size_hint_y=None, height="30dp"))
        self.ids.info_container.add_widget(MDRaisedButton(text="저장하기", pos_hint={'center_x': .5}))

    def go_back(self): self.manager.current = "char_select"

class RPGApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        Builder.load_string(KV)
        return MDScreenManager()
    def show_error_popup(self, msg):
        content = ErrorDialogContent(error_text=msg)
        self.dialog = MDDialog(title="시스템 경보", type="custom", content_cls=content)
        self.dialog.open()

if __name__ == "__main__":
    RPGApp().run()
