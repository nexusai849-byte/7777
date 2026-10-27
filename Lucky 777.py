import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
import random
import datetime

# Ultra Luxury Cinematic Dark Casino Theme
Window.clearcolor = (0.01, 0.02, 0.05, 1)

class VegasClubLobby(BoxLayout):
    balance_text = StringProperty("💵 10,000 ကျပ်")
    jackpot_text = StringProperty("💎 JPT: 5,000,000")
    vip_text = StringProperty("👑 VIP: Bronze 🥉")
    console_output = StringProperty("[color=00ffff][b]✨ APPLE VEGAS 777 (VISUAL FISH & SLOTS) သို့ ကြိုဆိုပါတယ် ဘိုတော်! ✨[/b][/color]\nHD ရုပ်ထွက်ငါးပစ်နှင့် စလော့ခန်းများ အဆင်သင့် ဖြစ်ပါပြီ။\n" + "="*55 + "\n")
    
    def __init__(self, **kwargs):
        super(VegasClubLobby, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10
        
        self.wallet_money = 10000
        self.jackpot_pool = 5000000
        self.total_actions = 0
        self.vip_points = 0
        self.last_claim_date = None

        # Symbols dictionary for all 14 Slot Rooms & Fish Game
        self.symbols_dict = {
            "Mahjong Ways": ['🀄', '🀅', '🀆', '🪙', '🀄'],
            "Sweet Bonanza": ['🍬', '🍭', '🍌', '🍎', '🍬'],
            "Classic Buffalo": ['🐃', '🦁', '🦅', '🪙', '🐃'],
            "Buffalo Gold": ['🐃', '✨', '🦅', '🌾', '🪙'],
            "Magic Genie": ['🧞‍♂️', '💎', '💠', '💍', '🧞‍♂️'],
            "Dragon Link": ['🐉', '🔥', '🪙', '🏮', '🐉'],
            "Olympus": ['⚡', '🏛️', '👑', '💎', '⚡'],
            "5 Dragons": ['🟢', '🔴', '🟡', '🐉', '🟢'],
            "Panda Magic": ['🐼', '🎋', '🏮', '✨', '🐼'],
            "Pharaoh": ['🏺', '👑', '🦅', '🐍', '🏺'],
            "Diamond Spin": ['💎', '💠', '💍', '7️⃣', '💎'],
            "Fortune Treasure": ['💰', '🪙', '🧧', '🏮', '💰'],
            "Crown of Vegas": ['👑', '7️⃣', '⭐', '🔔', '👑'],
            "Spin Mania": ['🔥', '🎰', '⚡', '🌟', '🔥'],
            "Fish Shooting HD": ['🐟', '🐠', '🐬', '🦈', '🐋', '🐉']
        }

        # --- 1. CINEMATIC GOLDEN HEADER ---
        header_layout = BoxLayout(size_hint_y=None, height=48, padding=5)
        with header_layout.canvas.before:
            Color(0.12, 0.08, 0.22, 1)
            self.header_bg = RoundedRectangle(pos=header_layout.pos, size=header_layout.size, radius=[10])
        header_layout.bind(pos=lambda *x: setattr(self.header_bg, 'pos', header_layout.pos),
                           size=lambda *x: setattr(self.header_bg, 'size', header_layout.size))
        
        header_label = Label(
            text='[b][color=ffd700]🌟 APPLE VEGAS 777 - HD VISUAL MASTER 🌟[/color][/b]',
            markup=True, font_size='18sp', halign='center', valign='middle'
        )
        header_label.bind(size=header_label.setter('text_size'))
        header_layout.add_widget(header_label)
        self.add_widget(header_layout)

        # --- 2. WALLET, JACKPOT & VIP PANEL ---
        info_grid = GridLayout(cols=3, spacing=8, size_hint_y=None, height=45)
        self.balance_label = Label(text=self.balance_text, font_size='13sp', bold=True, color=(0.2, 1, 0.6, 1))
        self.vip_label = Label(text=self.vip_text, font_size='12sp', color=(1, 0.84, 0, 1))
        self.jackpot_label = Label(text=self.jackpot_text, font_size='11sp', color=(0.8, 0.4, 1, 1))
        info_grid.add_widget(self.balance_label)
        info_grid.add_widget(self.vip_label)
        info_grid.add_widget(self.jackpot_label)
        self.add_widget(info_grid)

        # --- 3. BET INPUT PANEL ---
        bet_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=45)
        bet_label = Label(text='[b][color=00ffff]လောင်းကြေး (100-10,000):[/color][/b]', markup=True, font_size='13sp', size_hint_x=0.5)
        bet_grid.add_widget(bet_label)
        
        self.user_input = TextInput(text='100', multiline=False, font_size='16sp', input_filter='int', size_hint_x=0.5)
        bet_grid.add_widget(self.user_input)
        self.add_widget(bet_grid)

        # --- 4. UTILITY ACTION BUTTONS ---
        util_grid = GridLayout(cols=5, spacing=5, size_hint_y=None, height=40)
        
        btn_wheel = Button(text='🎡 Wheel', font_size='11sp', background_color=(0.9, 0.4, 0.1, 1), background_normal='')
        btn_wheel.bind(on_press=self.play_lucky_wheel)
        util_grid.add_widget(btn_wheel)

        btn_daily = Button(text='🎁 နေ့စဉ်ဆု', font_size='11sp', background_color=(0.1, 0.6, 0.8, 1), background_normal='')
        btn_daily.bind(on_press=self.claim_daily)
        util_grid.add_widget(btn_daily)

        btn_mission = Button(text='🎯 မစ်ရှင်', font_size='11sp', background_color=(0.2, 0.7, 0.3, 1), background_normal='')
        btn_mission.bind(on_press=self.check_missions)
        util_grid.add_widget(btn_mission)

        btn_trophy = Button(text='🏆 ဆုတံဆိပ်', font_size='11sp', background_color=(0.85, 0.65, 0.13, 1), background_normal='')
        btn_trophy.bind(on_press=self.view_trophy)
        util_grid.add_widget(btn_trophy)

        btn_reset = Button(text='🔄 အစက', font_size='11sp', background_color=(0.5, 0.5, 0.5, 1), background_normal='')
        btn_reset.bind(on_press=self.reset_game)
        util_grid.add_widget(btn_reset)
        
        self.add_widget(util_grid)

        # --- 5. SCROLLABLE GAME ROOMS ---
        scroll = ScrollView(size_hint=(1, 1))
        content = GridLayout(cols=1, spacing=16, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # Slot Section (14 Rooms)
        content.add_widget(Label(text='[b][color=ff99ff]🎰 ၅ ကွက်စလော့ခန်းများ (၁၄ ခန်း + 5-Reel HD Grid)[/color][/b]', markup=True, font_size='13sp', size_hint_y=None, height=25))
        slot_grid = GridLayout(cols=2, spacing=6, size_hint_y=None, height=330)
        for s_name in [k for k in self.symbols_dict.keys() if k != "Fish Shooting HD"]:
            b = Button(text=f"🎰 {s_name}", font_size='12sp', background_color=(0.4, 0.1, 0.55, 1), background_normal='')
            b.bind(on_press=lambda x, name=s_name: self.play_slot_room(name))
            slot_grid.add_widget(b)
        content.add_widget(slot_grid)

        # Table Section (11 Games)
        content.add_widget(Label(text='[b][color=33ff99]🟢 ၅ ဦးထိုင် ဖဲဝိုင်းများနှင့် စားပွဲဝိုင်းများ (ဒိုင် Mary & Lisa)[/color][/b]', markup=True, font_size='13sp', size_hint_y=None, height=25))
        table_grid = GridLayout(cols=2, spacing=6, size_hint_y=None, height=270)
        table_games = [
            "ရူလက် (Roulette)", "ဘက်ကာရား (Baccarat)", "ဘလက်ဂျက် (Blackjack 21)",
            "ဒေါင်ဂွန်တိုက်ဂါး (Dragon Tiger)", "စစ်ဘို / အန်စာတုံး (Sic Bo)", "ပိုကာ (Poker)",
            "ကီနို (Keno)", "ကရပ်စ် (Craps)", "တင်းပတ္တီ (Teen Patti)",
            "အန်ဒါဘဟာ (Andar Bahar)", "ရှမ်းကိုးမီး / ဘူကြီး (Boogyi)"
        ]
        for t_name in table_games:
            tb = Button(text=f"🟢 {t_name}", font_size='11sp', background_color=(0.05, 0.5, 0.3, 1), background_normal='')
            tb.bind(on_press=lambda x, name=t_name: self.play_table_room(name))
            table_grid.add_widget(tb)
        content.add_widget(table_grid)

        # Sports, Racing & Arcade Section (Fish shooting with Visual Slot Reels)
        content.add_widget(Label(text='[b][color=ffaa33]🏆 အားကစား၊ F1၊ မြင်းပြိုင်ပွဲ၊ ကြက်တိုက် နှင့် HD ငါးပစ်ဂိမ်း (စလော့ပုံစံ)[/color][/b]', markup=True, font_size='13sp', size_hint_y=None, height=25))
        arcade_grid = GridLayout(cols=2, spacing=6, size_hint_y=None, height=130)
        
        btn_single = Button(text='⚽ တစ်ပွဲချင်း လောင်းကစား', font_size='11sp', background_color=(0.2, 0.25, 0.5, 1), background_normal='')
        btn_single.bind(on_press=self.play_football_single)
        arcade_grid.add_widget(btn_single)

        btn_parlay = Button(text='🚀 ၄ ပွဲတွဲ စုံတွဲလောင်း (Parlay)', font_size='11sp', background_color=(0.35, 0.2, 0.65, 1), background_normal='')
        btn_parlay.bind(on_press=self.play_football_parlay)
        arcade_grid.add_widget(btn_parlay)

        btn_f1 = Button(text='🏎️ ဖော်မြူလာဝမ်း (F1 Racing)', font_size='11sp', background_color=(0.5, 0.2, 0.2, 1), background_normal='')
        btn_f1.bind(on_press=self.play_f1_racing)
        arcade_grid.add_widget(btn_f1)

        btn_horse = Button(text='🏇 မြင်းပြိုင်ပွဲ (Horse Racing)', font_size='11sp', background_color=(0.6, 0.35, 0.1, 1), background_normal='')
        btn_horse.bind(on_press=self.play_horse_racing)
        arcade_grid.add_widget(btn_horse)

        btn_cock = Button(text='🐓 ကြက်ခြင်းတိုက်', font_size='11sp', background_color=(0.8, 0.15, 0.15, 1), background_normal='')
        btn_cock.bind(on_press=self.play_cockfighting)
        arcade_grid.add_widget(btn_cock)

        btn_fish = Button(text='🐠 ငါးပစ်ဂိမ်း (5-Reel HD Fish)', font_size='11sp', background_color=(0.1, 0.5, 0.85, 1), background_normal='')
        btn_fish.bind(on_press=self.play_fish_shooting)
        arcade_grid.add_widget(btn_fish)

        content.add_widget(arcade_grid)
        scroll.add_widget(content)
        self.add_widget(scroll)

        # --- 6. VISUAL SLOT REELS DISPLAY PANEL ---
        reels_header = Label(text='[b][color=00ffcc]🎰 စလော့ & ငါးပစ် ၅ ကွက်ရုပ်ထွက်ပြခန်း (HD Reels):[/color][/b]', markup=True, font_size='12sp', size_hint_y=None, height=22, halign='left')
        reels_header.bind(size=reels_header.setter('text_size'))
        self.add_widget(reels_header)

        # 5-Reel Visual Box Grid
        self.reels_grid = GridLayout(cols=5, spacing=6, size_hint_y=None, height=55)
        self.reel_boxes = []
        for i in range(5):
            box = Label(text='?', font_size='22sp', bold=True, color=(1, 0.9, 0.2, 1))
            # Background for each reel box
            with box.canvas.before:
                Color(0.1, 0.15, 0.3, 1)
                box.bg_rect = RoundedRectangle(pos=box.pos, size=box.size, radius=[6])
            box.bind(pos=lambda inst, val, b=box: setattr(b.bg_rect, 'pos', val),
                     size=lambda inst, val, b=box: setattr(b.bg_rect, 'size', val))
            self.reel_boxes.append(box)
            self.reels_grid.add_widget(box)
        self.add_widget(self.reels_grid)

        # --- 7. CONSOLE LOG OUTPUT PANEL ---
        log_header = Label(text='[b][color=ffd700]ဂိမ်းမှတ်တမ်း & အကျိုးအမြတ် (Console Log):[/color][/b]', markup=True, font_size='12sp', size_hint_y=None, height=22, halign='left')
        log_header.bind(size=log_header.setter('text_size'))
        self.add_widget(log_header)

        log_scroll = ScrollView(size_hint=(1, None), height=90)
        self.output_label = Label(
            text=self.console_output,
            font_size='11sp',
            markup=True,
            halign='left',
            valign='top',
            size_hint_y=None,
            color=(0.95, 0.95, 0.95, 1)
        )
        self.output_label.bind(width=lambda *x: self.update_height())
        log_scroll.add_widget(self.output_label)
        self.add_widget(log_scroll)

        # Property bindings
        self.bind(balance_text=lambda i, v: setattr(self.balance_label, 'text', v))
        self.bind(vip_text=lambda i, v: setattr(self.vip_label, 'text', v))
        self.bind(jackpot_text=lambda i, v: setattr(self.jackpot_label, 'text', v))
        self.bind(console_output=lambda i, v: setattr(self.output_label, 'text', v))

    def update_height(self):
        self.output_label.text_size = (self.output_label.width * 0.95, None)
        self.output_label.height = max(self.output_label.texture_size[1], 70)

    def log(self, msg):
        self.console_output = f"-> {msg}\n" + "-"*50 + "\n" + self.console_output

    def update_reels_display(self, r_list):
        for i, val in enumerate(r_list):
            if i < len(self.reel_boxes):
                self.reel_boxes[i].text = val

    def get_bet(self):
        try:
            b = int(self.user_input.text)
            if 100 <= b <= self.wallet_money: return b
            self.log("[color=ff3333]⚠️ လောင်းကြေး 100 မှ လက်ကျန်ငွေအတွင်း ထည့်ပါ။[/color]")
        except:
            self.log("[color=ff3333]⚠️ ကိန်းဂဏန်းသာ ထည့်ပါ။[/color]")
        return -1

    def update_wallet(self, amt):
        self.wallet_money += amt
        self.total_actions += 1
        self.vip_points += 2
        self.balance_text = f"💵 {self.wallet_money:,} ကျပ်"
        self.jackpot_pool += random.randint(500, 1500)
        self.jackpot_text = f"💎 JPT: {self.jackpot_pool:,}"
        
        if self.vip_points >= 50: self.vip_text = "👑 VIP: Diamond 💎"
        elif self.vip_points >= 20: self.vip_text = "👑 VIP: Gold 🥇"
        elif self.vip_points >= 10: self.vip_text = "👑 VIP: Silver 🥈"

    def claim_daily(self, inst):
        today = datetime.date.today()
        if self.last_claim_date == today:
            self.log("[color=ff9999]⏳ ယနေ့အတွက် ယူပြီးသား ဖြစ်ပါသည်။[/color]")
        else:
            self.last_claim_date = today
            self.update_wallet(10000)
            self.log("[color=00ff00][b]🌟 [DAILY BONUS] +10,000 ကျပ် အောင်မြင်စွာ ရရှိသည်! 🌟[/b][/color]")

    def play_lucky_wheel(self, inst):
        won = random.choice([1000, 3000, 5000, 10000, 20000, 50000])
        self.update_wallet(won)
        self.log(f"[color=ffcc00][b]🎡 [WHEEL SPIN] ဆုငွေ +{won:,} ကျပ် ရရှိသည်![/b][/color]")

    def check_missions(self, inst):
        self.log(f"🎯 နေ့စဉ် မစ်ရှင် ဆော့ကစားမှု: {self.total_actions}/5 ကြိမ်")
        if self.total_actions >= 5:
            self.update_wallet(5000)
            self.log("[color=00ff00]✅ မစ်ရှင် ပြီးမြောက်၍ ဆုကြေး 5,000 ကျပ် ရရှိသည်![/color]")
        else:
            self.log(f"⏳ မစ်ရှင် ပြီးမြောက်ရန် နောက်ထပ် {5 - self.total_actions} ကြိမ် လိုအပ်ပါသည်။")

    def view_trophy(self, inst):
        tier = self.vip_text
        self.log(f"🏆 [Trophy Room] အဆင့်: {tier} | စုစုပေါင်း ကစားမှု: {self.total_actions} ကြိမ်")

    def trigger_free_spins(self, bet_cost, room_name):
        spins_count = random.choice([8, 12, 15])
        self.log(f"[color=00ffff][b]✨⚡ [{room_name}] FREE SPINS ({spins_count} SPINS) ACTIVATED! ⚡✨[/b][/color]")
        total_free_win = 0
        for fs in range(1, spins_count + 1):
            win_mul = random.choice([2, 5, 10, 25, 50])
            fs_win = bet_cost * win_mul
            total_free_win += fs_win
        return total_free_win

    def play_slot_room(self, room_name):
        bet = self.get_bet()
        if bet == -1: return
        self.update_wallet(-bet)
        
        symbols = self.symbols_dict[room_name]
        r1, r2, r3, r4, r5 = random.choices(symbols, k=5)
        self.update_reels_display([r1, r2, r3, r4, r5])
        self.log(f"🎰 [{room_name}] 5-Reel -> [ {r1} | {r2} | {r3} | {r4} | {r5} ]")
        
        if r1 == r2 == r3 == r4 == r5:
            win = bet * 50
            self.update_wallet(win)
            self.log(f"[color=ffd700][b]🌟 [MEGA JACKPOT] ၅ ကွက်စလုံးတူ! +{win:,} ကျပ် (50x) 🌟[/b][/color]")
        elif r1 == r2 == r3 == r4 or r2 == r3 == r4 == r5:
            win = bet * 20
            self.update_wallet(win)
            self.log(f"[color=00ff00][b]💎 [SUPER WIN] ၄ ကွက်တူ အနိုင်ရ! +{win:,} ကျပ် (20x) 💎[/b][/color]")
        elif (r1 == r2 == r3) or (r2 == r3 == r4) or (r3 == r4 == r5):
            win = bet * 5
            self.update_wallet(win)
            self.log(f"[color=00ffcc]🎉 ၃ ကွက်တူ အနိုင်ရ! +{win:,} ကျပ် (5x)[/color]")
        elif random.random() < 0.20:
            free_win = self.trigger_free_spins(bet, room_name)
            self.update_wallet(free_win)
            self.log(f"[color=ff99ff][b]🎯 FREE SPINS TOTAL WIN: +{free_win:,} ကျပ်[/b][/color]")
        else:
            self.log("[color=ff6666]❌ ရှုံးနိမ့်သည် (Try Again)[/color]")

    def play_table_room(self, table_name):
        bet = self.get_bet()
        if bet == -1: return
        self.update_wallet(-bet)
        self.log(f"🟢 [VIP Table: {table_name}] (AI ၄ ယောက် + ဒိုင် Mary/Lisa အသင့်ရှိ)...")
        if random.random() > 0.45:
            win = bet * 2
            self.update_wallet(win)
            self.log(f"[color=00ff00][b]🎉 [TABLE WIN] ဝိုင်းတွင် အနိုင်ရ +{win:,} ကျပ်[/b][/color]")
        else:
            self.log("[color=ff6666]❌ ရှုံးနိမ့်သည်[/color]")

    def play_football_single(self, inst):
        bet = self.get_bet()
        if bet == -1: return
        self.update_wallet(-bet)
        self.log("⚽ [Single Bet] Man Utd vs Liverpool (Odds: 2.1)...")
        if random.random() > 0.5:
            win = int(bet * 2.1)
            self.update_wallet(win)
            self.log(f"[color=00ff00]🎉 ပွဲစဉ်မှန်ကန်၍ အနိုင်ရ +{win:,} ကျပ်[/color]")
        else:
            self.log("[color=ff6666]❌ ရှုံးနိမ့်သည်[/color]")

    def play_football_parlay(self, inst):
        bet = self.get_bet()
        if bet == -1: return
        self.update_wallet(-bet)
        self.log("🚀 [Parlay ၄ ပွဲတွဲ] စုံတွဲလောင်း စစ်ဆေးနေသည်...")
        if random.random() < 0.35:
            win = int(bet * 7.5)
            self.update_wallet(win)
            self.log(f"[color=ffd700][b]🔥🔥 [PARLAY WIN] ၄ ပွဲတွဲ အောင်မြင်မှု! +{win:,} ကျပ် (7.5x) 🔥🔥[/b][/color]")
        else:
            self.log("[color=ff6666]❌ စုံတွဲလောင်း ရှုံးနိမ့်သည်[/color]")

    def play_f1_racing(self, inst):
        bet = self.get_bet()
        if bet == -1: return
        self.update_wallet(-bet)
        self.log("🏎️ [F1 Racing] Max Verstappen vs Hamilton...")
        if random.random() > 0.5:
            win = int(bet * 3.5)
            self.update_wallet(win)
            self.log(f"[color=00ff00]🎉 F1 ယာဉ်မောင်း ပထမရ၍ အနိုင်ရ +{win:,} ကျပ်[/color]")
        else:
            self.log("[color=ff6666]❌ ရှုံးနိမ့်သည်[/color]")

    def play_horse_racing(self, inst):
        bet = self.get_bet()
        if bet == -1: return
        self.update_wallet(-bet)
        self.log("🏇 [Horse Racing] မြင်းပြိုင်ပွဲ ယှဉ်ပြိုင်နေသည်...")
        if random.random() > 0.5:
            win = int(bet * 4.0)
            self.update_wallet(win)
            self.log(f"[color=00ff00]🎉 ရွေးချယ်ထားသောမြင်း ပထမရ၍ အနိုင်ရ +{win:,} ကျပ်[/color]")
        else:
            self.log("[color=ff6666]❌ ရှုံးနိမ့်သည်[/color]")

    def play_cockfighting(self, inst):
        bet = self.get_bet()
        if bet == -1: return
        self.update_wallet(-bet)
        res = random.choices([1, 2, 3], weights=[45, 45, 10], k=1)[0]
        self.log("🐓 ကြက်ခြင်းတိုက် (Cockfighting Arena)...")
        if res in [1, 2]:
            win = bet * 2
            self.update_wallet(win)
            self.log(f"[color=00ff00]🎉 ကြက်ပွဲ အနိုင်ရ +{win:,} ကျပ်[/color]")
        elif res == 3:
            win = bet * 8
            self.update_wallet(win)
            self.log(f"[color=ffd700][b]🔥🔥 [DRAW JACKPOT] သရေ ၈ ဆ +{win:,} ကျပ် ရရှိသည်! 🔥🔥[/b][/color]")
        else:
            self.log("[color=ff6666]❌ ရှုံးနိမ့်သည်[/color]")

    def play_fish_shooting(self, inst):
        bet = self.get_bet()
        if bet == -1: return
        self.update_wallet(-bet)
        
        # 5-Reel Visual HD Fish Shooting Reels
        fish_symbols = self.symbols_dict["Fish Shooting HD"]
        f1, f2, f3, f4, f5 = random.choices(fish_symbols, k=5)
        self.update_reels_display([f1, f2, f3, f4, f5])
        self.log(f"🐠 [ငါးပစ်ဂိမ်း 5-Reel HD] ရေအောက်ပစ်ခတ်မှု -> [ {f1} | {f2} | {f3} | {f4} | {f5} ]")
        
        if f5 == '🐉':
            win = bet * 50
            self.update_wallet(win)
            self.log(f"[color=ffd700][b]🌟🐉 [DRAGON BOSS] ဒဏ္ဍာရီ နဂါးဘော့စ်ကို ပစ်ခတ်နိုင်ခဲ့သည်! +{win:,} ကျပ် (50x) 🐉🌟[/b][/color]")
        elif f4 == '🦈' or f5 == '🐋':
            win = bet * 20
            self.update_wallet(win)
            self.log(f"[color=00ff00][b]💎🐋 [MEGA WHALE] ဝေလငါးကြီးကို ရရှိသည်! +{win:,} ကျပ် (20x) 🐋💎[/b][/color]")
        elif f1 == f2 == f3:
            win = bet * 5
            self.update_wallet(win)
            self.log(f"[color=00ffcc]🎉 ငါးအုပ်စု တူညီမှုအတွက် အနိုင်ရ +{win:,} ကျပ် (5x)[/color]")
        elif random.random() < 0.30:
            win = bet * 3
            self.update_wallet(win)
            self.log(f"[color=00ff00]🎯 ရွှေငါးလတ်များကို ပစ်ခတ်နိုင်ခဲ့သည်! +{win:,} ကျပ် (3x)[/color]")
        else:
            self.log("[color=ff6666]❌ ငါးများ လွတ်မြောက်သွားသည်၊ လွဲချော်သည်။[/color]")

    def reset_game(self, inst):
        self.wallet_money = 10000
        self.total_actions = 0
        self.vip_points = 0
        self.balance_text = "💵 10,000 ကျပ်"
        self.user_input.text = "100"
        self.console_output = ""
        self.update_reels_display(['?', '?', '?', '?', '?'])
        self.log("🔄 ဂိမ်းကို အစမှ ပြန်စလိုက်ပါပြီ။")

class AppleVegasHDApp(App):
    title = 'APPLE VEGAS 777 - HD Visual Fish & Slots Edition'
    def build(self): return VegasClubLobby()

if __name__ == '__main__':
    AppleVegasHDApp().run()
