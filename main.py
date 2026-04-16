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
from kivy.properties import StringProperty, ListProperty, DictProperty
from kivy.clock import Clock

# [폰트 무결성 수정] 모든 위젯에서 한글 깨짐 방지를 위해 전역 등록
FONT_PATH = "font.ttf"
try:
    LabelBase.register(name="CustomFont", fn_regular=FONT_PATH)
except Exception as e:
    print(f"Font Load Error: {e}")

class CustomTextInput(TextInput):
    """글자 중앙 배치 및 폰트 강제 적용"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "CustomFont"
        self.multiline = False
        self.font_size = '18sp'
        self.cursor_color = get_color_from_hex('#1a4361')
        self.background_color = (1, 1, 1, 0.9)
        self.bind(size=self._update_padding)

    def _update_padding(self, *args):
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0), 0]

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg = Image(source='bg.png', allow_stretch=True, keep_ratio=False, size=Window.size)

class MainScreen(BaseScreen):
    """계정 관리 및 전체 검색"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 40, 20, 20], spacing=15)
        self.layout.add_widget(Label(text="PristonTale", font_name="CustomFont", font_size='32sp', size_hint_y=0.1))
        
        search_area = BoxLayout(size_hint_y=0.08, spacing=5)
        self.search_in = CustomTextInput(hint_text="계정 검색...")
        self.search_in.bind(text=self.filter_accs)
        search_area.add_widget(self.search_in)
        self.layout.add_widget(search_area)
        
        add_btn = Button(text="+ 새 계정 만들기", size_hint_y=0.08, background_color=get_color_from_hex('#27ae60'), font_name="CustomFont")
        add_btn.bind(on_release=self.add_acc_pop)
        self.layout.add_widget(add_btn)
        
        self.scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, size_hint_y=None, spacing=12)
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        self.scroll.add_widget(self.acc_list)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def filter_accs(self, instance, value):
        app = App.get_running_app()
        self.acc_list.clear_widgets()
        filtered = [a for a in app.user_data.keys() if value.lower() in a.lower()]
        for a in filtered:
            row = BoxLayout(size_hint_y=None, height=100, spacing=8)
            btn = Button(text=f"계정: {a}", background_color=get_color_from_hex('#1e3a5f'), font_name="CustomFont")
            btn.bind(on_release=lambda x, n=a: self.go_slots(n))
            row.add_widget(btn)
            self.acc_list.add_widget(row)

    def add_acc_pop(self, *args):
        content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        self.new_id = CustomTextInput(hint_text="계정 ID 입력")
        done = Button(text="생성 완료", size_hint_y=0.4, font_name="CustomFont")
        content.add_widget(self.new_id); content.add_widget(done)
        pop = Popup(title="계정 생성", content=content, size_hint=(0.8, 0.4), title_font="CustomFont")
        done.bind(on_release=lambda x: [self.create_account(self.new_id.text), pop.dismiss()])
        pop.open()

    def create_account(self, acc_id):
        app = App.get_running_app()
        if acc_id.strip() and acc_id not in app.user_data:
            app.user_data[acc_id] = {str(i): {"이름": f"슬롯 {i}"} for i in range(1, 7)}
            self.filter_accs(None, self.search_in.text)

    def go_slots(self, name):
        app = App.get_running_app()
        app.current_acc = name
        self.manager.current = 'slots'

class SlotScreen(BaseScreen):
    """이름 자동 동기화 슬롯창 (7번 디자인)"""
    def on_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(text=f"[{app.current_acc}] 캐릭터 선택", font_name="CustomFont", font_size='22sp', size_hint_y=0.1))
        
        grid = GridLayout(cols=2, spacing=15, size_hint_y=0.7)
        for i in range(1, 7):
            char_name = app.user_data[app.current_acc][str(i)]["이름"]
            btn = Button(text=f"{char_name}", background_color=get_color_from_hex('#2c3e50'), font_name="CustomFont", halign='center')
            btn.bind(on_release=lambda x, s=i: self.go_detail(s))
            grid.add_widget(btn)
        layout.add_widget(grid)
        
        back = Button(text="뒤로가기", size_hint_y=0.1, font_name="CustomFont", on_release=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back); self.add_widget(layout)

    def go_detail(self, slot_num):
        app = App.get_running_app()
        app.current_slot = str(slot_num)
        self.manager.current = 'detail'

class DetailScreen(BaseScreen):
    """이름 입력 시 슬롯 자동 동기화 로직 포함"""
    def on_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        char_info = app.user_data[app.current_acc][app.current_slot]
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="[ 캐릭터 정보 ]", font_name="CustomFont", size_hint_y=0.08))
        
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=15)
        grid.bind(minimum_height=grid.setter('height'))
        
        # 이름 입력칸 (자동 동기화 핵심)
        name_row = BoxLayout(size_hint_y=None, height=90, spacing=10)
        name_row.add_widget(Label(text="이름", font_name="CustomFont", size_hint_x=0.3))
        self.name_input = CustomTextInput(text=char_info["이름"])
        self.name_input.bind(text=self.update_name)
        name_row.add_widget(self.name_input)
        grid.add_widget(name_row)
        
        stats = ["직위", "클랜", "레벨", "생명력", "기력", "근력", "힘", "정신력", "재능", "민첩", "건강", "명중", "공격", "방어", "흡수", "속도"]
        for s in stats:
            row = BoxLayout(size_hint_y=None, height=90, spacing=10)
            row.add_widget(Label(text=s, font_name="CustomFont", size_hint_x=0.3))
            row.add_widget(CustomTextInput(text=""))
            grid.add_widget(row)
            
        scroll.add_widget(grid); layout.add_widget(scroll)
        
        back = Button(text="저장 후 나가기", size_hint_y=0.1, font_name="CustomFont", on_release=lambda x: setattr(self.manager, 'current', 'slots'))
        layout.add_widget(back); self.add_widget(layout)

    def update_name(self, instance, value):
        app = App.get_running_app()
        # [이름 자동 동기화] 입력 즉시 데이터 갱신
        app.user_data[app.current_acc][app.current_slot]["이름"] = value

class PristonTaleApp(App):
    user_data = DictProperty({}) # 전역 데이터
    current_acc = StringProperty("")
    current_slot = StringProperty("")

    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SlotScreen(name='slots'))
        sm.add_widget(DetailScreen(name='detail'))
        return sm

if __name__ == '__main__':
    PristonTaleApp().run()
