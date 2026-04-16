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

# [자가 진단] 폰트 등록 및 예외 처리
try:
    if os.path.exists("font.ttf"):
        LabelBase.register(name="CustomFont", fn_regular="font.ttf")
    else:
        print("[자가진단] 경고: font.ttf 파일이 없습니다.")
except Exception as e:
    print(f"[자가진단] 폰트 등록 오류: {e}")

class CustomTextInput(TextInput):
    """S26 Ultra 해상도 대응: 글자 수직 정중앙 정렬 보정"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "CustomFont" if os.path.exists("font.ttf") else None
        self.multiline = False
        self.font_size = '18sp'
        self.cursor_color = get_color_from_hex('#1a4361')
        self.background_color = (1, 1, 1, 0.9)
        self.bind(size=self._update_padding)
        self.bind(text=self._on_text)

    def _update_padding(self, *args):
        # 정밀 계산: (칸 높이 / 2) - (글자 높이 / 2)
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0), 0]

    def _on_text(self, instance, value):
        app = App.get_running_app()
        current_screen = app.root.current_screen
        if hasattr(current_screen, 'scroll_to_bottom'):
            current_screen.scroll_to_bottom()

def show_confirm(title, text, on_confirm):
    """자가 진단 및 안전 장치 팝업"""
    content = BoxLayout(orientation='vertical', padding=20, spacing=20)
    msg = Label(text=text, font_size='17sp', halign='center')
    if os.path.exists("font.ttf"): msg.font_name = "CustomFont"
    
    content.add_widget(msg)
    btns = BoxLayout(size_hint_y=0.4, spacing=10)
    ok_btn = Button(text="확인", background_color=get_color_from_hex('#27ae60'))
    can_btn = Button(text="취소", background_color=get_color_from_hex('#c0392b'))
    if os.path.exists("font.ttf"):
        ok_btn.font_name = "CustomFont"
        can_btn.font_name = "CustomFont"
        
    popup = Popup(title=title, content=content, size_hint=(0.85, 0.35))
    if os.path.exists("font.ttf"): popup.title_font = "CustomFont"
    
    ok_btn.bind(on_release=lambda x: [on_confirm(), popup.dismiss()])
    can_btn.bind(on_release=popup.dismiss)
    btns.add_widget(ok_btn); btns.add_widget(can_btn)
    content.add_widget(btns); popup.open()

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            # 배경 이미지(73193.jpg -> bg.png) 설정
            self.bg = Image(source='bg.png', allow_stretch=True, keep_ratio=False, size=Window.size)

class MainScreen(BaseScreen):
    accounts = ListProperty([]) 
    filtered_accounts = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 40, 20, 20], spacing=15)
        title_lbl = Label(text="PristonTale", font_size='32sp', size_hint_y=0.1)
        if os.path.exists("font.ttf"): title_lbl.font_name = "CustomFont"
        self.layout.add_widget(title_lbl)
        
        search_area = BoxLayout(size_hint_y=0.08, spacing=5)
        self.search_in = CustomTextInput(hint_text="계정 검색...")
        self.search_in.bind(text=self.filter_results)
        search_area.add_widget(self.search_in)
        self.layout.add_widget(search_area)
        
        add_btn = Button(text="+ 새 계정 만들기", size_hint_y=0.08, background_color=get_color_from_hex('#27ae60'))
        if os.path.exists("font.ttf"): add_btn.font_name = "CustomFont"
        add_btn.bind(on_release=self.add_acc_pop)
        self.layout.add_widget(add_btn)
        
        self.scroll = ScrollView()
        self.acc_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=12)
        self.acc_list_layout.bind(minimum_height=self.acc_list_layout.setter('height'))
        self.scroll.add_widget(self.acc_list_layout)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def filter_results(self, instance, value):
        if not value: self.filtered_accounts = self.accounts
        else: self.filtered_accounts = [a for a in self.accounts if value.lower() in a.lower()]

    def on_filtered_accounts(self, instance, value):
        self.acc_list_layout.clear_widgets()
        for a in value:
            row = BoxLayout(size_hint_y=None, height=100, spacing=8)
            btn = Button(text=f"계정: {a}", background_color=get_color_from_hex('#1e3a5f'), font_size='18sp')
            if os.path.exists("font.ttf"): btn.font_name = "CustomFont"
            btn.bind(on_release=lambda x, n=a: self.go_slots(n))
            del_btn = Button(text="X", size_hint_x=0.15, background_color=get_color_from_hex('#c0392b'))
            del_btn.bind(on_release=lambda x, n=a: show_confirm("삭제", f"'{n}' 계정을 삭제하시겠습니까?", lambda: self.delete_account(n)))
            row.add_widget(btn); row.add_widget(del_btn)
            self.acc_list_layout.add_widget(row)

    def add_acc_pop(self, *args):
        content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        self.new_id_input = CustomTextInput(hint_text="새 계정 ID 입력")
        done = Button(text="생성 완료", size_hint_y=0.4, background_color=get_color_from_hex('#1e5631'))
        if os.path.exists("font.ttf"): done.font_name = "CustomFont"
        content.add_widget(self.new_id_input); content.add_widget(done)
        pop = Popup(title="계정 생성", content=content, size_hint=(0.8, 0.4))
        if os.path.exists("font.ttf"): pop.title_font = "CustomFont"
        done.bind(on_release=lambda x: [self.create_account(self.new_id_input.text), pop.dismiss()])
        pop.open()

    def create_account(self, acc_id):
        if acc_id.strip() and acc_id not in self.accounts:
            self.accounts.append(acc_id.strip())
            self.filter_results(None, self.search_in.text)

    def delete_account(self, acc_id):
        if acc_id in self.accounts: self.accounts.remove(acc_id)
        self.filter_results(None, self.search_in.text)

    def go_slots(self, name):
        self.manager.get_screen('slots').acc_name = name
        self.manager.current = 'slots'

class SlotScreen(BaseScreen):
    """이미지 레이아웃 반영: 반투명 보라 버튼 6슬롯 디자인"""
    acc_name = StringProperty("")
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=[30, 50, 30, 30], spacing=20)
        title = Label(text=f"[{self.acc_name}] 캐릭터 선택", font_size='24sp', size_hint_y=0.1)
        if os.path.exists("font.ttf"): title.font_name = "CustomFont"
        layout.add_widget(title)
        
        grid = GridLayout(cols=2, spacing=15, size_hint_y=0.7)
        for i in range(1, 7):
            btn = Button(
                text=f"슬롯 {i}", 
                background_color=(0.2, 0.2, 0.5, 0.6), # 반투명 보라
                font_size='18sp',
                halign='center'
            )
            if os.path.exists("font.ttf"): btn.font_name = "CustomFont"
            btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'detail'))
            grid.add_widget(btn)
        layout.add_widget(grid)
        
        back = Button(text="처음으로", size_hint_y=0.1, background_color=(0.3, 0.3, 0.3, 0.8))
        if os.path.exists("font.ttf"): back.font_name = "CustomFont"
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back); self.add_widget(layout)

class DetailScreen(BaseScreen):
    """요청 반영: 항목 그룹화 및 그룹 간 여백(한 칸 띄우기) 적용"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        title = Label(text="[ 캐릭터 정보 ]", size_hint_y=0.08)
        if os.path.exists("font.ttf"): title.font_name = "CustomFont"
        layout.add_widget(title)
        
        self.scroll = ScrollView(do_scroll_x=False)
        self.grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        # 지시하신 그룹별 항목 구성
        groups = [
            ["직위", "클랜", "레벨"],
            ["생명력", "기력", "근력", "힘"],
            ["정신력", "재능", "민첩", "건강", "명중"],
            ["공격", "방어", "흡수", "속도"]
        ]
        
        for idx, group in enumerate(groups):
            for s in group:
                row = BoxLayout(size_hint_y=None, height=90, spacing=10)
                lbl = Label(text=s, size_hint_x=0.3)
                if os.path.exists("font.ttf"): lbl.font_name = "CustomFont"
                row.add_widget(lbl)
                row.add_widget(CustomTextInput())
                self.grid.add_widget(row)
            
            # 그룹 사이 '한 칸 띄우기' (여백 추가)
            if idx < len(groups) - 1:
                self.grid.add_widget(BoxLayout(size_hint_y=None, height=45))
            
        self.scroll.add_widget(self.grid); layout.add_widget(self.scroll)
        
        nav = BoxLayout(size_hint_y=0.12, spacing=5)
        for t in ["장비", "인벤토리", "저장"]:
            b = Button(text=t, background_color=get_color_from_hex('#1a3a5a'))
            if os.path.exists("font.ttf"): b.font_name = "CustomFont"
            if t=="장비": b.bind(on_release=lambda x: setattr(self.manager, 'current', 'equip'))
            elif t=="인벤토리": b.bind(on_release=lambda x: setattr(self.manager, 'current', 'inven'))
            elif t=="저장": b.bind(on_release=lambda x: show_confirm("알림", "저장되었습니다.", lambda: None))
            nav.add_widget(b)
        layout.add_widget(nav)
        
        back = Button(text="뒤로가기", size_hint_y=0.08, on_release=lambda x: setattr(self.manager, 'current', 'slots'))
        if os.path.exists("font.ttf"): back.font_name = "CustomFont"
        layout.add_widget(back); self.add_widget(layout)

    def scroll_to_bottom(self):
        self.scroll.scroll_y = 0

class EquipScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        self.scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=20)
        content.bind(minimum_height=content.setter('height'))
        
        items = ["한손무기", "두손무기", "갑옷", "방패", "장갑", "부츠", "암릿", "링", "링", "아뮬렛", "기타"]
        for i in items:
            row = BoxLayout(size_hint_y=None, height=90, spacing=10)
            lbl = Label(text=i, size_hint_x=0.3)
            if os.path.exists("font.ttf"): lbl.font_name = "CustomFont"
            row.add_widget(lbl)
            row.add_widget(CustomTextInput(hint_text="입력..."))
            content.add_widget(row)
            
        self.scroll.add_widget(content); layout.add_widget(self.scroll)
        back = Button(text="뒤로가기", size_hint_y=0.1, on_release=lambda x: setattr(self.manager, 'current', 'detail'))
        if os.path.exists("font.ttf"): back.font_name = "CustomFont"
        layout.add_widget(back); self.add_widget(layout)

    def scroll_to_bottom(self):
        self.scroll.scroll_y = 0

class InvenScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.scroll = ScrollView()
        self.item_list = GridLayout(cols=1, size_hint_y=None, spacing=15)
        self.item_list.bind(minimum_height=self.item_list.setter('height'))
        self.scroll.add_widget(self.item_list)
        layout.add_widget(self.scroll)
        
        add = Button(text="+ 아이템 추가", size_hint_y=0.1, background_color=get_color_from_hex('#27ae60'))
        if os.path.exists("font.ttf"): add.font_name = "CustomFont"
        add.bind(on_release=self.add_row)
        layout.add_widget(add)
        
        back = Button(text="뒤로가기", size_hint_y=0.08, on_release=lambda x: setattr(self.manager, 'current', 'detail'))
        if os.path.exists("font.ttf"): back.font_name = "CustomFont"
        layout.add_widget(back); self.add_widget(layout)

    def add_row(self, *args):
        row = BoxLayout(size_hint_y=None, height=90, spacing=8)
        row.add_widget(CustomTextInput(hint_text="옵션 입력..."))
        del_b = Button(text="X", size_hint_x=0.2, background_color=get_color_from_hex('#c0392b'))
        del_b.bind(on_release=lambda x: self.item_list.remove_widget(row))
        row.add_widget(del_b)
        self.item_list.add_widget(row)
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.1)

    def scroll_to_bottom(self):
        self.scroll.scroll_y = 0

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
