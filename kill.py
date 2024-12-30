from mcdreforged.api.all import *
import os
import json
import random

PLUGIN_METADATA = {
    'id': 'kill_command',
    'version': '1.0.0',
    'name': 'Kill Command Plugin',
    'description': '一个插件，玩家输入!!kill时有随机几率kill自己',
    'author': 'Lc_Tiking',
    'link': 'https://github.com/Tiking-owo/Kill-Command-Plugin',
}

CONFIG_FILE = 'config/kill.json'
DEFAULT_CONFIG = {
    'damage': 20,
    'chance': 0.5  # 50% chance
}

def ensure_config():
    """Ensure the configuration file exists and has valid content."""
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

def load_config():
    """Load the configuration from the file."""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    """Save the configuration to the file."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def on_load(server: PluginServerInterface, old_module):
    ensure_config()
    server.logger.info('Kill Command Plugin加载成功！')

def on_user_info(server: PluginServerInterface, info: Info):
    if info.content.startswith('!!kill'):
        config = load_config()
        args = info.content.split()

        if len(args) == 1 and args[0] == '!!kill':
            damage = config.get('damage', DEFAULT_CONFIG['damage'])
            chance = config.get('chance', DEFAULT_CONFIG['chance'])

            if random.random() < chance:
                server.execute(f'damage {info.player} {damage}')
                server.tell(info.player, f'§c你受到了{damage}点伤害！下次小心点哦！')
            else:
                server.tell(info.player, '§a这次你运气不错，没有受到伤害！')

        elif len(args) == 2 and args[1] == 'help':
            server.tell(info.player, '§6==== Kill Command Plugin 帮助 ====' )
            server.tell(info.player, '§e!!kill §f- 执行随机伤害指令')
            server.tell(info.player, '§e!!kill damage [伤害数] §f- 设置伤害值 (需要MCDR管理员权限)')
            server.tell(info.player, '§e!!kill chance [概率] §f- 设置概率 (需要MCDR管理员权限)')
            server.tell(info.player, '§e!!kill help §f- 显示本帮助信息')

        elif len(args) == 3 and info.is_player and server.get_permission_level(info) >= PermissionLevel.ADMIN:
            command, key, value = args

            if key == 'damage':
                try:
                    damage = int(value)
                    if damage > 0:
                        config['damage'] = damage
                        save_config(config)
                        server.tell(info.player, f'§a伤害值已设置为 §b{damage}')
                    else:
                        server.tell(info.player, '§c伤害值必须大于0')
                except ValueError:
                    server.tell(info.player, '§c无效的伤害值，请输入一个正整数')

            elif key == 'chance':
                try:
                    chance = float(value)
                    if 0 <= chance <= 1:
                        config['chance'] = chance
                        save_config(config)
                        server.tell(info.player, f'§a概率已设置为 §b{chance * 100}%')
                    else:
                        server.tell(info.player, '§c概率必须在0到1之间')
                except ValueError:
                    server.tell(info.player, '§c无效的概率值，请输入一个0到1之间的小数')
            else:
                server.tell(info.player, '§c未知的设置项')
