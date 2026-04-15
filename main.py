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
from kivy.properties import StringProperty, ListProperty

# 폰트 등록
try:
    LabelBase.register(name="CustomFont", fn_regular="font.ttf")
except:
    pass

class CustomTextInput(TextInput):
    """S26 울트라 보정: 글자가 줄 바로 위에 오도록 패딩 조정"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "CustomFont"
        self.multiline = False
        self.background_color = (1, 1, 1, 0.9)
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0) + 12, 0]

def show_confirm(title, text, on_confirm):
    """사진 73755.jpg 스타일 확인 팝업"""
    content = BoxLayout(orientation='vertical', padding=20, spacing=20)
    content.add_widget(Label(text=text, font_name="CustomFont", font_size='16sp', halign='center'))
    btns = BoxLayout(size_hint_y=0.4, spacing=10)
    ok_btn = Button(text="확인", background_color=get_color_from_hex('#1a4361'), font_name="CustomFont")
    can_btn = Button(text="취소", background_color=get_color_from_hex('#444444'), font_name="CustomFont")
    popup = Popup(title=title, content=content, size_hint=(0.85, 0.35), title_font="CustomFont")
    ok_btn.bind(on_release=lambda x: [on_confirm(), popup.dismiss()])
    can_btn.bind(on_release=popup.dismiss)
    btns.add_widget(ok_btn); btns.add_widget(can_btn)
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
        layout = BoxLayout(orientation='vertical', padding=[20, 40, 20, 20], spacing=10)
        layout.add_widget(Label(text="[PT1 통합 매니저]", font_name="CustomFont", font_size='24sp', size_hint_y=0.08))
        
        search_area = BoxLayout(size_hint_y=0.08, spacing=2)
        self.search_in = CustomTextInput(hint_text="전체 검색(계정, 아이템, 레벨 등)")
        search_btn = Button(text="검색", size_hint_x=0.2, background_color=get_color_from_hex('#1a3a5a'), font_name="CustomFont")
        search_area.add_widget(self.search_in); search_area.add_widget(search_btn)
        layout.add_widget(search_area)
        
        add_btn = Button(text="+ 새 계정 만들기", size_hint_y=0.08, background_color=get_color_from_hex('#27ae60'), font_name="CustomFont")
        add_btn.bind(on_release=self.add_account_popup)
        layout.add_widget(add_btn)
        
        self.scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, size_hint_y=None, spacing=8)
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        self.scroll.add_widget(self.acc_list)
        layout.add_widget(self.scroll)
        self.add_widget(layout)
        self.refresh(["toopen", "toopen0", "toopen9"])

    def refresh(self, accs):
        self.acc_list.clear_widgets()
        for a in accs:
            row = BoxLayout(size_hint_y=None, height=70, spacing=5)
            btn = Button(text=f"계정: {a}", background_color=get_color_from_hex('#1e3a5f'), font_name="CustomFont")
            btn.bind(on_release=lambda x, name=a: self.go_slots(name))
            del_btn = Button(text="X", size_hint_x=0.2, background_color=get_color_from_hex('#5a1a1a'))
            del_btn.bind(on_release=lambda x: show_confirm("삭제", "계정을 삭제하시겠습니까?", lambda: print("Deleted")))
            row.add_widget(btn); row.add_widget(del_btn)
            self.acc_list.add_widget(row)

    def add_account_popup(self, inst):
        content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        new_id = CustomTextInput(hint_text="생성할 계정 ID")
        done = Button(text="생성 완료", size_hint_y=0.4, background_color=get_color_from_hex('#1e5631'), font_name="CustomFont")
        content.add_widget(new_id); content.add_widget(done)
        pop = Popup(title="계정 생성", content=content, size_hint=(0.8, 0.4), title_font="CustomFont")
        done.bind(on_release=pop.dismiss); pop.open()

    def go_slots(self, name):
        self.manager.get_screen('slots').acc_name = name
        self.manager.current = 'slots'

class SlotScreen(BaseScreen):
    acc_name = StringProperty("")
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=25, spacing=15)
        layout.add_widget(Label(text=f"[{self.acc_name}] 캐릭터 선택", font_name="CustomFont", font_size='20sp', size_hint_y=0.1))
        grid = GridLayout(cols=2, spacing=10, size_hint_y=0.7)
        for i in range(1, 7):
            btn = Button(text=f"슬롯 {i}\n(캐릭터 이름)", background_color=get_color_from_hex('#4a5a8a'), font_name="CustomFont")
            btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'detail'))
            grid.add_widget(btn)
        layout.add_widget(grid)
        back = Button(text="처음으로", size_hint_y=0.1, background_color=get_color_from_hex('#555555'), font_name="CustomFont")
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back); self.add_widget(layout)

class DetailScreen(BaseScreen):
    """정보 모드: 스탯 출력"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="[ 캐릭터 정보 ]", font_name="CustomFont", size_hint_y=0.1))
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))
        stats = ["직위", "이름", "클랜", "레벨", "생명력", "기력", "근력", "힘", "정신력", "재능", "민첩", "건강", "명중", "공격", "방어", "흡수", "속도"]
        for s in stats:
            row = BoxLayout(size_hint_y=None, height=45)
            row.add_widget(Label(text=s, font_name="CustomFont", size_hint_x=0.4))
            row.add_widget(CustomTextInput(text="0"))
            grid.add_widget(row)
        scroll.add_widget(grid); layout.add_widget(scroll)
        
        nav = BoxLayout(size_hint_y=0.1, spacing=5)
        btn1 = Button(text="장비", font_name="CustomFont", on_release=lambda x: setattr(self.manager, 'current', 'equip'))
        btn2 = Button(text="인벤토리", font_name="CustomFont", on_release=lambda x: setattr(self.manager, 'current', 'inven'))
        btn3 = Button(text="저장", background_color=get_color_from_hex('#2980b9'), font_name="CustomFont", on_release=lambda x: show_confirm("저장", "저장하시겠습니까?", lambda: print("Saved")))
        nav.add_widget(btn1); nav.add_widget(btn2); nav.add_widget(btn3)
        layout.add_widget(nav); self.add_widget(layout)

