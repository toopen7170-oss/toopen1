
import os
import sys
import traceback

# [자가 진단 핵심] Kivy 로딩 전 최상단 예외 그물망 설치
try:
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
except Exception as e:
    print(f"Critical Import Error: {e}")

# 리소스 경로 정의
FONT_PATH = os.path.join(os.path.dirname(__file__), "font.ttf")
BG_PATH = os.path.join(os.path.dirname(__file__), "bg.png")

def safe_register_font():
    try:
        if os.path.exists(FONT_PATH):
            LabelBase.register(name="CustomFont", fn_regular=FONT_PATH)
            return True
    except: pass
    return False

HAS_FONT = safe_register_font()

class DiagnosticLabel(Label):
    """시스템 폰트를 강제 사용하여 어떤 상황에서도 출력 보장"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if HAS_FONT: self.font_name = "CustomFont"
        self.font_size = '15sp'
        self.color = (1, 0.3, 0.3, 1)
        self.halign = 'left'
        self.valign = 'middle'
        self.bind(size=self.setter('text_size'))

class CustomTextInput(TextInput):
    """S26 Ultra 최적화: 중앙 정렬 및 가독성 팝업"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if HAS_FONT: self.font_name = "CustomFont"
        self.multiline = False
        self.font_size = '18sp'
        self.halign = 'center'
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
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        full_input = TextInput(text=self.text, font_size='18sp', multiline=True)
        if HAS_FONT: full_input.font_name = "CustomFont"
        btn = Button(text="확인", size_hint_y=0.2, background_color=get_color_from_hex('#2980b9'))
        if HAS_FONT: btn.font_name = "CustomFont"
        content.add_widget(full_input); content.add_widget(btn)
        pop = Popup(title="내용 수정", content=content, size_hint=(0.9, 0.6))
        if HAS_FONT: pop.title_font = "CustomFont"
        btn.bind(on_release=lambda x: [setattr(self, 'text', full_input.text), pop.dismiss()])
        pop.open()

def show_confirm(title, text, on_confirm):
    """모든 삭제 및 중요 동작 전 확인 절차 강제화"""
    content = BoxLayout(orientation='vertical', padding=20, spacing=20)
    msg = Label(text=text, font_size='17sp', halign='center')
    if HAS_FONT: msg.font_name = "CustomFont"
    content.add_widget(msg)
    btns = BoxLayout(size_hint_y=0.4, spacing=10)
    ok_btn = Button(text="확인", background_color=get_color_from_hex('#c0392b'))
    can_btn = Button(text="취소", background_color=get_color_from_hex('#7f8c8d'))
    if HAS_FONT: ok_btn.font_name = "CustomFont"; can_btn.font_name = "CustomFont"
    popup = Popup(title=title, content=content, size_hint=(0.85, 0.35))
    if HAS_FONT: popup.title_font = "CustomFont"
    ok_btn.bind(on_release=lambda x: [on_confirm(), popup.dismiss()])
    can_btn.bind(on_release=popup.dismiss)
    btns.add_widget(ok_btn); btns.add_widget(can_btn); content.add_widget(btns); popup.open()

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            source = BG_PATH if os.path.exists(BG_PATH) else ""
            self.bg = Image(source=source, allow_stretch=True, keep_ratio=False, size=Window.size)
        Window.bind(on_keyboard_height=self._on_keyboard_height)

    def _on_keyboard_height(self, window, height):
        self.y = height * 0.5 if height > 0 else 0

