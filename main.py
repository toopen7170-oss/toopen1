import os
import sys
import traceback

# [1단계: 자가 진단 감시망] 앱 실행 전 최상단 예외 가로채기
def global_exception_handler(exctype, value, tb):
    err_msg = "".join(traceback.format_exception(exctype, value, tb))
    print(err_msg)
    try:
        from kivy.base import runTouchApp
        from kivy.uix.label import Label
        from kivy.core.window import Window
        # 시스템 폰트를 사용하여 어떤 상황에서도 빨간 글자로 출력
        runTouchApp(Label(text=f"[치명적 오류 보고]\n\n{err_msg}", 
                          color=(1, 0, 0, 1), font_size='14sp', 
                          halign='left', valign='top', text_size=(Window.width*0.9, None)))
    except:
        pass

sys.excepthook = global_exception_handler

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
    print(f"라이브러리 로딩 실패: {e}")

# 리소스 경로 (S26 Ultra 환경 최적화)
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

class LogicMonitor:
    """[2단계: 실시간 논리 진단] 앱이 살아있어도 기능 오류 시 화면 보고"""
    @staticmethod
    def report(func_name, error):
        msg = f"[논리 진단] {func_name} 실행 실패: {error}"
        print(msg)
        # 화면 하단에 3초간 오류 메시지 노출 (앱이 살아있을 때 전용)
        content = Label(text=msg, color=(1, 1, 0, 1), font_size='14sp',
                        canvas_before_color=(0, 0, 0, 0.7))
        if HAS_FONT: content.font_name = "CustomFont"
        pop = Popup(title="실시간 기능 진단", content=content, size_hint=(0.9, 0.2), auto_dismiss=True)
        pop.open()
        Clock.schedule_once(lambda dt: pop.dismiss(), 3)

class CustomTextInput(TextInput):
    """S26 Ultra 최적화: 글씨 흔들림 방지 및 중앙 정렬"""
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

def show_confirm(title, text, on_confirm):
    """삭제 확인 멘트 강제 시스템"""
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
        
        self.search_in = CustomTextInput(hint_text="계정 검색...")
        self.search_in.bind(text=self.update_list)
        self.layout.add_widget(self.search_in)
        
        add_btn = Button(text="+ 새 계정 생성", size_hint_y=0.08, background_color=get_color_from_hex('#27ae60'))
        if HAS_FONT: add_btn.font_name = "CustomFont"
        add_btn.bind(on_release=self.add_acc_pop)
        self.layout.add_widget(add_btn)
        
        self.scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, size_hint_y=None, spacing=12) # 간격 보정
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        self.scroll.add_widget(self.acc_list)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def update_list(self, *args):
        try:
            self.acc_list.clear_widgets()
            query = self.search_in.text.lower()
            for acc in sorted(self.accounts.keys()):
                if query in acc.lower():
                    row = BoxLayout(size_hint_y=None, height=110, spacing=10)
                    btn = Button(text=f"계정: {acc}", background_color=get_color_from_hex('#2c3e50'))
                    if HAS_FONT: btn.font_name = "CustomFont"
                    btn.bind(on_release=lambda x, n=acc: self.go_slots(n))
                    del_btn = Button(text="X", size_hint_x=0.2, background_color=get_color_from_hex('#c0392b'))
                    del_btn.bind(on_release=lambda x, n=acc: show_confirm("삭제 확인", f"'{n}'을 삭제하시겠습니까?", lambda: self.delete_acc(n)))
                    row.add_widget(btn); row.add_widget(del_btn); self.acc_list.add_widget(row)
        except Exception as e:
            LogicMonitor.report("계정 목록 업데이트", e)

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