class EquipScreen(BaseScreen):
    """장비 모드 및 사진 연동"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="[ 장비 및 사진 ]", font_name="CustomFont", size_hint_y=0.1))
        
        items = ["무기", "갑옷", "방패", "장갑", "부츠", "링1", "링2", "아뮬렛"]
        grid = GridLayout(cols=2, spacing=5, size_hint_y=0.5)
        for i in items:
            grid.add_widget(Label(text=i, font_name="CustomFont"))
            grid.add_widget(CustomTextInput(hint_text="장비명"))
        layout.add_widget(grid)
        
        pic_btn = Button(text="사진 추가 (갤러리)", size_hint_y=0.1, background_color=get_color_from_hex('#8e44ad'), font_name="CustomFont")
        layout.add_widget(pic_btn)
        
        back = Button(text="뒤로가기", size_hint_y=0.1, on_release=lambda x: setattr(self.manager, 'current', 'detail'))
        layout.add_widget(back); self.add_widget(layout)

class InvenScreen(BaseScreen):
    """인벤토리 모드"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="[ 인벤토리 리스트 ]", font_name="CustomFont", size_hint_y=0.1))
        self.scroll = ScrollView()
        self.list = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.list.bind(minimum_height=self.list.setter('height'))
        self.scroll.add_widget(self.list)
        layout.add_widget(self.scroll)
        
        add_btn = Button(text="+ 아이템 추가", size_hint_y=0.1, font_name="CustomFont")
        add_btn.bind(on_release=self.add_item)
        layout.add_widget(add_btn)
        layout.add_widget(Button(text="뒤로가기", size_hint_y=0.1, on_release=lambda x: setattr(self.manager, 'current', 'detail')))
        self.add_widget(layout)

    def add_item(self, x):
        row = BoxLayout(size_hint_y=None, height=50)
        row.add_widget(CustomTextInput(hint_text="아이템 이름"))
        del_b = Button(text="-", size_hint_x=0.2, on_release=lambda x: self.list.remove_widget(row))
        row.add_widget(del_b)
        self.list.add_widget(row)

class PristonTaleApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SlotScreen(name='slots'))
        sm.add_widget(DetailScreen(name='detail'))
        sm.add_widget(EquipScreen(name='equip'))
        sm.add_widget(InvenScreen(name='inven'))
        return sm

if __name__ == '__main__':
    PristonTaleApp().run()