class MainScreen(BaseScreen):
    accounts = DictProperty({})
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[20, 40, 20, 20], spacing=15)
        title = Label(text="PT1 Manager", font_size='28sp', size_hint_y=0.1)
        if HAS_FONT: title.font_name = "CustomFont"
        self.layout.add_widget(title)
        
        search_area = BoxLayout(size_hint_y=0.08)
        self.search_in = CustomTextInput(hint_text="전체 계정 검색...")
        self.search_in.bind(text=self.update_list)
        search_area.add_widget(self.search_in)
        self.layout.add_widget(search_area)
        
        add_btn = Button(text="+ 새 계정 생성", size_hint_y=0.08, background_color=get_color_from_hex('#27ae60'))
        if HAS_FONT: add_btn.font_name = "CustomFont"
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
        for acc in sorted(self.accounts.keys()):
            if query in acc.lower():
                row = BoxLayout(size_hint_y=None, height=100, spacing=5)
                btn = Button(text=f"계정: {acc}", background_color=get_color_from_hex('#2c3e50'))
                if HAS_FONT: btn.font_name = "CustomFont"
                btn.bind(on_release=lambda x, n=acc: self.go_slots(n))
                del_btn = Button(text="X", size_hint_x=0.2, background_color=get_color_from_hex('#c0392b'))
                del_btn.bind(on_release=lambda x, n=acc: show_confirm("삭제 확인", f"'{n}' 계정을 삭제하시겠습니까?", lambda: self.delete_acc(n)))
                row.add_widget(btn); row.add_widget(del_btn); self.acc_list.add_widget(row)

    def add_acc_pop(self, *args):
        content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        new_id = CustomTextInput(hint_text="ID 입력")
        done = Button(text="생성 완료", size_hint_y=0.4, background_color=get_color_from_hex('#2980b9'))
        if HAS_FONT: done.font_name = "CustomFont"
        content.add_widget(new_id); content.add_widget(done)
        pop = Popup(title="계정 추가", content=content, size_hint=(0.8, 0.4))
        done.bind(on_release=lambda x: [self.create_acc(new_id.text), pop.dismiss()])
        pop.open()

    def create_acc(self, acc_id):
        if acc_id.strip() and acc_id not in self.accounts:
            self.accounts[acc_id] = {f"Slot {i}": f"슬롯 {i}" for i in range(1, 7)}
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
        title = Label(text=f"[{self.acc_name}] 캐릭터 선택", font_size='22sp', size_hint_y=0.1)
        if HAS_FONT: title.font_name = "CustomFont"
        layout.add_widget(title)
        grid = GridLayout(cols=2, spacing=15, size_hint_y=0.7)
        slots_data = App.get_running_app().root.get_screen('main').accounts[self.acc_name]
        for i in range(1, 7):
            char_name = slots_data.get(f"Slot {i}", f"슬롯 {i}")
            btn = Button(text=char_name, background_color=(0.2, 0.3, 0.4, 0.8))
            if HAS_FONT: btn.font_name = "CustomFont"
            btn.bind(on_release=lambda x, s=i: self.go_detail(s))
            grid.add_widget(btn)
        layout.add_widget(grid)
        back = Button(text="목록으로", size_hint_y=0.1, background_color=(0.3, 0.3, 0.3, 1))
        if HAS_FONT: back.font_name = "CustomFont"
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back); self.add_widget(layout)

    def go_detail(self, slot_num):
        self.manager.get_screen('detail').current_acc = self.acc_name
        self.manager.get_screen('detail').current_slot = str(slot_num)
        self.manager.current = 'detail'

class DetailScreen(BaseScreen):
    current_acc = StringProperty("")
    current_slot = StringProperty("")
    def on_enter(self):
        self.clear_widgets()
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
        grid.bind(minimum_height=grid.setter('height'))
        self.inputs = {}
        
        groups = [["이름", "직위", "클랜", "레벨"], ["생명력", "기력", "근력", "힘"], ["정신력", "재능", "민첩", "건강", "명중"], ["공격", "방어", "흡수", "속도"]]
        for group in groups:
            for s in group:
                row = BoxLayout(size_hint_y=None, height=85, spacing=10)
                lbl = Label(text=s, size_hint_x=0.3)
                if HAS_FONT: lbl.font_name = "CustomFont"
                ti = CustomTextInput(); self.inputs[s] = ti
                row.add_widget(lbl); row.add_widget(ti); grid.add_widget(row)
        
        scroll.add_widget(grid); main_layout.add_widget(scroll)
        nav = BoxLayout(size_hint_y=0.12, spacing=5)
        for t in ["장비", "인벤", "저장"]:
            btn = Button(text=t, background_color=get_color_from_hex('#1a3a5a'))
            if HAS_FONT: btn.font_name = "CustomFont"
            if t=="저장": btn.bind(on_release=self.save_data)
            else: btn.bind(on_release=lambda x, target=t: setattr(self.manager, 'current', 'equip' if target=="장비" else 'inven'))
            nav.add_widget(btn)
        main_layout.add_widget(nav)
        back = Button(text="뒤로가기", size_hint_y=0.08, on_release=lambda x: setattr(self.manager, 'current', 'slots'))
        if HAS_FONT: back.font_name = "CustomFont"
        main_layout.add_widget(back); self.add_widget(main_layout)

    def save_data(self, *args):
        name = self.inputs["이름"].text.strip() or f"슬롯 {self.current_slot}"
        App.get_running_app().root.get_screen('main').accounts[self.current_acc][f"Slot {self.current_slot}"] = name
        show_confirm("저장 완료", f"'{name}' 정보가 안전하게 저장되었습니다.", lambda: None)

