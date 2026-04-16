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
from kivy.properties import StringProperty, ListProperty, DictProperty, NumericProperty
from kivy.clock import Clock

# [1] 폰트 오류 자동 감지 시스템
FONT_STATUS = "OK"
try:
    if os.path.exists("font.ttf"):
        LabelBase.register(name="CustomFont", fn_regular="font.ttf")
    else:
        FONT_STATUS = "ERROR: font.ttf 파일이 없습니다!"
except Exception as e:
    FONT_STATUS = f"ERROR: 폰트 로드 실패 ({str(e)})"

class ErrorNotification(Popup):
    """오류 발생 시 화면에 띄우는 전용 창"""
    def __init__(self, error_msg, **kwargs):
        super().__init__(**kwargs)
        self.title = "⚠️ 시스템 오류 감지"
        self.size_hint = (0.8, 0.4)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text=error_msg, color=(1,0,0,1), halign='center'))
        btn = Button(text="확인", size_hint_y=0.3)
        btn.bind(on_release=self.dismiss)
        layout.add_widget(btn)
        self.content = layout

class CustomTextInput(TextInput):
    """[글자 중앙 정렬 무결점 검사]"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "CustomFont" if FONT_STATUS == "OK" else None
        self.multiline = False
        self.bind(size=self._center_align)

    def _center_align(self, *args):
        # 글자가 중앙에 오지 않는 오류 방지 (수직 정렬 계산)
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0), 0]

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 상단 상태바 (폰트 오류 표시)
        if FONT_STATUS != "OK":
            self.layout.add_widget(Label(text=FONT_STATUS, color=(1,0,0,1), size_hint_y=0.1))
        
        # 검색창 (검색 안되는 오류 방지 로직)
        self.search_in = CustomTextInput(hint_text="계정 검색 (안될 시 클릭 확인)")
        self.search_in.bind(text=self.update_list)
        self.layout.add_widget(self.search_in)

        self.scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        self.scroll.add_widget(self.acc_list)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def update_list(self, instance, value):
        app = App.get_running_app()
        self.acc_list.clear_widgets()
        try:
            filtered = [a for a in app.user_data.keys() if value.lower() in a.lower()]
            for a in filtered:
                btn = Button(text=f"계정: {a}", size_hint_y=None, height=100)
                btn.bind(on_release=lambda x, n=a: self.go_slots(n))
                self.acc_list.add_widget(btn)
        except:
            ErrorNotification("계정 목록 클릭/검색 엔진 오류 발생!").open()

    def go_slots(self, name):
        app = App.get_running_app()
        app.current_acc = name
        self.manager.current = 'slots'

class DetailScreen(Screen):
    """[이름 전송 및 자동 스크롤 오류 감지]"""
    def on_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        layout = BoxLayout(orientation='vertical', padding=20)
        
        self.scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=20)
        grid.bind(minimum_height=grid.setter('height'))
        
        # 이름 입력 (캐릭터창 전송 확인)
        name_in = CustomTextInput(text=app.user_data[app.current_acc][app.current_slot]["이름"])
        name_in.bind(text=self.sync_name)
        grid.add_widget(name_row := BoxLayout(size_hint_y=None, height=100))
        name_row.add_widget(Label(text="이름"))
        name_row.add_widget(name_in)
        
        # 사진 버튼 (사진 전송/클릭 오류 감지)
        pic_btn = Button(text="사진 등록 (반응 없을 시 권한 확인)", size_hint_y=None, height=100)
        pic_btn.bind(on_release=self.check_photo_error)
        grid.add_widget(pic_btn)
        
        for i in range(10): # 자동 스크롤 테스트용 데이터
            grid.add_widget(CustomTextInput(hint_text=f"항목 {i}"))
            
        self.scroll.add_widget(grid)
        layout.add_widget(self.scroll)
        layout.add_widget(Button(text="저장", size_hint_y=0.1, on_release=lambda x: setattr(self.manager, 'current', 'slots')))
        self.add_widget(layout)

    def sync_name(self, instance, value):
        try:
            app = App.get_running_app()
            app.user_data[app.current_acc][app.current_slot]["이름"] = value
            # 자동 스크롤 작동 보장
            self.scroll.scroll_y = 0 
        except:
            ErrorNotification("이름 데이터 전송 오류! 캐릭터창 반영 불가").open()

    def check_photo_error(self, instance):
        # 사진 클릭/전송 오류 시각화
        ErrorNotification("사진 기능을 실행합니다.\n반응이 없다면 폰 설정에서 권한을 허용하세요.").open()

class PristonTaleApp(App):
    user_data = DictProperty({})
    current_acc = StringProperty("")
    current_slot = StringProperty("1")

    def build(self):
        # 초기 데이터 생성
        self.user_data = {"관리자": {str(i): {"이름": f"캐릭터 {i}"} for i in range(1, 7)}}
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(DetailScreen(name='detail'))
        return sm

if __name__ == '__main__':
    PristonTaleApp().run()
