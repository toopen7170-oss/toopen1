import sys
import traceback
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton

# [시스템] 오류 핀포인트 전광판: 모든 예외를 가로채 화면에 즉시 리포팅
def global_exception_handler(exctype, value, tb):
    err_msg = "".join(traceback.format_exception(exctype, value, tb))
    app = App.get_running_app()
    if app and hasattr(app, 'show_error_on_screen'):
        app.show_error_on_screen(err_msg)

sys.excepthook = global_exception_handler

KV = '''
<ErrorOverlay>:
    orientation: 'vertical'
    canvas.before:
        Color: rgba: 0.1, 0, 0, 0.95
        Rectangle: pos: self.pos, size: self.size
    MDLabel:
        text: "🚨 SYSTEM ERROR DETECTED 🚨"
        halign: "center"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        bold: True
    ScrollView:
        MDLabel:
            text: root.error_text
            theme_text_color: "Custom"
            text_color: 1, 0.4, 0.4, 1
            size_hint_y: None
            height: self.texture_size[1]

<InventoryItem>:
    orientation: 'horizontal'
    size_hint_y: None
    height: "50dp"
    padding: "5dp"
    spacing: "5dp"
    MDTextField:
        text: root.item_text
        on_focus: if self.focus: root.open_detail_edit()
    MDRaisedButton:
        text: "저장"
        on_release: root.save_item()
    MDRaisedButton:
        text: "삭제"
        md_bg_color: 0.8, 0.2, 0.2, 1
        on_release: root.delete_item()

ScreenManager:
    AccountScreen:
    CharSelectScreen:
    CharInfoScreen:
    CharGearScreen:
    InventoryScreen:
    PhotoSelectScreen:

# 1. 계정생성창
<AccountScreen>:
    name: 'account'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar: title: "계정 생성 및 관리"
        MDTextField:
            hint_text: "계정 전체 검색바"
            mode: "rectangle"
            size_hint_x: 0.9
            pos_hint: {"center_x": .5}
        MDLabel: text: "계정 ID 선택"; halign: "center"
        ScrollView:
            MDList:
                OneLineListItem:
                    text: "ID: RPG_Master_01"
                    on_release: root.manager.current = 'char_select'
        MDRaisedButton:
            text: "새 계정 생성"
            pos_hint: {"center_x": .5}

# 2. 케릭선택창
<CharSelectScreen>:
    name: 'char_select'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar: title: "캐릭터 선택 (6슬롯)"
        GridLayout:
            cols: 2
            padding: "20dp"
            spacing: "20dp"
            Button: text: "캐릭터 1"; on_release: root.manager.current = 'char_info'
            Button: text: "캐릭터 2"
            Button: text: "캐릭터 3"
            Button: text: "캐릭터 4"
            Button: text: "캐릭터 5"
            Button: text: "캐릭터 6"

# 3. 케릭정보창 (제1원칙 목록 고정 및 투명 여백)
<CharInfoScreen>:
    name: 'char_info'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar: title: "캐릭터 상세 정보"
        ScrollView:
            MDBoxLayout:
                id: info_container
                orientation: 'vertical'
                adaptive_height: True
                padding: "15dp"
        MDBoxLayout:
            size_hint_y: None; height: "60dp"
            spacing: "10dp"; padding: "5dp"
            MDRaisedButton: text: "장비"; size_hint_x: 1; on_release: root.manager.current = 'char_gear'
            MDRaisedButton: text: "인벤"; size_hint_x: 1; on_release: root.manager.current = 'inventory'
            MDRaisedButton: text: "사진"; size_hint_x: 1; on_release: root.manager.current = 'photo_select'

# 4. 케릭장비창 (11개 목록 고정)
<CharGearScreen>:
    name: 'char_gear'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar: title: "장비 관리"
        ScrollView:
            MDList: id: gear_list
        MDRaisedButton: text: "정보창으로"; pos_hint: {"center_x": .5}; on_release: root.manager.current = 'char_info'

# 5. 인벤토리창 (상세 수정 모드)
<InventoryScreen>:
    name: 'inventory'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar: title: "인벤토리 (저장/삭제)"
        ScrollView:
            MDList: id: inv_list
        MDRaisedButton: text: "아이템 추가"; pos_hint: {"center_x": .5}; on_release: app.add_inv_item()
        MDRaisedButton: text: "돌아가기"; on_release: root.manager.current = 'char_info'

# 6. 사진선택창 (권한 및 멀티 업로드/다운로드)
<PhotoSelectScreen>:
    name: 'photo_select'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar: title: "갤러리 사진 관리"
        MDLabel: text: "권한 허용 후 사진 선택 (멀티 가능)"; halign: "center"
        ScrollView:
            GridLayout: id: photo_display; cols: 3; adaptive_height: True; padding: "10dp"
        BoxLayout:
            size_hint_y: None; height: "60dp"
            padding: "10dp"; spacing: "10dp"
            MDRaisedButton: text: "업로드"; size_hint_x: 1; on_release: app.pick_photos()
            MDRaisedButton: text: "다운로드"; size_hint_x: 1
            MDRaisedButton: text: "전체삭제"; size_hint_x: 1; md_bg_color: 1, 0, 0, 1
        MDRaisedButton: text: "돌아가기"; on_release: root.manager.current = 'char_info'
'''

