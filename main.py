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

# [자가 진단] 폰트 및 리소스 체크
FONT_PATH = "font.ttf"
BG_PATH = "bg.png"

try:
    if os.path.exists(FONT_PATH):
        LabelBase.register(name="CustomFont", fn_regular=FONT_PATH)
except Exception as e:
    print(f"Font Load Error: {e}")

class CustomTextInput(TextInput):
    """
    S26 Ultra 최적화: 수직 정렬 보정 및 
    긴 글 터치 시 전체 보기 팝업 기능 통합
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "CustomFont" if os.path.exists(FONT_PATH) else None
        self.multiline = False
        self.font_size = '18sp'
        self.cursor_color = get_color_from_hex('#1a4361')
        self.background_color = (1, 1, 1, 0.9)
        self.bind(size=self._update_padding)

    def _update_padding(self, *args):
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0), 0]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            self.show_full_text_popup()
            return True
        return super().on_touch_down(touch)

    def show_full_text_popup(self):
        """사진 피드백: 글이 길면 읽을 수 없다는 점 해결"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        full_input = TextInput(text=self.text, font_name=self.font_name, font_size='18sp', multiline=True)
        close_btn = Button(text="확인 및 닫기", size_hint_y=0.2, background_color=get_color_from_hex('#2980b9'))
        if os.path.exists(FONT_PATH): close_btn.font_name = "CustomFont"
        
        content.add_widget(full_input)
        content.add_widget(close_btn)
        
        popup = Popup(title="전체 내용 보기/수정", content=content, size_hint=(0.9, 0.6))
        if os.path.exists(FONT_PATH): popup.title_font = "CustomFont"
        
        close_btn.bind(on_release=lambda x: [setattr(self, 'text', full_input.text), popup.dismiss()])
        popup.open()

def show_confirm(title, text, on_confirm):
    """사진 피드백: 삭제 시 확인 멘트 강화"""
    content = BoxLayout(orientation='vertical', padding=20, spacing=20)
    msg = Label(text=text, font_size='17sp', halign='center')
    if os.path.exists(FONT_PATH): msg.font_name = "CustomFont"
    content.add_widget(msg)
    
    btns = BoxLayout(size_hint_y=0.4, spacing=10)
    ok_btn = Button(text="확인", background_color=get_color_from_hex('#c0392b'))
    can_btn = Button(text="취소", background_color=get_color_from_hex('#7f8c8d'))
    if os.path.exists(FONT_PATH):
        ok_btn.font_name = "CustomFont"
        can_btn.font_name = "CustomFont"
    
    popup = Popup(title=title, content=content, size_hint=(0.85, 0.35))
    if os.path.exists(FONT_PATH): popup.title_font = "CustomFont"
    
    ok_btn.bind(on_release=lambda x: [on_confirm(), popup.dismiss()])
    can_btn.bind(on_release=popup.dismiss)
    btns.add_widget(ok_btn); btns.add_widget(can_btn)
    content.add_widget(btns); popup.open()

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            source = BG_PATH if os.path.exists(BG_PATH) else ""
            self.bg = Image(source=source, allow_stretch=True, keep_ratio=False, size=Window.size)
        Window.bind(on_keyboard_height=self._on_keyboard_height)

    def _on_keyboard_height(self, window, height):
        """사진 피드백: 자동스크롤 및 글자 가려짐 방지 로직"""
        if height > 0:
            self.y = height * 0.5  # 키보드 높이만큼 화면을 밀어 올림
        else:
            self.y = 0

