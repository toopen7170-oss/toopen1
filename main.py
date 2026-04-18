import os
import sys
import traceback
from kivy.app import App
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

# [이미지 1-3] 자가 진단: 폰트 등록 및 예외 처리
try:
    if os.path.exists("font.ttf"):
        LabelBase.register(name="CustomFont", fn_regular="font.ttf")
    else:
        print("[자가진단] 경고: font.ttf 파일이 없습니다.")
except Exception as e:
    print(f"[자가진단] 폰트 등록 오류: {e}")

# [이미지 4-7] S26 Ultra 해상도 대응: 수직 정중앙 정렬 보정 입력창
class CustomTextInput(TextInput):
    """S26 Ultra 해상도 대응: 글자 수직 정중앙 정렬 보정"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if os.path.exists("font.ttf"):
            self.font_name = "CustomFont"
        self.multiline = False
        self.font_size = '18sp'
        self.cursor_color = get_color_from_hex('#1a4361')
        self.background_color = (1, 1, 1, 0.9)
        self.bind(size=self._update_padding)

    def _update_padding(self, *args):
        # 정밀 계산: (칸 높이 / 2) - (글자 높이 / 2)
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0), 0]

# [이미지 8] 모든 화면의 기초가 되는 배경 이미지 설정 클래스
class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            # 배경 이미지(bg.png) 설정 로직 고착
            self.bg_rect = Rectangle(source='bg.png', size=Window.size, pos=self.pos)
        self.bind(size=self._update_bg)

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

# [이미지 8-11] 메인 화면: 계정 검색 및 생성 리스트
class MainScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 40, 20, 20], spacing=15)
        
        # 타이틀 (PristonTale)
        title_lbl = Label(text="PristonTale", font_size='32sp', size_hint_y=0.1)
        if os.path.exists("font.ttf"): title_lbl.font_name = "CustomFont"
        self.layout.add_widget(title_lbl)

        # 검색창 영역 (이미지 9)
        search_area = BoxLayout(size_hint_y=0.08, spacing=5)
        self.search_in = CustomTextInput(hint_text="계정 검색...")
        search_area.add_widget(self.search_in)
        self.layout.add_widget(search_area)

        # 새 계정 만들기 버튼 (이미지 10)
        add_btn = Button(text="+ 새 계정 만들기", size_hint_y=0.08, background_color=get_color_from_hex('#27ae60'))
        if os.path.exists("font.ttf"): add_btn.font_name = "CustomFont"
        self.layout.add_widget(add_btn)

        # 계정 리스트 영역 (이미지 11)
        self.scroll = ScrollView()
        self.acc_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=12)
        self.acc_list_layout.bind(minimum_height=self.acc_list_layout.setter('height'))
        self.scroll.add_widget(self.acc_list_layout)
        self.layout.add_widget(self.scroll)

        self.add_widget(self.layout)

# [제1원칙 고착] 캐릭터 정보창 (4/3/5/5 구조 절대 보존)
class CharInfoScreen(BaseScreen):
    groups = [
        [('이름', ''), ('직위', ''), ('클랜', ''), ('레벨', '')], # 4
        [('생명력', ''), ('기력', ''), ('근력', '')],              # 3
        [('힘', ''), ('정신력', ''), ('재능', ''), ('민첩', ''), ('건강', '')], # 5
        [('명중', ''), ('공격', ''), ('방어', ''), ('흡수', ''), ('속도', '')]  # 5
    ]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=15)
        self.scroll = ScrollView()
        self.info_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=2)
        self.info_container.bind(minimum_height=self.info_container.setter('height'))
        
        for i, group in enumerate(self.groups):
            for label_text, val in group:
                self.info_container.add_widget(CustomTextInput(hint_text=label_text, text=val))
            if i < len(self.groups) - 1:
                self.info_container.add_widget(Label(size_hint_y=None, height="30dp"))
        
        self.scroll.add_widget(self.info_container)
        self.main_layout.add_widget(self.scroll)
        self.add_widget(self.main_layout)

class PT1App(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CharInfoScreen(name='char_info'))
        return sm

if __name__ == "__main__":
    PT1App().run()
