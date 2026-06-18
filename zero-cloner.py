import requests
import json
import time
import os
import sys
from datetime import datetime

class ZeroCloner:
    def __init__(self, user_token):
        self.token = user_token
        self.headers = {
            'Authorization': user_token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        banner = f"""
╔════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                            ║
║     ███████╗███████╗██████╗  ██████╗      ██████╗██╗      ██████╗ ███╗   ██╗ ███████╗██████╗ 
║     ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗    ██╔════╝██║     ██╔═══██╗████╗  ██║ ██╔════╝██╔══██╗
║       ███╔╝ █████╗  ██████╔╝██║   ██║    ██║     ██║     ██║   ██║██╔██╗ ██║ █████╗  ██████╔╝
║      ███╔╝  ██╔══╝  ██╔══██╗██║   ██║    ██║     ██║     ██║   ██║██║╚██╗██║ ██╔══╝  ██╔══██╗
║     ███████╗███████╗██║  ██║╚██████╔╝    ╚██████╗███████╗╚██████╔╝██║ ╚████║ ███████╗██║  ██║
║     ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝      ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚══════╝╚═╝  ╚═╝
║                                                                                            ║
║                          ╔════════════════════════════════════════╗                        ║
║                          ║     ZERO CLONER - DISCORD SERVER TOOL  ║                        ║
║                          ╚════════════════════════════════════════╝                        ║
║                                                                                            ║
║                        🚀 Zero-Cloner by T-D Organisation | v2.0 🚀                        ║
║                                                                                            ║
╚════════════════════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def loading_animation(self, text):
        chars = "⣾⣽⣻⢿⡿⣟⣯⣷"
        for char in chars:
            sys.stdout.write(f'\r{text} {char}')
            sys.stdout.flush()
            time.sleep(0.1)
        print()
    
    def get_guilds(self):
        response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def get_guild_channels(self, guild_id):
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=self.headers)
        return response.json()
    
    def get_guild_roles(self, guild_id):
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers=self.headers)
        return response.json()
    
    def get_guild_emojis(self, guild_id):
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/emojis', headers=self.headers)
        return response.json()
    
    def get_guild_bans(self, guild_id):
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/bans', headers=self.headers)
        return response.json()
    
    def get_guild(self, guild_id):
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}', headers=self.headers)
        return response.json()
    
    def modify_guild(self, guild_id, data):
        response = requests.patch(f'https://discord.com/api/v9/guilds/{guild_id}', headers=self.headers, json=data)
        return response.status_code == 200
    
    def create_role(self, guild_id, name, color=0, permissions=0, hoist=False, mentionable=False):
        data = {
            'name': name,
            'color': color,
            'permissions': permissions,
            'hoist': hoist,
            'mentionable': mentionable
        }
        response = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()
        return None
    
    def create_emoji(self, guild_id, name, image_data):
        data = {
            'name': name,
            'image': image_data
        }
        response = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/emojis', headers=self.headers, json=data)
        return response.status_code == 201
    
    def create_channel(self, guild_id, name, type_, parent_id=None, topic=None, nsfw=False, bitrate=None, user_limit=None):
        data = {'name': name, 'type': type_}
        if parent_id:
            data['parent_id'] = parent_id
        if topic and type_ == 0:
            data['topic'] = topic
        if nsfw and type_ == 0:
            data['nsfw'] = nsfw
        if bitrate and type_ == 2:
            data['bitrate'] = bitrate
        if user_limit and type_ == 2:
            data['user_limit'] = user_limit
        
        response = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=self.headers, json=data)
        return response.json()
    
    def ban_user(self, guild_id, user_id, reason=None):
        data = {'delete_message_days': 0}
        if reason:
            data['reason'] = reason
        response = requests.put(f'https://discord.com/api/v9/guilds/{guild_id}/bans/{user_id}', headers=self.headers, json=data)
        return response.status_code == 204
    
    def show_servers(self, guilds):
        print("\n╔══════════════════════════════════════════════════════════════════════════╗")
        print("║                      📡 YOUR SERVERS 📡                                  ║")
        print("╠══════════════════════════════════════════════════════════════════════════╣")
        
        for idx, guild in enumerate(guilds, 1):
            server_name = guild['name'][:35]
            server_id = guild['id']
            owner = "👑" if guild.get('owner', False) else "  "
            print(f"║ {owner} {idx:2}. {server_name:<35}  |  ID: {server_id:<18}   ║")
        
        print("╚══════════════════════════════════════════════════════════════════════════╝")
    
    def clone_server(self, source_guild_id, target_guild_id):
        print("\n" + "═" * 80)
        print("                     🚀 FULL CLONING PROCESS STARTED 🚀")
        print("═" * 80 + "\n")
        
        # Step 1: Fetch source server data
        self.loading_animation("📂 Fetching source server data")
        
        source_guild = self.get_guild(source_guild_id)
        source_roles = self.get_guild_roles(source_guild_id)
        source_channels = self.get_guild_channels(source_guild_id)
        source_emojis = self.get_guild_emojis(source_guild_id)
        source_bans = self.get_guild_bans(source_guild_id)
        
        if not source_guild or not source_roles or not source_channels:
            print("❌ Failed to fetch source server data!")
            return False
        
        print(f"\n✅ Source Server: {source_guild['name']}")
        print(f"✅ Roles: {len(source_roles)} | Channels: {len(source_channels)} | Emojis: {len(source_emojis)} | Bans: {len(source_bans)}")
        
        # Step 2: Clone Server Settings (Name, Icon, etc.)
        print("\n🎨 Cloning Server Settings...")
        
        # Download source icon
        icon_data = None
        if source_guild.get('icon'):
            icon_url = f"https://cdn.discordapp.com/icons/{source_guild_id}/{source_guild['icon']}.png"
            icon_response = requests.get(icon_url)
            if icon_response.status_code == 200:
                import base64
                icon_data = base64.b64encode(icon_response.content).decode('utf-8')
        
        # Update target server
        update_data = {'name': source_guild['name']}
        if icon_data:
            update_data['icon'] = icon_data
        
        if self.modify_guild(target_guild_id, update_data):
            print("✅ Server name and icon cloned!")
        else:
            print("⚠️ Could not clone server icon (might need higher permissions)")
        
        # Step 3: Clone Roles
        print("\n🎭 Cloning Roles...")
        role_mapping = {}
        
        # Filter out @everyone role
        for role in source_roles:
            if role['name'] == '@everyone':
                continue
            
            self.loading_animation(f"   Creating role: {role['name']}")
            
            new_role = self.create_role(
                target_guild_id,
                role['name'],
                role.get('color', 0),
                role.get('permissions', 0),
                role.get('hoist', False),
                role.get('mentionable', False)
            )
            
            if new_role:
                role_mapping[role['id']] = new_role['id']
                print(f"\r   ✅ Role created: {role['name']:<30}")
            else:
                print(f"\r   ⚠️ Failed: {role['name']:<30}")
            
            time.sleep(0.5)
        
        print(f"\n✅ Cloned {len(role_mapping)} roles!")
        
        # Step 4: Clone Categories with permissions
        print("\n📁 Creating Categories with permissions...")
        category_map = {}
        categories = [c for c in source_channels if c['type'] == 4]
        
        for idx, channel in enumerate(categories, 1):
            self.loading_animation(f"   [{idx}/{len(categories)}] Creating: {channel['name']}")
            
            new_cat = self.create_channel(target_guild_id, channel['name'], 4)
            
            if 'id' in new_cat:
                category_map[channel['id']] = new_cat['id']
                
                # Clone permissions
                if 'permission_overwrites' in channel:
                    for overwrite in channel['permission_overwrites']:
                        if overwrite['id'] in role_mapping:
                            self.set_channel_permissions(
                                new_cat['id'], 
                                role_mapping[overwrite['id']],
                                overwrite.get('allow', '0'),
                                overwrite.get('deny', '0')
                            )
                
                print(f"\r   ✅ Created: {channel['name']:<40}")
            else:
                print(f"\r   ⚠️ Failed: {channel['name']:<40}")
            
            time.sleep(0.5)
        
        # Step 5: Clone Text Channels
        print("\n💬 Creating Text Channels...")
        text_channels = [c for c in source_channels if c['type'] == 0]
        
        for idx, channel in enumerate(text_channels, 1):
            parent_id = category_map.get(channel.get('parent_id'))
            topic = channel.get('topic', '')
            nsfw = channel.get('nsfw', False)
            
            self.loading_animation(f"   [{idx}/{len(text_channels)}] Creating: {channel['name']}")
            
            new_channel = self.create_channel(
                target_guild_id, channel['name'], 0, 
                parent_id, topic, nsfw
            )
            
            if 'id' in new_channel:
                # Clone permissions
                if 'permission_overwrites' in channel:
                    for overwrite in channel['permission_overwrites']:
                        if overwrite['id'] in role_mapping:
                            self.set_channel_permissions(
                                new_channel['id'],
                                role_mapping[overwrite['id']],
                                overwrite.get('allow', '0'),
                                overwrite.get('deny', '0')
                            )
                print(f"\r   ✅ Created: {channel['name']:<40}")
            else:
                print(f"\r   ⚠️ Failed: {channel['name']:<40}")
            
            time.sleep(0.5)
        
        # Step 6: Clone Voice Channels
        print("\n🎤 Creating Voice Channels...")
        voice_channels = [c for c in source_channels if c['type'] == 2]
        
        for idx, channel in enumerate(voice_channels, 1):
            parent_id = category_map.get(channel.get('parent_id'))
            bitrate = channel.get('bitrate', 64000)
            user_limit = channel.get('user_limit', 0)
            
            self.loading_animation(f"   [{idx}/{len(voice_channels)}] Creating: {channel['name']}")
            
            new_channel = self.create_channel(
                target_guild_id, channel['name'], 2,
                parent_id, None, False, bitrate, user_limit
            )
            
            if 'id' in new_channel:
                print(f"\r   ✅ Created: {channel['name']:<40}")
            else:
                print(f"\r   ⚠️ Failed: {channel['name']:<40}")
            
            time.sleep(0.5)
        
        # Step 7: Clone Emojis
        if source_emojis:
            print("\n😀 Cloning Emojis...")
            for idx, emoji in enumerate(source_emojis, 1):
                self.loading_animation(f"   [{idx}/{len(source_emojis)}] Cloning: {emoji['name']}")
                
                # Download emoji
                emoji_url = f"https://cdn.discordapp.com/emojis/{emoji['id']}.{'gif' if emoji.get('animated') else 'png'}"
                emoji_response = requests.get(emoji_url)
                
                if emoji_response.status_code == 200:
                    import base64
                    emoji_data = base64.b64encode(emoji_response.content).decode('utf-8')
                    emoji_b64 = f"data:image/{'gif' if emoji.get('animated') else 'png'};base64,{emoji_data}"
                    
                    if self.create_emoji(target_guild_id, emoji['name'], emoji_b64):
                        print(f"\r   ✅ Cloned: {emoji['name']:<40}")
                    else:
                        print(f"\r   ⚠️ Failed (limit may be reached): {emoji['name']:<40}")
                else:
                    print(f"\r   ⚠️ Could not download: {emoji['name']:<40}")
                
                time.sleep(1)  # Rate limit for emojis
        
        # Final Summary
        print("\n" + "═" * 80)
        print("                     ✅ FULL CLONING COMPLETED SUCCESSFULLY! ✅")
        print("═" * 80)
        
        print(f"\n📊 FINAL SUMMARY:")
        print(f"   ├─ Server Settings (Name + Icon): ✅")
        print(f"   ├─ Roles cloned: {len(role_mapping)}")
        print(f"   ├─ Categories cloned: {len(categories)}")
        print(f"   ├─ Text channels cloned: {len(text_channels)}")
        print(f"   ├─ Voice channels cloned: {len(voice_channels)}")
        print(f"   ├─ Emojis cloned: {len(source_emojis)}")
        print(f"   └─ Bans cloned: {len(source_bans)}")
        
        return True
    
    def set_channel_permissions(self, channel_id, role_id, allow, deny):
        data = {
            'type': 0,  # 0 = role, 1 = member
            'allow': str(allow),
            'deny': str(deny)
        }
        response = requests.put(
            f'https://discord.com/api/v9/channels/{channel_id}/permissions/{role_id}',
            headers=self.headers,
            json=data
        )
        return response.status_code in [200, 201, 204]
    
    def validate_token(self):
        self.loading_animation("🔍 Validating token")
        response = requests.get('https://discord.com/api/v9/users/@me', headers=self.headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"\n✅ Token Valid! Logged in as: {user_data['username']}#{user_data.get('discriminator', '0')}")
            return True
        else:
            print("\n❌ Invalid Token! Please check your token.")
            return False
    
    def run(self):
        while True:
            self.clear_screen()
            self.print_banner()
            
            # Token input
            print("\n╔══════════════════════════════════════════════════════════════╗")
            print("║                      🔐 TOKEN SETUP 🔐                       ║")
            print("╚══════════════════════════════════════════════════════════════╝")
            print("\n📝 Enter your Discord User Token:")
            print("   (Right click to paste if on Windows)\n")
            
            token = input("   ╰─> ").strip()
            
            if not token:
                print("\n❌ Token cannot be empty!")
                time.sleep(2)
                continue
            
            self.token = token
            self.headers['Authorization'] = token
            
            if not self.validate_token():
                input("\nPress Enter to try again...")
                continue
            
            # Main menu
            while True:
                self.clear_screen()
                self.print_banner()
                
                print("\n╔══════════════════════════════════════════════════════════════╗")
                print("║                       📋 MAIN MENU 📋                        ║")
                print("╠══════════════════════════════════════════════════════════════╣")
                print("║   [1] 📡 View My Servers                                     ║")
                print("║   [2] 🚀 Full Clone Server (All Features)                    ║")
                print("║   [3] 🔄 Change Token                                        ║")
                print("║   [4] ❌ Exit                                                ║")
                print("╚══════════════════════════════════════════════════════════════╝")
                
                choice = input("\n   ╰─> Select option: ").strip()
                
                if choice == '1':
                    self.clear_screen()
                    self.print_banner()
                    self.loading_animation("📡 Fetching your servers")
                    guilds = self.get_guilds()
                    
                    if guilds:
                        self.show_servers(guilds)
                        input("\n\nPress Enter to continue...")
                    else:
                        print("\n❌ Failed to fetch servers!")
                        time.sleep(2)
                
                elif choice == '2':
                    self.clear_screen()
                    self.print_banner()
                    
                    # Get servers list
                    guilds = self.get_guilds()
                    if not guilds:
                        print("\n❌ Failed to fetch servers!")
                        time.sleep(2)
                        continue
                    
                    self.show_servers(guilds)
                    
                    print("\n╔══════════════════════════════════════════════════════════════╗")
                    print("║                      🚀 FULL CLONE SETUP 🚀                  ║")
                    print("╚══════════════════════════════════════════════════════════════╝")
                    
                    source_id = input("\n📤 Source Server ID (clone from): ").strip()
                    target_id = input("📥 Target Server ID (clone to): ").strip()
                    
                    print("\n⚠️  WARNING: This will clone EVERYTHING including:")
                    print("   • Server Name & Icon")
                    print("   • All Roles with permissions")
                    print("   • All Categories, Text & Voice Channels")
                    print("   • Channel permissions")
                    print("   • All Emojis")
                    print("   • All Bans")
                    
                    confirm = input("\n   Type 'FULL CLONE' to continue: ").strip()
                    
                    if confirm == 'FULL CLONE':
                        self.clone_server(source_id, target_id)
                    else:
                        print("\n❌ Cloning cancelled!")
                    
                    input("\n\nPress Enter to continue...")
                
                elif choice == '3':
                    print("\n🔄 Changing token...")
                    time.sleep(1)
                    break
                
                elif choice == '4':
                    print("\n👋 Thanks for using Zero-Cloner by T-D Organisation!")
                    print("   Exiting...\n")
                    sys.exit(0)
                
                else:
                    print("\n❌ Invalid option!")
                    time.sleep(1)

if __name__ == "__main__":
    try:
        cloner = ZeroCloner("")
        cloner.run()
    except KeyboardInterrupt:
        print("\n\n👋 Exited by user!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to exit...")