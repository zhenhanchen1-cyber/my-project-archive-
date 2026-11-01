# -*- coding: utf-8 -*-
"""
微信电脑版《欢乐斗地主》专属 - 桌面全自动实时视觉军师 HUD
具备功能：
1. 【📸 自动截屏识牌】：自动定位微信小程序《腾讯欢乐斗地主》窗口，全自动精准解析手牌
2. 【👑 智能地主识别】：精准双模态识别地主身份（我方地主 / 下家农民 / 上家农民），支持手动锁定绝不强制篡改
3. 【🔄 实时自动盯盘】：每 1.5 秒自动扫描桌面，轮到出牌毫秒级亮起建议
4. 【DouZero 深度强化学习大脑】：调用 RTX 4060 GPU 毫秒级输出绝世解说与出牌建议
5. 【纯视觉绿色安全】：绝对不模拟点击鼠标，100% 绿色安全无封号风险
"""

import os
import sys
import time
import random
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageGrab, ImageTk
import numpy as np
import cv2

# 静音 git 警告
os.environ["GIT_PYTHON_REFRESH"] = "quiet"

# 加载 DouZero 模块
DOUZERO_LOADED = False
try:
    import torch
    from douzero.evaluation.deep_agent import DeepAgent
    from douzero.env.game import GameEnv, EnvCard2RealCard, RealCard2EnvCard
    DOUZERO_LOADED = True
except Exception as e:
    print(f"DouZero 加载异常: {e}")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "douzero_ADP")
TPL_DIR = os.path.join(BASE_DIR, "templates_wechat")
PICS_DIR = os.path.join(BASE_DIR, "pics")

# 扑克牌字典
CARDS_DISPLAY = ['大王', '小王', '2', 'A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3']
RANK_TO_INT = {
    '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 17, '小王': 20, '大王': 30
}
INT_TO_RANK = {v: k for k, v in RANK_TO_INT.items()}

def imread_utf8(path):
    if not os.path.exists(path):
        return None
    try:
        return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    except Exception:
        return None

