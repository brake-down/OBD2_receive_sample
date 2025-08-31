import serial
import re

ser = serial.Serial('/dev/cu.usbmodem1101', 9600, timeout=1)

pattern = re.compile(r'/S(\d+)/R(\d+)/P([0-9]+\.[0-9]+)/B(\d+)')

# 마지막으로 인정된 값 저장용
S_val, R_val, P_val, B_val = None, None, None, None

while True:
    line = ser.readline().decode('utf-8').strip()
    if not line:
        continue

    match = pattern.fullmatch(line)
    if match:
        new_S = int(match.group(1))
        new_R = int(match.group(2))
        new_P = float(match.group(3))
        new_B = int(match.group(4))

        # --- 조건 검사 및 갱신 ---
        # S: 갑자기 0으로 떨어지는 경우 무시
        if not (S_val is not None and S_val > 0 and new_S == 0):
            S_val = new_S

        # R: 0이면 무시
        if new_R != 0:
            R_val = new_R

        # P: 0.0이면 무시
        if new_P != 0.0:
            P_val = new_P

        # B는 항상 갱신
        B_val = new_B

        print(f"S={S_val}, R={R_val}, P={P_val}, B={B_val}")