class MainScreen(BaseScreen):
    accounts = DictProperty({}) # 계정명: {슬롯데이터}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 40, 20, 20], spacing=15)
        title = Label(text="PristonTale Manager", font_size='28sp', size_hint_y=0.1)
        if os.path.exists(FONT_PATH): title.font_name = "CustomFont"
        self.layout.add_widget(title)
        
        # 전체 검색 기능
        search_area = BoxLayout(size_hint_y=0.08)
        self.search_in = CustomTextInput(hint_text="계정 전체 검색...")
        self.search_in.bind(text=self.update_list)
        search_area.add_widget(self.search_in)
        self.layout.add_widget(search_area)
        
        add_btn = Button(text="+ 새 계정 만들기", size_hint_y=0.08, background_color=get_color_from_hex('#27ae60'))
        if os.path.exists(FONT_PATH): add_btn.font_name = "CustomFont"
        add_btn.bind(on_release=self.add_acc_pop)
        self.layout.add_widget(add_btn)
        
        self.scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        self.scroll.add_widget(self.acc_list)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def update_list(self, *args):
        self.acc_list.clear_widgets()
        query = self.search_in.text.lower()
        for acc in self.accounts.keys():
            if query in acc.lower():
                row = BoxLayout(size_hint_y=None, height=100, spacing=5)
                btn = Button(text=f"계정: {acc}", background_color=get_color_from_hex('#2c3e50'))
                if os.path.exists(FONT_PATH): btn.font_name = "CustomFont"
                btn.bind(on_release=lambda x, n=acc: self.go_slots(n))
                
                del_btn = Button(text="X", size_hint_x=0.2, background_color=get_color_from_hex('#c0392b'))
                del_btn.bind(on_release=lambda x, n=acc: show_confirm("계정 삭제", f"'{n}' 계정을 삭제하시겠습니까?", lambda: self.delete_acc(n)))
                
                row.add_widget(btn); row.add_widget(del_btn)
                self.acc_list.add_widget(row)

    def add_acc_pop(self, *args):
        content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        new_id = CustomTextInput(hint_text="계정 ID 입력")
        done = Button(text="생성", size_hint_y=0.4, background_color=get_color_from_hex('#2980b9'))
        if os.path.exists(FONT_PATH): done.font_name = "CustomFont"
        content.add_widget(new_id); content.add_widget(done)
        pop = Popup(title="신규 계정", content=content, size_hint=(0.8, 0.4))
        done.bind(on_release=lambda x: [self.create_acc(new_id.text), pop.dismiss()])
        pop.open()

    def create_acc(self, acc_id):
        if acc_id.strip() and acc_id not in self.accounts:
            self.accounts[acc_id] = {f"Slot {i}": "비어있음" for i in range(1, 7)}
            self.update_list()

    def delete_acc(self, acc_id):
        if acc_id in self.accounts: del self.accounts[acc_id]; self.update_list()

    def go_slots(self, name):
        self.manager.get_screen('slots').acc_name = name
        self.manager.current = 'slots'

class SlotScreen(BaseScreen):
    acc_name = StringProperty("")
    
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=[30, 50, 30, 30], spacing=20)
        title = Label(text=f"[{self.acc_name}] 캐릭터 선택", font_size='24sp', size_hint_y=0.1)
        if os.path.exists(FONT_PATH): title.font_name = "CustomFont"
        layout.add_widget(title)
        
        grid = GridLayout(cols=2, spacing=15, size_hint_y=0.7)
        slots_data = App.get_running_app().root.get_screen('main').accounts[self.acc_name]
        
        for i in range(1, 7):
            char_name = slots_data.get(f"Slot {i}", f"슬롯 {i}")
            btn = Button(text=char_name, background_color=(0.2, 0.2, 0.5, 0.6), font_size='16sp')
            if os.path.exists(FONT_PATH): btn.font_name = "CustomFont"
            btn.bind(on_release=lambda x, s=i: self.go_detail(s))
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        back = Button(text="처음으로", size_hint_y=0.1, background_color=(0.3, 0.3, 0.3, 0.8))
        if os.path.exists(FONT_PATH): back.font_name = "CustomFont"
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back); self.add_widget(layout)

    def go_detail(self, slot_num):
        self.manager.get_screen('detail').current_acc = self.acc_name
        self.manager.get_screen('detail').current_slot = slot_num
        self.manager.current = 'detail'

