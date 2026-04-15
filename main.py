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

# 폰트 등록 (한글 깨짐 방지)
try:
    LabelBase.register(name="CustomFont", fn_regular="font.ttf")
except:
    pass

class CustomTextInput(TextInput):
    """S26 울트라 최적화: 글자가 입력선 바로 위에 오도록 패딩 조정"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "CustomFont"
        self.multiline = False
        self.background_color = (1, 1, 1, 0.15)
        self.foreground_color = (1, 1, 1, 1)
        self.cursor_color = get_color_from_hex('#3498db')
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0) + 10, 10]

def show_confirm(title, text, on_confirm):
    """스크린샷 73755.jpg 스타일의 확인 팝업"""
    content = BoxLayout(orientation='vertical', padding=20, spacing=20)
    content.add_widget(Label(text=text, font_name="CustomFont", font_size='18sp', halign='center'))
    
    btns = BoxLayout(size_hint_y=0.4, spacing=15)
    ok_btn = Button(text="확인", background_color=get_color_from_hex('#1a4361'), font_name="CustomFont")
    cancel_btn = Button(text="취소", background_color=get_color_from_hex('#444444'), font_name="CustomFont")
    
    popup = Popup(title=title, content=content, size_hint=(0.85, 0.4), title_font="CustomFont")
    
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
            # 스크린샷 73753.jpg 스타일 배경
            self.bg = Image(source='bg.png', allow_stretch=True, keep_ratio=False, size=Window.size)

class MainScreen(BaseScreen):
    """메인 화면: 검색 및 계정 목록"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 상단 검색바
        search_box = BoxLayout(size_hint_y=0.08, spacing=10)
        self.search_input = CustomTextInput(hint_text="캐릭터/아이템 검색")
        search_btn = Button(text="검색", size_hint_x=0.25, background_color=get_color_from_hex('#0d2a3d'), font_name="CustomFont")
        search_box.add_widget(self.search_input)
        search_box.add_widget(search_btn)
        
        # 계정 리스트 영역
        self.scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        self.scroll.add_widget(self.acc_list)
        
        # 하단 계정 추가 버튼
        add_btn = Button(text="+ 새 계정 만들기", size_hint_y=0.08, background_color=get_color_from_hex('#1e5631'), font_name="CustomFont")
        add_btn.bind(on_release=self.go_to_manage)
        
        layout.add_widget(search_box)
        layout.add_widget(self.scroll)
        layout.add_widget(add_btn)
        self.add_widget(layout)

    def go_to_manage(self, instance):
        self.manager.current = 'manage'

class AccountManageScreen(BaseScreen):
    """계정 관리 창: 정보 입력, 저장 및 삭제"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        layout.add_widget(Label(text="[ 계정 정보 설정 ]", font_name="CustomFont", font_size='22sp', size_hint_y=0.1))
        
        # 입력 필드들
        self.id_input = CustomTextInput(hint_text="계정 ID 입력")
        self.pw_input = CustomTextInput(hint_text="비밀번호 입력")
        self.char_input = CustomTextInput(hint_text="대표 캐릭터명")
        
        layout.add_widget(self.id_input)
        layout.add_widget(self.pw_input)
        layout.add_widget(self.char_input)
        
        # 버튼 영역
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=15)
        save_btn = Button(text="계정 저장", background_color=get_color_from_hex('#2980b9'), font_name="CustomFont")
        del_btn = Button(text="계정 삭제", background_color=get_color_from_hex('#c0392b'), font_name="CustomFont")
        back_btn = Button(text="뒤로가기", background_color=get_color_from_hex('#7f8c8d'), font_name="CustomFont")
        
        save_btn.bind(on_release=lambda x: show_confirm("저장", "이 계정 정보를 저장할까요?", self.save_process))
        del_btn.bind(on_release=lambda x: show_confirm("삭제", "정말로 이 정보를 삭제하시겠습니까?", self.delete_process))
        back_btn.bind(on_release=self.go_back)
        
        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(del_btn)
        btn_layout.add_widget(back_btn)
        
        layout.add_widget(btn_layout)
        layout.add_widget(BoxLayout(size_hint_y=0.3)) # 하단 여백
        self.add_widget(layout)

    def save_process(self):
        # 실제 저장 로직 (DB 또는 파일 저장) 수행 지점
        print(f"Saving: {self.id_input.text}")
        self.manager.current = 'main'

    def delete_process(self):
        # 실제 삭제 로직 수행 지점
        print("Data Deleted")
        self.manager.current = 'main'

    def go_back(self, instance):
        self.manager.current = 'main'

class PristonTaleApp(App):
    def build(self):
        self.title = "PT1 Manager Official"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AccountManageScreen(name='manage'))
        return sm

if __name__ == '__main__':
    PristonTaleApp().run()
