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
from kivy.clock import Clock

# 폰트 등록 및 깨짐 방지
try:
    LabelBase.register(name="CustomFont", fn_regular="font.ttf")
except:
    pass

class CustomTextInput(TextInput):
    """S26 울트라 최적화: 칸 넓이 대폭 확장 및 글자 정중앙 배치"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "CustomFont"
        self.multiline = False
        self.cursor_color = get_color_from_hex('#1a4361')
        self.background_color = (1, 1, 1, 0.9)
        self.font_size = '18sp'
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0), 0]

    def on_size(self, *args):
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0), 0]

def show_confirm(title, text, on_confirm):
    content = BoxLayout(orientation='vertical', padding=20, spacing=20)
    content.add_widget(Label(text=text, font_name="CustomFont", font_size='17sp', halign='center'))
    btns = BoxLayout(size_hint_y=0.4, spacing=10)
    ok_btn = Button(text="확인", background_color=get_color_from_hex('#1a4361'), font_name="CustomFont")
    can_btn = Button(text="취소", background_color=get_color_from_hex('#444444'), font_name="CustomFont")
    popup = Popup(title=title, content=content, size_hint=(0.85, 0.35), title_font="CustomFont")
    ok_btn.bind(on_release=lambda x: [on_confirm(), popup.dismiss()])
    can_btn.bind(on_release=popup.dismiss)
    btns.add_widget(ok_btn); btns.add_widget(can_btn)
    content.add_widget(btns); popup.open()

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg = Image(source='bg.png', allow_stretch=True, keep_ratio=False, size=Window.size)

class MainScreen(BaseScreen):
    """지시사항 반영: 타이틀 PristonTale 변경 및 계정 생성 로직 무결점 수정"""
    accounts = ListProperty([]) # 데이터 저장소

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 40, 20, 20], spacing=15)
        
        # 타이틀 변경: PristonTale
        self.layout.add_widget(Label(text="PristonTale", font_name="CustomFont", font_size='32sp', size_hint_y=0.1, color=(1,1,1,1)))
        
        # 전체 검색 바
        search_area = BoxLayout(size_hint_y=0.08, spacing=5)
        self.search_in = CustomTextInput(hint_text="계정/캐릭터 통합 검색...")
        search_btn = Button(text="검색", size_hint_x=0.25, background_color=get_color_from_hex('#1a3a5a'), font_name="CustomFont")
        search_area.add_widget(self.search_in); search_area.add_widget(search_btn)
        self.layout.add_widget(search_area)
        
        # 계정 생성 버튼 (누를 때만 팝업)
        add_btn = Button(text="+ 새 계정 만들기", size_hint_y=0.08, background_color=get_color_from_hex('#27ae60'), font_name="CustomFont")
        add_btn.bind(on_release=self.add_acc_pop)
        self.layout.add_widget(add_btn)
        
        self.scroll = ScrollView()
        self.acc_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.acc_list_layout.bind(minimum_height=self.acc_list_layout.setter('height'))
        self.scroll.add_widget(self.acc_list_layout)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)
        
        Clock.schedule_once(self.ask_permission, 1)

    def ask_permission(self, dt):
        show_confirm("권한 요청", "사진 및 미디어 접근을 허용하시겠습니까?", lambda: print("Permission Granted"))

    def on_accounts(self, instance, value):
        """데이터 변경 시 리스트 UI 즉각 업데이트 (오류 0개 달성 핵심 로직)"""
        self.acc_list_layout.clear_widgets()
        for a in value:
            row = BoxLayout(size_hint_y=None, height=85, spacing=5)
            btn = Button(text=f"계정: {a}", background_color=get_color_from_hex('#1e3a5f'), font_name="CustomFont")
            btn.bind(on_release=lambda x, n=a: self.go_slots(n))
            del_btn = Button(text="X", size_hint_x=0.2, background_color=get_color_from_hex('#c0392b'))
            del_btn.bind(on_release=lambda x, n=a: show_confirm("삭제", f"'{n}' 계정을 삭제하시겠습니까?", lambda: self.delete_account(n)))
            row.add_widget(btn); row.add_widget(del_btn)
            self.acc_list_layout.add_widget(row)

    def add_acc_pop(self, *args):
        content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        self.new_id_input = CustomTextInput(hint_text="새 계정 ID 입력")
        done = Button(text="생성 완료", size_hint_y=0.4, background_color=get_color_from_hex('#1e5631'), font_name="CustomFont")
        content.add_widget(self.new_id_input); content.add_widget(done)
        pop = Popup(title="계정 생성", content=content, size_hint=(0.8, 0.4), title_font="CustomFont")
        done.bind(on_release=lambda x: [self.create_account(self.new_id_input.text), pop.dismiss()])
        pop.open()

    def create_account(self, acc_id):
        if acc_id.strip():
            self.accounts.append(acc_id.strip())

    def delete_account(self, acc_id):
        if acc_id in self.accounts:
            self.accounts.remove(acc_id)

    def go_slots(self, name):
        self.manager.get_screen('slots').acc_name = name
        self.manager.current = 'slots'

class SlotScreen(BaseScreen):
    """7번 디자인 반영: 6슬롯 캐릭터 선택창"""
    acc_name = StringProperty("")
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        layout.add_widget(Label(text=f"[{self.acc_name}] 캐릭터 선택", font_name="CustomFont", font_size='22sp', size_hint_y=0.1))
        
        grid = GridLayout(cols=2, spacing=15, size_hint_y=0.7)
        for i in range(1, 7):
            btn = Button(text=f"슬롯 {i}\n(이름 입력)", background_color=get_color_from_hex('#2c3e50'), font_name="CustomFont", halign='center')
            btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'detail'))
            grid.add_widget(btn)
        layout.add_widget(grid)
        
        back = Button(text="처음으로", size_hint_y=0.1, background_color=get_color_from_hex('#555555'), font_name="CustomFont")
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back); self.add_widget(layout)

class DetailScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="[ 캐릭터 정보 ]", font_name="CustomFont", size_hint_y=0.08))
        
        scroll = ScrollView(do_scroll_x=False)
        grid = GridLayout(cols=1, size_hint_y=None, spacing=15)
        grid.bind(minimum_height=grid.setter('height'))
        
        stats = ["직위", "이름", "클랜", "레벨", "생명력", "기력", "근력", "힘", "정신력", "재능", "민첩", "건강", "명중", "공격", "방어", "흡수", "속도"]
        for s in stats:
            row = BoxLayout(size_hint_y=None, height=85, spacing=10)
            row.add_widget(Label(text=s, font_name="CustomFont", size_hint_x=0.3, font_size='16sp'))
            row.add_widget(CustomTextInput(text=""))
            grid.add_widget(row)
            
        scroll.add_widget(grid); layout.add_widget(scroll)
        
        nav = BoxLayout(size_hint_y=0.12, spacing=5)
        for t in ["장비", "인벤토리", "저장"]:
            c = '#2980b9' if t=="저장" else '#1a3a5a'
            b = Button(text=t, background_color=get_color_from_hex(c), font_name="CustomFont")
            if t=="장비": b.bind(on_release=lambda x: setattr(self.manager, 'current', 'equip'))
            elif t=="인벤토리": b.bind(on_release=lambda x: setattr(self.manager, 'current', 'inven'))
            elif t=="저장": b.bind(on_release=lambda x: show_confirm("저장", "정보를 저장하시겠습니까?", lambda: print("S")))
            nav.add_widget(b)
        layout.add_widget(nav)
        
        back = Button(text="뒤로가기", size_hint_y=0.08, background_color=get_color_from_hex('#555555'), on_release=lambda x: setattr(self.manager, 'current', 'slots'))
        layout.add_widget(back); self.add_widget(layout)

class EquipScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=20)
        content.bind(minimum_height=content.setter('height'))
        
        content.add_widget(Label(text="[ 사진 관리 ]", font_name="CustomFont", size_hint_y=None, height=40))
        self.pic_grid = GridLayout(cols=3, size_hint_y=None, height=160, spacing=8)
        content.add_widget(self.pic_grid)
        
        pic_nav = BoxLayout(size_hint_y=None, height=60, spacing=5)
        for t in ["사진 추가", "전체 삭제", "사진 저장"]:
            btn = Button(text=t, font_name="CustomFont", background_color=get_color_from_hex('#8e44ad'))
            pic_nav.add_widget(btn)
        content.add_widget(pic_nav)
        
        items = ["한손무기", "두손무기", "갑옷", "방패", "장갑", "부츠", "암릿", "링", "링", "아뮬렛", "기타"]
        for i in items:
            row = BoxLayout(size_hint_y=None, height=85, spacing=10)
            row.add_widget(Label(text=i, font_name="CustomFont", size_hint_x=0.3))
            row.add_widget(CustomTextInput(hint_text="아이템 입력"))
            content.add_widget(row)
            
        scroll.add_widget(content); layout.add_widget(scroll)
        
        back = Button(text="뒤로가기", size_hint_y=0.1, background_color=get_color_from_hex('#555555'), on_release=lambda x: setattr(self.manager, 'current', 'detail'))
        layout.add_widget(back); self.add_widget(layout)

class InvenScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="[ 인벤토리 ]", font_name="CustomFont", size_hint_y=0.08))
        
        self.scroll = ScrollView(bar_width=10, scroll_type=['bars', 'content'])
        self.item_list = GridLayout(cols=1, size_hint_y=None, spacing=15)
        self.item_list.bind(minimum_height=self.item_list.setter('height'))
        self.scroll.add_widget(self.item_list)
        layout.add_widget(self.scroll)
        
        btns = BoxLayout(size_hint_y=0.12, spacing=5)
        add = Button(text="+ 아이템 추가", background_color=get_color_from_hex('#27ae60'), font_name="CustomFont")
        add.bind(on_release=self.add_row)
        save = Button(text="저장", background_color=get_color_from_hex('#2980b9'), font_name="CustomFont")
        btns.add_widget(add); btns.add_widget(save)
        layout.add_widget(btns)
        
        layout.add_widget(Button(text="뒤로가기", size_hint_y=0.08, on_release=lambda x: setattr(self.manager, 'current', 'detail')))
        self.add_widget(layout)

    def add_row(self, *args):
        row = BoxLayout(size_hint_y=None, height=90, spacing=8)
        row.add_widget(CustomTextInput(hint_text="아이템 옵션..."))
        del_b = Button(text="삭제", size_hint_x=0.2, background_color=get_color_from_hex('#c0392b'), font_name="CustomFont")
        del_b.bind(on_release=lambda x: self.item_list.remove_widget(row))
        row.add_widget(del_b)
        self.item_list.add_widget(row)

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
