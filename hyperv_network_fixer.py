import sys
import os
import ctypes
import subprocess
import json
import base64
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading

def is_admin():
    """관리자 권한 여부 확인"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():
    """관리자 권한으로 재실행"""
    try:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
        if sys.executable.endswith("python.exe") or sys.executable.endswith("pythonw.exe"):
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit(0)
    except Exception as e:
        messagebox.showerror("오류", f"관리자 권한 승격 중 오류가 발생했습니다:\n{e}")

def run_powershell(command):
    """PowerShell 명령을 EncodedCommand로 실행하여 한글/특수문자 파싱 오류 원천 차단"""
    try:
        encoded_cmd = base64.b64encode(command.encode('utf-16le')).decode('ascii')
        process = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-EncodedCommand", encoded_cmd],
            capture_output=True,
            text=True,
            encoding='cp949',
            errors='replace',
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return process.returncode, process.stdout.strip(), process.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

class HyperVFixerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hyper-V 인터넷망 가상스위치 자동 복구 툴 v1.0")
        self.root.geometry("860x680")
        self.root.minsize(820, 600)
        
        self.setup_styles()
        
        self.vswitches = []
        self.phy_adapters = []
        self.vms = []
        
        self.create_widgets()
        self.refresh_all_info()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # 색상 팔레트
        self.c_bg = "#F4F6F9"
        self.c_card = "#FFFFFF"
        self.c_primary = "#1E88E5"
        self.c_primary_hover = "#1565C0"
        self.c_accent = "#2E7D32"
        self.c_accent_hover = "#1B5E20"
        self.c_text = "#263238"
        self.c_subtext = "#546E7A"

        self.root.configure(bg=self.c_bg)

        style.configure(".", font=("Segoe UI", 10), background=self.c_bg, foreground=self.c_text)
        style.configure("TLabelframe", background=self.c_card, relief="solid", borderwidth=1)
        style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"), background=self.c_card, foreground=self.c_primary)
        style.configure("TFrame", background=self.c_card)
        style.configure("TLabel", background=self.c_card, foreground=self.c_text)
        style.configure("Header.TLabel", font=("Segoe UI", 15, "bold"), background=self.c_bg, foreground="#0D47A1")
        style.configure("SubHeader.TLabel", font=("Segoe UI", 9), background=self.c_bg, foreground=self.c_subtext)
        
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background=self.c_primary, foreground="white", padding=8)
        style.map("Primary.TButton", background=[("active", self.c_primary_hover)])
        
        style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"), background=self.c_accent, foreground="white", padding=5)
        style.map("Accent.TButton", background=[("active", self.c_accent_hover)])
        
        style.configure("Action.TButton", font=("Segoe UI", 9), padding=4)

    def create_widgets(self):
        # 상단 타이틀
        header_frame = tk.Frame(self.root, bg=self.c_bg)
        header_frame.pack(fill="x", padx=16, pady=8)
        
        title_label = ttk.Label(header_frame, text="🔌 Hyper-V 인터넷망 네트워크 어댑터 자동 복구", style="Header.TLabel")
        title_label.pack(anchor="w")
        
        sub_label = ttk.Label(header_frame, text="부팅 시 물리 이더넷 번호 변경으로 인한 vEthernet(인터넷망) 언플러그 문제 해결", style="SubHeader.TLabel")
        sub_label.pack(anchor="w", pady=(1, 0))

        # 메인 자동 복구 카드
        auto_card = ttk.LabelFrame(self.root, text=" ⚡ 원클릭 자동 복구 (가상PC 재부팅 포함) ", padding=12)
        auto_card.pack(fill="x", padx=16, pady=(0, 6))
        
        auto_desc = ttk.Label(
            auto_card,
            text="'식별되지 않은 네트워크' 물리 랜카드를 자동 감지하여\n가상스위치 연결 재설정 후 가상PC(VM) 재부팅까지 원스톱 처리합니다.",
            justify="left"
        )
        auto_desc.pack(side="left", fill="both", expand=True)

        self.btn_auto_fix = ttk.Button(auto_card, text="🚀 원클릭 자동 복구 실행", style="Primary.TButton", command=self.start_auto_fix_thread)
        self.btn_auto_fix.pack(side="right", padx=5)

        # 수동 제어 카드
        manual_card = ttk.LabelFrame(self.root, text=" 🛠️ 감지 정보 및 수동 제어 ", padding=12)
        manual_card.pack(fill="x", padx=16, pady=4)
        
        manual_frame = ttk.Frame(manual_card)
        manual_frame.pack(fill="x", expand=True)
        manual_frame.columnconfigure(1, weight=1)

        # 1. 가상 스위치 선택
        ttk.Label(manual_frame, text="1. 가상 스위치 선택:").grid(row=0, column=0, sticky="w", pady=4)
        self.combo_vswitch = ttk.Combobox(manual_frame, state="readonly")
        self.combo_vswitch.grid(row=0, column=1, sticky="ew", padx=10, pady=4)

        # 2. 물리 랜카드 선택
        ttk.Label(manual_frame, text="2. 연결할 물리 어댑터:").grid(row=1, column=0, sticky="w", pady=4)
        self.combo_phy = ttk.Combobox(manual_frame, state="readonly")
        self.combo_phy.grid(row=1, column=1, sticky="ew", padx=10, pady=4)

        # 수동 적용 버튼
        self.btn_manual_apply = ttk.Button(manual_frame, text="선택 어댑터로 가상스위치 변경", style="Accent.TButton", command=self.apply_manual_fix)
        self.btn_manual_apply.grid(row=1, column=2, sticky="e", padx=2, pady=4)

        # 3. 가상 PC 재부팅
        ttk.Label(manual_frame, text="3. 가상 PC(VM) 관리:").grid(row=2, column=0, sticky="w", pady=4)
        self.combo_vm = ttk.Combobox(manual_frame, state="readonly")
        self.combo_vm.grid(row=2, column=1, sticky="ew", padx=10, pady=4)

        self.btn_vm_restart = ttk.Button(manual_frame, text="가상PC 1회 재부팅", style="Action.TButton", command=self.restart_selected_vm)
        self.btn_vm_restart.grid(row=2, column=2, sticky="ew", padx=2, pady=4)

        # 새로고침 버튼
        btn_refresh = ttk.Button(manual_card, text="🔄 목록 다시 불러오기", command=self.refresh_all_info)
        btn_refresh.pack(anchor="e", pady=(4, 0))

        # 로그 출력 창
        log_card = ttk.LabelFrame(self.root, text=" 📜 실시간 처리 로그 ", padding=10)
        log_card.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        self.log_area = scrolledtext.ScrolledText(log_card, height=12, font=("Consolas", 10), bg="#1E1E1E", fg="#D4D4D4", insertbackground="white")
        self.log_area.pack(fill="both", expand=True)

    def log(self, message):
        """스레드 안전한 로그 출력 (메인 스레드에서 실행 보장)"""
        def _append():
            self.log_area.insert(tk.END, message + "\n")
            self.log_area.see(tk.END)
        self.root.after(0, _append)

    def clear_log(self):
        """스레드 안전한 로그 초기화"""
        def _clear():
            self.log_area.delete('1.0', tk.END)
        self.root.after(0, _clear)

    def refresh_all_info(self):
        """가상스위치, 물리 어댑터, VM 목록 갱신"""
        self.clear_log()
        self.log("==========================================")
        self.log("🔍 시스템 정보 및 네트워크 상태 탐지 시작...")
        self.log("==========================================")
        
        threading.Thread(target=self._fetch_info_thread, daemon=True).start()

    def _fetch_info_thread(self):
        # 1. 가상 스위치 조회
        ps_cmd_vswitch = "Get-VMSwitch | Select-Object Name, SwitchType, NetAdapterInterfaceDescription | ConvertTo-Json -Compress"
        code, out, err = run_powershell(ps_cmd_vswitch)
        self.vswitches = []
        if code == 0 and out:
            try:
                data = json.loads(out)
                if isinstance(data, dict):
                    data = [data]
                self.vswitches = data
            except Exception as e:
                self.log(f"⚠️ 가상 스위치 JSON 파싱 예외: {e}")

        # 2. 물리 어댑터 조회 + "식별되지 않은 네트워크" 1순위 정렬 알고리즘
        ps_cmd_phy = (
            "$phyAdapters = Get-NetAdapter | Where-Object {"
            "  $_.Status -eq 'Up' -and"
            "  $_.Virtual -ne $true -and"
            "  $_.InterfaceDescription -notlike '*Hyper-V*' -and"
            "  $_.InterfaceDescription -notlike '*Virtual*' -and"
            "  $_.InterfaceDescription -notlike '*Bluetooth*' -and"
            "  $_.InterfaceDescription -notlike '*Loopback*' -and"
            "  $_.InterfaceDescription -notlike '*Npcap*' -and"
            "  $_.InterfaceDescription -notlike '*TAP*'"
            "};"
            "$list = @();"
            "foreach ($a in $phyAdapters) {"
            "  $p = Get-NetConnectionProfile -InterfaceIndex $a.ifIndex -ErrorAction SilentlyContinue;"
            "  $netName = if ($p -and $p.Name) { $p.Name } else { '식별되지 않은 네트워크' };"
            "  $isUnidentified = ($netName -like '*식별되지 않은*' -or $netName -like '*Unidentified*');"
            "  $priority = if ($isUnidentified) { 1 } else { 2 };"
            "  $list += [PSCustomObject]@{"
            "    Name = $a.Name;"
            "    InterfaceDescription = $a.InterfaceDescription;"
            "    NetworkName = $netName;"
            "    IsUnidentified = $isUnidentified;"
            "    Priority = $priority"
            "  }"
            "};"
            "$list | Sort-Object Priority, Name | ConvertTo-Json -Compress"
        )
        code, out, err = run_powershell(ps_cmd_phy)
        self.phy_adapters = []
        if code == 0 and out:
            try:
                data = json.loads(out)
                if isinstance(data, dict):
                    data = [data]
                self.phy_adapters = data
            except Exception as e:
                self.log(f"⚠️ 물리 어댑터 JSON 파싱 예외: {e}")

        # 3. VM 목록 조회
        ps_cmd_vm = "Get-VM | Select-Object Name, State, Status | ConvertTo-Json -Compress"
        code, out, err = run_powershell(ps_cmd_vm)
        self.vms = []
        if code == 0 and out:
            try:
                data = json.loads(out)
                if isinstance(data, dict):
                    data = [data]
                self.vms = data
            except Exception:
                pass

        # UI 업데이트 (메인 스레드에서)
        self.root.after(0, self._update_ui_after_refresh)

    def _update_ui_after_refresh(self):
        # 가상 스위치 Combobox 갱신
        vswitch_names = [sw.get('Name', '') for sw in self.vswitches if sw.get('Name')]
        self.combo_vswitch['values'] = vswitch_names
        if vswitch_names:
            target_idx = 0
            for idx, name in enumerate(vswitch_names):
                if '인터넷망' in name or '인터넷' in name:
                    target_idx = idx
                    break
            self.combo_vswitch.current(target_idx)
            self.log(f"✅ 가상 스위치 탐지 완료: {len(vswitch_names)}개 ({', '.join(vswitch_names)})")
        else:
            self.log("⚠️ 등록된 Hyper-V 가상 스위치가 없습니다.")

        # 물리 어댑터 Combobox 갱신 ("식별되지 않은 네트워크" 1순위 배치 표시)
        phy_display_list = []
        for adapter in self.phy_adapters:
            name = adapter.get('Name', '')
            desc = adapter.get('InterfaceDescription', '')
            net_name = adapter.get('NetworkName', '식별되지 않은 네트워크')
            
            display_text = f"[{name}] {desc} - ({net_name})"
            phy_display_list.append(display_text)

        self.combo_phy['values'] = phy_display_list
        if phy_display_list:
            self.combo_phy.current(0)  # 1순위 ("식별되지 않은 네트워크") 자동 선택
            self.log(f"🟢 랜선이 연결된(Status: Up) 물리 어댑터 감지: {len(phy_display_list)}개")
            for item in phy_display_list:
                self.log(f"   ➔ {item}")
        else:
            self.log("🔴 랜선이 연결된(Status: Up) 물리 어댑터를 찾지 못했습니다!")
            self.log("   (PC 뒷면에 인터넷 랜선이 제대로 꽂혀있는지 확인해주세요.)")

        # VM Combobox 갱신
        vm_display = [f"{vm.get('Name')} ({vm.get('State')})" for vm in self.vms if vm.get('Name')]
        self.combo_vm['values'] = vm_display
        if vm_display:
            target_vm_idx = 0
            for idx, item in enumerate(vm_display):
                if '인터넷' in item:
                    target_vm_idx = idx
                    break
            self.combo_vm.current(target_vm_idx)
            self.log(f"🖥️ 가상PC(VM) 목록: {len(vm_display)}대 감지됨")
        else:
            self.log("ℹ️ 실행 중인 VM이 없거나 VM 조회가 되지 않았습니다.")

        self.log("\n 준비 완료. '원클릭 자동 복구 실행' 버튼을 누르면 어댑터 바인딩과 가상PC 재부팅이 자동 수행됩니다.")

    def start_auto_fix_thread(self):
        self.btn_auto_fix.config(state="disabled")
        self.clear_log()
        self.log("==========================================")
        self.log("🚀 원클릭 자동 복구 프로세스 시작...")
        self.log("==========================================")
        threading.Thread(target=self._auto_fix_worker, daemon=True).start()

    def _auto_fix_worker(self):
        target_vswitch = self.combo_vswitch.get()
        if not target_vswitch:
            target_vswitch = "인터넷망"

        self.log(f"1단계: 타겟 가상스위치 설정확인 ➔ '{target_vswitch}'")

        # "식별되지 않은 네트워크" 1순위 어댑터 자동 추출
        ps_cmd_phy = (
            "$phyAdapters = Get-NetAdapter | Where-Object {"
            "  $_.Status -eq 'Up' -and"
            "  $_.Virtual -ne $true -and"
            "  $_.InterfaceDescription -notlike '*Hyper-V*' -and"
            "  $_.InterfaceDescription -notlike '*Virtual*' -and"
            "  $_.InterfaceDescription -notlike '*Bluetooth*' -and"
            "  $_.InterfaceDescription -notlike '*Loopback*' -and"
            "  $_.InterfaceDescription -notlike '*Npcap*' -and"
            "  $_.InterfaceDescription -notlike '*TAP*'"
            "};"
            "$list = @();"
            "foreach ($a in $phyAdapters) {"
            "  $p = Get-NetConnectionProfile -InterfaceIndex $a.ifIndex -ErrorAction SilentlyContinue;"
            "  $netName = if ($p -and $p.Name) { $p.Name } else { '식별되지 않은 네트워크' };"
            "  $isUnidentified = ($netName -like '*식별되지 않은*' -or $netName -like '*Unidentified*');"
            "  $priority = if ($isUnidentified) { 1 } else { 2 };"
            "  $list += [PSCustomObject]@{"
            "    Name = $a.Name;"
            "    InterfaceDescription = $a.InterfaceDescription;"
            "    NetworkName = $netName;"
            "    Priority = $priority"
            "  }"
            "};"
            "$list | Sort-Object Priority, Name | ConvertTo-Json -Compress"
        )
        code, out, err = run_powershell(ps_cmd_phy)
        adapters = []
        if code == 0 and out:
            try:
                data = json.loads(out)
                if isinstance(data, dict):
                    adapters = [data]
                else:
                    adapters = data
            except Exception:
                pass

        if not adapters:
            self.log("❌ 오류: 랜선이 꽂힌(Up) 물리 이더넷 랜카드를 찾을 수 없습니다!")
            self.log("   PC 뒷면에 녹색/파란색 인터넷 랜선이 정상 꽂혀 있는지 확인하세요.")
            self.root.after(0, lambda: self.btn_auto_fix.config(state="normal"))
            return

        selected_adapter = adapters[0]
        adapter_name = selected_adapter.get('Name')
        adapter_desc = selected_adapter.get('InterfaceDescription')
        net_name = selected_adapter.get('NetworkName', '식별되지 않은 네트워크')

        self.log(f"2단계: 감지된 외부 인터넷 랜카드 선택 ➔ [{adapter_name}] {adapter_desc} - ({net_name})")

        self.log(f"3단계: Hyper-V 가상스위치 바인딩 갱신 중...")
        
        ps_set_cmd = f'''
        $swName = "{target_vswitch}"
        $desc = "{adapter_desc}"
        
        $sw = Get-VMSwitch -Name $swName -ErrorAction SilentlyContinue
        if (-not $sw) {{
            $sw = Get-VMSwitch | Where-Object {{ $_.Name -like '*인터넷망*' -or $_.SwitchType -eq 'External' }} | Select-Object -First 1
        }}
        
        if (-not $sw) {{
            throw "지정한 가상스위치($swName)를 찾을 수 없습니다."
        }}

        Set-VMSwitch -Name $sw.Name -NetAdapterInterfaceDescription $desc
        Write-Output ("SUCCESS:" + $sw.Name)
        '''
        code, out, err = run_powershell(ps_set_cmd)

        if code == 0 and "SUCCESS:" in out:
            actual_sw_name = out.split("SUCCESS:")[1].splitlines()[0].strip()
            self.log(f"🎉 성공! 가상스위치('{actual_sw_name}')에 물리 어댑터 바인딩이 성공적으로 변경되었습니다!")
            
            self.log("4단계: vEthernet 가상 어댑터 상태 갱신 중...")
            run_powershell(f'Get-NetAdapter -Name "*{actual_sw_name}*" -ErrorAction SilentlyContinue | Restart-NetAdapter -ErrorAction SilentlyContinue')
            
            # 5단계: 가상 PC(VM) 자동 탐지 및 재부팅 원스톱 수행
            self.log("5단계: 인터넷 가상PC(VM) 자동 탐지 및 재부팅 수행 중...")
            ps_vm_restart = '''
            $vm = Get-VM | Where-Object { $_.Name -like '*인터넷*' -or $_.State -eq 'Running' } | Select-Object -First 1
            if ($vm) {
                Restart-VM -Name $vm.Name -Force
                Write-Output ("RESTARTED:" + $vm.Name)
            } else {
                Write-Output "NO_VM"
            }
            '''
            v_code, v_out, v_err = run_powershell(ps_vm_restart)
            if "RESTARTED:" in v_out:
                restarted_vm_name = v_out.split("RESTARTED:")[1].splitlines()[0].strip()
                self.log(f"🔄 가상PC('{restarted_vm_name}') 재부팅 명령이 성공적으로 전달되었습니다!")
            else:
                self.log("ℹ️ 자동 재부팅 대상 가상PC(VM)가 탐지되지 않았거나 꺼져있는 상태입니다.")

            self.log("\n==========================================")
            self.log("✅ 어댑터 바인딩 복구 및 가상PC 재부팅이 완료되었습니다!")
            self.log(f"   [적용 내역] 가상스위치 '{actual_sw_name}' ➔ [{adapter_name}] {adapter_desc} - ({net_name})")
            self.log("==========================================")
            self.log("💡 잠시 후 가상PC 부팅이 완료되면 인터넷 통신 상태를 확인해주세요.")
        else:
            self.log("❌ 가상스위치 바인딩 변경 실패!")
            clean_err = err.splitlines()[-1] if err else "가상스위치를 찾지 못했습니다."
            self.log(f"   오류 메시지: {clean_err}")

        self.root.after(0, lambda: self.btn_auto_fix.config(state="normal"))

    def apply_manual_fix(self):
        target_vswitch = self.combo_vswitch.get()
        phy_str = self.combo_phy.get()

        if not target_vswitch or not phy_str:
            messagebox.showwarning("경고", "가상스위치와 연결할 물리 어댑터를 선택해주세요.")
            return

        try:
            adapter_name = phy_str.split(']')[0].replace('[', '').strip()
            rest = phy_str.split(']', 1)[1].strip()
            adapter_desc = rest.split(' - (')[0].strip()
        except Exception:
            adapter_name = phy_str
            adapter_desc = phy_str

        self.clear_log()
        self.log(f"🛠️ 수동 바인딩 적용: 가상스위치 '{target_vswitch}' ➔ 어댑터 '{adapter_name}' ({adapter_desc})")
        
        def _worker():
            ps_set_cmd = f'''
            $swName = "{target_vswitch}"
            $desc = "{adapter_desc}"
            
            $sw = Get-VMSwitch -Name $swName -ErrorAction SilentlyContinue
            if (-not $sw) {{
                $sw = Get-VMSwitch | Where-Object {{ $_.Name -like '*인터넷망*' -or $_.SwitchType -eq 'External' }} | Select-Object -First 1
            }}
            
            if ($sw) {{
                Set-VMSwitch -Name $sw.Name -NetAdapterInterfaceDescription $desc
            }} else {{
                throw "가상스위치를 찾지 못했습니다."
            }}
            '''
            code, out, err = run_powershell(ps_set_cmd)

            if code == 0:
                self.log("✅ 성공적으로 지정한 어댑터로 수동 바인딩되었습니다.")
            else:
                clean_err = err.splitlines()[-1] if err else "오류가 발생했습니다."
                self.log(f"❌ 실패: {clean_err}")

        threading.Thread(target=_worker, daemon=True).start()

    def restart_selected_vm(self):
        vm_str = self.combo_vm.get()
        if not vm_str:
            messagebox.showwarning("경고", "재부팅할 가상PC(VM)를 선택해주세요.")
            return

        vm_name = vm_str.split('(')[0].strip()
        
        if not messagebox.askyesno("확인", f"가상PC '{vm_name}'을(를) 재부팅하시겠습니까?"):
            return

        self.log(f"🔄 가상PC '{vm_name}' 재부팅 요청 중...")
        
        def _worker():
            code, out, err = run_powershell(f'Restart-VM -Name "{vm_name}" -Force')
            if code == 0:
                self.log(f"✅ 가상PC '{vm_name}' 재부팅 명령이 전송되었습니다.")
            else:
                self.log(f"❌ 재부팅 실패: {err}")

        threading.Thread(target=_worker, daemon=True).start()


if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
    else:
        root = tk.Tk()
        app = HyperVFixerApp(root)
        root.mainloop()
