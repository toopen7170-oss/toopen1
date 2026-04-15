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

# 한글 폰트 및 배경 설정
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
        # 텍스트가 줄 바로 위에 오도록 패딩 조정
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0) + 10, 10]

def show_confirm(title, text, on_confirm):
    content = BoxLayout(orientation='vertical', padding=10, spacing=10)
    content.add_widget(Label(text=text, font_name="CustomFont"))
    btns = BoxLayout(size_hint_y=0.4, spacing=10)
    
    ok_btn = Button(text="확인", background_color=get_color_from_hex('#2ecc71'), font_name="CustomFont")
    cancel_btn = Button(text="취소", background_color=get_color_from_hex('#e74c3c'), font_name="CustomFont")
    
    popup = Popup(title=title, content=content, size_hint=(0.8, 0.4), title_font="CustomFont")
    
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
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 통합 검색 영역
        search_box = BoxLayout(size_hint_y=0.1, spacing=5)
        self.search_input = CustomTextInput(hint_text="전체 검색(계정, 캐릭터, 아이템 등)")
        search_btn = Button(text="검색", size_hint_x=0.2, background_color=get_color_from_hex('#3498db'), font_name="CustomFont")
        search_box.add_widget(self.search_input)
        search_box.add_widget(search_btn)
        
        # 스크롤 가능한 리스트 영역
        self.scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        self.scroll.add_widget(self.acc_list)
        
        # 하단 저장/추가 버튼
        add_btn = Button(text="새 계정 추가", size_hint_y=0.1, background_color=get_color_from_hex('#2ecc71'), font_name="CustomFont")
        add_btn.bind(on_release=self.ask_save_account)
        
        layout.add_widget(search_box)
        layout.add_widget(self.scroll)
        layout.add_widget(add_btn)
        self.add_widget(layout)

    def ask_save_account(self, instance):
        show_confirm("저장 확인", "신규 계정 정보를 저장하시겠습니까?", self.save_logic)

    def save_logic(self):
        # 실제 저장 로직 수행
        print("데이터 저장 완료")

    def ask_delete_account(self, instance):
        show_confirm("삭제 확인", "정말 삭제하시겠습니까?", self.delete_logic)

    def delete_logic(self):
        # 실제 삭제 로직 수행
        print("데이터 삭제 완료")

class PristonTaleApp(App):
    def build(self):
        self.title = "PristonTale Manager"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        return sm

    def on_start(self):
        # 시작 시 사진 권한 확인 멘트
        show_confirm("권한 요청", "사진 및 미디어 접근을 허용하시겠습니까?", lambda: print("Permission Granted"))

if __name__ == '__main__':
    PristonTaleApp().run()
