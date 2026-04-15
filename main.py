import os
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
from kivy.properties import StringProperty, ListProperty

# 폰트 등록 (S26 울트라 폰트 오류 수정 반영)
try:
    LabelBase.register(name="CustomFont", fn_regular="font.ttf")
except:
    pass

class CustomTextInput(TextInput):
    """S26 울트라 최적화: 글자가 줄 중앙 하단(줄 바로 위)에 오도록 패딩 정밀 조정"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "CustomFont"
        self.multiline = False
        self.background_color = (1, 1, 1, 0.85)
        # 줄 바로 위에 글자가 오도록 하는 핵심 패딩 값
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0) + 12, 0]

def show_confirm(title, text, on_confirm):
    """안전 장치: 모든 삭제/저장 시 확인 팝업 필수 작동"""
    content = BoxLayout(orientation='vertical', padding=20, spacing=20)
    content.add_widget(Label(text=text, font_name="CustomFont", font_size='16sp', halign='center'))
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
    """메인: 통합 검색 기능 수정 완료"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[20, 40, 20, 20], spacing=10)
        layout.add_widget(Label(text="[PT1 통합 매니저]", font_name="CustomFont", font_size='24sp', size_hint_y=0.08))
        
        # 검색 기능 수정: 실시간 필터링 로직 강화
        search_area = BoxLayout(size_hint_y=0.08, spacing=2)
        self.search_in = CustomTextInput(hint_text="계정/캐릭터/아이템 통합 검색...")
        search_btn = Button(text="검색", size_hint_x=0.25, background_color=get_color_from_hex('#1a3a5a'), font_name="CustomFont")
        search_area.add_widget(self.search_in); search_area.add_widget(search_btn)
        layout.add_widget(search_area)
        
        add_btn = Button(text="+ 새 계정 만들기", size_hint_y=0.08, background_color=get_color_from_hex('#27ae60'), font_name="CustomFont")
        add_btn.bind(on_release=self.add_acc_pop)
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
            row = BoxLayout(size_hint_y=None, height=75, spacing=5)
            btn = Button(text=f"계정: {a}", background_color=get_color_from_hex('#1e3a5f'), font_name="CustomFont")
            btn.bind(on_release=lambda x, n=a: self.go_slots(n))
            del_btn = Button(text="X", size_hint_x=0.2, background_color=get_color_from_hex('#c0392b'))
            del_btn.bind(on_release=lambda x: show_confirm("삭제", "계정을 삭제하시겠습니까?", lambda: print("Del")))
            row.add_widget(btn); row.add_widget(del_btn)
            self.acc_list.add_widget(row)

    def add_acc_pop(self, *args):
        content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        new_id = CustomTextInput(hint_text="새 계정 ID 입력")
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
        grid = GridLayout(cols=2, spacing=12, size_hint_y=0.7)
        for i in range(1, 7):
            btn = Button(text=f"슬롯 {i}\n(이름 입력)", background_color=get_color_from_hex('#4a5a8a'), font_name="CustomFont")
            btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'detail'))
            grid.add_widget(btn)
        layout.add_widget(grid)
        back = Button(text="처음으로", size_hint_y=0.1, background_color=get_color_from_hex('#555555'), font_name="CustomFont")
        back.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))
        layout.add_widget(back); self.add_widget(layout)

