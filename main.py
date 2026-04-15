import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.properties import StringProperty

# 한글 폰트 등록
try:
    LabelBase.register(name="CustomFont", fn_regular="font.ttf")
except:
    pass

class CustomTextInput(TextInput):
    """S26 울트라 보정: 글자가 입력선 바로 위에 오도록 설정"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "CustomFont"
        self.multiline = False
        self.background_color = (0.95, 0.95, 0.95, 1)
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0) + 5, 5]

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            # 배경화면 유지
            self.bg = Image(source='bg.png', allow_stretch=True, keep_ratio=False, size=Window.size)

class MainScreen(BaseScreen):
    """사진 72696 스타일 재현"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[20, 50, 20, 20], spacing=15)
        
        # 타이틀
        layout.add_widget(Label(text="[PT1 통합 매니저]", font_name="CustomFont", font_size='26sp', size_hint_y=0.08))
        
        # 검색바 (사진 72696 스타일)
        search_area = BoxLayout(size_hint_y=0.08, spacing=2)
        self.search_input = CustomTextInput(hint_text="계정/캐릭터 검색...")
        search_btn = Button(text="검색", size_hint_x=0.25, background_color=get_color_from_hex('#1a3a5a'), font_name="CustomFont")
        search_area.add_widget(self.search_input)
        search_area.add_widget(search_btn)
        layout.add_widget(search_area)
        
        # 새 계정 만들기 버튼 (초록색)
        add_btn = Button(text="+ 새 계정 만들기", size_hint_y=0.08, background_color=get_color_from_hex('#27ae60'), font_name="CustomFont")
        add_btn.bind(on_release=self.show_add_popup)
        layout.add_widget(add_btn)
        
        # 계정 리스트 (사진 72696 삭제 버튼 포함)
        self.scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        self.scroll.add_widget(self.acc_list)
        layout.add_widget(self.scroll)
        
        self.add_widget(layout)
        # 초기 데이터 로드 시뮬레이션
        self.refresh_list(["toopen", "toopen0", "toopen9"])

    def refresh_list(self, accounts):
        self.acc_list.clear_widgets()
        for acc in accounts:
            row = BoxLayout(size_hint_y=None, height=75, spacing=5)
            # 계정 버튼 (파란색 바)
            btn = Button(text=f"계정: {acc}", background_color=get_color_from_hex('#1e3a5f'), font_name="CustomFont", padding=(20, 0))
            btn.bind(on_release=lambda x, a=acc: self.go_to_slots(a))
            # 삭제 버튼 (빨간색 X)
            del_btn = Button(text="X", size_hint_x=0.22, background_color=get_color_from_hex('#5a1a1a'), font_name="CustomFont")
            
            row.add_widget(btn)
            row.add_widget(del_btn)
            self.acc_list.add_widget(row)

    def show_add_popup(self, instance):
        """사진 73235 스타일의 생성 팝업"""
        content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        self.new_id = CustomTextInput(hint_text="생성할 계정 ID")
        done_btn = Button(text="생성 완료", size_hint_y=0.4, background_color=get_color_from_hex('#1e5631'), font_name="CustomFont")
        content.add_widget(self.new_id)
        content.add_widget(done_btn)
        
        popup = Popup(title="계정 생성", content=content, size_hint=(0.8, 0.4), title_font="CustomFont")
        done_btn.bind(on_release=popup.dismiss)
        popup.open()

    def go_to_slots(self, acc_name):
        self.manager.get_screen('slots').target_account = acc_name
        self.manager.current = 'slots'

class SlotScreen(BaseScreen):
    """사진 73193 스타일 재현: 6개 슬롯 화면"""
    target_account = StringProperty("")

    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=25, spacing=20)
        
        # 타이틀
        layout.add_widget(Label(text=f"[{self.target_account}] 캐릭터 선택", font_name="CustomFont", font_size='20sp', size_hint_y=0.1))
        
        # 6개 슬롯 (2열 3행 그리드)
        grid = GridLayout(cols=2, spacing=12, size_hint_y=0.7)
        for i in range(1, 7):
            btn = Button(text=f"슬롯 {i}", background_color=get_color_from_hex('#4a5a8a'), font_name="CustomFont")
            grid.add_widget(btn)
        layout.add_widget(grid)
        
        # 하단 처음으로 버튼
        back_btn = Button(text="처음으로", size_hint_y=0.1, background_color=get_color_from_hex('#555555'), font_name="CustomFont")
        back_btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back_btn)
        
        self.add_widget(layout)

class PristonTaleApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SlotScreen(name='slots'))
        return sm

if __name__ == '__main__':
    PristonTaleApp().run()