class DetailScreen(BaseScreen):
    current_acc = StringProperty("")
    current_slot = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.scroll = ScrollView(do_scroll_x=False)
        self.grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        # 사진 피드백 반영: 그룹화 및 이름 연동을 위한 상단 배치
        self.inputs = {}
        groups = [
            ["이름", "직위", "클랜", "레벨"],
            ["생명력", "기력", "근력", "힘"],
            ["정신력", "재능", "민첩", "건강", "명중"],
            ["공격", "방어", "흡수", "속도"]
        ]
        
        for idx, group in enumerate(groups):
            for s in group:
                row = BoxLayout(size_hint_y=None, height=85, spacing=10)
                lbl = Label(text=s, size_hint_x=0.3)
                if os.path.exists(FONT_PATH): lbl.font_name = "CustomFont"
                ti = CustomTextInput()
                self.inputs[s] = ti
                row.add_widget(lbl); row.add_widget(ti)
                self.grid.add_widget(row)
            if idx < len(groups)-1:
                self.grid.add_widget(BoxLayout(size_hint_y=None, height=40))
                
        self.scroll.add_widget(self.grid)
        self.main_layout.add_widget(self.scroll)
        
        # 하단 메뉴 (사진 구성 반영)
        nav = BoxLayout(size_hint_y=0.12, spacing=5)
        for t in ["장비", "인벤토리", "저장"]:
            btn = Button(text=t, background_color=get_color_from_hex('#1a3a5a'))
            if os.path.exists(FONT_PATH): btn.font_name = "CustomFont"
            if t=="저장": btn.bind(on_release=self.save_data)
            else: btn.bind(on_release=lambda x, target=t: self.move_to(target))
            nav.add_widget(btn)
        
        self.main_layout.add_widget(nav)
        back = Button(text="뒤로가기", size_hint_y=0.08, on_release=lambda x: setattr(self.manager, 'current', 'slots'))
        if os.path.exists(FONT_PATH): back.font_name = "CustomFont"
        self.main_layout.add_widget(back)
        self.add_widget(self.main_layout)

    def save_data(self, *args):
        """사진 피드백: 이름을 입력하면 슬롯에 자동 연동"""
        name = self.inputs["이름"].text.strip() or f"슬롯 {self.current_slot}"
        app_main = App.get_running_app().root.get_screen('main')
        app_main.accounts[self.current_acc][f"Slot {self.current_slot}"] = name
        show_confirm("저장 완료", f"'{name}' 정보가 저장되었습니다.", lambda: None)

    def move_to(self, target):
        dest = 'equip' if target == "장비" else 'inven'
        self.manager.current = dest

class EquipScreen(BaseScreen):
    """사진 피드백: 장비창 사진 버튼 및 업다운로드 로직 기반 마련"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        scroll = ScrollView()
        content = GridLayout(cols=1, size_hint_y=None, spacing=15)
        content.bind(minimum_height=content.setter('height'))
        
        items = ["한손무기", "두손무기", "갑옷", "방패", "장갑", "부츠", "링1", "링2", "아뮬렛"]
        for i in items:
            row = BoxLayout(size_hint_y=None, height=100, spacing=10)
            lbl = Label(text=i, size_hint_x=0.25)
            if os.path.exists(FONT_PATH): lbl.font_name = "CustomFont"
            ti = CustomTextInput(hint_text="옵션...")
            cam_btn = Button(text="📷", size_hint_x=0.15, background_color=get_color_from_hex('#34495e'))
            row.add_widget(lbl); row.add_widget(ti); row.add_widget(cam_btn)
            content.add_widget(row)
            
        scroll.add_widget(content); layout.add_widget(scroll)
        back = Button(text="뒤로가기", size_hint_y=0.1, on_release=lambda x: setattr(self.manager, 'current', 'detail'))
        if os.path.exists(FONT_PATH): back.font_name = "CustomFont"
        layout.add_widget(back); self.add_widget(layout)

class InvenScreen(BaseScreen):
    """사진 피드백: 아이템 추가 시 삭제 확인 멘트 적용"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.scroll = ScrollView()
        self.list = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.list.bind(minimum_height=self.list.setter('height'))
        self.scroll.add_widget(self.list)
        layout.add_widget(self.scroll)
        
        add = Button(text="+ 아이템 추가", size_hint_y=0.1, background_color=get_color_from_hex('#27ae60'))
        if os.path.exists(FONT_PATH): add.font_name = "CustomFont"
        add.bind(on_release=self.add_item)
        layout.add_widget(add)
        
        back = Button(text="뒤로가기", size_hint_y=0.08, on_release=lambda x: setattr(self.manager, 'current', 'detail'))
        if os.path.exists(FONT_PATH): back.font_name = "CustomFont"
        layout.add_widget(back); self.add_widget(layout)

    def add_item(self, *args):
        row = BoxLayout(size_hint_y=None, height=90, spacing=10)
        ti = CustomTextInput(hint_text="아이템 정보...")
        del_btn = Button(text="X", size_hint_x=0.2, background_color=get_color_from_hex('#c0392b'))
        del_btn.bind(on_release=lambda x: show_confirm("아이템 삭제", "이 아이템을 목록에서 삭제할까요?", lambda: self.list.remove_widget(row)))
        row.add_widget(ti); row.add_widget(del_btn)
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
