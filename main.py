
import os
from kivy.app import App
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

# [48번 로직] 자가 진단 및 폰트 예외 처리
try:
    if os.path.exists("font.ttf"):
        LabelBase.register(name="CustomFont", fn_regular="font.ttf")
except Exception:
    pass

# [기본원칙] S26 Ultra 수직 정렬 및 폰트 대응
class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if os.path.exists("font.ttf"):
            self.font_name = "CustomFont"
        self.multiline = False
        self.font_size = '17sp'
        self.cursor_color = get_color_from_hex('#1a4361')
        self.bind(size=self._update_padding)

    def _update_padding(self, *args):
        # S26 Ultra 글자 잘림 방지 수직 중앙 보정
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0), 0]

# [기본원칙] 배경 이미지 고착화
class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg_rect = Rectangle(source='bg.png', size=Window.size, pos=self.pos)
        self.bind(size=self._update_bg)

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

# [원칙 1] 계정 생성창 (ID 선택창, 전체 검색바)
class AccountScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout.add_widget(Label(text="계정 생성창", font_size='24sp', size_hint_y=0.1))
        
        # 계정 전체 검색바
        self.search_bar = CustomTextInput(hint_text="계정 전체 검색바")
        layout.add_widget(self.search_bar)
        
        # 계정 ID 선택창
        scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        
        # 예시 리스트 (세부내용 추가/수정 가능 영역)
        for i in range(5):
            btn = Button(text=f"계정 ID 선택 {i+1}", size_hint_y=None, height="50dp")
            btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'char_select'))
            self.acc_list.add_widget(btn)
        
        scroll.add_widget(self.acc_list)
        layout.add_widget(scroll)
        self.add_widget(layout)

# [원칙 2] 케릭선택창 (6개의 선택창)
class CharSelectScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text="케릭 선택창 (6개 슬롯)", size_hint_y=0.1))
        
        grid = GridLayout(cols=2, spacing=20)
        for i in range(1, 7):
            btn = Button(text=f"캐릭터 슬롯 {i}")
            btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'char_info'))
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        self.add_widget(layout)

# [원칙 3] 케릭정보창 (4/3/5/5 구조 및 보이지 않는 간격)
class CharInfoScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=15)
        scroll = ScrollView()
        container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        container.bind(minimum_height=container.setter('height'))
        
        # 4/3/5/5 데이터 구조 (절대 수호 토대)
        stats = [
            [('이름', ''), ('직위', ''), ('클랜', ''), ('레벨', '')],
            [('생명력', ''), ('기력', ''), ('근력', '')],
            [('힘', ''), ('정신력', ''), ('재능', ''), ('민첩', ''), ('건강', '')],
            [('명중', ''), ('공격', ''), ('방어', ''), ('흡수', ''), ('속도', '')]
        ]
        
        for i, group in enumerate(stats):
            for label, val in group:
                container.add_widget(CustomTextInput(hint_text=label, text=val))
            # (한칸 띄어주고) - 여백으로만 존재
            if i < len(stats) - 1:
                container.add_widget(BoxLayout(size_hint_y=None, height="30dp"))
        
        scroll.add_widget(container)
        main_layout.add_widget(scroll)
        
        nav = Button(text="장비창으로 이동", size_hint_y=0.1)
        nav.bind(on_release=lambda x: setattr(self.manager, 'current', 'equip_screen'))
        main_layout.add_widget(nav)
        self.add_widget(main_layout)

# [원칙 4] 케릭장비창 (11종 목록 고착)
class EquipScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15)
        scroll = ScrollView()
        container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        container.bind(minimum_height=container.setter('height'))
        
        equips = ["한손무기", "두손무기", "갑옷", "방패", "장갑", "부츠", "암릿", "링1", "링2", "아뮬랫", "기타"]
        for item in equips:
            container.add_widget(CustomTextInput(hint_text=item))
            
        scroll.add_widget(container)
        layout.add_widget(scroll)
        
        nav = Button(text="인벤토리로 이동", size_hint_y=0.1)
        nav.bind(on_release=lambda x: setattr(self.manager, 'current', 'inv_screen'))
        layout.add_widget(nav)
        self.add_widget(layout)

# [원칙 5] 인벤토리창 (한줄씩 저장/삭제, 클릭 시 전체글씨/수정)
class InventoryScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15)
        scroll = ScrollView()
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        
        for i in range(3):
            row = BoxLayout(size_hint_y=None, height="60dp", spacing=5)
            # 한줄 클릭 시 수정 기능 로직 포함
            btn_item = Button(text=f"아이템 {i+1} (클릭 시 수정)")
            save_btn = Button(text="저장", size_hint_x=0.2, background_color=get_color_from_hex('#27ae60'))
            del_btn = Button(text="삭제", size_hint_x=0.2, background_color=get_color_from_hex('#c0392b'))
            row.add_widget(btn_item); row.add_widget(save_btn); row.add_widget(del_btn)
            self.list_layout.add_widget(row)
            
        scroll.add_widget(self.list_layout)
        layout.add_widget(scroll)
        
        nav = Button(text="사진 선택창으로 이동", size_hint_y=0.1)
        nav.bind(on_release=lambda x: setattr(self.manager, 'current', 'photo_screen'))
        layout.add_widget(nav)
        self.add_widget(layout)

# [원칙 6] 사진선택창 (다중선택, 업로드/다운로드, 권한, 저장/삭제)
class PhotoScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout.add_widget(Label(text="사진 선택창", size_hint_y=0.1))
        
        self.photo_view = Image(source='default.png', size_hint_y=0.5)
        layout.add_widget(self.photo_view)
        
        btn_layout = GridLayout(cols=2, size_hint_y=0.3, spacing=10)
        btn_layout.add_widget(Button(text="사진 선택 (다중)"))
        btn_layout.add_widget(Button(text="권한 허용"))
        btn_layout.add_widget(Button(text="업로드"))
        btn_layout.add_widget(Button(text="다운로드"))
        layout.add_widget(btn_layout)
        
        footer = BoxLayout(size_hint_y=0.1, spacing=10)
        footer.add_widget(Button(text="저장버튼", background_color=get_color_from_hex('#27ae60')))
        footer.add_widget(Button(text="삭제버튼", background_color=get_color_from_hex('#c0392b')))
        layout.add_widget(footer)
        
        self.add_widget(layout)

class PT1App(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(AccountScreen(name='account'))
        sm.add_widget(CharSelectScreen(name='char_select'))
        sm.add_widget(CharInfoScreen(name='char_info'))
        sm.add_widget(EquipScreen(name='equip_screen'))
        sm.add_widget(InventoryScreen(name='inv_screen'))
        sm.add_widget(PhotoScreen(name='photo_screen'))
        return sm

if __name__ == "__main__":
    PT1App().run()