class EquipScreen(BaseScreen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        scroll = ScrollView()
        content = GridLayout(cols=1, size_hint_y=None, spacing=15)
        content.bind(minimum_height=content.setter('height'))
        
        # 암릿(Armlet) 반영 완료
        items = ["한손무기", "두손무기", "갑옷", "방패", "장갑", "부츠", "링1", "링2", "암릿", "아뮬렛", "쉘터"]
        for i in items:
            row = BoxLayout(size_hint_y=None, height=100, spacing=10)
            lbl = Label(text=i, size_hint_x=0.25)
            if HAS_FONT: lbl.font_name = "CustomFont"
            row.add_widget(lbl); row.add_widget(CustomTextInput(hint_text="옵션 입력..."))
            row.add_widget(Button(text="📷", size_hint_x=0.15, background_color=get_color_from_hex('#34495e')))
            content.add_widget(row)
            
        scroll.add_widget(content); layout.add_widget(scroll)
        back = Button(text="뒤로가기", size_hint_y=0.1, on_release=lambda x: setattr(self.manager, 'current', 'detail'))
        if HAS_FONT: back.font_name = "CustomFont"
        layout.add_widget(back); self.add_widget(layout)

class InvenScreen(BaseScreen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.scroll = ScrollView()
        self.list = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.list.bind(minimum_height=self.list.setter('height'))
        self.scroll.add_widget(self.list); layout.add_widget(self.scroll)
        
        btns = BoxLayout(size_hint_y=0.1, spacing=10)
        add = Button(text="+ 아이템 추가", background_color=get_color_from_hex('#27ae60'))
        if HAS_FONT: add.font_name = "CustomFont"
        add.bind(on_release=self.add_item); btns.add_widget(add)
        layout.add_widget(btns)
        
        back = Button(text="뒤로가기", size_hint_y=0.08, on_release=lambda x: setattr(self.manager, 'current', 'detail'))
        if HAS_FONT: back.font_name = "CustomFont"
        layout.add_widget(back); self.add_widget(layout)

    def add_item(self, *args):
        row = BoxLayout(size_hint_y=None, height=90, spacing=10)
        row.add_widget(CustomTextInput(hint_text="아이템 정보..."))
        del_btn = Button(text="X", size_hint_x=0.2, background_color=get_color_from_hex('#c0392b'))
        del_btn.bind(on_release=lambda x: show_confirm("삭제 확인", "이 아이템을 정말 삭제하시겠습니까?", lambda: self.list.remove_widget(row)))
        row.add_widget(del_btn); self.list.add_widget(row)

class PristonTaleApp(App):
    def build(self):
        try:
            sm = ScreenManager(transition=FadeTransition())
            sm.add_widget(MainScreen(name='main'))
            sm.add_widget(SlotScreen(name='slots'))
            sm.add_widget(DetailScreen(name='detail'))
            sm.add_widget(EquipScreen(name='equip'))
            sm.add_widget(InvenScreen(name='inven'))
            return sm
        except Exception:
            # [자가 진단] 치명적 오류 발생 시 화면에 강제 출력
            err_box = BoxLayout(orientation='vertical', padding=50)
            err_box.add_widget(DiagnosticLabel(text="[시스템 진단 보고]\n\n" + traceback.format_exc()))
            return err_box

if __name__ == '__main__':
    try:
        PristonTaleApp().run()
    except Exception:
        # Kivy 윈도우조차 못 띄울 경우 콘솔 및 시스템 로그 남김
        traceback.print_exc()