class ErrorOverlay(BoxLayout):
    error_text = StringProperty()

class InventoryItem(BoxLayout):
    item_text = StringProperty()
    def open_detail_edit(self): print("한 줄 클릭: 전체 글씨 보기 및 수정 모드 활성화")
    def save_item(self): print("아이템 저장 완료")
    def delete_item(self): self.parent.remove_widget(self)

class RPGManagerApp(MDApp):
    # 제1원칙: 목록 절대 불변 (17개 정보항목 그룹화)
    info_groups = [
        [('이름', ''), ('직위', ''), ('클랜', ''), ('레벨', '')],
        [('생명력', ''), ('기력', ''), ('근력', '')],
        [('힘', ''), ('정신력', ''), ('재능', ''), ('민첩', ''), ('건강', '')],
        [('명중', ''), ('공격', ''), ('방어', ''), ('흡수', ''), ('속도', '')]
    ]
    # 장비 11개 목록 고정
    gear_names = ["한손무기", "두손무기", "갑옷", "방패", "장갑", "부츠", "암릿", "링1", "링2", "아뮬랫", "기타"]

    def build(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.root = Builder.load_string(KV)
        self.init_data_structures()
        return self.root

    def init_data_structures(self):
        # 정보창 17개 배치 및 그룹 사이 여백 삽입
        info_container = self.root.get_screen('char_info').ids.info_container
        for i, group in enumerate(self.info_groups):
            for name, val in group:
                f = MDTextField(hint_text=name, text=val, mode="line")
                info_container.add_widget(f)
            # 제1원칙: 그룹 사이 투명 여백 (화면에 안 보이게 처리)
            if i < len(self.info_groups) - 1:
                info_container.add_widget(Widget(size_hint_y=None, height="30dp"))

        # 장비창 11개 배치
        gear_list = self.root.get_screen('char_gear').ids.gear_list
        for name in self.gear_names:
            from kivymd.uix.list import OneLineAvatarIconListItem
            item = OneLineAvatarIconListItem(text=name)
            gear_list.add_widget(item)

    def add_inv_item(self):
        self.root.get_screen('inventory').ids.inv_list.add_widget(InventoryItem(item_text="신규 아이템"))

    def pick_photos(self):
        print("Android 14 권한 요청 및 갤러리 멀티 선택창 활성화")

    def show_error_on_screen(self, error_msg):
        self.root.add_widget(ErrorOverlay(error_text=error_msg))

if __name__ == '__main__':
    RPGManagerApp().run()