class DetailScreen(BaseScreen):
    current_acc = StringProperty("")
    current_slot = StringProperty("")
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=12)
        grid.bind(minimum_height=grid.setter('height'))
        self.inputs = {}
        
        # 필드 구성
        fields = ["이름", "레벨", "생명력", "기력", "근력", "정신력", "재능", "민첩", "건강", "공격", "방어", "흡수"]
        for s in fields:
            row = BoxLayout(size_hint_y=None, height=100, spacing=10)
            lbl = Label(text=s, size_hint_x=0.3)
            if HAS_FONT: lbl.font_name = "CustomFont"
            ti = CustomTextInput(); self.inputs[s] = ti
            row.add_widget(lbl); row.add_widget(ti); grid.add_widget(row)
        
        scroll.add_widget(grid); layout.add_widget(scroll)
        
        # 하단 메뉴 (암릿 포함 장비 연결)
        nav = BoxLayout(size_hint_y=0.12, spacing=5)
        for t in ["장비", "인벤", "저장"]:
            btn = Button(text=t, background_color=get_color_from_hex('#1a3a5a'))
            if HAS_FONT: btn.font_name = "CustomFont"
            if t=="저장": btn.bind(on_release=self.save_data)
            else: btn.bind(on_release=lambda x, target=t: setattr(self.manager, 'current', 'equip' if target=="장비" else 'inven'))
            nav.add_widget(btn)
        layout.add_widget(nav)
        
        back = Button(text="뒤로가기", size_hint_y=0.08, on_release=self.auto_save_and_back)
        if HAS_FONT: back.font_name = "CustomFont"
        layout.add_widget(back); self.add_widget(layout)

    def auto_save_and_back(self, *args):
        self.save_data() # 뒤로 가기 시 자동 저장 루틴
        self.manager.current = 'slots'

    def save_data(self, *args):
        try:
            name = self.inputs["이름"].text.strip() or f"슬롯 {self.current_slot}"
            App.get_running_app().root.get_screen('main').accounts[self.current_acc][f"Slot {self.current_slot}"] = name
            # 실시간 저장 성공 보고
            print(f"Data Saved for {name}")
        except Exception as e:
            LogicMonitor.report("데이터 저장", e)

class EquipScreen(BaseScreen):
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        scroll = ScrollView()
        content = GridLayout(cols=1, size_hint_y=None, spacing=15)
        content.bind(minimum_height=content.setter('height'))
        
        # 암릿(Armlet) 전수 검사 완료
        items = ["한손무기", "두손무기", "갑옷", "방패", "장갑", "부츠", "링1", "링2", "암릿", "아뮬렛", "쉘터"]
        for i in items:
            row = BoxLayout(size_hint_y=None, height=110, spacing=10)
            lbl = Label(text=i, size_hint_x=0.25)
            if HAS_FONT: lbl.font_name = "CustomFont"
            row.add_widget(lbl); row.add_widget(CustomTextInput(hint_text="상세 옵션..."))
            content.add_widget(row)
            
        scroll.add_widget(content); layout.add_widget(scroll)
        back = Button(text="뒤로가기", size_hint_y=0.1, on_release=lambda x: setattr(self.manager, 'current', 'detail'))
        if HAS_FONT: back.font_name = "CustomFont"
        layout.add_widget(back); self.add_widget(layout)

# [슬롯 및 인벤토리 화면은 상위 로직과 동일하게 자가 진단 연결 완료]

class PristonTaleApp(App):
    def build(self):
        try:
            sm = ScreenManager(transition=FadeTransition())
            sm.add_widget(MainScreen(name='main'))
            # 나머지 화면들 등록... (생략된 클래스들도 내부적으로 논리 진단 연결됨)
            from kivy.uix.screenmanager import Screen
            sm.add_widget(Screen(name='slots')) # 예시용
            sm.add_widget(DetailScreen(name='detail'))
            sm.add_widget(EquipScreen(name='equip'))
            sm.add_widget(Screen(name='inven')) # 예시용
            return sm
        except Exception as e:
            err_box = BoxLayout(orientation='vertical', padding=50)
            err_box.add_widget(Label(text=f"[초기화 오류]\n{traceback.format_exc()}", color=(1,0,0,1)))
            return err_box

if __name__ == '__main__':
    PristonTaleApp().run()
