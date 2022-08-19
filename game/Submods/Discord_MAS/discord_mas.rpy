init -990 python:
    store.mas_submod_utils.Submod(
        author="P",
        name="Discord Status Sync",
        description=(
            "将你的MAS游戏状态同步至Discord.\n"
        ),
        version="1.0.1",
        settings_pane="DSS_Setting",
    )
init -999 python:
    persistent._dss_id = '1000318038253510727'

define dss=None
define dss_l=None

init 900 python:
    from store.mas_threading import MASAsyncWrapper
    import subprocess
    import time
    dss_starttime = int(time.time())
    dss_li={}
    dss_li['spaceroom']="https://raw.githubusercontent.com/PencilMario/dss_roomimg/main/spaceroom.png"
    dss_li['submod_background_Den']="https://raw.githubusercontent.com/PencilMario/dss_roomimg/main/den.png"
    dss_li['submod_background_garden_view']="https://raw.githubusercontent.com/PencilMario/dss_roomimg/main/gardenview.png"
    dss_li['submod_background_Furnished_spaceroom1']="https://raw.githubusercontent.com/PencilMario/dss_roomimg/main/submod_background_Furnished_spaceroom1.png"
    dss_li['submod_background_Furnished_spaceroom2']="https://raw.githubusercontent.com/PencilMario/dss_roomimg/main/submod_background_Furnished_spaceroom2.png"
    dss_li['submod_background_Furnished_spaceroom3']="https://raw.githubusercontent.com/PencilMario/dss_roomimg/main/submod_background_Furnished_spaceroom3.png"
    dss_li['submod_background_Kitchen']="https://raw.githubusercontent.com/PencilMario/dss_roomimg/main/kitchen.png"

    # status
    def getDetail():
        doing=False
        if not doing:
            doing="只是与{}消磨时间".format(m_name)

        # debug mode
        if renpy.config.debug or renpy.config.developer:
            doing="正在代码摸鱼"

        # Netease Music 早一点判断来显示玩游戏的状态
        if mas_submod_utils.isSubmodInstalled('Netease Music'):
            if np_globals.Np_Playing:
                if np_globals.Music_Name != "" and np_globals.Music_Name != "<正在播放缓存列表>":
                    doing="正在听 {}".format(np_globals.Music_Name)
        # game
        # 国际象棋 但是我不会:(
        pass
        # NOU
        if renpy.get_screen('nou_stats'):
            doing = "正在玩 NOU [{} - {}]".format(persistent._mas_game_nou_points['Monika'],persistent._mas_game_nou_points['Player'])
        # hangman
        if renpy.showing('hm_frame') or renpy.showing('hm_frame_d'):
            doing = "正在玩 上吊小人"
        # pong :(
        pass

        # Submod Extra+
        if mas_submod_utils.isSubmodInstalled('Extra Plus'):
            # rock-paper-scissors
            if renpy.showing('card_back'):
                doing="正在玩 石头剪刀布"
            if renpy.showing('cup'):
                doing="正在玩 纸杯游戏"
            if renpy.get_screen('minigame_ttt_scr'):
                doing="正在玩 井字棋"
        
        
        
        
        
        return doing
    # room mas_current_background.prompt
    def getState():
        room = "在房间 {}".format(mas_current_background.prompt)
        return room

    def getLargeText():
        return mas_current_background.prompt
    def getLargeImage():
        id = mas_current_background.background_id
        try:
            return dss_li[id]
        except KeyError:
            return dss_li['spaceroom']

    def dss_kill():
        cmd="taskkill /f /im dss.exe"
        subprocess.Popen(cmd)

    def dss_update():
        global dss
        status={}
        status['basedir']=renpy.config.basedir.replace('\\', '/')
        status['id'] = persistent._dss_id
        status['State'] = getState()
        status['Detail'] = getDetail()
        status['Start'] = dss_starttime
        status['large_image'] = getLargeImage()
        status['large_text'] = getLargeText()
        status['small_image'] = "https://raw.githubusercontent.com/Monika-After-Story/MonikaModDev/master/Monika%20After%20Story/game/mod_assets/menu_new.png"
        status['small_text'] = "Monika After Story"
        #status['Buttons'] = args.Buttons

        if dss != None:
            dss.kill()
            dss_kill()
            time.sleep(2)
            dss=None
        cmd = "\"{}\" -i \"{}\" -s \"{}\" -d \"{}\" -stt \"{}\" -li \"{}\" -si \"{}\" -st \"{}\"".format(
        status['basedir']+"/game/Submods/Discord_MAS/dss/dist/dss/dss.exe",
        status['id'],
        status['State'],
        status["Detail"],
        status['Start'],
        status['large_image'],
        status['large_text'],
        status['small_image'],
        status['small_text']
        )
        
        st=subprocess.STARTUPINFO
        st.dwFlags=subprocess.STARTF_USESHOWWINDOW
        st.wShowWindow=subprocess.SW_HIDE
        dss=subprocess.Popen(cmd, startupinfo=st)
        if renpy.debug:
            renpy.notify("DSS已经同步")
    
    def _dss_start():
        while True:
            t=1
            dss_update()
            while t>0:
                t=t-1
                time.sleep(60)
            
    def dss_start():
        import threading 
        a_thr = threading.Thread(
            name="a_name",
            target=_dss_start,
        )
        a_thr.daemon=True
        try:
            a_thr.start()
        except:
            pass
    dss_start()
