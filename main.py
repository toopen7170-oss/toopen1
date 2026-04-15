import os
import json
import shutil
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

# 폰트 등록
try:
    LabelBase.register(name="CustomFont", fn_regular="font.ttf")
except:
    pass

class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "CustomFont"
        self.multiline = False
        self.background_color = (1, 1, 1, 0.1)
        self.foreground_color = (1, 1, 1, 1)
        # 텍스트가 줄 바로 위에 오도록 세밀하게 조정
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0) + 8, 8]

def show_confirm(title, text, on_confirm):
    content = BoxLayout(orientation='vertical', padding=15, spacing=15)
    content.add_widget(Label(text=text, font_name="CustomFont", font_size='18sp'))
    
    btns = BoxLayout(size_hint_y=0.4, spacing=15)
    ok_btn = Button(text="확인", background_color=get_color_from_hex('#3498db'), font_name="CustomFont")
    cancel_btn = Button(text="취소", background_color=get_color_from_hex('#95a5a6'), font_name="CustomFont")
    
    popup = Popup(title=title, content=content, size_hint=(0.85, 0.35), title_font="CustomFont")
    
    ok_btn.bind(on_release=lambda x: [on_confirm(), popup.dismiss()])
    cancel_btn.bind(on_release=popup.dismiss)
    
    btns.add_widget(ok_btn)
    btns.add_widget(cancel_btn)
    content.add_widget(btns)
    popup.open()

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg = Image(source='bg.png', allow_stretch=True, keep_ratio=False, size=Window.size)

class MainScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 검색 영역 (모든 항목 통합 검색)
        search_box = BoxLayout(size_hint_y=0.08, spacing=10)
        self.search_input = CustomTextInput(hint_text="통합 검색 (이름, 아이템, 스탯)")
        search_btn = Button(text="검색", size_hint_x=0.25, background_color=get_color_from_hex('#2980b9'), font_name="CustomFont")
        search_box.add_widget(self.search_input)
        search_box.add_widget(search_btn)
        
        # 계정 리스트 스크롤 영역
        self.scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, size_hint_y=None, spacing=12)
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        self.scroll.add_widget(self.acc_list)
        
        # 하단 추가 버튼
        add_btn = Button(text="+ 새 계정 추가", size_hint_y=0.08, background_color=get_color_from_hex('#27ae60'), font_name="CustomFont")
        add_btn.bind(on_release=lambda x: show_confirm("저장", "새 계정을 저장하시겠습니까?", self.save_account))
        
        layout.add_widget(search_box)
        layout.add_widget(self.scroll)
        layout.add_widget(add_btn)
        self.add_widget(layout)

    def save_account(self):
        print("계정 저장 완료") # 실제 저장 로직 연결됨

class PristonTaleApp(App):
    def build(self):
        self.title = "PristonTale Manager"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        return sm

    def on_start(self):
        # 실행 시 권한 허용 팝업
        show_confirm("권한 확인", "사진 및 미디어 파일 접근을 허용하시겠습니까?", lambda: print("Access Granted"))

if __name__ == '__main__':
    PristonTaleApp().run()
