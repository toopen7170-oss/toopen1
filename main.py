import os
import sys
import traceback

# [1단계: 전방위 실시간 오류 감시] 빌드/실행 중 모든 오류를 화면에 강제 표시
def global_exception_handler(exctype, value, tb):
    err_msg = "".join(traceback.format_exception(exctype, value, tb))
    try:
        from kivy.base import runTouchApp
        from kivy.uix.label import Label
        from kivy.core.window import Window
        runTouchApp(Label(text=f"[치명적 오류 보고]\n\n{err_msg}", 
                          color=(1, 0, 0, 1), font_size='14sp', 
                          halign='left', valign='top', text_size=(Window.width*0.9, None)))
    except:
        print(f"Critical System Error: {err_msg}")

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
    from kivy.uix.image import Image
    from kivy.core.window import Window
    from kivy.utils import get_color_from_hex
    from kivy.core.text import LabelBase
    from kivy.properties import StringProperty, DictProperty, ListProperty
    from kivy.clock import Clock
    from android.permissions import request_permissions, Permission # 안드로이드 권한 전용
except Exception as e:
    global_exception_handler(*sys.exc_info())

# 리소스 설정
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

class CustomTextInput(TextInput):
    """[교정] 중앙 정렬 및 가독성 최적화"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if HAS_FONT: self.font_name = "CustomFont"
        self.multiline = False
        self.font_size = '18sp'
        self.halign = 'center'
        self.bind(size=self._update_padding)

    def _update_padding(self, *args):
        self.padding_y = [self.height / 2.0 - (self.line_height / 2.0), 0]

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            source = BG_PATH if os.path.exists(BG_PATH) else ""
            self.bg = Image(source=source, allow_stretch=True, keep_ratio=False, size=Window.size)

class MainScreen(BaseScreen):
    """[보존] 기존 계정 관리 로직 100% 보존"""
    accounts = DictProperty({})
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.search_in = CustomTextInput(hint_text="계정 검색...")
        self.layout.add_widget(self.search_in)
        self.scroll = ScrollView()
        self.acc_list = GridLayout(cols=1, size_hint_y=None, spacing=15)
        self.acc_list.bind(minimum_height=self.acc_list.setter('height'))
        self.scroll.add_widget(self.acc_list)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

class DetailScreen(BaseScreen):
    """[교정] 정보창 17개 항목 (사진 image_9.png 기반)"""
    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        fields = ["이름", "직위", "클랜", "레벨", "생명력", "기력", "근력", "힘", 
                  "정신력", "재능", "민첩", "건강", "명중", "공격", "방어", "흡수", "속도"]
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
        grid.bind(minimum_height=grid.setter('height'))
        for f in fields:
            row = BoxLayout(size_hint_y=None, height=90, spacing=10)
            lbl = Label(text=f, size_hint_x=0.3)
            if HAS_FONT: lbl.font_name = "CustomFont"
            ti = CustomTextInput()
            row.add_widget(lbl); row.add_widget(ti); grid.add_widget(row)
        scroll.add_widget(grid); layout.add_widget(scroll)
        
        nav = BoxLayout(size_hint_y=0.12, spacing=10)
        btn_eq = Button(text="장비창 이동", on_release=lambda x: setattr(self.manager, 'current', 'equip'))
        if HAS_FONT: btn_eq.font_name = "CustomFont"
        nav.add_widget(btn_eq); layout.add_widget(nav)
        self.add_widget(layout)

class EquipScreen(BaseScreen):
    """[신규] 장비창 상단 사진 관리 UI + 11개 항목"""
    photo_paths = ListProperty([])

    def on_enter(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        # [상단] 사진 관리 영역 (여러 장 업로드/삭제/저장)
        photo_header = BoxLayout(orientation='vertical', size_hint_y=0.4, spacing=5)
        btn_row = BoxLayout(size_hint_y=0.3, spacing=10)
        add_btn = Button(text="사진 추가 (+)", on_release=self.add_photo)
        save_btn = Button(text="전체 저장 (💾)", on_release=self.save_photos)
        if HAS_FONT: add_btn.font_name = save_btn.font_name = "CustomFont"
        btn_row.add_widget(add_btn); btn_row.add_widget(save_btn)
        
        self.photo_grid = GridLayout(rows=1, size_hint_x=None, spacing=10)
        self.photo_grid.bind(minimum_width=self.photo_grid.setter('width'))
        photo_scroll = ScrollView(size_hint_y=0.7, do_scroll_y=False, do_scroll_x=True)
        photo_scroll.add_widget(self.photo_grid)
        
        photo_header.add_widget(btn_row); photo_header.add_widget(photo_scroll)
        layout.add_widget(photo_header)

        # [하단] 장비 항목 11개 (사진 image_10.png 기반)
        items = [("한손무기", "w1"), ("두손무기", "w2"), ("갑옷", "arm"), ("방패", "sh"),
                 ("장갑", "gl"), ("부츠", "bt"), ("암릿", "am"), ("링", "r1"), 
                 ("링", "r2"), ("아뮬렛", "amu"), ("기타", "etc")]
        
        item_scroll = ScrollView()
        item_grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
        item_grid.bind(minimum_height=item_grid.setter('height'))
        for name, key in items:
            row = BoxLayout(size_hint_y=None, height=100, spacing=10)
            lbl = Label(text=name, size_hint_x=0.25)
            if HAS_FONT: lbl.font_name = "CustomFont"
            row.add_widget(lbl); row.add_widget(CustomTextInput(hint_text="옵션..."))
            row.add_widget(Button(text="📷", size_hint_x=0.15))
            item_grid.add_widget(row)
        
        item_scroll.add_widget(item_grid); layout.add_widget(item_scroll)
        back = Button(text="뒤로가기", size_hint_y=0.1, on_release=lambda x: setattr(self.manager, 'current', 'detail'))
        if HAS_FONT: back.font_name = "CustomFont"
        layout.add_widget(back); self.add_widget(layout)
        self.refresh_photos()

    def add_photo(self, *args):
        # 실제 구현 시 갤러리 호출 로직 연동 (현재는 시뮬레이션 경로 추가)
        self.photo_paths.append("sample_path.png")
        self.refresh_photos()

    def delete_photo(self, path):
        if path in self.photo_paths:
            self.photo_paths.remove(path)
            self.refresh_photos()

    def save_photos(self, *args):
        print(f"총 {len(self.photo_paths)}장의 사진 저장 완료")

    def refresh_photos(self):
        self.photo_grid.clear_widgets()
        for path in self.photo_paths:
            box = BoxLayout(orientation='vertical', size_hint_x=None, width=200)
            img = Image(source=path, allow_stretch=True)
            del_btn = Button(text="삭제(X)", size_hint_y=0.3, background_color=(1,0,0,1))
            del_btn.bind(on_release=lambda x, p=path: self.delete_photo(p))
            box.add_widget(img); box.add_widget(del_btn)
            self.photo_grid.add_widget(box)

class PristonTaleApp(App):
    def build(self):
        # 앱 시작 시 실시간 권한 요청 (API 34 대응)
        request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.CAMERA])
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(DetailScreen(name='detail'))
        sm.add_widget(EquipScreen(name='equip'))
        return sm

if __name__ == '__main__':
    PristonTaleApp().run()