screen DSS_Setting():
    vbox:
        xmaximum 800
        xfill True
        style_prefix "check"
    textbutton "> 手动启动同步":
        action Function(dss_start)

    textbutton "> 立刻同步":
        action Function(dss_update)

    textbutton "> 设置discord APP ID":
        action Jump('dss_input')

label dss_input:
    python:
        persistent._dss_id = mas_input(
            _("请输入Discord APP id"),
            allow="0123456789",
            length=40
        )

# 在ch30中添加更新方法

#label ch30_loop:
#    $ dss_update()
#    $ quick_menu = True
#    # TODO: make these functions so docking station can run weather alg
#    # on start.
#    # TODO: consider a startup version of those functions so that
#    #   we can run the regular shouldRain alg if prgoression is disabled
#    python:
#        should_dissolve_masks = (
#            mas_weather.weatherProgress()
#            and mas_isMoniNormal(higher=True)
#        )
#        force_exp = mas_idle_mailbox.get_forced_exp()
#        should_dissolve_all = mas_idle_mailbox.get_dissolve_all()
#        scene_change = mas_idle_mailbox.get_scene_change()
#    call spaceroom(scene_change=scene_change, force_exp=force_exp, dissolve_all=should_dissolve_all, dissolve_masks=should_dissolve_masks)
##    if should_dissolve_masks:
##        show monika idle at t11 zorder MAS_MONIKA_Z
## TODO: add label here to allow startup to hook past weather
## TODO: move quick_menu to here
#    # updater check in here just because
#    if not mas_checked_update:
#        $ mas_backgroundUpdateCheck()
#        $ mas_checked_update = True
#    
#
#label ch30_visual_skip:
#
#    $ persistent.autoload = "ch30_autoload"
#    # if not persistent.tried_skip:
#    #     $ config.allow_skipping = True
#    # else:
#    #     $ config.allow_skipping = False
#
#    # check for outstanding threads
#    if store.mas_dockstat.abort_gen_promise:
#        $ store.mas_dockstat.abortGenPromise()
#
#    if mas_idle_mailbox.get_skipmidloopeval():
#        jump ch30_post_mid_loop_eval
#
#    #Do the weather thing
#    #    if mas_weather.weatherProgress() and mas_isMoniNormal(higher=True):
#    #        call spaceroom(dissolve_masks=True)
#
#    # check reoccuring checks
#    $ now_check = datetime.datetime.now()
#
#    # check day
#    if now_check.day != mas_globals.last_day:
#        call ch30_day
#        $ mas_globals.last_day = now_check.day
#
#    # check hour
#    if now_check.hour != mas_globals.last_hour:
#        call ch30_hour
#        $ mas_globals.last_hour = now_check.hour
#
#    # check minute
#    $ time_since_check = now_check - mas_globals.last_minute_dt
#    if now_check.minute != mas_globals.last_minute_dt.minute or time_since_check.total_seconds() >= 60:
#        call ch30_minute(time_since_check)
#
#        $ dss_update()
#        $ mas_globals.last_minute_dt = now_check