import sys
import traceback
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import OneLineListItem
from kivy.properties import StringProperty, ListProperty
from kivy.utils import platform

# [전수 검사 보강] 실시간 에러 전광판 로직
# 앱 실행 중 오류 발생 시 꺼지지 않고 화면에 에러를 표시합니다.
def global_exception_handler(exctype, value, tb):
    err_msg = "".join(traceback.format_exception(exctype, value, tb))
    print(err_msg)
    try:
        app = MDApp.get_running_app()
        if app and app.root:
            app.show_error_popup(err_msg)
    except:
        pass

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
    EquipmentScreen:
    InventoryScreen:
    PhotoScreen:

<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "RPG 계정 관리자"
            elevation: 4
        MDBoxLayout:
            orientation: "vertical"
            padding: "10dp"
            spacing: "10dp"
            # [검색 시스템] 실시간 ID 검색바
            MDTextField:
                id: search_field
                hint_text: "계정 ID 검색"
                on_text: root.filter_accounts(self.text)
            ScrollView:
                MDList:
                    id: account_list
            MDRaisedButton:
                text: "새 계정 생성"
                pos_hint: {"center_x": .5}
                on_release: root.create_account()

<CharSelectScreen>:
    name: "char_select"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "캐릭터 선택 (6슬롯)"
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
            title: "캐릭터 정보 (17종)"
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "10dp"
                spacing: "5dp"
                id: info_container

<EquipmentScreen>:
    name: "equipment"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "장비 정보 (11종)"
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "10dp"
                spacing: "5dp"
                id: equip_container

<InventoryScreen>:
    name: "inventory"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "인벤토리"
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        MDBoxLayout:
            padding: "10dp"
            spacing: "10dp"
            size_hint_y: None
            height: "60dp"
            MDTextField:
                id: item_input
                hint_text: "아이템 추가"
            MDIconButton:
                icon: "plus"
                on_release: root.add_item()
        ScrollView:
            MDList:
                id: inv_list
'''

class ErrorDialogContent(MDScreen):
    error_text = StringProperty("")

class MainScreen(MDScreen):
    def filter_accounts(self, text):
        # 검색 로직: ID 포함 여부 확인
        self.ids.account_list.clear_widgets()
        accounts = ["Admin_01", "Player_Toopen", "Guest_User"] # 샘플 데이터
        for acc in accounts:
            if text.lower() in acc.lower():
                self.ids.account_list.add_widget(
                    OneLineListItem(text=acc, on_release=lambda x, a=acc: self.select_account(a))
                )

    def select_account(self, acc_id):
        self.manager.current = "char_select"

    def create_account(self):
        pass

class CharSelectScreen(MDScreen):
    def on_enter(self):
        self.ids.char_slots.clear_widgets()
        for i in range(1, 7):
            self.ids.char_slots.add_widget(
                MDRaisedButton(text=f"Slot {i}\\n캐릭터 정보", on_release=lambda x: self.go_info())
            )
    
    def go_info(self):
        self.manager.current = "char_info"
    
    def go_back(self):
        self.manager.current = "main"

class CharInfoScreen(MDScreen):
    # [제1원칙] 17개 정보 항목 보존
    info_list = [
        "이름", "직위", "클랜", "레벨", "생명력", "기력", "근력", 
        "힘", "정신력", "재능", "민첩", "건강", "명중", "공격", "방어", "흡수", "속도"
    ]
    def on_enter(self):
        self.ids.info_container.clear_widgets()
        for item in self.info_list:
            self.ids.info_container.add_widget(MDTextField(hint_text=item))
        self.ids.info_container.add_widget(MDRaisedButton(text="장비 관리", on_release=lambda x: self.go_equip()))

    def go_equip(self):
        self.manager.current = "equipment"

    def go_back(self):
        self.manager.current = "char_select"

class EquipmentScreen(MDScreen):
    # [제1원칙] 11개 장비 항목 보존
    equip_list = [
        "한손무기", "두손무기", "갑옷", "방패", "장갑", "부츠", "암릿", "링1", "링2", "아뮬랫", "기타"
    ]
    def on_enter(self):
        self.ids.equip_container.clear_widgets()
        for item in self.equip_list:
            self.ids.equip_container.add_widget(MDTextField(hint_text=item))
        self.ids.equip_container.add_widget(MDRaisedButton(text="인벤토리 관리", on_release=lambda x: self.go_inv()))

    def go_inv(self):
        self.manager.current = "inventory"

    def go_back(self):
        self.manager.current = "char_info"

class InventoryScreen(MDScreen):
    def add_item(self):
        text = self.ids.item_input.text
        if text:
            item = OneLineListItem(text=text)
            item.bind(on_release=lambda x: self.show_item_detail(x))
            self.ids.inv_list.add_widget(item)
            self.ids.item_input.text = ""

    def show_item_detail(self, item_widget):
        # 인벤토리 상세 수정 및 삭제 로직
        self.dialog = MDDialog(
            title="아이템 관리",
            text=f"선택된 아이템: {item_widget.text}",
            buttons=[
                MDFlatButton(text="삭제", on_release=lambda x: self.delete_item(item_widget)),
                MDFlatButton(text="닫기", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()

    def delete_item(self, item):
        self.ids.inv_list.remove_widget(item)
        self.dialog.dismiss()

    def go_back(self):
        self.manager.current = "equipment"

class RPGApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        Builder.load_string(KV)
        return MDScreenManager()

    def show_error_popup(self, error_msg):
        content = ErrorDialogContent()
        content.error_text = error_msg
        self.dialog = MDDialog(
            title="시스템 오류 발생",
            type="custom",
            content_cls=content,
            buttons=[MDFlatButton(text="확인", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

if __name__ == "__main__":
    RPGApp().run()
