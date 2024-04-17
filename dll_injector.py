import win32con
import win32process
import win32api
import win32service
import re
import argparse


def init_parser():
    """
    Parses arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('pid', type=int)
    parser.add_argument('path', type=str)
    args = parser.parse_args()

    return args.pid, args.path


def injector(path, pid, memory):
    """
    Injects the DLL in the path given the PID.
    Allocate the memory based on the DLL size.
    """
    p_hnd = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
    mem_addr = win32process.VirtualAllocEx(p_hnd, 0, memory, win32con.MEM_COMMIT | win32con.MEM_RESERVE,
                                           win32con.PAGE_READWRITE)
    print(hex(mem_addr))
    win32process.WriteProcessMemory(p_hnd, mem_addr, path)

    hk32 = win32api.GetModuleHandle('kernel32.dll')
    hloadlibrary = win32api.GetProcAddress(hk32, "LoadLibraryA")

    if not win32process.CreateRemoteThread(p_hnd, None, 0, hloadlibrary, mem_addr, 0):
        print("[!] Failed to inject DLL, exit...")
    else:
        print("Successfuly injected.")
    win32api.CloseHandle(p_hnd)


def main():
    pid, path = init_parser()
    memory = 150000000
    injector(path, pid, memory)


if __name__ == "__main__":
    main()
