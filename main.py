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
from kivymd.uix.list import OneLineListItem, TwoLineAvatarIconListItem, IconLeftWidget
from kivy.properties import StringProperty

# [무한 검증] 실시간 에러 포착 시스템
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
    EquipmentScreen:
    InventoryScreen:
    PhotoSelectScreen:

<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "계정 생성창 (ID 선택/전체검색)"
            elevation: 4
        MDBoxLayout:
            orientation: "vertical"
            padding: "10dp"
            spacing: "10dp"
            MDTextField:
                id: search_bar
                hint_text: "계정 ID 전체검색바"
            ScrollView:
                MDList:
                    id: account_list

<CharSelectScreen>:
    name: "char_select"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "케릭선택창 (6개 슬롯)"
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
            title: "케릭정보창 (4/3/5/5)"
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "15dp"
                spacing: "2dp"
                id: info_container

<EquipmentScreen>:
    name: "equipment"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "케릭장비창 (11종 목록)"
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: "10dp"
                spacing: "5dp"
                id: equip_list

<InventoryScreen>:
    name: "inventory"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "인벤토리창 (저장/삭제/수정)"
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        ScrollView:
            MDList:
                id: inv_list

<PhotoSelectScreen>:
    name: "photo_select"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "사진선택창"
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "20dp"
            MDLabel:
                text: "핸드폰 사진 다중 선택 및 업로드/다운로드"
                halign: "center"
            MDRaisedButton:
                text: "저장버튼"
                pos_hint: {"center_x": .5}
            MDRaisedButton:
                text: "삭제버튼"
                md_bg_color: 1, 0, 0, 1
                pos_hint: {"center_x": .5}
'''

class ErrorDialogContent(MDScreen):
    error_text = StringProperty("")

class MainScreen(MDScreen):
    def on_enter(self):
        self.ids.account_list.clear_widgets()
        # [제1원칙] 계정 ID 선택 목록 보존
        for i in range(3):
            self.ids.account_list.add_widget(OneLineListItem(text=f"계정 ID {i}", on_release=lambda x: self.go_char()))
    def go_char(self): self.manager.current = "char_select"

class CharSelectScreen(MDScreen):
    def on_enter(self):
        self.ids.char_slots.clear_widgets()
        # [제1원칙] 6개의 선택창 보존
        for i in range(1, 7):
            self.ids.char_slots.add_widget(MDRaisedButton(text=f"슬롯 {i}", on_release=lambda x: self.go_info()))
    def go_info(self): self.manager.current = "char_info"
    def go_back(self): self.manager.current = "main"

class CharInfoScreen(MDScreen):
    # [제1원칙] 4/3/5/5 구조 정확히 배치
    groups = [
        [('이름', ''), ('직위', ''), ('클랜', ''), ('레벨', '')],
        [('생명력', ''), ('기력', ''), ('근력', '')],
        [('힘', ''), ('정신력', ''), ('재능', ''), ('민첩', ''), ('건강', '')],
        [('명중', ''), ('공격', ''), ('방어', ''), ('흡수', ''), ('속도', '')]
    ]
    def on_enter(self):
        self.ids.info_container.clear_widgets()
        for i, group in enumerate(self.groups):
            for label, val in group:
                self.ids.info_container.add_widget(MDTextField(hint_text=label, text=val))
            # [제1원칙] (한칸 띄어주고) - 투명 위젯 처리
            if i < len(self.groups) - 1:
                self.ids.info_container.add_widget(Widget(size_hint_y=None, height="30dp"))
        self.ids.info_container.add_widget(MDRaisedButton(text="장비창 이동", on_release=lambda x: self.go_equip()))
    def go_equip(self): self.manager.current = "equipment"
    def go_back(self): self.manager.current = "char_select"

class EquipmentScreen(MDScreen):
    # [제1원칙] 11종 목록 절대 보존
    items = ["한손무기", "두손무기", "갑옷", "방패", "장갑", "부츠", "암릿", "링1", "링2", "아뮬랫", "기타"]
    def on_enter(self):
        self.ids.equip_list.clear_widgets()
        for item in self.items:
            self.ids.equip_list.add_widget(MDTextField(hint_text=item))
        self.ids.equip_list.add_widget(MDRaisedButton(text="인벤토리 이동", on_release=lambda x: self.go_inv()))
    def go_inv(self): self.manager.current = "inventory"
    def go_back(self): self.manager.current = "char_info"

class InventoryScreen(MDScreen):
    def on_enter(self):
        self.ids.inv_list.clear_widgets()
        for i in range(5):
            # [제1원칙] 저장/삭제 버튼 및 클릭 수정 로직 보존
            item = TwoLineAvatarIconListItem(text=f"아이템 {i}", secondary_text="클릭 시 수정 및 사진 선택")
            item.add_widget(IconLeftWidget(icon="content-save", on_release=lambda x: print("저장")))
            item.on_release = self.go_photo
            self.ids.inv_list.add_widget(item)
    def go_photo(self): self.manager.current = "photo_select"
    def go_back(self): self.manager.current = "equipment"

class PhotoSelectScreen(MDScreen):
    def go_back(self): self.manager.current = "inventory"

class PT1App(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        Builder.load_string(KV)
        return MDScreenManager()
    def show_error_popup(self, msg):
        content = ErrorDialogContent(error_text=msg)
        self.dialog = MDDialog(title="시스템 오류", type="custom", content_cls=content)
        self.dialog.open()

if __name__ == "__main__":
    PT1App().run()