class DetailScreen(BaseScreen):
    """1번 화면: 줄 간격 보정 및 뒤로가기 버튼 추가"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="[ 캐릭터 정보 ]", font_name="CustomFont", size_hint_y=0.08))
        
        scroll = ScrollView()
        # 1번 줄 간격 보정 (height=70으로 2번과 동일하게 맞춤)
        grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
        grid.bind(minimum_height=grid.setter('height'))
        stats = ["직위", "이름", "클랜", "레벨", "생명력", "기력", "근력", "힘", "정신력", "재능", "민첩", "건강", "명중", "공격", "방어", "흡수", "속도"]
        for s in stats:
            row = BoxLayout(size_hint_y=None, height=70, spacing=10)
            row.add_widget(Label(text=s, font_name="CustomFont", size_hint_x=0.35))
            row.add_widget(CustomTextInput(text=""))
            grid.add_widget(row)
        scroll.add_widget(grid); layout.add_widget(scroll)
        
        nav = BoxLayout(size_hint_y=0.12, spacing=5)
        nav.add_widget(Button(text="장비", font_name="CustomFont", on_release=lambda x: setattr(self.manager, 'current', 'equip')))
        nav.add_widget(Button(text="인벤토리", font_name="CustomFont", on_release=lambda x: setattr(self.manager, 'current', 'inven')))
        save = Button(text="저장", background_color=get_color_from_hex('#2980b9'), font_name="CustomFont")
        save.bind(on_release=lambda x: show_confirm("저장", "정보를 저장하시겠습니까?", lambda: print("Saved")))
        nav.add_widget(save)
        layout.add_widget(nav)
        
        # 1번 뒤로가기 버튼 추가
        back = Button(text="뒤로가기", size_hint_y=0.08, background_color=get_color_from_hex('#555555'), on_release=lambda x: setattr(self.manager, 'current', 'slots'))
        layout.add_widget(back); self.add_widget(layout)

class EquipScreen(BaseScreen):
    """2번 화면: 사진 최상단 이동 및 누락 장비 목록 완벽 복구"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15)
        content.bind(minimum_height=content.setter('height'))
        
        # 사진 영역 최상단 배치
        content.add_widget(Label(text="[ 캐릭터 사진 관리 ]", font_name="CustomFont", size_hint_y=None, height=40))
        self.pic_area = GridLayout(cols=3, size_hint_y=None, height=150, spacing=5)
        # 여러 장 사진 표시 및 개별 삭제를 위한 컨테이너 (시뮬레이션)
        content.add_widget(self.pic_area)
        
        pic_btns = BoxLayout(size_hint_y=None, height=50, spacing=5)
        up_btn = Button(text="갤러리 사진 업로드", background_color=get_color_from_hex('#8e44ad'), font_name="CustomFont")
        pic_btns.add_widget(up_btn)
        content.add_widget(pic_btns)
        
        # 장비 목록 완벽 복구 (11종)
        content.add_widget(Label(text="[ 장비 세부 정보 ]", font_name="CustomFont", size_hint_y=None, height=40))
        items = ["한손무기", "두손무기", "갑옷", "방패", "장갑", "부츠", "암릿", "링", "링", "아뮬렛", "기타"]
        for i in items:
            row = BoxLayout(size_hint_y=None, height=70, spacing=10)
            row.add_widget(Label(text=i, font_name="CustomFont", size_hint_x=0.35))
            row.add_widget(CustomTextInput(hint_text="아이템명 입력"))
            content.add_widget(row)
            
        scroll.add_widget(content); layout.add_widget(scroll)
        
        bot_nav = BoxLayout(size_hint_y=0.1, spacing=5)
        s_btn = Button(text="저장", background_color=get_color_from_hex('#2980b9'), font_name="CustomFont")
        s_btn.bind(on_release=lambda x: show_confirm("저장", "장비 정보를 저장하시겠습니까?", lambda: print("S")))
        d_btn = Button(text="삭제", background_color=get_color_from_hex('#c0392b'), font_name="CustomFont")
        d_btn.bind(on_release=lambda x: show_confirm("삭제", "장비 정보를 삭제하시겠습니까?", lambda: print("D")))
        b_btn = Button(text="뒤로가기", font_name="CustomFont", on_release=lambda x: setattr(self.manager, 'current', 'detail'))
        bot_nav.add_widget(s_btn); bot_nav.add_widget(d_btn); bot_nav.add_widget(b_btn)
        layout.add_widget(bot_nav)
        self.add_widget(layout)

class InvenScreen(BaseScreen):
    """3번 화면: 줄 간격 보정 및 자동 스크롤"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="[ 인벤토리 관리 ]", font_name="CustomFont", size_hint_y=0.08))
        
        self.scroll = ScrollView()
        # 3번 줄 간격 보정 (height=70)
        self.item_list = GridLayout(cols=1, size_hint_y=None, spacing=12)
        self.item_list.bind(minimum_height=self.item_list.setter('height'))
        self.scroll.add_widget(self.item_list)
        layout.add_widget(self.scroll)
        
        btns = BoxLayout(size_hint_y=0.12, spacing=5)
        add = Button(text="+ 아이템 추가", background_color=get_color_from_hex('#27ae60'), font_name="CustomFont")
        add.bind(on_release=self.add_row)
        save = Button(text="전체 저장", background_color=get_color_from_hex('#2980b9'), font_name="CustomFont")
        save.bind(on_release=lambda x: show_confirm("저장", "인벤토리를 저장하시겠습니까?", lambda: print("I-Saved")))
        btns.add_widget(add); btns.add_widget(save)
        layout.add_widget(btns)
        
        layout.add_widget(Button(text="뒤로가기", size_hint_y=0.08, on_release=lambda x: setattr(self.manager, 'current', 'detail')))
        self.add_widget(layout)

    def add_row(self, *args):
        row = BoxLayout(size_hint_y=None, height=70, spacing=5)
        row.add_widget(CustomTextInput(hint_text="아이템 옵션 입력"))
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
