"""Writes boards/kestrel_fc/board.json: the Kestrel H7 flight controller (FPV project, board 1 of 3).

    "$KICAD_PYTHON" boards/kestrel_fc/make_brief.py          (MERCH_PREVIEW=<svg> for a sketch)

A 40 x 40 mm, 6-layer, 30.5 mm-stack flight controller for a 5" 6S quad: STM32H743, ICM-20602 (Betaflight
gyro) + BMI088 (INAV / ArduPilot second IMU), MS5611, 16 MB blackbox flash, 5 V / 2 A and switchable
10 V / 2 A BECs from 2-6S, and JST-SH ports for the 4-in-1 ESC, a digital VTX (DJI O3 / Walksnail /
HDZero), an ELRS receiver and a GPS + compass. The pin map follows the MATEKH743 target so the
Betaflight, INAV and ArduPilot configurations can follow a proven layout.

Top face: the MCU, the four ports, USB-C, LEDs and the BOOT button. Bottom face: both IMUs (under the
MCU, the board's centre), the BECs, the LDOs, the flash, the baro, and the solder pads.
Edit this file, not board.json. Frame 40 x 40 mm, origin top-left, y down.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import merch_kit as K  # noqa: E402

W = H = 40.0
CX = CY = 20.0
HOLE = 15.25                     # 30.5 mm pattern

MCU_PINS = {
    "U?.1": "PINIO_VTX", "U?.2": "LED0", "U?.3": "LED1", "U?.9": "CS_ICM",
    "U?.15": "VBAT_ADC", "U?.16": "CURR_ADC",
    "U?.22": "M3", "U?.23": "M4", "U?.24": "M5", "U?.25": "M6",
    "U?.29": "SPI1_SCK", "U?.30": "SPI1_MISO", "U?.88": "SPI1_MOSI", "U?.36": "INT_ICM",
    "U?.34": "M1", "U?.35": "M2",
    "U?.37": "UART7_RX", "U?.38": "UART7_TX",
    "U?.39": "INT_BMI_GYR", "U?.40": "CS_BMI_GYR", "U?.41": "CS_BMI_ACC",
    "U?.42": "SPI4_SCK", "U?.43": "SPI4_MISO", "U?.44": "SPI4_MOSI", "U?.45": "INT_BMI_ACC",
    "U?.55": "UART3_TX", "U?.56": "UART3_RX", "U?.59": "M7", "U?.60": "M8", "U?.62": "BEEPER",
    "U?.63": "UART6_TX", "U?.64": "UART6_RX", "U?.67": "LED_STRIP",
    "U?.68": "UART1_TX", "U?.69": "UART1_RX", "U?.70": "USB_DM", "U?.71": "USB_DP",
    "U?.77": "CS_FLASH", "U?.78": "SPI3_SCK", "U?.79": "SPI3_MISO", "U?.80": "SPI3_MOSI",
    "U?.86": "UART2_TX", "U?.87": "UART2_RX", "U?.92": "I2C1_SCL", "U?.93": "I2C1_SDA",
    "U?.95": "UART4_RX",
}
MCU_NC = ["U?.%d" % p for p in (4, 5, 7, 8, 17, 18, 28, 31, 32, 33, 46, 47, 51, 52, 53, 54, 57, 58, 61,
                                 65, 66, 81, 82, 83, 84, 85, 89, 90, 91, 96, 97, 98)]

BLOCKS = [
    {"block": "kestrel_h743_core", "as": "mcu", "title": "STM32H743VIT6, 480 MHz", "pinNets": MCU_PINS, "no_connect": MCU_NC},
    {"block": "kestrel_imu_icm20602", "as": "imu1", "title": "Gyro 1: ICM-20602 on SPI1 (Betaflight)",
     "nets": {"VDD": "3V3_GYRO", "SCK": "SPI1_SCK", "MOSI": "SPI1_MOSI", "MISO": "SPI1_MISO", "CS": "CS_ICM", "INT": "INT_ICM"}},
    {"block": "kestrel_imu_bmi088", "as": "imu2", "title": "Gyro 2: BMI088 on SPI4 (INAV / ArduPilot)",
     "nets": {"VDD": "3V3_GYRO", "SCK": "SPI4_SCK", "MOSI": "SPI4_MOSI", "MISO": "SPI4_MISO", "CS_ACC": "CS_BMI_ACC",
              "CS_GYR": "CS_BMI_GYR", "INT_ACC": "INT_BMI_ACC", "INT_GYR": "INT_BMI_GYR"}},
    {"block": "kestrel_baro_ms5611", "as": "baro", "title": "MS5611 on I2C1 (0x77)",
     "nets": {"VDD": "3V3", "SDA": "I2C1_SDA", "SCL": "I2C1_SCL"}},
    {"block": "kestrel_flash_w25q128", "as": "flash", "title": "16 MB blackbox on SPI3",
     "nets": {"VCC": "3V3", "CS": "CS_FLASH", "MISO": "SPI3_MISO", "MOSI": "SPI3_MOSI", "SCK": "SPI3_SCK"}},
    {"block": "kestrel_vbat_sense", "as": "vbat", "title": "VBAT in, TVS, sense dividers",
     "nets": {"VBAT": "VBAT", "CURR_IN": "CURR", "VBAT_ADC": "VBAT_ADC", "CURR_ADC": "CURR_ADC"}},
    {"block": "kestrel_bec_5v", "as": "bec5", "title": "5 V / 2 A BEC", "nets": {"VIN": "VBAT", "VOUT": "5V"}},
    {"block": "kestrel_bec_10v", "as": "bec10", "title": "10 V / 2 A VTX BEC, switchable",
     "nets": {"VIN": "VBAT", "VOUT": "10V", "EN": "EN_10V"}},
    {"block": "merch_lowside_fet", "as": "vtxsw", "title": "VTX power switch (Betaflight PINIO): high = 10 V off",
     "nets": {"LOAD": "EN_10V", "EN": "PINIO_VTX"}},
    {"block": "kestrel_ldo_3v3", "as": "ldo", "title": "3V3 for the MCU, flash, baro, LEDs", "nets": {"VIN": "5V", "VOUT": "3V3"}},
    {"block": "kestrel_ldo_3v3", "as": "ldog", "title": "3V3_GYRO for the two IMUs alone", "nets": {"VIN": "5V", "VOUT": "3V3_GYRO"}},
    {"block": "kestrel_esc_port", "as": "esc", "title": "ESC 8-pin",
     "nets": {"VBAT": "VBAT", "CURR": "CURR", "TLM": "UART4_RX", "M1": "M1", "M2": "M2", "M3": "M3", "M4": "M4"}},
    {"block": "kestrel_vtx_port", "as": "vtx", "title": "Digital VTX 6-pin",
     "nets": {"PWR": "10V", "TX": "UART3_TX", "RX": "UART3_RX", "SBUS": "UART6_RX"}},
    {"block": "kestrel_rx_port", "as": "rx", "title": "ELRS receiver 4-pin on UART7", "nets": {"5V": "5V", "RX": "UART7_RX", "TX": "UART7_TX"}},
    {"block": "kestrel_gps_port", "as": "gps", "title": "GPS + compass 6-pin",
     "nets": {"5V": "5V", "TX": "UART2_TX", "RX": "UART2_RX", "SDA": "I2C1_SDA", "SCL": "I2C1_SCL"}},
    {"block": "kestrel_usb_c", "as": "usb", "title": "USB-C: configuration, DFU, power on the bench",
     "nets": {"USB_DP": "USB_DP", "USB_DM": "USB_DM"}},
    {"block": "usb_esd_usblc6", "as": "esd", "title": "USB ESD", "nets": {"USB_DP": "USB_DP", "USB_DM": "USB_DM"}},
    {"block": "kestrel_usb_power", "as": "usbpwr", "title": "VBUS into 5V through a Schottky"},
    {"block": "merch_lowside_fet", "as": "buz", "title": "Buzzer driver (5 V buzzer on the BZ pads)",
     "nets": {"LOAD": "BZ_NEG", "EN": "BEEPER"}},
    {"block": "gpio_led", "as": "led0", "title": "Status LED 0 (blue)", "nets": {"SIG": "LED0"}, "values": {"D?": "Blue", "R?": "1k"}},
    {"block": "gpio_led", "as": "led1", "title": "Status LED 1 (green)", "nets": {"SIG": "LED1"}, "values": {"D?": "Green", "R?": "1k"}},
    {"block": "gpio_led", "as": "ledp", "title": "Power LED (red, on 3V3)", "nets": {"SIG": "3V3"}, "values": {"D?": "Red", "R?": "1k"}},
    {"block": "kestrel_aux_pads", "as": "pads", "title": "Solder pads",
     "nets": {"M5": "M5", "M6": "M6", "M7": "M7", "M8": "M8", "UART6_TX": "UART6_TX", "UART6_RX": "UART6_RX",
              "UART1_TX": "UART1_TX", "UART1_RX": "UART1_RX", "LED_STRIP": "LED_STRIP", "LED_PAD": "LED_PAD",
              "BZ_NEG": "BZ_NEG", "5V": "5V", "10V": "10V"}},
    {"block": "kestrel_mount_30x30", "as": "mnt", "title": "30.5 mm stack holes"},
]

# ---------------------------------------------------------------------------------------- outline
outline = K.Shape.rect(0, 0, W, H, r=3.0)
holes = [(CX + sx * HOLE, CY + sy * HOLE) for sx in (-1, 1) for sy in (-1, 1)]

# ---------------------------------------------------------------------------------------- parts
parts = K.design_footprints(BLOCKS, os.path.join(os.path.dirname(HERE), "..", "blocks"))
L = K.Layout(parts)
for i, (hx, hy) in enumerate(holes):
    L.lock("mnt:H%d?" % (i + 1), hx, hy, 0, "30.5 mm stack hole; its courtyard is the grommet's keep-out",
           overhang=True)
# top face
L.lock("mcu:U?", CX, CY, 0, "MCU in the middle; its four pin sides face their ports")
L.lock("gps:J?", CX, 3.4, 180, "GPS port on the top edge, beside PD5/PD6 and PB6/PB7", overhang=True)
L.lock("usb:J?", W - 3.6, 14.8, 90, "USB-C on the right edge, beside PA11/PA12", overhang=True)
L.lock("rx:J?", 3.4, 24.0, 270, "receiver port on the left edge (UART7)", overhang=True)
L.lock("esc:J?", CX, H - 3.4, 0, "ESC port in the middle of the bottom edge, motors 1-2 above it", overhang=True)
L.lock("vtx:J?", W - 3.4, 25.6, 90, "VTX port on the right edge under the USB, beside PD8/PD9", overhang=True)
L.lock("mcu:Y?", 9.4, 17.6, 90, "8 MHz crystal at PH0/PH1")
L.lock("mcu:SW?", 9.6, 11.0, 0, "BOOT button")
L.lock("esd:U?", 29.5, 14.8, 90, "USB ESD behind the receptacle", side="bottom")
# bottom face
L.lock("imu1:U?", CX - 1.6, CY + 1.0, 0, "gyro 1 under the MCU, at the board's centre", side="bottom")
L.lock("imu2:U?", CX + 5.4, CY - 0.2, 90, "gyro 2 beside it, turned so its signal pads face the centre; CS_GYR (pin 5) alone faces right, where the board is open for its via", side="bottom")
# its two 100 nF 2.6 mm off its right pad row, not against it: CS_GYR (pin 5) sits between GND pins 4
# and 6 there, and with the capacitors 0.4 mm away no solve found room for its via (five solves). At
# 1.9 mm one net stayed open, at 1.3 and 2.6 mm none; 2.6 mm took the fewest vias (125 to 130)
# gyro 1's second capacitor 0.5 mm off its body: the kit put it 0.25 mm away, and its silk met the
# ICM-20602's pin-1 mark (a DRC silk_overlap warning)
L.lock("imu1:C2?", 15.65, 22.25, 90, "ICM-20602 capacitor, clear of its pin-1 mark", side="bottom")
L.lock("imu2:C1?", CX + 10.2, CY - 1.5, 90, "BMI088 VDD capacitor, clear of the pad row's escape vias", side="bottom")
L.lock("imu2:C2?", CX + 10.2, CY + 0.7, 90, "BMI088 VDD capacitor, clear of the pad row's escape vias", side="bottom")
L.lock("ldog:U?", CX, CY - 5.0, 0, "the gyros' own LDO", side="bottom")
L.lock("ldo:U?", CX + 5.0, CY - 5.0, 0, "MCU LDO", side="bottom")
L.lock("bec5:U?", 9.0, 13.0, 0, "5 V BEC", side="bottom")
L.lock("bec5:L?", 9.0, 19.0, 0, "5 V inductor", side="bottom")
L.lock("bec10:U?", 9.0, 26.0, 0, "10 V BEC", side="bottom")
L.lock("bec10:L?", 14.0, 30.5, 0, "10 V inductor", side="bottom")
L.lock("vbat:D?", 22.5, 33.5, 0, "TVS by the ESC port", side="bottom")
L.lock("flash:U?", 26.2, 9.0, 0, "blackbox flash under SPI3, clear of the USB-C shell tabs", side="bottom")
L.lock("baro:U?", 14.0, 7.8, 90, "baro under the GPS side: cover it with foam", side="bottom")
L.lock("usbpwr:D?", 30.2, 23.2, 0, "VBUS diode, below the USB-C shell tabs", side="bottom")

L.lock("vtxsw:Q?", 13.4, 25.0, 90, "VTX power switch beside the 10 V BEC's EN", side="bottom")
L.lock("buz:Q?", 18.7, 6.0, 0, "buzzer driver under the BZ pads", side="bottom")
L.lock("led0:D?", 5.2, 13.0, 0, "status LED 0, left edge")
L.lock("led1:D?", 5.2, 15.4, 0, "status LED 1")
L.lock("ledp:D?", 5.2, 17.8, 0, "power LED")
# bottom face: solder pads along the left and top edges, SWD under the ESC port
PAD_COL = ["M5", "M6", "M7", "M8", "T1", "R1", "T6", "R6"]
for i, name in enumerate(PAD_COL):
    L.lock("pads:TP%d?" % (i + 1), 2.6, 10.6 + 2.65 * i, 0, "pad %s on the left edge" % name, side="bottom")
PAD_ROW = ["LED", "BZ-", "BZ+", "5V", "10V", "GND"]
for i, name in enumerate(PAD_ROW):
    L.lock("pads:TP%d?" % (9 + i), 12.95 + 2.82 * i, 2.6, 0, "pad %s on the top edge" % name, side="bottom")
for i, name in enumerate(["SWDIO", "SWCLK", "NRST"]):
    L.lock("mcu:TP%d?" % (i + 1), 25.0 + 2.0 * i, H - 1.6, 0, "SWD pad %s" % name, side="bottom")

# every remaining part beside its block's anchor, on the anchor's face (the SDK placer would put them
# all on the top face, away from the bottom-face regulators and IMUs they belong to)
SAT = L.place_satellites(BLOCKS, os.path.join(os.path.dirname(HERE), "..", "blocks"), outline, edge=0.4)
print("kit placed %d satellites" % len(SAT))

if os.environ.get("MERCH_PREVIEW"):
    K.preview(os.environ["MERCH_PREVIEW"], outline, L, [], {})
L.check(outline, edge=0.4, keep={})

WORDS = {"pads:TP%d?" % (i + 1): n for i, n in enumerate(PAD_COL + PAD_ROW)}
WORDS.update({"mcu:TP1?": "DIO", "mcu:TP2?": "CLK", "mcu:TP3?": "RST", "mcu:SW?": "BOOT",
              "esc:J?": "ESC", "vtx:J?": "VTX", "rx:J?": "RX", "gps:J?": "GPS", "usb:J?": "USB"})

brief = {
    "name": "kestrel_fc",
    "title": "Kestrel H7 - FPV flight controller: STM32H743, dual IMU, baro, 16 MB blackbox, 5 V + 10 V BECs, 2-6S",
    "revision": "A",
    "brief": "A 40 x 40 mm, 6-layer flight controller on the 30.5 mm stack for a 5-inch 6S FPV quad. STM32H743VIT6 "
             "(480 MHz) with an 8 MHz crystal; ICM-20602 on SPI1 (Betaflight's gyro) and BMI088 on SPI4 (the "
             "second IMU for INAV and ArduPilot), both on their own 3.3 V LDO; MS5611 barometer on I2C1; "
             "W25Q128 16 MB blackbox on SPI3. Power from the ESC harness (2-6S, SMAJ30A TVS): LMR51430 BECs for "
             "5 V / 2 A and a switchable 10 V / 2 A for a digital VTX (Betaflight PINIO). JST-SH ports for a "
             "4-in-1 ESC (8-pin: VBAT, GND, CURR, TLM, M1-M4), a DJI O3 / Walksnail / HDZero VTX (6-pin), an "
             "ELRS receiver (4-pin) and a GPS + compass (6-pin); USB-C for configuration and DFU; pads for "
             "motors 5-8, two spare UARTs, an LED strip and a buzzer. Pin map after the MATEKH743 target.",
    "blocks": BLOCKS,
    "pwrFlags": ["GND", "VBAT", "5V", "10V", "VBUS"],
    "netClasses": [
        {"name": "VBAT", "nets": ["VBAT"], "track": 0.4, "clearance": 0.15, "currentA": 1.2,
         "why": "the two BECs' input: 5 V x 2 A + 10 V x 1 A (a DJI O3) at 90 % is 1.1 A from a 6S pack, "
                "1.6 A from 4S. 0.4 mm of 1 oz outer copper carries 1.23 A at a 10 C rise (IPC-2221), 1.67 A "
                "at 20 C. The default via, not a bigger class via: Freerouting's fanout used the default "
                "padstack on these nets and KiCad's SES import then gave it the class drill (0.45 / 0.3 mm, "
                "a 0.075 mm annular ring), 2026-10-05"},
        {"name": "BEC", "nets": ["5V", "10V"], "track": 0.4, "clearance": 0.15, "currentA": 1.2,
         "why": "5 V feeds the receiver, GPS, LED strip and both LDOs (and is the In3 plane, so its tracks "
                "are only pad escapes); 10 V the VTX (about 1 A for a DJI O3)"},
    ],
    "board": {
        "width": W, "height": H, "corner_radius": 3.0, "layers": 6, "origin": [100.0, 100.0],
        "rules": {"clearance": 0.13, "track": 0.13, "via": [0.45, 0.2], "edge_clearance": 0.4,
                  "hole_to_hole": 0.5, "min_through_hole": 0.2, "min_track": 0.1,
                  "why": "LQFP-100 at 0.5 mm pitch on a 40 mm board; JLC's multilayer line is 0.09 / 0.09 mm, "
                         "0.15 mm drill"},
        "planes": {"In1.Cu": "GND", "In3.Cu": "5V"},
        "pours": {"In2.Cu": "3V3"},
        "notes": "6 layers: F signals / In1 GND plane / In2 signals, then 3V3 poured after routing / In3 5V "
                 "plane / In4 signals, then GND poured / B signals. 5V is a plane because it reaches both "
                 "LDOs, three ports, the pads and the USB diode across the whole board: as 0.5 mm tracks it "
                 "was left open in Freerouting's solves (2026-10-05), as was the gyro cluster on 4 layers. "
                 "The IMUs sit under the MCU at the board's centre, away from the BECs on the left.",
    },
    "placement": L.locks,
    "route": {"passes": 40, "fanout": True, "solve_s": 600},
    "stitch_pitch": 4.0,
    "silk": {"words": WORDS,
             "title": [{"text": "KESTREL H7", "y": 33.0, "size": 1.2, "bold": True},
                       {"text": "rev {revision}  heypcb.ai", "y": 34.6, "size": 0.8}]},
    "captions": {"done_3d": "Kestrel H7: STM32H743 flight controller, 40 x 40 mm, 30.5 mm stack."},
}
K.write_brief(os.path.join(HERE, "board.json"), brief)
print("wrote board.json: %d blocks, %d locks" % (len(BLOCKS), len(L.locks)))
