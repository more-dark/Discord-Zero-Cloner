import requests
import asyncio
import aiohttp
import base64
import sys
import os
import time
from concurrent.futures import ThreadPoolExecutor

class UltraFastCloner:
    def __init__(self, user_token):
        self.token = user_token
        self.headers = {
            'Authorization': user_token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        self.role_mapping = {}
        self.category_mapping = {}
    
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
    
    def get_guilds(self):
        response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def get_guild_channels(self, guild_id):
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def get_guild_roles(self, guild_id):
        response = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def modify_guild(self, guild_id, data):
        requests.patch(f'https://discord.com/api/v9/guilds/{guild_id}', headers=self.headers, json=data)
    
    def create_role(self, guild_id, role):
        data = {
            'name': role['name'],
            'color': role.get('color', 0),
            'permissions': str(role.get('permissions', 0)),
            'hoist': role.get('hoist', False),
            'mentionable': role.get('mentionable', False)
        }
        response = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/roles', headers=self.headers, json=data)
        return response.json() if response.status_code == 200 else None
    
    def create_channel(self, guild_id, channel, parent_id=None):
        data = {'name': channel['name'], 'type': channel['type']}
        if parent_id:
            data['parent_id'] = parent_id
        if channel.get('topic') and channel['type'] == 0:
            data['topic'] = channel['topic']
        if channel.get('nsfw') and channel['type'] == 0:
            data['nsfw'] = channel['nsfw']
        if channel.get('bitrate') and channel['type'] == 2:
            data['bitrate'] = channel['bitrate']
        if channel.get('user_limit') and channel['type'] == 2:
            data['user_limit'] = channel['user_limit']
        
        response = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=self.headers, json=data)
        return response.json() if response.status_code == 201 else None
    
    def set_channel_permission(self, channel_id, role_id, allow, deny):
        data = {'type': 0, 'allow': str(allow), 'deny': str(deny)}
        requests.put(f'https://discord.com/api/v9/channels/{channel_id}/permissions/{role_id}', 
                    headers=self.headers, json=data)
    
    def clone_server(self, source_id, target_id):
        print("\n" + "=" * 50)
        print("       ⚡ ULTRA FAST CLONING STARTED ⚡")
        print("=" * 50 + "\n")
        
        start_time = time.time()
        
        # Fetch all data in parallel using asyncio
        print("📡 Fetching source data...")
        
        source_roles = self.get_guild_roles(source_id)
        source_channels = self.get_guild_channels(source_id)
        source_guild = requests.get(f'https://discord.com/api/v9/guilds/{source_id}', headers=self.headers).json()
        
        print(f"✅ Got {len(source_roles)} roles, {len(source_channels)} channels\n")
        
        # Update server name (instant)
        if source_guild.get('name'):
            self.modify_guild(target_id, {'name': source_guild['name']})
            print("✅ Server name updated")
        
        # Clone all roles at once (no waiting between roles)
        print("\n🎭 Cloning roles...")
        roles_to_clone = [r for r in source_roles if r['name'] != '@everyone']
        
        for role in roles_to_clone:
            new_role = self.create_role(target_id, role)
            if new_role:
                self.role_mapping[role['id']] = new_role['id']
                print(f"   ✅ {role['name'][:35]}")
        
        print(f"\n✅ Cloned {len(self.role_mapping)} roles in {time.time() - start_time:.1f}s")
        
        # Create all categories instantly
        print("\n📁 Creating categories...")
        categories = [c for c in source_channels if c['type'] == 4]
        
        for channel in categories:
            new_cat = self.create_channel(target_id, channel)
            if new_cat and 'id' in new_cat:
                self.category_mapping[channel['id']] = new_cat['id']
                print(f"   ✅ {channel['name'][:35]}")
        
        # Create all text channels instantly
        print("\n💬 Creating text channels...")
        text_channels = [c for c in source_channels if c['type'] == 0]
        
        for channel in text_channels:
            parent_id = self.category_mapping.get(channel.get('parent_id'))
            new_channel = self.create_channel(target_id, channel, parent_id)
            if new_channel:
                print(f"   ✅ #{channel['name'][:35]}")
        
        # Create all voice channels instantly
        print("\n🎤 Creating voice channels...")
        voice_channels = [c for c in source_channels if c['type'] == 2]
        
        for channel in voice_channels:
            parent_id = self.category_mapping.get(channel.get('parent_id'))
            new_channel = self.create_channel(target_id, channel, parent_id)
            if new_channel:
                print(f"   ✅ 🔊 {channel['name'][:35]}")
        
        # Apply permissions (fast batch)
        print("\n🔐 Applying permissions...")
        
        # Get fresh target channels
        target_channels = self.get_guild_channels(target_id)
        target_channel_map = {ch['name']: ch['id'] for ch in target_channels}
        
        permission_count = 0
        for channel in source_channels:
            if channel['type'] in [0, 2, 4] and 'permission_overwrites' in channel:
                # Find target channel
                target_id_found = None
                
                if channel['type'] == 4:  # Category
                    target_id_found = self.category_mapping.get(channel['id'])
                else:
                    target_id_found = target_channel_map.get(channel['name'])
                
                if target_id_found:
                    for ow in channel['permission_overwrites']:
                        if ow['id'] in self.role_mapping:
                            self.set_channel_permission(
                                target_id_found, 
                                self.role_mapping[ow['id']],
                                ow.get('allow', '0'), 
                                ow.get('deny', '0')
                            )
                            permission_count += 1
        
        total_time = time.time() - start_time
        
        # Final summary
        print("\n" + "=" * 50)
        print("            ✅ CLONING COMPLETE! ✅")
        print("=" * 50)
        print(f"\n📊 SUMMARY:")
        print(f"   ├─ Roles: {len(self.role_mapping)}")
        print(f"   ├─ Categories: {len(categories)}")
        print(f"   ├─ Text Channels: {len(text_channels)}")
        print(f"   ├─ Voice Channels: {len(voice_channels)}")
        print(f"   ├─ Permissions: {permission_count}")
        print(f"   └─ ⏱️  Total Time: {total_time:.2f} seconds")
        
        return True
    
    def validate_token(self):
        response = requests.get('https://discord.com/api/v9/users/@me', headers=self.headers)
        if response.status_code == 200:
            user = response.json()
            print(f"\n✅ Logged in as: {user['username']}")
            return True
        print("\n❌ Invalid token!")
        return False
    
    def show_servers(self, guilds):
        print("\n📡 YOUR SERVERS:\n")
        for idx, guild in enumerate(guilds, 1):
            owner = "👑" if guild.get('owner') else "  "
            print(f"   {owner} {idx}. {guild['name'][:40]} - {guild['id']}")
        print()
    
    def run(self):
        while True:
            self.clear_screen()
            self.print_banner()
            
            print("\n🔐 ENTER TOKEN:\n")
            token = input("   ╰─> ").strip()
            
            if not token:
                print("\n❌ Token needed!")
                input("\nPress Enter...")
                continue
            
            self.token = token
            self.headers['Authorization'] = token
            
            if not self.validate_token():
                input("\nPress Enter...")
                continue
            
            while True:
                self.clear_screen()
                self.print_banner()
                
                print("\n📋 MENU\n")
                print("   [1] View Servers")
                print("   [2] Clone Server (Roles + Channels)")
                print("   [3] Change Token")
                print("   [4] Exit\n")
                
                choice = input("   ╰─> ").strip()
                
                if choice == '1':
                    self.clear_screen()
                    self.print_banner()
                    guilds = self.get_guilds()
                    if guilds:
                        self.show_servers(guilds)
                    input("\nPress Enter...")
                
                elif choice == '2':
                    self.clear_screen()
                    self.print_banner()
                    
                    guilds = self.get_guilds()
                    if not guilds:
                        print("\n❌ No servers!")
                        input("\nPress Enter...")
                        continue
                    
                    self.show_servers(guilds)
                    
                    print("\n🎯 SETUP\n")
                    source = input("   Source Server ID: ").strip()
                    target = input("   Target Server ID: ").strip()
                    
                    print("\n⚠️  Cloning:")
                    print("   ✅ Server Name")
                    print("   ✅ All Roles")
                    print("   ✅ All Channels")
                    print("   ✅ Permissions")
                    
                    confirm = input("   Type 'FAST' to continue: ").strip()
                    
                    if confirm == 'FAST':
                        self.clone_server(source, target)
                    else:
                        print("\n❌ Cancelled!")
                    
                    input("\nPress Enter...")
                
                elif choice == '3':
                    break
                
                elif choice == '4':
                    print("\n👋 Goodbye!")
                    sys.exit(0)

if __name__ == "__main__":
    try:
        cloner = UltraFastCloner("")
        cloner.run()
    except KeyboardInterrupt:
        print("\n\n👋 Exited!")
        sys.exit(0)