'''
    @author Daniel Victor Freire Feitosa
    @version 0.0.1
    @since 2025-05-20
    @package PenBoot
    @file PenBoot.py
    @description Make an pendrive bootable with python
    @date 2025-05-20
    @git https://github.com/proxyanon
'''
import subprocess, os, platform, ctypes, argparse, asyncio, traceback
    
class PenBootPy(object):
    
    def __init__(self: object, pendrive_abs_path: str = '', iso_abs_path: str = '', verbose: bool = True, script_filename: str = 'scriptsToPenBoot.txt') -> None:
        
        self.pendrive_abs_path = pendrive_abs_path
        self.iso_abs_path = iso_abs_path
        self.verbose = verbose
        self.script_filename = script_filename
        self.disk: int = 1
    
    def check_platform(self: object) -> None:
        if platform() != "Windows": 
            raise Exception("[Sorry this only run in linux...]")
        else:
            return True
    
    def is_admin(self: object) -> bool:
        try:
            if ctypes.windll.shell32.IsUserAnAdmin() != 0: return True
        except PermissionError:
            return False
    
    def init_args(self: object) ->  argparse.Namespace:
        
        args: argparse.ArgumentParser = argparse.ArgumentParser(
                prog='PenBootPy', 
                usage="python PenBoot.py --pendrive_path/-P/-p --iso_path/-I/-i", 
                description='Ex: PeenBoot.py --pendrive_path "E:\\" --iso_path .\\my_iso.iso',
                epilog="python PenBoot.py -h to help", 
                add_help=True, 
                help='python PenBoot.py -P E:\\ -I my_iso.iso',
            )

        args.add_argument('--pendrive_abs_path', '-P', '-p', help='Pendrive absolute path (e.g. E:\\)', required=True)
        args.add_argument('--iso_abs_path', '-I', '-i', help='ISO absolute path (e.g. my_iso.iso)', required=True)
        
        args: argparse.Namespace = args.parse_args()

        return args
        
    def banner(self: object) -> None:
        self.log("   ██████╗ ███████╗███╗   ██╗██████╗  ██████╗  ██████╗ ████████╗\n" +
                    "██╔══██╗██╔════╝████╗  ██║██╔══██╗██╔═══██╗██╔═══██╗╚══██╔══╝\n" +
                    "██████╔╝█████╗  ██╔██╗ ██║██████╔╝██║   ██║██║   ██║   ██║\n" +
                    "██╔═══╝ ██╔══╝  ██║╚██╗██║██╔══██╗██║   ██║██║   ██║   ██║\n" +
                    "██║     ███████╗██║ ╚████║██████╔╝╚██████╔╝╚██████╔╝   ██║\n" +
                    "╚═╝     ╚══════╝╚═╝  ╚═══╝╚═════╝  ╚═════╝  ╚═════╝    ╚═╝\n" +

                    "██████╗ ██╗   ██╗     ██████╗ ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗ █████╗ ███╗   ██╗ ██████╗ ███╗   ██╗\n" +
                    "██╔══██╗╚██╗ ██╔╝    ██╔═══██╗██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝██╔══██╗████╗  ██║██╔═══██╗████╗  ██║\n" +
                    "██████╔╝ ╚████╔╝     ██║██╗██║██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝ ███████║██╔██╗ ██║██║   ██║██╔██╗ ██║\n" +
                    "██╔══██╗  ╚██╔╝      ██║██║██║██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝  ██╔══██║██║╚██╗██║██║   ██║██║╚██╗██║\n" +
                    "██████╔╝   ██║       ╚█║████╔╝██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║   ██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║\n" +
                    "╚═════╝    ╚═╝        ╚╝╚═══╝ ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝\n\n")
    
    def log(self: object, msg: str) -> None:
        if self.verbose : print(msg)
        
    async def auto_create_script_file(self: object) -> None:

        try:
            handle = open(self.script_filename, 'w', encoding='utf8')
            handle.close()
        except Exception as e:
            self.log(f"[Error in auto_create_script_file]: {str(e)}")
    
    async def generate_scripts(self: object, content: str) -> str | Exception:
        
        if content in ["", " ", "\n"]:
            raise Exception("[Error in generate_scripts]: command cannot be empty", message='ERROR')
        elif content not in ["list disk", "select disk", "format fs=ntfs quick", "clean", "active"]:
            raise Exception(f"[Error in generate_scripts]: The command passed is invalid {content}", message='ERROR')
        
        cmd: str = f"diskpart /s {content}" # command to execute commands in diskpart with file
        
        try:
            handle = open(self.script_filename, 'w', encoding='utf8')
            if os.file_exists(self.script_filename): raise Exception(f"[Error in generate_scripts]: {str(e)}", message='ERROR')
            handle.write(cmd); handle.close() if handle.writable() else self.log(f"[Error in generate_scripts]: this file is not writeable {self.script_filename}")
        except IOError as e:
            raise IOError(self.log(f"[IOError in generate_scripts]: {str(e)}\r\n[Error traceback]: {traceback.format_exception()}\n"))
        except Exception as e:
            raise Exception(self.log(f"[Error in generate_scripts]: {str(e)}\r\n[Error in generate_scripts traceback]: {traceback.format_exception()}\n"))
            
        return cmd

    async def run(self: object) -> None:

        cmd: str = self.generate_scripts("list disk")
        output: subprocess.run = subprocess.run([cmd], capture_output=True, text=True)
        self.log(f"\r\n[Output lit_disks]: {output.stdout}")
        self.disk = input(f"\r\n[Choose any disk number]: ")
        
        self.generate_scripts(f"select disk {self.disk}") # select disk for make bootable
        self.log("[THIS DISK WILL FORMATED]\n")
        
        y_n: str = input("[?] Continue: [Y/N]")
        
        if y_n in ["Y", "y", "", None, len(y_n) == 1]:
            
            self.log("[Ok let's making the procedure]")
            
            try:

                self.log("\n\n[Formating...]")
                await self.generate_scripts("clean") # formating pendrive
                
                self.log("[Creating primary partition]")
                await self.generate_scripts("create partition primary") # creating partition for bootable ISO
                await self.generate_scripts("select partition 1") # select unique partition in disk
                
                self.log("[Change format to NTFS]")
                await self.generate_scripts("format=ntfs quick") # change format FAT32 to NTFS
                
                self.log("[Active pendrive]")
                await self.generate_scripts("active") # active actual changes
                
                self.log("[Finished]\n")
            except Exception as e:
                raise Exception(self.log(f"[Error in run]: {str(e)}\r\n[Error traceback]: {traceback.format_exception()}\n"))
            
        else:
            self.log("[Exiting...]")
            exit(0)

    @staticmethod
    def copy_iso_to_usb(self: object) -> RuntimeError | None | str:

        try:
        
            self.log(f"\r\n[Copying ISO: {self.iso_abs_path}\r\nto USB: {self.pendrive_abs_path}...]")
            self.log("[Maybe this will take a while...]")
            
            subprocess.run([
                "xcopy", self.iso_abs_pathname, self.usb_abs_pathname, "/E", "/H", "/K"
            ], check=True)
        
        except subprocess.CalledProcessError:
            raise RuntimeError("[Failed to copy ISO contents to USB drive]")

    async def main(self: object) -> None | Exception | RuntimeError | PermissionError:

        self.init_args()
        self.banner()
        self.check_platform()
        
        if not self.is_admin(): raise PermissionError("[You must have run this script with admin privileges]", message='ERROR')
        
        await self.auto_create_script_file()
        
        try: await self.run()
        except subprocess.CalledProcessError as e: raise RuntimeError(self.log(f"[Error in make_bootable]: {e.__str__()}\n[Error traceback]: {e.__traceback__}"))

        try: self.copy_iso_to_usb()
        except subprocess.CalledProcessError as e: raise RuntimeError(self.log(f"\n[Erro in main can't transfer the ISO: {self.iso_abs_path}\r\nto USB: {self.usb_abs_path}]\n[Error traceback]: {e.__traceback__}\n[Error message]: {str(e)}"))
        
            
if __name__ == '__main__':    
    penbootpy: PenBootPy = PenBootPy()
    asyncio.run(penbootpy.main())
