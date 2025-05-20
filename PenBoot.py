'''
    @author Daniel Victor Freire Feitosa
    @version 0.0.1
    @since 2025-05-20
    @package penbootpy
    @file penbootpy.py
    @description Make an pendrive bootable with python
    @date 2025-05-20
    @git https://github.com/proxyanon
'''
import subprocess, os, platform, ctypes, pathlib

if platform() != "Windows":
    print("[Sorry this only run in windows...]")
    exit(0)

class PenBootPy(object):
    
    def __init__(self: object, pendrive_abs_path: str = '', iso_abs_path: str = '', verbose: bool = True, script_filename: str = 'scriptsToPenBoot.txt') -> None:
        
        self.pendrive_abs_path = pendrive_abs_path
        self.iso_abs_path = iso_abs_path
        self.verbose = verbose
        self.script_filename = script_filename
        self.disk: int = 1
    
    def is_admin(self: object) -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
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
        
    def auto_create_script_file(self: object) -> None:

        try:
            handle = open(self.script_filename, 'w', encoding='utf8')
            handle.close()
        except Exception as e:
            self.log(f"[Error in auto_create_script_file]: {str(e)}")
    
    def generate_scripts(self: object, content: str) -> str | Exception:
        
        cmd = f"diskpart /s {content}"
        
        try:
            handle = open(self.script_filename, 'w', encoding='utf8')
            if os.file_exists(self.script_filename): return Exception(f"[Error in generate_scripts]: {str(e)}", message='ERROR')
            handle.write(cmd); handle.close() if handle.writable() else self.log(f"[Error in generate_scripts]: this file is not writeable {self.script_filename}")
        except IOError as e:
            self.log(f"[IOError in generate_scripts]: {str(e)}", message='ERROR')
        except Exception as e:
            self.log(f"[Error in generate_scripts]: {str(e)}", message='ERROR')
            
        return cmd

    def make_bootable(self: object) -> None:
                
        cmd: str = self.generate_scripts("list disk")
        output: subprocess.run = subprocess.run([cmd], capture_output=True, text=True)
        self.log(f"[Output lit_disks]: {output.stdout}")
        self.disk = input(f"\n[Choose any disk number]: ")
        
        self.generate_scripts(f"select disk {self.disk}") # select disk for make bootable
        self.log("[THIS DISK WILL FORMATED]\n")
        
        y_n: str = input("[?] Continue: [Y/N]")
        
        if y_n in ["Y", "y", ""]:
            
            self.log("[Ok making procedure]")
            
            self.log("\n\n[Formating...]")
            self.generate_scripts("clean") # formating pendrive
            
            self.log("[Creating primary partition]")
            self.generate_scripts("create partition primary") # creating partition for bootable ISO
            self.generate_scripts("select partition 1") # select unique partition in disk
            
            self.log("[Change format to NTFS]")
            self.generate_scripts("format=ntfs quick") # change format FAT32 to NTFS
            
            self.log("[Active pendrive]")
            self.generate_scripts("active") # active actual changes
            
            self.log("[Finished]")
            
        else:
            self.log("[Exiting...]")
            exit(0)
            
    def main(self: object) -> None | Exception:

        self.banner()
        
        if not self.is_admin():
            return Exception("[You must have run this script with admin privileges]", message='ERROR')
        
        self.auto_create_script_file()
        
        try:
            self.make_bootable()
        except Exception as e:
            self.log(f'[Error in make_bootable]: {e.__str__()}\n[Error traceback]: {e.__traceback__}')
            
        try:
            self.log(f"\n[Copying ISO {self.iso_abs_path} to {self.pendrive_abs_path}...]")
            self.log("[Maybe this will take a while...]")
            pathlib.copy(self.iso_abs_path, self.pendrive_abs_path)
        except Exception as e:
            self.log(f"[Error in main]: {str(e)}")
            
if __name__ == '__main__':
    penbootpy: PenBootPy = PenBootPy()
    penbootpy.main()