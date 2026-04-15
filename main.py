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

# 폰트 등록
try:
    LabelBase.register(name="CustomFont", fn_regular="font.ttf")
except:
    pass

class CustomTextInput(TextInput):
    """S26 울트라 수직 정렬 보정 입력창"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "CustomFont"
        self.multiline = False
        self.background_color = (1, 1, 1, 0.1)
        self.foreground_color = (1, 1, 1, 1)
        # 글자가 입력 라인 바로 위에 오도록 조정
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0) + 8, 8]

def show_confirm(title, text, on_confirm):
    """확인 절차 강제 팝업"""
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
        
        # 검색바
        search_box = BoxLayout(size_hint_y=0.08, spacing=10)
        self.search_input = CustomTextInput(hint_text="캐릭터/아이템 검색")
        search_btn = Button(text="검색", size_hint_x=0.25, background_color=get_color_from_hex('#2980b9'), font_name="CustomFont")
        search_box.add_widget(self.search_input)
        search_box.add_widget(search_btn)
        
        # 리스트
        self.scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, size_hint_y=None, spacing=12)
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        self.scroll.add_widget(self.acc_list)
        
        # 추가 버튼
        add_btn = Button(text="+ 정보 추가", size_hint_y=0.08, background_color=get_color_from_hex('#27ae60'), font_name="CustomFont")
        add_btn.bind(on_release=lambda x: show_confirm("저장", "데이터를 저장하시겠습니까?", self.save_data))
        
        layout.add_widget(search_box)
        layout.add_widget(self.scroll)
        layout.add_widget(add_btn)
        self.add_widget(layout)

    def save_data(self):
        print("Data saved.")

class PristonTaleApp(App):
    def build(self):
        self.title = "PT1 Manager Official"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        return sm

    def on_start(self):
        show_confirm("권한 확인", "시스템 접근 권한이 필요합니다.", lambda: print("OK"))

if __name__ == '__main__':
    PristonTaleApp().run()
