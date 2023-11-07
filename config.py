# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os#ArchWiki
import subprocess#ArchWiki
import colors #Derek Taylor
#para import psutil no es necesario importar solo hay que desgargar python-psutil

from libqtile import bar, layout, widget #(para activar solo los widgets de qtile, pero para los extras hay que dasabilitar esta)
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# Make sure 'qtile-extras' is installed or this config will not work.
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration

from libqtile import hook#ArchWiki

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn("alacritty"), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    #Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    
    #Lanzar rofi
    Key([mod], "m", lazy.spawn("rofi -show drun"), desc="Launch rofi"),

    #Configurar monitor
    Key([mod], "p", lazy.spawn("mons -e right"), desc="Extend Monitor Right"),

    # Volume
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    Key([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),   

    #Control multimedia
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    
    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

    #Print Screen
    Key([], "Print", lazy.spawn("flameshot gui")),

    #Lock Screen
    Key([mod], "s", lazy.spawn("betterlockscreen -l")),

    # Switch focus of monitors(solo cambia entre monitores no entre escritorios)
    Key([mod], "period", lazy.next_screen()),
    Key([mod], "comma", lazy.prev_screen()),

    #Change keyboarlayout betwen "us", and "latam". Pa los compas: cambia el teclado
    Key([mod], "t", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."),

    #Atajo para boton de inicio
    Key([mod,"shift"], "s", lazy.spawn("rofi -show power-menu -modi power-menu:/home/gzeppeli/.local/bin/rofi-power-menu")),

    #Atajo para abrir firefox rapido
    Key([mod], "f", lazy.spawn("firefox")),
    
]

groups = [Group(i) for i in "1234"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

### COLORSCHEME ###
# Colors are defined in a separate 'colors.py' file.
# There 10 colorschemes available to choose from:
#
# colors = colors.DoomOne
# colors = colors.Dracula
# colors = colors.GruvboxDark
# colors = colors.MonokaiPro
# colors = colors.Nord
# colors = colors.OceanicNext
# colors = colors.Palenight
# colors = colors.SolarizedDark
# colors = colors.SolarizedLight
# colors = colors.TomorrowNight
#
# It is best not manually change the colorscheme; instead run 'dtos-colorscheme'
# which is set to 'MOD + p c'

#Definimos colores dependiendo del tema que elijamos en colors.py
colors = colors.DoomOne

### LAYOUTS ### 
layouts = [
    layout.Columns(
        #border_focus_stack=["#d75f5f", "#8f3d3d"],
        border_width=2,
        border_focus = colors[6],
        border_normal = colors[2],
        margin = 4,
        single_margin =0,
        align = 0,
        margin_on_single = 0,
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(border_focus = colors[6],border_normal = colors[2],margin = 4,border_width=2,),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    # layout.Spiral(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        #bottom
        top=bar.Bar(
            [
                widget.Spacer(length = 8),
                widget.Image(
                    filename = "~/.config/qtile/icons/archlinux.png",
                    scale = "False",
                    mouse_callbacks = {'Button1': lazy.spawn('rofi -show power-menu -modi power-menu:/home/gzeppeli/.local/bin/rofi-power-menu')},
                ),
                widget.Spacer(length = 8),
                
                #widget.CurrentLayout(),
                widget.GroupBox(
                    active = colors[5],
                    inactive = colors[1],
                    highlight_method='line',
                    block_highlight_text_color = colors[3],
                    highlight_color = colors[0],
                    other_screen_border = colors[5],
                    other_current_screen_border = colors[3],
                    this_current_screen_border = colors[3],
                    this_screen_border = colors[5],
                    borderwidth = 3,
                    fontsize = 17,
                ),
                widget.Spacer(length = 8),
                widget.CurrentLayoutIcon(
                        #background = colors[0],
                        padding = 3,
                        scale = 0.7,
                        decorations=[
                            BorderDecoration(
                                colour = colors[1],
                                border_width = [0, 0, 2, 0],
                            )
                        ],     
                    ),
                widget.Spacer(length = 8),

                widget.Prompt(),
                widget.Spacer(length = 8),
                widget.WindowName(
                    foreground = colors[7],
                ),
                widget.Spacer(length = 8),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                
                widget.Spacer(length = 8),
                
                widget.Net(
                       format = '🖧: {down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}',
                       foreground = colors[3],
                       decorations=[
                        BorderDecoration(
                            colour = colors[3],
                            border_width = [0, 0, 2, 0],
                        )
                    ],
                ),

                widget.Spacer(length = 8),

                widget.CPU(
                    format = ' Cpu: {load_percent}%',
                    foreground = colors[4],
                    decorations=[
                        BorderDecoration(
                            colour = colors[4],
                            border_width = [0, 0, 2, 0],
                        )
                    ],
                ),
                widget.Spacer(length = 8),
                widget.Memory(
                        foreground = colors[8],
                        mouse_callbacks = {'Button1': lazy.spawn('alacritty' + ' -e htop')},
                        format = '{MemUsed: .0f}{mm}',
                        fmt = '🖥  Mem: {} used',
                        decorations=[
                            BorderDecoration(
                                colour = colors[8],
                                border_width = [0, 0, 2, 0],
                            )
                        ],
                ),
                widget.Spacer(length = 8),
                widget.DF(
                        update_interval = 60,
                        foreground = colors[5],
                        mouse_callbacks = {'Button1': lazy.spawn('alacritty --hold -e df -Th')},
                        partition = '/',
                        #format = '[{p}] {uf}{m} ({r:.0f}%)',
                        format = '{uf}{m} free',
                        fmt = '🖴 Disk: {}',
                        visible_on_warn = False,
                        decorations=[
                            BorderDecoration(
                                colour = colors[5],
                                border_width = [0, 0, 2, 0],
                            )
                        ],
                ),
                widget.Spacer(length = 8),
                widget.KeyboardLayout(
                    configured_keyboards=['us', 'latam'], 
                    foreground = colors[4],
                    fmt = '⌨ Kbd: {}',
                    decorations=[
                        BorderDecoration(
                            colour = colors[4],
                            border_width = [0, 0, 2, 0],
                        )
                    ],
                ),
                widget.Spacer(length = 8),
                
                #widget.QuickExit(),
                widget.Volume(
                    mouse_callbacks = {'Button1': lazy.spawn('pavucontrol -t 4')},
                    foreground = colors[7],
                    fmt = '󰓃 Vol: {}',
                    decorations=[
                        BorderDecoration(
                            colour = colors[7],
                            border_width = [0, 0, 2, 0],
                        )
                    ],
                ),
                widget.Spacer(length = 8),
                widget.Clock(
                    foreground = colors[8],
                    format = "  %a, %b %d - ⏱ %H:%M",
                    decorations=[
                        BorderDecoration(
                            colour = colors[8],
                            border_width = [0, 0, 2, 0],
                        )
                    ],
                ),
                widget.Spacer(length = 8),
                widget.BatteryIcon(
                    foreground = colors[4],
                    update_interval = 5,
                    scale=1.7,
                    battery = "BAT0",
                    low_foreground = colors[1],
                    low_percentage = 0.2,
                    decorations=[
                        BorderDecoration(
                            colour = colors[4],
                            border_width = [0, 0, 2, 0],
                        )
                    ],    
                ),
                widget.Battery(
                    update_interval = 10,
                    foreground = colors[4],
                    format = "{percent:2.0%}({hour:d}:{min:02d})",# 
                    decorations=[
                        BorderDecoration(
                            colour = colors[4],
                            border_width = [0, 0, 2, 0],
                        )
                    ],     
                ),
                
                widget.Spacer(length = 8),
                widget.CheckUpdates(
                        foreground = colors[5],
                        update_interval = 5,
                        distro = 'Arch_checkupdates',
                        display_format = "📦: {updates} ",
                        no_update_string = '󰏖',
                        fontsize = 17,
                        colour_have_updates = colors[5],
                        colour_no_updates = colors[5],
                        mouse_callbacks = {'Button1': lazy.spawn('alacritty')},
                        decorations=[
                            BorderDecoration(
                                colour = colors[5],
                                    border_width = [0, 0, 2, 0],
                            )
                        ],
                ),
                widget.Spacer(length = 8),
                widget.Systray(),
                widget.Spacer(length = 8),
            ],
            24,
            background = colors[2],
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([script])