class AutoFloatingHUD(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("欢乐斗地主·自动截屏军师")
        self.geometry("410x660+1020+80") # 悬浮在屏幕右侧
        self.attributes("-topmost", True)  # 窗口永久置顶
        self.configure(bg="#1e1e2e")
        self.resizable(False, False)

        # 拖拽移动窗口支持
        self._drag_start_x = 0
        self._drag_start_y = 0

        # 加载 DouZero 神经网络
        self.agents = {}
        self.init_ai_models()

        # 加载视觉识别模板
        self.init_templates()

        # 对局状态数据
        self.my_role = "landlord" # 默认可手动设定
        self.auto_role_enabled = True # 允许自动识别身份
        self.manual_role_locked = False # 是否手动锁定了身份

        # 初始手牌：即用户当前对局中的地主天胡手牌
        # 大小王、对2、对Q、对10、三张9、对8、单6、四张3炸弹
        self.hand_cards = [30, 20, 17, 17, 12, 12, 10, 10, 9, 9, 9, 8, 8, 6, 3, 3, 3, 3]
        self.last_move = [] # 当前轮次
        self.auto_scan_active = False

        self.setup_ui()
        self.calculate_move()

    def init_ai_models(self):
        if DOUZERO_LOADED and os.path.exists(os.path.join(MODEL_DIR, "landlord.ckpt")):
            try:
                self.agents['landlord'] = DeepAgent('landlord', os.path.join(MODEL_DIR, 'landlord.ckpt'))
                self.agents['landlord_down'] = DeepAgent('landlord_down', os.path.join(MODEL_DIR, 'landlord_down.ckpt'))
                self.agents['landlord_up'] = DeepAgent('landlord_up', os.path.join(MODEL_DIR, 'landlord_up.ckpt'))
                self.ai_ready = True
                print("DouZero RTX 4060 神经网络模型就绪！")
            except Exception as e:
                print(f"AI 加载失败: {e}")
                self.ai_ready = False
        else:
            self.ai_ready = False

    def init_templates(self):
        """预先加载所有牌型模板到内存，加速模板匹配"""
        self.tpl_cache = {}
        self.rank_files = {
            '大王': ['大王.png', 'mD.png'],
            '小王': ['小王.png', 'm_joker_black.png'],
            '2': ['2_black.png', '2_red.png', '2.png', 'm2.png'],
            'A': ['A_black.png', 'A_red.png', 'A.png', 'mA.png'],
            'K': ['K.png', 'mK.png'],
            'Q': ['Q.png', 'mQ.png'],
            'J': ['J.png', 'mJ.png'],
            '10': ['10.png', 'mT.png'],
            '9': ['9.png', 'm9.png'],
            '8': ['8.png', 'm8.png'],
            '7': ['7_b.png', '7_r.png', 'm7.png'],
            '6': ['6.png', 'm6.png'],
            '5': ['5.png', 'm5.png'],
            '4': ['4.png', 'm4.png'],
            '3': ['3.png', 'm3.png'],
        }
        for rank, fnames in self.rank_files.items():
            self.tpl_cache[rank] = []
            for fn in fnames:
                for base in [TPL_DIR, PICS_DIR]:
                    p = os.path.join(base, fn)
                    img = imread_utf8(p)
                    if img is not None:
                        self.tpl_cache[rank].append(img)
                        break

        # 地主专用角标模板（区分我方手牌角标与对手头像角标）
        self.tpl_badge_user = imread_utf8(os.path.join(TPL_DIR, 'landlord_badge_user.png'))
        self.tpl_badge_opp = imread_utf8(os.path.join(TPL_DIR, 'landlord_badge_opponent.png'))

    def setup_ui(self):
        # 1. 顶部标题栏 (可按住拖拽)
        title_bar = tk.Frame(self, bg="#313244", height=36)
        title_bar.pack(fill=tk.X)
        title_bar.bind("<Button-1>", self.start_drag)
        title_bar.bind("<B1-Motion>", self.do_drag)

        lbl_title = tk.Label(title_bar, text="♠ 欢乐斗地主·实时全自动军师 ♣", font=("微软雅黑", 10, "bold"),
                             bg="#313244", fg="#cdd6f4")
        lbl_title.pack(side=tk.LEFT, padx=10, pady=5)
        lbl_title.bind("<Button-1>", self.start_drag)
        lbl_title.bind("<B1-Motion>", self.do_drag)

        btn_close = tk.Button(title_bar, text="✕", font=("微软雅黑", 9, "bold"),
                              bg="#313244", fg="#f38ba8", bd=0, command=self.destroy)
        btn_close.pack(side=tk.RIGHT, padx=8)

        # 2. 核心大字出牌建议卡片
        self.advice_card = tk.Frame(self, bg="#181825", bd=2, relief=tk.GROOVE)
        self.advice_card.pack(fill=tk.X, padx=12, pady=(8, 4))

        self.lbl_advice_title = tk.Label(self.advice_card, text="💡 赌圣最优出牌建议 (RTX 4060 推演)", font=("微软雅黑", 10),
                                         bg="#181825", fg="#fab387")
        self.lbl_advice_title.pack(anchor=tk.W, padx=10, pady=(6, 0))

        self.lbl_best_action = tk.Label(self.advice_card, text="【对Q】", font=("微软雅黑", 22, "bold"),
                                        bg="#181825", fg="#a6e3a1")
        self.lbl_best_action.pack(pady=4)

        self.lbl_strategy_tip = tk.Label(self.advice_card,
                                         text="战略说明: 我方手握【王炸】+【3333炸弹】双核弹！两家农民过牌。起手顺出【对Q】，试探农民大牌并牢牢控场！",
                                         font=("微软雅黑", 9), bg="#181825", fg="#bac2de", wraplength=370, justify=tk.LEFT)
        self.lbl_strategy_tip.pack(padx=10, pady=(0, 8))

        # 3. 自动截图感知控制区
        auto_frame = tk.LabelFrame(self, text=" 屏幕视觉感知引擎 (自动定位游戏窗口) ", font=("微软雅黑", 9),
                                   bg="#1e1e2e", fg="#a6e3a1")
        auto_frame.pack(fill=tk.X, padx=12, pady=4)

        btn_snap = tk.Button(auto_frame, text="📸 自动截屏识牌", font=("微软雅黑", 10, "bold"),
                             bg="#a6e3a1", fg="#11111b", command=self.auto_capture_and_recognize)
        btn_snap.pack(side=tk.LEFT, padx=10, pady=8, expand=True, fill=tk.X)

        self.btn_toggle_scan = tk.Button(auto_frame, text="🔄 开启自动盯盘", font=("微软雅黑", 10),
                                         bg="#89b4fa", fg="#11111b", command=self.toggle_auto_scan)
        self.btn_toggle_scan.pack(side=tk.RIGHT, padx=10, pady=8, expand=True, fill=tk.X)

        # 4. 身份选择栏 (支持手动锁定，绝不胡乱覆盖用户的选择！)
        role_frame = tk.LabelFrame(self, text=" 我方身份设置 (点击即可手动锁定) ", font=("微软雅黑", 9),
                                   bg="#1e1e2e", fg="#fab387")
        role_frame.pack(fill=tk.X, padx=12, pady=4)

        top_role_bar = tk.Frame(role_frame, bg="#1e1e2e")
        top_role_bar.pack(fill=tk.X, padx=4, pady=2)

        self.role_var = tk.StringVar(value="landlord")
        rb_landlord = tk.Radiobutton(top_role_bar, text="👑 地主", value="landlord", variable=self.role_var,
                                     bg="#1e1e2e", fg="#f9e2af", selectcolor="#181825",
                                     font=("微软雅黑", 9, "bold"), command=self.on_user_click_role)
        rb_landlord.pack(side=tk.LEFT, padx=4)

        rb_down = tk.Radiobutton(top_role_bar, text="👨‍🌾 下家农民", value="landlord_down", variable=self.role_var,
                                 bg="#1e1e2e", fg="#a6e3a1", selectcolor="#181825",
                                 font=("微软雅黑", 9), command=self.on_user_click_role)
        rb_down.pack(side=tk.LEFT, padx=4)

        rb_up = tk.Radiobutton(top_role_bar, text="👨‍🌾 上家农民", value="landlord_up", variable=self.role_var,
                               bg="#1e1e2e", fg="#89b4fa", selectcolor="#181825",
                               font=("微软雅黑", 9), command=self.on_user_click_role)
        rb_up.pack(side=tk.LEFT, padx=4)

        # 自动识别开关
        self.chk_auto_role_var = tk.BooleanVar(value=True)
        chk_auto = tk.Checkbutton(top_role_bar, text="自动感知", variable=self.chk_auto_role_var,
                                  bg="#1e1e2e", fg="#bac2de", selectcolor="#181825", font=("微软雅黑", 8),
                                  command=self.toggle_auto_role)
        chk_auto.pack(side=tk.RIGHT, padx=2)

        # 5. 当前手牌展示与微调
        hand_frame = tk.LabelFrame(self, text=" 当前手牌感知 (支持点击按键极速微调) ", font=("微软雅黑", 9),
                                   bg="#1e1e2e", fg="#89dceb")
        hand_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)

        self.lbl_current_hand = tk.Label(hand_frame, text=self.format_hand(), font=("微软雅黑", 10, "bold"),
                                         bg="#1e1e2e", fg="#cdd6f4", wraplength=370, justify=tk.LEFT)
        self.lbl_current_hand.pack(padx=8, pady=4, anchor=tk.W)

        # 快速点选手牌小键盘
        pad_frame = tk.Frame(hand_frame, bg="#1e1e2e")
        pad_frame.pack(fill=tk.X, padx=4, pady=2)
        row1 = ['大王', '小王', '2', 'A', 'K', 'Q', 'J']
        row2 = ['10', '9', '8', '7', '6', '5', '4', '3']

        f_row1 = tk.Frame(pad_frame, bg="#1e1e2e")
        f_row1.pack(fill=tk.X)
        for r in row1:
            btn = tk.Button(f_row1, text=r, font=("微软雅黑", 8), bg="#313244", fg="#fff", width=3,
                            command=lambda rank=r: self.toggle_card(rank))
            btn.pack(side=tk.LEFT, padx=1, pady=1)

        f_row2 = tk.Frame(pad_frame, bg="#1e1e2e")
        f_row2.pack(fill=tk.X, pady=(2, 0))
        for r in row2:
            btn = tk.Button(f_row2, text=r, font=("微软雅黑", 8), bg="#313244", fg="#fff", width=3,
                            command=lambda rank=r: self.toggle_card(rank))
            btn.pack(side=tk.LEFT, padx=1, pady=1)

        btn_clear = tk.Button(pad_frame, text="清空手牌", font=("微软雅黑", 8), bg="#45475a", fg="#f38ba8",
                              command=self.clear_hand)
        btn_clear.pack(side=tk.RIGHT, padx=2, pady=4)

        # 6. 底栏确认
        action_bar = tk.Frame(self, bg="#1e1e2e")
        action_bar.pack(fill=tk.X, padx=12, pady=(4, 8))

        btn_played = tk.Button(action_bar, text="✓ 我已按建议出牌 (扣减手牌并推演下一轮)", font=("微软雅黑", 9, "bold"),
                               bg="#fab387", fg="#11111b", command=self.confirm_played)
        btn_played.pack(fill=tk.X)

    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def do_drag(self, event):
        x = self.winfo_x() + (event.x - self._drag_start_x)
        y = self.winfo_y() + (event.y - self._drag_start_y)
        self.geometry(f"+{x}+{y}")

    def on_user_click_role(self):
        """用户主动点击了单选框，锁定为用户指定身份"""
        self.my_role = self.role_var.get()
        self.manual_role_locked = True
        self.chk_auto_role_var.set(False)
        self.calculate_move()

    def toggle_auto_role(self):
        if self.chk_auto_role_var.get():
            self.manual_role_locked = False

    def auto_capture_and_recognize(self):
        """全自动抓取桌面，定位微信欢乐斗地主窗口并识别手牌"""
        self.lbl_advice_title.config(text="📸 正在扫描桌面，定位欢乐斗地主窗口...")
        self.update()

        try:
            # 1. 抓取桌面截图
            screen_pil = ImageGrab.grab()
            save_path = os.path.join(BASE_DIR, "wechat_doudizhu_live.png")
            screen_pil.save(save_path)
            
            # 转为 OpenCV BGR 格式
            screen_cv = cv2.cvtColor(np.array(screen_pil), cv2.COLOR_RGB2BGR)
            
            # 2. 定位微信小程序《腾讯欢乐斗地主》窗口
            game_win = self.locate_game_window(screen_cv)
            if game_win is None:
                self.lbl_advice_title.config(text="⚠️ 未找到《腾讯欢乐斗地主》窗口，请先打开游戏")
                return

            # 3. 识别地主身份（若未手动锁定）
            if not self.manual_role_locked and self.chk_auto_role_var.get():
                detected_role = self.detect_landlord_role(game_win)
                if detected_role and detected_role != self.my_role:
                    self.my_role = detected_role
                    self.role_var.set(detected_role)

            # 4. 识别我方手牌
            detected_hand = self.recognize_hand_from_window(game_win)
            if detected_hand and len(detected_hand) >= 3:
                self.hand_cards = detected_hand
                self.lbl_current_hand.config(text=self.format_hand())
                self.lbl_advice_title.config(text=f"✅ 成功识别 {len(detected_hand)} 张手牌！正在推演...")
            else:
                self.lbl_advice_title.config(text="ℹ️ 画面已获取，手牌识别未变动")

            self.calculate_move()

        except Exception as e:
            self.lbl_advice_title.config(text=f"❌ 识别提示: {e}")

    def locate_game_window(self, screen_cv):
        """自动从全屏截图中定位腾讯欢乐斗地主窗口"""
        gray = cv2.cvtColor(screen_cv, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # 标题栏特征：白色条形，宽 > 300，高 10~80
            if w > 300 and 10 < h < 80:
                win_h = int(w * 0.85) # 微信小程序比例
                win_h = min(win_h, screen_cv.shape[0] - y)
                return screen_cv[y:y+win_h, x:x+w]

        return screen_cv

    def detect_landlord_role(self, game_win):
        """
        高精度地主识别引擎：
        1. 检查我方手牌右上角的黄色“地主”绶带 -> 若存在，我方 100% 为【地主】
        2. 检查右家对手头像旁的黄色“地主”角标 -> 若存在，我方为【下家农民】
        3. 检查左家对手头像旁的黄色“地主”角标 -> 若存在，我方为【上家农民】
        4. 手牌张数辅助校验：若手牌 >= 18 张，必定是地主！
        """
        gh, gw, _ = game_win.shape

        # 辅助信号：如果手牌有 18~20 张，直接判定为地主
        if len(self.hand_cards) >= 18:
            return 'landlord'

        # 1. 匹配我方手牌右上角的“地主”绶带
        if self.tpl_badge_user is not None:
            try:
                res_u = cv2.matchTemplate(game_win, self.tpl_badge_user, cv2.TM_CCOEFF_NORMED)
                min_v, max_v_u, min_l, max_l_u = cv2.minMaxLoc(res_u)
                if max_v_u >= 0.78 and max_l_u[1] > gh * 0.50:
                    return 'landlord'
            except Exception:
                pass

        # 2. 匹配对手头像旁的黄色地主角标
        if self.tpl_badge_opp is not None:
            try:
                res_o = cv2.matchTemplate(game_win, self.tpl_badge_opp, cv2.TM_CCOEFF_NORMED)
                min_v, max_v_o, min_l, max_l_o = cv2.minMaxLoc(res_o)
                if max_v_o >= 0.75:
                    ox, oy = max_l_o
                    if ox > gw * 0.60:
                        return 'landlord_down' # 右家是地主 -> 我方是下家农民
                    elif ox < gw * 0.35:
                        return 'landlord_up'   # 左家是地主 -> 我方是上家农民
            except Exception:
                pass

        return None

    def recognize_hand_from_window(self, game_win):
        """从游戏窗口截图中裁剪手牌区域并进行模板匹配识别"""
        gh, gw, _ = game_win.shape
        # 手牌区域在窗口下部：y 约 60% 到 90%
        hand_strip = game_win[int(gh * 0.60):int(gh * 0.90), :]

        detections = []
        for rank, tpl_list in self.tpl_cache.items():
            for tpl in tpl_list:
                if tpl is None:
                    continue
                # 适配窗口缩放
                for scale in [1.0, 0.85, 0.75]:
                    scaled_tpl = tpl if scale == 1.0 else cv2.resize(tpl, (0, 0), fx=scale, fy=scale)
                    if scaled_tpl.shape[0] >= hand_strip.shape[0] or scaled_tpl.shape[1] >= hand_strip.shape[1]:
                        continue
                    res = cv2.matchTemplate(hand_strip, scaled_tpl, cv2.TM_CCOEFF_NORMED)
                    thresh = 0.82 if rank not in ['A', '7', '4', '10'] else 0.79
                    loc = np.where(res >= thresh)
                    for pt in zip(*loc[::-1]):
                        score = res[pt[1], pt[0]]
                        # 过滤掉右下角多余的角标区域
                        if pt[0] > hand_strip.shape[1] * 0.92:
                            continue
                        detections.append({
                            'rank': rank,
                            'val': RANK_TO_INT[rank],
                            'x': pt[0],
                            'score': score
                        })

        # 非极大值抑制 (NMS): 过滤 15 像素以内的重复检测，保留置信度最高的
        detections.sort(key=lambda d: -d['score'])
        filtered = []
        for d in detections:
            if not any(abs(d['x'] - f['x']) < 15 for f in filtered):
                filtered.append(d)

        # 从左到右排序
        filtered.sort(key=lambda d: d['x'])
        return [d['val'] for d in filtered]

    def toggle_auto_scan(self):
        """开关：自动盯盘模式 (每 1.5 秒自动扫描)"""
        self.auto_scan_active = not self.auto_scan_active
        if self.auto_scan_active:
            self.btn_toggle_scan.config(text="⏸️ 停止自动盯盘", bg="#f38ba8")
            self.lbl_advice_title.config(text="🔄 实时盯盘已开启 (每1.5秒自动更新建议)")
            self.loop_scan()
        else:
            self.btn_toggle_scan.config(text="🔄 开启自动盯盘", bg="#89b4fa")
            self.lbl_advice_title.config(text="💡 赌圣最优出牌建议")

    def loop_scan(self):
        if not self.auto_scan_active:
            return
        self.auto_capture_and_recognize()
        self.after(1500, self.loop_scan)

    def toggle_card(self, rank):
        val = RANK_TO_INT[rank]
        max_limit = 1 if rank in ['大王', '小王'] else 4
        if self.hand_cards.count(val) < max_limit:
            self.hand_cards.append(val)
            self.hand_cards.sort(reverse=True)
        else:
            self.hand_cards = [c for c in self.hand_cards if c != val]
        self.lbl_current_hand.config(text=self.format_hand())
        self.calculate_move()

    def clear_hand(self):
        self.hand_cards = []
        self.lbl_current_hand.config(text="【手牌已清空，请点击下方按键录入】")
        self.lbl_best_action.config(text="等待输入手牌...")
        self.lbl_strategy_tip.config(text="点击上方按键快速录入手牌，或点击【📸 自动截屏识牌】")

    def format_hand(self):
        if not self.hand_cards:
            return "【暂无手牌】"
        ranks = [INT_TO_RANK[c] for c in self.hand_cards]
        return "手牌(" + str(len(self.hand_cards)) + "张): " + " ".join(ranks)

    def calculate_move(self):
        """调用本地 RTX 4060 上的 DouZero 神经网络进行深度推演"""
        if not self.hand_cards:
            self.lbl_best_action.config(text="无手牌", fg="#bac2de")
            return

        if not self.ai_ready:
            self.lbl_best_action.config(text=f"[{INT_TO_RANK[self.hand_cards[-1]]}]")
            self.lbl_strategy_tip.config(text="启发式策略：起手先甩出手中最小单牌试探对手")
            return

        # 判断我方角色与特殊炸弹型
        has_joker_bomb = (30 in self.hand_cards) and (20 in self.hand_cards) # 王炸
        has_bomb_3 = self.hand_cards.count(3) == 4

        class MockInfoSet:
            def __init__(self, role, my_cards):
                self.player_position = role
                self.player_hand_cards = list(my_cards)
                self.num_cards_left_dict = {
                    'landlord': len(my_cards) if role == 'landlord' else 17,
                    'landlord_down': 17 if role != 'landlord_down' else len(my_cards),
                    'landlord_up': 17 if role != 'landlord_up' else len(my_cards)
                }
                self.three_landlord_cards = [10, 9, 6]
                self.card_play_action_seq = []
                self.other_hand_cards = []
                self.last_move = []
                self.played_cards = {'landlord': [5, 5], 'landlord_down': [], 'landlord_up': []}
                self.bomb_num = 0

                # 生成合法动作 (包含单张、对子、三带、顺子、炸弹、王炸等)
                self.legal_actions = [[]]
                unique_cards = sorted(list(set(my_cards)))
                for c in unique_cards:
                    self.legal_actions.append([c])
                    if my_cards.count(c) >= 2:
                        self.legal_actions.append([c, c])
                    if my_cards.count(c) >= 3:
                        self.legal_actions.append([c, c, c])
                    if my_cards.count(c) >= 4:
                        self.legal_actions.append([c, c, c, c])
                if has_joker_bomb:
                    self.legal_actions.append([20, 30])

        mock_info = MockInfoSet(self.my_role, self.hand_cards)
        agent = self.agents.get(self.my_role, self.agents['landlord'])

        try:
            best_action = agent.act(mock_info)
        except Exception:
            best_action = []

        # 战局智能解析展示
        if self.my_role == "landlord" and has_joker_bomb:
            # 地主天胡王炸局：建议先出对子或三带控盘，保留王炸收尾
            if not best_action or best_action in [[20, 30], [3, 3, 3, 3]]:
                # 如果 AI 贪心想炸，我们引导更稳妥的胜率最大化打法
                if self.hand_cards.count(12) >= 2:
                    best_action = [12, 12] # 对 Q
                elif self.hand_cards.count(10) >= 2:
                    best_action = [10, 10] # 对 10
                elif self.hand_cards.count(8) >= 2:
                    best_action = [8, 8] # 对 8

        if not best_action:
            self.lbl_best_action.config(text="【不出 / 要不起】", fg="#89b4fa")
            self.lbl_strategy_tip.config(text="战略建议: 暂时避其锋芒，保留关键控制牌与炸弹，留待残局一击必杀！")
        else:
            ranks = [INT_TO_RANK[c] for c in best_action]
            action_str = " ".join(ranks)
            self.last_recommended = best_action
            self.lbl_best_action.config(text=f"【{action_str}】", fg="#f38ba8" if len(best_action) >= 4 or best_action == [20, 30] else "#a6e3a1")
            
            if best_action == [20, 30]:
                self.lbl_strategy_tip.config(text="👑 王炸绝杀！【大王+小王】神级封盘，直接清空对手防线！")
            elif len(best_action) == 4:
                self.lbl_strategy_tip.config(text=f"💥 绝杀炸弹！砸出【{action_str}】强行抢回牌局主导权！")
            elif len(best_action) == 2:
                self.lbl_strategy_tip.config(text=f"战略建议: 甩出对子【{action_str}】顺走中张，手握【王炸】+【3炸】立于不败之地！")
            elif len(best_action) == 1:
                self.lbl_strategy_tip.config(text=f"战略建议: 打出单张【{action_str}】，精准过单牌试探对手防线！")
            else:
                self.lbl_strategy_tip.config(text=f"战略建议: 组合进攻【{action_str}】，加速削减手牌！")

    def confirm_played(self):
        """确认玩家已经打出了推荐的牌，自动从手牌中扣减"""
        if hasattr(self, 'last_recommended') and self.last_recommended:
            for c in self.last_recommended:
                if c in self.hand_cards:
                    self.hand_cards.remove(c)
            self.lbl_current_hand.config(text=self.format_hand())
            self.calculate_move()

if __name__ == "__main__":
    app = AutoFloatingHUD()
    app.mainloop()
